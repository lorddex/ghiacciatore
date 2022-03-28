import os

import boto3

from archiver.archiver import Archiver


class ArchiverAWSS3(Archiver):
    def __init__(self):
        super().__init__()
        self._client = boto3.client("s3")

    def _get_bucket(self, name):
        pass

    def _get_storage(self, name):
        s3 = boto3.resource("s3")
        return s3.Bucket(name)

    def _create_storage(self, name, storage):
        # Create the S3 Bucket
        storage = storage.create(
            ACL="private",
            CreateBucketConfiguration={
                "LocationConstraint": os.getenv("AWS_DEFAULT_REGION")
            }
        )
        # Set up Encryption
        self._client.put_bucket_encryption(
            Bucket=name,
            ServerSideEncryptionConfiguration={
                "Rules": [
                    {"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}
                ]
            }
        )
        # Block any public access
        self._client.put_public_access_block(
            Bucket=name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True,
            },
        )
        return storage

    def store_file(self, storage_name, filename):
        return boto3.resource("s3").Object(storage_name, f"test/{filename}").put(
            Body=open(filename, "rb")
        )

    def list_storages(self):
        pass
