from src.nvme_imager.imaging import build_dd_command


def test_build_dd_command():
    command = build_dd_command("/images/test.img", "/dev/sdb")

    assert command == [
        "sudo",
        "dd",
        "if=/images/test.img",
        "of=/dev/sdb",
        "bs=4M",
        "status=progress",
    ]