"""Tests for check() without lab images or a network."""

from pathlib import Path

from check_data import check


def _touch_jpg(directory: Path, name: str = "000001.jpg") -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_bytes(b"")


def _lab_tree(root: Path, with_practice_gt: bool = True, extra_images: bool = True) -> None:
    for index in range(1, 6):
        name = f"video_{index}"
        if extra_images or name == "video_1":
            _touch_jpg(root / name / "img1")
        else:
            (root / name).mkdir(parents=True, exist_ok=True)
    if with_practice_gt:
        gt_dir = root / "video_1" / "gt"
        gt_dir.mkdir(parents=True, exist_ok=True)
        (gt_dir / "gt.txt").write_text("1,1,0,0,10,10,1,1,1\n", encoding="utf-8")


def test_ready_pack_passes(tmp_path: Path) -> None:
    _lab_tree(tmp_path)
    assert check(tmp_path) is True


def test_missing_images_fails(tmp_path: Path) -> None:
    _lab_tree(tmp_path, extra_images=False)
    assert check(tmp_path) is False


def test_video_without_labels_still_passes(tmp_path: Path) -> None:
    _lab_tree(tmp_path)
    assert not (tmp_path / "video_2" / "gt").exists()
    assert check(tmp_path) is True


def test_practice_video_without_labels_fails(tmp_path: Path) -> None:
    _lab_tree(tmp_path, with_practice_gt=False)
    assert check(tmp_path) is False
