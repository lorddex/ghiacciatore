import os

import boto3

from storages.storage import Storage


class StorageAWSS3(Storage):
    def __init__(self, name, storage=None):
        super().__init__(name, storage)
        self._client = boto3.client("s3")
        self._s3_resource = boto3.resource("s3")
        self._s3_bucket = self._s3_resource.Bucket(self.name)
        self.exists = self._s3_bucket.creation_date is not None

    def create(self):
        # Create the S3 Bucket
        self._s3_bucket = self._s3_bucket.create(
            ACL="private",
            CreateBucketConfiguration={
                "LocationConstraint": os.getenv("AWS_DEFAULT_REGION")
            },
        )
        # Set up Encryption
        self._client.put_bucket_encryption(
            Bucket=self.name,
            ServerSideEncryptionConfiguration={
                "Rules": [
                    {"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}
                ]
            },
        )
        # Block any public access
        self._client.put_public_access_block(
            Bucket=self.name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            },
        )

    def add_file(self, file_name):
        boto3.resource("s3").Object(self.name, f"{file_name}").put(
            Body=open(file_name, "rb")
        )
