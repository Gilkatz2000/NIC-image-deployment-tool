import logging
import platform
import re
import subprocess
import sys

from .size_utils import format_size


logger = logging.getLogger("nvme-imager")


def list_linux_disks():
    result = subprocess.run(
        ["lsblk", "-b", "-d", "-o", "NAME,SIZE,TYPE,MODEL"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        logger.error("Error running lsblk.")
        sys.exit(1)

    disks = []

    for line in result.stdout.strip().splitlines()[1:]:
        parts = line.split()

        if len(parts) < 3:
            continue

        name = parts[0]
        size_bytes = int(parts[1])
        disk_type = parts[2]
        model = " ".join(parts[3:]) if len(parts) > 3 else "Unknown model"

        if disk_type == "disk":
            disks.append({
                "path": f"/dev/{name}",
                "size_bytes": size_bytes,
                "model": model,
            })

    return disks


def list_macos_disks():
    result = subprocess.run(
        ["diskutil", "list"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        logger.error("Error running diskutil list.")
        sys.exit(1)

    disks = []

    for line in result.stdout.splitlines():
        line = line.strip()

        if line.startswith("/dev/disk"):
            disk_path = line.split()[0]
            size_bytes = get_macos_disk_size_bytes(disk_path)

            disks.append({
                "path": disk_path,
                "size_bytes": size_bytes,
                "model": "macOS disk",
            })

    return disks


def get_macos_disk_size_bytes(disk):
    result = subprocess.run(
        ["diskutil", "info", disk],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return None

    for line in result.stdout.splitlines():
        if "Disk Size" in line:
            match = re.search(r"\((\d+)\s+Bytes\)", line)
            if match:
                return int(match.group(1))

    return None


def list_disks():
    current_os = platform.system()

    if current_os == "Linux":
        return list_linux_disks()

    if current_os == "Darwin":
        return list_macos_disks()

    logger.error(f"Unsupported operating system: {current_os}")
    sys.exit(1)


def is_system_disk(disk_path):
    current_os = platform.system()

    if current_os == "Darwin":
        return disk_path == "/dev/disk0"

    if current_os == "Linux":
        result = subprocess.run(
            ["findmnt", "-n", "-o", "SOURCE", "/"],
            capture_output=True,
            text=True,
            check=False,
        )

        root_source = result.stdout.strip()
        return root_source.startswith(disk_path)

    return False


def validate_disk_is_safe(disk_path):
    if is_system_disk(disk_path):
        logger.error(f"Refusing to use protected system disk: {disk_path}")
        sys.exit(1)


def select_disk():
    disks = list_disks()

    if not disks:
        logger.error("No disks detected.")
        sys.exit(1)

    print("\nAvailable Disks:\n")

    for index, disk in enumerate(disks):
        disk_path = disk["path"]
        size = (
            format_size(disk["size_bytes"])
            if disk["size_bytes"] is not None
            else "size unknown"
        )
        model = disk["model"]
        protected_label = " [SYSTEM/PROTECTED]" if is_system_disk(disk_path) else ""

        print(f"{index}: {disk_path} ({size}, {model}){protected_label}")

    while True:
        try:
            choice = int(input("\nSelect target disk number: ").strip())
            selected_disk = disks[choice]

            if is_system_disk(selected_disk["path"]):
                print(f"\nRefusing to use protected system disk: {selected_disk['path']}")
                print("Please choose another disk.")
                continue

            return selected_disk

        except (ValueError, IndexError):
            print("Invalid disk selection. Please try again.")

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)


def validate_image_fits_disk(image_path, disk):
    image_size = image_path.stat().st_size
    disk_size = disk["size_bytes"]

    if disk_size is None:
        print("\nWarning: Could not determine target disk size.")
        print("Skipping image size validation.")
        return

    print("\nCapacity Check:")
    print(f"Image size: {format_size(image_size)}")
    print(f"Disk size:  {format_size(disk_size)}")

    if image_size > disk_size:
        print("\nERROR: Image is larger than the target disk.")
        print("Operation blocked to prevent a failed or partial write.")
        sys.exit(1)

    print("Capacity check passed.")


def confirm_operation(image_path, disk, dry_run=True):
    disk_path = disk["path"]

    validate_disk_is_safe(disk_path)
    validate_image_fits_disk(image_path, disk)

    print("\n⚠️ WARNING ⚠️")
    print(f"This will ERASE ALL DATA on {disk_path}")
    print(f"Image: {image_path}")

    while True:
        try:
            confirm = input("\nType YES to continue or NO to cancel: ").strip().upper()

            if confirm == "YES":
                break

            if confirm == "NO":
                print("Operation cancelled.")
                sys.exit(0)

            print("Invalid input. Please type YES or NO.")

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)

    if not dry_run:
        while True:
            try:
                final_confirm = input(
                    "\nREAL WRITE MODE ENABLED. Type BURN to execute or CANCEL to stop: "
                ).strip().upper()

                if final_confirm == "BURN":
                    break

                if final_confirm == "CANCEL":
                    print("Operation cancelled.")
                    sys.exit(0)

                print("Invalid input. Please type BURN or CANCEL.")

            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                sys.exit(0)