# Ghiacciatore
Ghiacciatore is a CLI tool that allows to push data from your local computer to:
* S3
* Glacier

It requires that your AWS account is configured locally (see here https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html).

## Setup

```
% python -m venv .
% source venv/bin/activate
% pip install -r requirements.txt
```
## Run
```
% python main.py --create-missing-storage /home/user/folder

```
## Help
```
usage: main.py [-h] [--storage-type STORAGE_TYPE] [--storage-name STORAGE_NAME] [--create-missing-storage] [--reduce-path-when-importing REDUCE_PATH_WHEN_IMPORTING] path

Synchronises a local folder to a remote AWS S3 or Glacier Storage.

positional arguments:
  path                  The file or folder to backup

optional arguments:
  -h, --help            show this help message and exit
  --storage-type STORAGE_TYPE
                        The type of storage to use (s3 -default-, glacier)
  --storage-name STORAGE_NAME
                        The name of the storage that will be used as name of the created resource (Vault or Bucket)
  --create-missing-storage
                        If the storage (Vault or Bucket) must be created if missing
  --reduce-path-when-importing REDUCE_PATH_WHEN_IMPORTING
                        Prefix of the `path` parameter that must not be used when importing the file in the storage. E.g. if path is /home/test/folder, and this parameter
                        is /home/test, in the destination `/home/test` won't be used
```
