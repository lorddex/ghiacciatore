import logging
from typing import Any, Optional

import boto3

from storages.storage import Storage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class StorageAWSGlacier(Storage):
    _client: Any = None
    _glacier_resource: Any = None
    _glacier_vault: Any = None
    exists: bool = False

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._client = boto3.client("glacier")
        self._glacier_resource = boto3.resource("glacier")
        self._glacier_vault = self._glacier_resource.Vault(self._account_id, name)
        self.exists = self._glacier_vault.creation_date is not None
        logger.info(f"Init Glacier Storage {name} (exists={self.exists}")

    def create(self) -> None:
        logger.info(f"Creating a new Glacier Vault {self.name}")
        pass

    def add_file(self, file_name: str, import_name: Optional[str] = None) -> dict:
        logger.info(f"Uploading {file_name}")
        return self._glacier_vault.upload_archive(
            archiveDescription=file_name if not import_name else import_name,
            body=open(file_name, "rb"),
        )
