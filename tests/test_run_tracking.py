"""Kiểm tra giao diện tracking bằng mô hình giả, không tải trọng số."""

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest


@pytest.fixture
def tracking_module(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    modules = {name: ModuleType(name) for name in ("cv2", "numpy", "torch", "ultralytics", "boxmot", "boxmot.tracker_zoo")}
    config_dir = tmp_path / "boxmot" / "configs"
    config_dir.mkdir(parents=True)
    (config_dir / "bytetrack.yaml").write_text("{}")
    modules["boxmot"].__file__ = str(config_dir.parent / "__init__.py")
    modules["torch"].device = lambda name: ("device", name)
    calls = {}

    class Detector:
        def __init__(self, weights):
            calls["weights"] = weights

        def to(self, device):
            calls["detector_device"] = device
            return self

    modules["ultralytics"].YOLO = Detector

    # Signature cũ không có per_class: phải chạy được mà không đổi phiên bản.
    def factory(tracker_type, tracker_config, reid_weights, device, half):
        calls["tracker"] = (tracker_type, tracker_config, reid_weights, device, half)
        return SimpleNamespace(update=lambda dets, frame: [])

    modules["boxmot.tracker_zoo"].create_tracker = factory
    for name, module in modules.items():
        monkeypatch.setitem(sys.modules, name, module)
    script = Path(__file__).parents[1] / "scripts" / "run_tracking.py"
    spec = importlib.util.spec_from_file_location("tracking_under_test", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "detect", lambda *args, **kwargs: [])
    return module, calls


def test_old_tracker_api_and_evidence_for_empty_frames(tracking_module, monkeypatch, tmp_path: Path) -> None:
    module, calls = tracking_module
    monkeypatch.setattr(module, "iter_frames", lambda source: iter([(0, object()), (1, object())]))
    args = argparse.Namespace(source=str(tmp_path), out=str(tmp_path / "out"), seq_name="video_1",
                              tracker="bytetrack", conf=0.3, iou=0.5, device="cpu",
                              save_video=False, fps=30, max_frames=0)
    module.run(args)
    assert calls["weights"] == "yolo26n.pt"
    assert calls["detector_device"] == "cpu"
    assert calls["tracker"][3] == ("device", "cpu")
    metadata = json.loads((tmp_path / "out" / "video_1_run.json").read_text())
    assert metadata["frames_processed"] == 2
    assert metadata["max_frames"] == 0
    assert metadata["rows"] == 0
    assert metadata["imgsz"] == 640
    assert metadata["class_id"] == 0
    assert (tmp_path / "out" / "video_1.txt").read_text() == ""


def test_corrupt_frame_cannot_be_reported_as_success(tracking_module, monkeypatch, tmp_path: Path) -> None:
    module, _ = tracking_module
    monkeypatch.setattr(module, "iter_frames", lambda source: iter([(0, None)]))
    args = argparse.Namespace(source=str(tmp_path), out=str(tmp_path / "out"), seq_name="video_1",
                              tracker="bytetrack", conf=0.3, iou=0.5, device="cpu",
                              save_video=False, fps=30, max_frames=0)
    with pytest.raises(ValueError, match="frame 1"):
        module.run(args)
    assert not (tmp_path / "out" / "video_1.txt").exists()
    assert not (tmp_path / "out" / "video_1_run.json").exists()
