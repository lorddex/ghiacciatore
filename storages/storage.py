# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABC, abstractmethod
from typing import Type, TypeVar, Optional

import boto3

from storages.enums import StorageType

Self = TypeVar("Self", bound="Storage")


class Storage(ABC):

    name: str = None
    _account_id: str = None
    exists: bool = False

    @staticmethod
    def get_storage_class(storage_type: StorageType) -> Type[Self]:
        if storage_type == StorageType.AWS_GLACIER:
            from storages.glacier import StorageAWSGlacier

            return StorageAWSGlacier
        elif storage_type == StorageType.AWS_S3:
            from storages.s3 import StorageAWSS3

            return StorageAWSS3

    def __init__(self, name: str) -> None:
        self._account_id = boto3.client("sts").get_caller_identity().get("Account")
        self.name = name

    @abstractmethod
    def create(self) -> Self:
        pass

    @abstractmethod
    def add_file(self, file_name: str, import_name: Optional[str] = None) -> dict:
        pass
