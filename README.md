releasemaker
==============

What Does This Do
-----------------

This simple utility creates GitHub releases. This tool is very specialized and isn't generally useful (maybe it will be in the future).

How Do You Use It
-----------------

```
pip install releasemaker
```

Once installed, just follow the useful CLI prompts.

```sh
$ releasemaker create -h
usage: releasemaker create [-h] --organization ORGANIZATION --repository
                           REPOSITORY [--api-key API_KEY] --start-commit
                           START_COMMIT [--filename FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  --organization ORGANIZATION
  --repository REPOSITORY
  --api-key API_KEY     Your GitHub API token. Defaults to value on OS X
                        keychain.
  --start-commit START_COMMIT
                        The first commit to draw release notes from.
  --filename FILENAME   An optional file to upload along with the release.
```
