import boto3

from storages.storage import Storage


class StorageAWSGlacier(Storage):
    def __init__(self, name, storage=None):
        super().__init__(name, storage)
        self._client = boto3.client("glacier")
        self._glacier_resource = boto3.resource("glacier")
        self._glacier_vault = self._glacier_resource.Vault(self._account_id, name)
        self.exists = self._glacier_vault.creation_date is not None

    def create(self):
        pass

    def add_file(self, file_name):
        return self._glacier_vault.upload_archive(
            archiveDescription=file_name, body=open(file_name, "rb")
        )
