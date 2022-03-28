from typing import Any

import boto3

from storages.storage import Storage


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

    def create(self) -> None:
        pass

    def add_file(self, file_name: str) -> dict:
        return self._glacier_vault.upload_archive(
            archiveDescription=file_name, body=open(file_name, "rb")
        )
