# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

import logging
import os
from typing import Optional, Tuple

import boto3

from ghiacciatore.storages.storage import Storage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class StorageAWSS3(Storage):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._client = boto3.client("s3")
        self._s3_resource = boto3.resource("s3")
        self._s3_bucket = self._s3_resource.Bucket(self.name)
        self.exists = self._s3_bucket.creation_date is not None
        logger.info(f"Init S3 Storage {name} (exists={self.exists})")

    def create(self) -> StorageAWSS3:
        logger.info(f"Creating a new S3 Bucket {self.name}")
        # Create the S3 Bucket
        self._s3_bucket = self._s3_bucket.create(
            ACL="private",
            CreateBucketConfiguration={
                "LocationConstraint": os.getenv("AWS_DEFAULT_REGION")
            },
        )
        # Set up Encryption
        logger.debug("Setup encryption")
        self._client.put_bucket_encryption(
            Bucket=self.name,
            ServerSideEncryptionConfiguration={
                "Rules": [
                    {"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}
                ]
            },
        )
        # Block any public access
        logger.debug("Block public access")
        self._client.put_public_access_block(
            Bucket=self.name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            },
        )
        return self

    def add_file(
        self, file_name: str, import_name: Optional[str] = None
    ) -> Tuple[StorageAWSS3, dict]:
        logger.info(f"Uploading {file_name}")
        return (
            self,
            boto3.resource("s3")
            .Object(self.name, file_name if not import_name else import_name)
            .put(Body=open(file_name, "rb")),
        )

    def get_file(
        self, file_key: str, to_path: Optional[str] = None
    ) -> Tuple[StorageAWSS3, dict]:
        logger.info(f"Downloading {file_key}")
        return (
            self,
            boto3.resource("s3")
            .Object(self.name, file_key)
            .download_file(to_path if to_path else file_key),
        )
