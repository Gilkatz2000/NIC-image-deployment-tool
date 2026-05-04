from src.nvme_imager.size_utils import format_size


def test_format_size_bytes():
    assert format_size(0) == "0 bytes"
    assert format_size(512) == "512 bytes"


def test_format_size_kb():
    assert format_size(1024) == "1.0 KB"


def test_format_size_mb():
    assert format_size(1024 ** 2) == "1.0 MB"


def test_format_size_gb():
    assert format_size(1024 ** 3) == "1.0 GB"


def test_format_size_unknown():
    assert format_size(None) == "unknown"