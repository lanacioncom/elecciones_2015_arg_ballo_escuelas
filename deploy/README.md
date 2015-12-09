
We have used the [_gulp-requirejs_](https://www.npmjs.com/package/gulp-requirejs) node package to integrate the requirejs optimization in our gulp deployment process.

Usage info: [here](server/README.md)

Deployment usage
================

## Introduction

This deployment uses SMB protocol to mount the server target folder, then use fabric to copy the files from the build folder into it and finally unmount the server.

**This process is internal to La Nación and thus not interesting for others to reuse, anyhow we publish the source because maybe someone needs to adapt it to their needs and still find it useful**

## Requirements
* Python 2.7.\* && virtualenv && pip installed 

## Process
1. Create a virtualenv

        $ virtualenv .venv

2. Activate the created virtualenv

        $ source .venv/bin/activate

3. Install dependencies

        $ pip install -r requirements.txt

4. Setup required environment variables or change defaults in fabfile.py
    * SAMBA_CONN10: The SMB connection command to be ran for server 10
    * SAMBA_CONN11: The SMB connection command to be ran for server 11
    * PROJECT_PATH: The path on the server where the app will be deployed
    * TMP_PATH: A test path to ensure that the deployment process is working prior to actual deployment

5. Use _fab_ to list the available tasks

        $ fab

6. (Optional) Run the task to test the deployment process to one of our servers

        $ fab test_deploy10 

7. Run the task to deploy to our servers

        $ fab deploy 

## Implementation notes

* Tested on MAC and Linux machines, not sure about windows results.
