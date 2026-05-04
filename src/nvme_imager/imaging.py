import logging
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger("nvme-imager")


def validate_dd_available() -> None:
    if shutil.which("dd") is None:
        logger.error("Required command not found: dd")
        sys.exit(1)


def build_dd_command(image_path: str | Path, disk: str) -> list[str]:
    return [
        "sudo",
        "dd",
        f"if={image_path}",
        f"of={disk}",
        "bs=4M",
        "status=progress",
    ]


def burn_image(image_path: str | Path, disk: str, dry_run: bool = True) -> None:
    validate_dd_available()

    command = build_dd_command(image_path, disk)

    if dry_run:
        logger.info("DRY RUN MODE enabled")
        print("\nDRY RUN MODE")
        print("Command that would run:")
        print(" ".join(command))
        print("\nNo disk was written.")
        return

    logger.warning("REAL WRITE MODE enabled")
    logger.warning("Writing image %s to disk %s", image_path, disk)

    try:
        subprocess.run(command, check=True)
        logger.info("Image successfully written.")
    except subprocess.CalledProcessError as error:
        logger.error("Disk imaging failed with exit code %s", error.returncode)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user.")
        sys.exit(0)