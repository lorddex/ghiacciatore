import logging
import os
from abc import ABC, abstractmethod
from enum import Enum

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ArchiverType(Enum):
    AWS_GLACIER = "glacier"
    AWS_S3 = "s3"


class Storage:

    def __init__(self, name, storage):
        self.name = name
        self.storage = storage


class Archiver(ABC):

    def __init__(self):
        self._account_id = boto3.client("sts").get_caller_identity().get("Account")
        self._storages = dict()

    @staticmethod
    def _get_storage(self, name):
        pass

    @staticmethod
    def get_instance(archiver_type):
        if archiver_type == ArchiverType.AWS_GLACIER:
            from .glacier import ArchiverAWSGlacier

            return ArchiverAWSGlacier()
        elif archiver_type == ArchiverType.AWS_S3:
            from .s3 import ArchiverAWSS3

            return ArchiverAWSS3()

    @staticmethod
    def _log_response(request_type, response):
        logger.debug(f"{request_type}: {response}")

    @abstractmethod
    def list_storages(self):
        pass

    @abstractmethod
    def _create_storage(self, name, storage):
        pass

    @abstractmethod
    def store_file(self, storage_name, file_name):
        pass

    def store_folder(self, storage_name, folder_name, recursive=False):
        total_size = 0
        for dir_element in os.listdir(folder_name):
            full_file_name = os.path.join(folder_name, dir_element)
            if os.path.isdir(full_file_name) and recursive:
                logger.debug(f"Found a Folder, recursively storing: {full_file_name}")
                self.store_folder(storage_name, full_file_name, recursive)
                return
            try:
                file_size = os.path.getsize(full_file_name)
            except FileNotFoundError:
                file_size = 0
            total_size += file_size
            logger.debug(f"{full_file_name} {file_size}")
            self.store_file(storage_name, full_file_name)

    def get_storage(self, name, create_if_missing=False):
        if name not in self._storages.keys():
            storage = self._get_storage(name)
            if not storage.creation_date and create_if_missing:
                self._create_storage(name, storage)
            self._storages.update(
                {
                    name: Storage(name, storage)
                }
            )
            return storage
        return self._storages[name]
