#!/usr/bin/env bash
# Chỉ tải hai trọng số còn thiếu; không cài lại các thư viện.
set -euo pipefail
cd "$(dirname "$0")/.."
export MPLCONFIGDIR="$PWD/.config/matplotlib"
export YOLO_CONFIG_DIR="$PWD/.config/ultralytics"
export TORCH_HOME="$PWD/.cache/torch"

if [[ ! -s yolo26n.pt ]]; then
    printf 'Đang tải detector cố định của đề...\n'
    curl --fail --location --retry 2 --connect-timeout 20 \
        'https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26n.pt' \
        --output yolo26n.pt.partial
    mv yolo26n.pt.partial yolo26n.pt
fi
if [[ ! -s osnet_x0_25_msmt17.pt ]]; then
    printf 'Đang tải Re-ID cố định của đề...\n'
    .venv/bin/python -m gdown \
        'https://drive.google.com/uc?id=1sSwXSUlj4_tHZequ_iZ8w_Jh0VaRQMqF' \
        --output osnet_x0_25_msmt17.pt.partial
    mv osnet_x0_25_msmt17.pt.partial osnet_x0_25_msmt17.pt
fi

.venv/bin/python - <<'PY'
from pathlib import Path
import torch
from ultralytics import YOLO
from boxmot.tracker_zoo import create_tracker, get_tracker_config

YOLO("yolo26n.pt")
create_tracker("botsort", get_tracker_config("botsort"),
               Path("osnet_x0_25_msmt17.pt"), torch.device("cpu"), False, False)
print("Đã tải và nạp được cả hai trọng số. Môi trường đã sẵn sàng chạy lab.")
PY
