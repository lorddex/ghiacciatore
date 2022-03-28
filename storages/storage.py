from abc import ABC, abstractmethod

import boto3

from storages.enums import StorageType


class Storage(ABC):
    @staticmethod
    def get_storage_class(storage_type):
        if storage_type == StorageType.AWS_GLACIER:
            from storages.glacier import StorageAWSGlacier

            return StorageAWSGlacier
        elif storage_type == StorageType.AWS_S3:
            from storages.s3 import StorageAWSS3

            return StorageAWSS3

    def __init__(self, name, storage=None):
        self._account_id = boto3.client("sts").get_caller_identity().get("Account")
        self.name = name
        self.storage = storage

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def add_file(self, file_name):
        pass
