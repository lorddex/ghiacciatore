# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Tuple, Type

import boto3

from ghiacciatore.storages.enums import StorageType


class Storage(ABC):
    def __init__(self, name: str) -> None:
        self._account_id: str = boto3.client("sts").get_caller_identity().get("Account")
        self.name: str = name

    @staticmethod
    def get_storage_class(storage_type: StorageType) -> Type[Storage]:
        if storage_type == StorageType.AWS_GLACIER:
            from ghiacciatore.storages.glacier import StorageAWSGlacier

            return StorageAWSGlacier
        elif storage_type == StorageType.AWS_S3:
            from ghiacciatore.storages.s3 import StorageAWSS3

            return StorageAWSS3

    @abstractmethod
    def create(self) -> Storage:
        pass

    @abstractmethod
    def add_file(
        self, file_name: str, import_name: Optional[str] = None
    ) -> Tuple[Storage, dict]:
        pass

    @abstractmethod
    def get_file(
        self, file_key: str, destination_path: Optional[str] = None
    ) -> Tuple[Storage, dict]:
        pass
