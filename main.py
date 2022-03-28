import logging
import sys

from archiver.archiver import Archiver
from storages.enums import StorageType

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    ghiacciatore = Archiver(StorageType.AWS_S3)
    # storages = ghiacciatore.list_storages()
    # logger.debug(f"Found {len(storages)} vaults.")
    # ghiacciatore.get_storage("ghiacciatore", create_if_missing=True)
    # upload = ghiacciatore.store_file("ghiacciatore", "test_upload.txt")
    # logger.debug(upload)

    ghiacciatore.store_folder("ghiacciatore", "test", recursive=True)


if __name__ == "__main__":
    logger.debug("Starting main")
    main()
