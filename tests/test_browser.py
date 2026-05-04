from src.nvme_imager.browser import get_images


def test_get_images_returns_sorted_files(tmp_path):
    (tmp_path / "windows.img").write_text("test")
    (tmp_path / "ubuntu.img").write_text("test")

    images = get_images(tmp_path)

    assert images == ["ubuntu.img", "windows.img"]