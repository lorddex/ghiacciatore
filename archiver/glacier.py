import boto3

from archiver.archiver import Archiver


class ArchiverAWSGlacier(Archiver):
    def __init__(self):
        super().__init__()
        self._client = boto3.client("glacier")

    def _list_vaults(self):
        response = self._client.list_vaults()
        self._log_response("list_vaults", response)
        if "VaultList" not in response:
            return []
        vaults = []
        for v in response["VaultList"]:
            vaults.append(v["VaultName"])
        return vaults

    def _create_storage(self, name, storage):
        pass

    def _get_storage(self, name):
        glacier = boto3.resource("glacier")
        return glacier.Vault(self._account_id, name)

    def list_storages(self):
        return self._list_vaults()

    def store_file(self, storage_name, filename):
        storage = self.get_storage(storage_name)
        return storage.upload_archive(
            archiveDescription=filename, body=open(filename, "rb")
        )
