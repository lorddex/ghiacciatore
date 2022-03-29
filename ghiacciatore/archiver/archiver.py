# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import os
from typing import List, Optional, Type

from ghiacciatore.storages.enums import StorageType
from ghiacciatore.storages.storage import Storage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Archiver:
    def __init__(
        self,
        storage_type: StorageType,
        create_missing_storage: Optional[bool] = False,
        reduce_path_when_importing: Optional[str] = None,
    ) -> None:
        self._storage_class = Storage.get_storage_class(storage_type)
        self._create_missing_storage = create_missing_storage
        self._reduce_path_when_importing = reduce_path_when_importing
        logger.debug(f"Created an Archiver of type {self._storage_class}")
        self._storages = dict()

    def _get_storage_instance(self, name: str) -> Type[Storage]:
        return self._storage_class(name)

    def store_folder(
        self, storage_name: str, folder_name: str, recursive: Optional[bool] = False
    ) -> None:
        logger.debug(f"Uploading folder {folder_name}, recursive: {recursive}")
        storage: Type[Storage] = self.get_storage(
            storage_name, self._create_missing_storage
        )
        for dir_element in os.listdir(folder_name):
            full_file_name: str = os.path.join(folder_name, dir_element)
            if os.path.isdir(full_file_name) and recursive:
                logger.debug(f"Found a Folder, recursively storing: {full_file_name}")
                self.store_folder(storage.name, full_file_name, recursive)
            else:
                import_file_name: str = full_file_name
                if self._reduce_path_when_importing:
                    import_file_name = full_file_name.replace(
                        self._reduce_path_when_importing,
                        ""
                    )
                storage.add_file(full_file_name, import_file_name)

    def get_storage(
        self, name: str, create_if_missing: Optional[bool] = False
    ) -> Type[Storage]:
        if name in self._storages.keys():
            logger.debug(f"Storage {name} cached")
            return self._storages[name]

        storage: Type[Storage] = self._get_storage_instance(name)
        if not storage.exists and create_if_missing:
            logger.info(f"Creating a new storage with name {name}")
            storage.create()
        self._storages.update({name: storage})
        return storage

    def list_storages(self) -> List[Storage]:
        # response = self._client.list_vaults()
        # if "VaultList" not in response:
        #    return []
        # vaults = []
        # for v in response["VaultList"]:
        #    vaults.append(v["VaultName"])
        # return vaults
        pass
