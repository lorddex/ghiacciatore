import logging
import sys

import pystray
from PIL import Image, ImageDraw
from pystray import Menu, MenuItem

from archiver.archiver import Archiver
from storages.enums import StorageType

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


state = False


def on_clicked(icon, item):
    global state
    state = not item.checked


def main():
    # ghiacciatore = Archiver(StorageType.AWS_S3)
    # storages = ghiacciatore.list_storages()
    # logger.debug(f"Found {len(storages)} vaults.")
    # ghiacciatore.get_storage("ghiacciatore", create_if_missing=True)
    # upload = ghiacciatore.store_file("ghiacciatore", "test_upload.txt")
    # logger.debug(upload)
    # ghiacciatore.store_folder("ghiacciatore", "test", recursive=True)

    icon = pystray.Icon(
        "Ghiacciatore",
        icon=Image.open("icon.png"),
        menu=Menu(
            MenuItem("Checkable", on_clicked, checked=lambda item: state),
            MenuItem("Checkable", on_clicked, checked=lambda item: state),
        ),
    )
    icon.run()


if __name__ == "__main__":
    logger.debug("Starting main")
    main()
