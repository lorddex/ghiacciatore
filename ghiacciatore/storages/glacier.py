# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

import logging
from typing import Optional, Tuple

import boto3

from ghiacciatore.storages.storage import Storage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class StorageAWSGlacier(Storage):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._client = boto3.client("glacier")
        self._glacier_resource = boto3.resource("glacier")
        self._glacier_vault = self._glacier_resource.Vault(self._account_id, name)
        self.exists = self._glacier_vault.creation_date is not None
        logger.info(f"Init Glacier Storage {name} (exists={self.exists}")

    def create(self) -> StorageAWSGlacier:
        logger.info(f"Creating a new Glacier Vault {self.name}")
        logger.error("Method StorageAWSGlacier.create NOT implemented")
        return self

    def add_file(
        self, file_name: str, import_name: Optional[str] = None
    ) -> Tuple[StorageAWSGlacier, dict]:
        logger.info(f"Uploading {file_name}")
        return self._glacier_vault.upload_archive(
            archiveDescription=file_name if not import_name else import_name,
            body=open(file_name, "rb"),
        )

    def get_file(
        self, file_key: str, destination_path: Optional[str] = None
    ) -> Tuple[StorageAWSGlacier, dict]:
        # TODO To be implemented
        logger.error("Method StorageAWSGlacier.get_file NOT implemented!")
        return self, {}
