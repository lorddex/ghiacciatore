import logging
import os

from storages.storage import Storage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Archiver:
    def __init__(self, storage_type):
        self._storage_class = Storage.get_storage_class(storage_type)
        self._storages = dict()

    def _get_storage_instance(self, name):
        return self._storage_class(name)

    def store_folder(self, storage_name, folder_name, recursive=False):
        storage = self.get_storage(storage_name)
        for dir_element in os.listdir(folder_name):
            full_file_name = os.path.join(folder_name, dir_element)
            if os.path.isdir(full_file_name) and recursive:
                logger.debug(f"Found a Folder, recursively storing: {full_file_name}")
                self.store_folder(storage.name, full_file_name, recursive)
                return
            logger.debug(f"{full_file_name}")
            storage.add_file(full_file_name)

    def get_storage(self, name, create_if_missing=False):
        if name in self._storages.keys():
            return self._storages[name]

        storage = self._get_storage_instance(name)
        if not storage.exists and create_if_missing:
            storage.create()
        self._storages.update({name: storage})
        return storage

    def list_storages(self):
        # response = self._client.list_vaults()
        # if "VaultList" not in response:
        #    return []
        # vaults = []
        # for v in response["VaultList"]:
        #    vaults.append(v["VaultName"])
        # return vaults
        pass
