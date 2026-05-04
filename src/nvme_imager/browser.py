import logging
import sys
from pathlib import Path

from .size_utils import format_size


logger = logging.getLogger("nvme-imager")


def get_images(image_dir):
    if not image_dir.exists():
        logger.error(f"Image directory does not exist: {image_dir}")
        sys.exit(1)

    images = [
        file.name
        for file in image_dir.iterdir()
        if file.is_file()
    ]

    if not images:
        logger.error("No image files found.")
        sys.exit(1)

    return sorted(images)


def get_image_size_bytes(image_path):
    return Path(image_path).stat().st_size


def select_image(images, image_dir):
    print("Available Images:\n")

    for index, image in enumerate(images):
        image_path = Path(image_dir) / image
        image_size = get_image_size_bytes(image_path)
        print(f"{index}: {image} ({format_size(image_size)})")

    while True:
        try:
            choice = int(input("\nSelect image number: ").strip())
            return images[choice]

        except (ValueError, IndexError):
            print("Invalid image selection. Please try again.")

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)