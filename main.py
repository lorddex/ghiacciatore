# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import argparse
import logging
import sys
from typing import Optional

from ghiacciatore.archiver.archiver import Archiver
from ghiacciatore.storages.enums import StorageType

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main(
    storage_type: StorageType,
    storage_name: str,
    path: str,
    create_missing_storage: Optional[bool] = False,
    reduce_path_when_importing: Optional[str] = None,
) -> None:
    ghiacciatore: Archiver = Archiver(
        StorageType.value_of(storage_type.lower()),
        create_missing_storage=create_missing_storage,
        reduce_path_when_importing=reduce_path_when_importing,
    )
    ghiacciatore.store_folder(storage_name, path, recursive=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Synchronises a local folder to a remote AWS S3 or Glacier Storage."
    )
    parser.add_argument(
        "--storage-type",
        default=StorageType.AWS_S3.value,
        help="The type of storage to use (s3 -default-, glacier)",
    )
    parser.add_argument(
        "--storage-name",
        default="ghiacciatore",
        help="The name of the storage that will be used as name of the created resource "
        "(Vault or Bucket)",
    )
    parser.add_argument(
        "--create-missing-storage",
        action="store_true",
        default=False,
        help="If the storage (Vault or Bucket) must be created if missing",
    )
    parser.add_argument(
        "--reduce-path-when-importing",
        help="Prefix of the `path` parameter that must not be used when importing the file in the"
        " storage.\nE.g. if path is /home/test/folder, and this parameter is /home/test, in "
        "the destination `/home/test` won't be used",
    )
    parser.add_argument("path", help="The file or folder to backup")
    args = parser.parse_args()
    logger.info("Starting Ghiacciatore")
    main(
        args.storage_type,
        args.storage_name,
        args.path,
        args.create_missing_storage,
        args.reduce_path_when_importing,
    )
    logger.info("End Ghiacciatore")
