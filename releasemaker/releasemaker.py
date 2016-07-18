#!/usr/bin/env python

import os
import sys
import logging
import requests
import json
import pprint
import re
import subprocess
import operator

import git
import uritemplate

logger = logging.getLogger(__name__)
GITHUB_API_ENDPOINT = "https://api.github.com"
github_url = lambda *components: "{}/{}".format(GITHUB_API_ENDPOINT, "/".join(components))

class ReleaseMaker(object):
    def __init__(self, api_key, organization, repository):
        self.api_key = api_key
        self.organization = organization
        self.repository = repository

    @property
    def HEADERS(self):
        return {
            'Authorization': "token {}".format(self.api_key),
            'Content-Type': "application/json",
            'Accept': "application/json"
        }

    @property
    def release_url(self):
        return github_url("repos", self.organization, self.repository, "releases")

    def create(self, version, bundle, since_ref=None, paths=[]):
        release_data = {
            'tag_name': "v{}-alpha+{}".format(version, bundle),
            'name': "{} ({})".format(version, bundle),
            'prerelease': True
        }

        repo = git.Repo()

        tasks_completed = []
        closed_issues = set()
        issues = set()

        issue_close_re = re.compile("(close[ds]?|fix|fixe[ds])? (#\d+)", re.MULTILINE)
        issue_ref_re = re.compile("(#\d+)", re.MULTILINE)
        list_re = re.compile("^- .*", re.MULTILINE)

        if since_ref is None:
            tags = sorted(repo.tags, key=operator.attrgetter("commit.committed_date"), reverse=True)
            if len(tags) > 0:
                since_ref = tags[0].commit.hexsha
            else:
                # From http://stackoverflow.com/a/1007545
                since_ref = repo.git.rev_list("--max-parents=0", "HEAD")

        for commit in repo.iter_commits("HEAD...{}".format(since_ref)):
            for item in issue_close_re.finditer(commit.message):
                issue = item.group(2)
                closed_issues.add(issue)
                if issue in issues:
                    issues.remove(issue)

            for item in issue_ref_re.finditer(commit.message):
                issue = item.group(0)
                if issue not in closed_issues:
                    issues.add(issue)

            for item in list_re.finditer(commit.message):
                tasks_completed.append(item.group(0))

        closed_issues_list = u", ".join(sorted(closed_issues))
        issues_list = u", ".join(sorted(issues))

        body = u""

        sections = []
        if len(closed_issues) > 0:
            sections.append(u"### Closed Issues ({})\n{}".format(len(closed_issues), closed_issues_list))

        if len(issues) > 0:
            sections.append(u"### Issues Worked On ({})\n{}".format(len(issues), issues_list))

        if len(tasks_completed) > 0:
            sections.append(u"### Completed Tasks ({})\n{}".format(len(tasks_completed), "\n".join(tasks_completed)))

        release_data['body'] = "\n\n".join(sections)

        release_response = requests.post(self.release_url, data=json.dumps(release_data), headers=self.HEADERS)
        errors = release_response.json().get('errors', [])
        if len(errors) > 0:
            for error in errors:
                print error

            return False

        for path in paths:
            filename = os.path.basename(path)
            upload_url = uritemplate.expand(release_response.json()['upload_url'], {'name': filename})
            headers = self.HEADERS
            headers['Content-Type'] = "application/zip"

            with open(path, 'rb') as f:
                requests.post(upload_url, data=f.read(), headers=self.HEADERS)

        if release_response.status_code == 201:
            return True
        else:
            return False

