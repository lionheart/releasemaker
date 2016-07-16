#!/usr/bin/env python

import os
import sys
import logging
import requests
import json
import pprint
import re
import subprocess

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

    def create(self, version, bundle, last_commit, filename):
        release_data = {
            'tag_name': "v{}-alpha+{}".format(version, bundle),
            'name': "{} ({})".format(version, bundle),
            'prerelease': True
        }

        repo = git.Repo(".")

        tasks_completed = []

        issue_re = re.compile("#\d*", re.MULTILINE)
        list_re = re.compile("^- .*", re.MULTILINE)
        for commit in repo.iter_commits("HEAD...{}".format(last_commit)):
            for item in issue_re.finditer(commit.message):
                print item.group(0)

            for item in list_re.finditer(commit.message):
                tasks_completed.append(item.group(0))

        tasks = "\n".join(tasks_completed)
        release_data['body'] = tasks

        response = requests.post(self.release_url, data=json.dumps(release_data), headers=self.HEADERS)

        if filename is not None:
            upload_url = uritemplate.expand(response.json()['upload_url'], {'name': os.path.basename(filename)})
            headers = self.HEADERS
            headers['Content-Type'] = "application/zip"

            with open(filename, 'rb') as f:
                response = requests.post(upload_url, data=f.read(), headers=self.HEADERS)

        if response.status_code == 201:
            return 0
        else:
            return 1
