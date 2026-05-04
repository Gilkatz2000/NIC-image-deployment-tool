import argparse
from pathlib import Path

from .browser import get_images, select_image
from .disk import select_disk, confirm_operation, validate_disk_is_safe, validate_image_fits_disk
from .imaging import burn_image
from .config import DEFAULT_IMAGE_DIR
from .logger import setup_logger


def parse_args():
    parser = argparse.ArgumentParser(
        description="NVMe Image Deployment Tool"
    )

    parser.add_argument(
        "--image",
        help="Image file name"
    )

    parser.add_argument(
        "--disk",
        help="Target disk path"
    )

    parser.add_argument(
        "--image-dir",
        type=Path,
        default=DEFAULT_IMAGE_DIR,
        help="Directory containing image files"
    )

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually write image to disk"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed logging"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    logger = setup_logger(args.verbose)

    image_dir = args.image_dir
    dry_run = not args.execute

    logger.info("Starting NVMe Image Deployment Tool")
    logger.info(f"Image directory: {image_dir}")
    logger.info(f"Dry run mode: {dry_run}")

    images = get_images(image_dir)

    if args.image:
        if args.image not in images:
            logger.error("Specified image not found in directory.")
            return
        selected_image = args.image
    else:
        selected_image = select_image(images, image_dir)

    image_path = Path(image_dir) / selected_image
    logger.info(f"Selected image: {selected_image}")

    if args.disk:
        disk = {
            "path": args.disk,
            "size_bytes": None,
            "model": "manual input",
        }
        validate_disk_is_safe(disk["path"])
    else:
        disk = select_disk()

    logger.info(f"Selected disk: {disk['path']}")

    confirm_operation(image_path, disk, dry_run=dry_run)
    burn_image(image_path, disk["path"], dry_run=dry_run)

    logger.info("Operation completed")