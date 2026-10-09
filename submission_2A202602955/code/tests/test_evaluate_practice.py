"""Kiểm tra chuẩn bị chấm, không cần ảnh hay thư viện tracking."""

import configparser
import json
from pathlib import Path

import pytest

from evaluate_practice import _load_eval_config, run_trackeval, stage


def test_load_config(tmp_path: Path) -> None:
    folder = tmp_path / "video_1"
    folder.mkdir()
    (folder / "eval_config.json").write_text(json.dumps({"benchmark": "LAB21", "split": "train"}))
    assert _load_eval_config(tmp_path) == {"benchmark": "LAB21", "split": "train"}


def test_missing_config_is_explicit(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="eval_config.json"):
        _load_eval_config(tmp_path)


def test_stage_preserves_labels_and_normalizes_metadata(tmp_path: Path) -> None:
    source = tmp_path / "lab_data" / "video_1"
    (source / "gt").mkdir(parents=True)
    labels = "1,1,0,0,10,10,1,1,1\n"
    (source / "gt" / "gt.txt").write_text(labels)
    original = "[Sequence]\nname=original_sequence\nseqLength=3\nframeRate=30\n"
    (source / "seqinfo.ini").write_text(original)
    submission = tmp_path / "video_1.txt"
    submission.write_text("1,1,0,0,10,10,0.9,-1,-1,-1\n")
    root = tmp_path / "TrackEval"

    stage(root, source.parent, submission, "trial", "LAB21", "test")

    dest = root / "data" / "gt" / "mot_challenge" / "LAB21-test" / "video_1"
    assert (dest / "gt" / "gt.txt").read_text() == labels
    metadata = configparser.ConfigParser()
    metadata.read(dest / "seqinfo.ini")
    assert metadata["Sequence"]["name"] == "video_1"
    assert metadata["Sequence"]["seqLength"] == "3"
    assert (source / "seqinfo.ini").read_text() == original
    result = root / "data" / "trackers" / "mot_challenge" / "LAB21-test" / "trial" / "data" / "video_1.txt"
    assert result.read_text() == submission.read_text()


def test_numpy_patch_runs_in_child(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    calls = []
    monkeypatch.setattr("evaluate_practice.subprocess.run", lambda cmd, **kwargs: calls.append((cmd, kwargs)))
    run_trackeval(tmp_path, "trial", "LAB21", "train")
    cmd, kwargs = calls[0]
    assert cmd[1] == "-c"
    assert "np.float = getattr(np, 'float', float)" in cmd[2]
    assert "np.int = getattr(np, 'int', int)" in cmd[2]
    assert "np.bool = getattr(np, 'bool', bool)" in cmd[2]
    assert "runpy.run_path" in cmd[2]
    assert cmd[cmd.index("--SEQ_INFO") + 1] == "video_1"
    assert cmd[cmd.index("--BREAK_ON_ERROR") + 1] == "True"
    assert kwargs["check"] is True
    assert kwargs["env"]["MPLBACKEND"] == "Agg"
    assert kwargs["env"]["PYTHONUNBUFFERED"] == "1"
