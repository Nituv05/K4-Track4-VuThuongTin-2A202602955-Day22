#!/usr/bin/env bash
# Chuẩn bị môi trường và trọng số trong thư mục bài lab.
set -euo pipefail
cd "$(dirname "$0")/.."

export PIP_CACHE_DIR="$PWD/.cache/pip"
export MPLCONFIGDIR="$PWD/.config/matplotlib"
export YOLO_CONFIG_DIR="$PWD/.config/ultralytics"
export TORCH_HOME="$PWD/.cache/torch"
mkdir -p "$PIP_CACHE_DIR" "$MPLCONFIGDIR" "$YOLO_CONFIG_DIR" "$TORCH_HOME"
if [[ "${LAB_SETUP_LOGGING:-0}" != "1" ]]; then
    export LAB_SETUP_LOGGING=1
    bash "$PWD/scripts/setup_local.sh" "$@" 2>&1 | tee "$PWD/.cache/setup_local.log"
    exit 0
fi
# Chỉ rõ kho chính thức thay vì dùng cấu hình kho gói của Terminal.
export PIP_INDEX_URL="https://pypi.org/simple"

if [[ ! -x .venv/bin/python ]]; then
    python3.12 -m venv .venv
fi
PYTHON="$PWD/.venv/bin/python"

"$PYTHON" -m pip install --upgrade pip wheel
# BoxMOT 10 còn dùng pkg_resources, cần bản setuptools có mô-đun này.
"$PYTHON" -m pip install 'setuptools==79.0.1'
# BoxMOT 10.0.42 ghim NumPy 1.23.1, chưa có wheel Python 3.12.
# Giữ nguyên phiên bản tracker; cài riêng phụ thuộc với NumPy 1.26.4.
# Mac ARM + Python 3.12: dùng đúng wheel chính thức, không phụ thuộc
# việc pip liệt kê được phiên bản NumPy trên trang simple index.
PLATFORM="$($PYTHON -c 'import platform,sys; print(f"{platform.system()}-{platform.machine()}-{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ "$PLATFORM" == "Darwin-arm64-3.12" ]]; then
    NUMPY_WHEEL="https://files.pythonhosted.org/packages/75/5b/ca6c8bd14007e5ca171c7c03102d17b4f4e0ceb53957e8c44343a9546dcc/numpy-1.26.4-cp312-cp312-macosx_11_0_arm64.whl#sha256=03a8c78d01d9781b28a6989f6fa1bb2c4f2d51201cf99d3dd875df6fbd96b23b"
    "$PYTHON" -m pip install --no-deps "$NUMPY_WHEEL"
else
    "$PYTHON" -m pip install 'numpy==1.26.4'
fi
"$PYTHON" -m pip install \
    'numpy==1.26.4' 'opencv-python==4.11.0.86' \
    'torch==2.5.1' 'torchvision==0.20.1' \
    'ultralytics>=8.4,<8.5' 'scipy==1.14.1' 'pandas==2.2.3' \
    'scikit-learn>=1.3,<1.6' 'filterpy>=1.4.5' 'ftfy>=6.1.1' \
    'gdown>=4.7.1' 'GitPython>=3.1.0' 'lapx>=0.5.4' 'loguru>=0.7.0' \
    'PyYAML>=5.3.1' 'regex>=2023.6.3' 'tensorboard>=2.13.0' \
    'yacs>=0.1.8' 'pre-commit>=3.3.3' matplotlib pytest \
    nbformat nbclient ipykernel tqdm tabulate pillow
"$PYTHON" -m pip install --no-deps 'boxmot==10.0.42'

if [[ ! -d TrackEval ]]; then
    git clone https://github.com/JonathonLuiten/TrackEval.git TrackEval
fi
"$PYTHON" -m pip install --no-deps -e TrackEval/

# Tải đúng detector của đề và để BoxMOT tải đúng Re-ID của đề.
"$PYTHON" - <<'PY'
import inspect
from pathlib import Path

import boxmot
import torch
from ultralytics import YOLO
from boxmot.tracker_zoo import create_tracker

YOLO("yolo26n.pt")
config = Path(boxmot.__file__).parent / "configs" / "botsort.yaml"
kwargs = {
    "tracker_type": "botsort",
    "tracker_config": config,
    "reid_weights": Path("osnet_x0_25_msmt17.pt"),
    "device": torch.device("cpu"),
    "half": False,
}
if "per_class" in inspect.signature(create_tracker).parameters:
    kwargs["per_class"] = False
create_tracker(**kwargs)
print("Đã nạp được detector và tracker có Re-ID.")
PY

"$PYTHON" -m pytest -q
printf '\nMôi trường đã sẵn sàng. Quay lại Codex để tiếp tục chạy thí nghiệm.\n'
