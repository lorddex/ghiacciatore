import logging
import sys

from archiver.archiver import Archiver
from storages.enums import StorageType
import argparse

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main(storage_type: StorageType, storage_name: str, path: str) -> None:
    ghiacciatore: Archiver = Archiver(StorageType.value_of(storage_type.lower()))
    ghiacciatore.store_folder(storage_name, path, recursive=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Starts a Synchronisation")
    parser.add_argument(
        "--storage-type",
        default=StorageType.AWS_S3.value,
        help="The type of storage to use (s3 -default-, glacier)",
    )
    parser.add_argument(
        "--storage-name",
        default="ghiacciatore",
        help="The name of the storage that will be used as name of the created resource (Vault or Bucket)",
    )
    parser.add_argument("path", help="The file or folder to backup")
    args = parser.parse_args()
    logger.debug("Starting Ghiacciatore")
    main(args.storage_type, args.storage_name, args.path)
