# Bài nộp lab Tracking — 2A202602955

Thành viên: Vũ Thượng Tin — 2A202602955.

## Nộp bài

Nộp năm file video_1.txt đến video_5.txt và BAO_CAO.md. Notebook đã chạy và thư mục evidence đi kèm để đối chiếu. File ZIP không chứa ảnh dữ liệu, trọng số hoặc các video lớn.

| Video | Tracker | conf | iou | Số frame |
|---|---|---|---|---|
| video_1 | botsort | 0.3 | 0.5 | 600 |
| video_2 | bytetrack | 0.15 | 0.5 | 1050 |
| video_3 | bytetrack | 0.3 | 0.5 | 837 |
| video_4 | bytetrack | 0.15 | 0.5 | 900 |
| video_5 | bytetrack | 0.3 | 0.5 | 750 |

Điểm video_1: HOTA 28.228, MOTA 19.800, IDF1 28.517; không có điểm cho bốn video không nhãn.

## Tái lập từ repo bài lab

Kích hoạt môi trường bằng source .venv/bin/activate. Đặt LAB_DATA trỏ tới lab_data đã chuẩn bị. Không thay detector yolo26n.pt, kích thước 640, lớp người hoặc Re-ID osnet_x0_25_msmt17.pt.

```bash
python scripts/check_data.py --lab-data-root "$LAB_DATA"
python scripts/run_tracking.py --source "$LAB_DATA/video_1/img1" --seq-name video_1 --tracker botsort --conf 0.3 --iou 0.5 --out runs/nop_bai --save-video --device cpu --fps 30
python scripts/run_tracking.py --source "$LAB_DATA/video_2/img1" --seq-name video_2 --tracker bytetrack --conf 0.15 --iou 0.5 --out runs/nop_bai --save-video --device cpu
python scripts/run_tracking.py --source "$LAB_DATA/video_3/img1" --seq-name video_3 --tracker bytetrack --conf 0.3 --iou 0.5 --out runs/nop_bai --save-video --device cpu
python scripts/run_tracking.py --source "$LAB_DATA/video_4/img1" --seq-name video_4 --tracker bytetrack --conf 0.15 --iou 0.5 --out runs/nop_bai --save-video --device cpu
python scripts/run_tracking.py --source "$LAB_DATA/video_5/img1" --seq-name video_5 --tracker bytetrack --conf 0.3 --iou 0.5 --out runs/nop_bai --save-video --device cpu
python scripts/evaluate_practice.py --trackeval-root "$PWD/TrackEval" --lab-data-root "$LAB_DATA" --submission runs/nop_bai/video_1.txt --run-name submission_2A202602955
pytest
```

Để thử nhanh, thêm --max-frames 150 và xuất sang thư mục khác; không dùng tùy chọn này cho bản nộp. Khi mở notebook trên máy này, chọn kernel Python (cv_robotics_lab21).

## Chạy từ code trong gói

Chuyển vào thư mục code, dựng môi trường bằng bash scripts/setup_local.sh và tải trọng số bằng bash scripts/download_weights.sh nếu còn thiếu. Chuẩn bị lab_data ở bên ngoài ZIP; video_1 cần eval_config.json chứa {"benchmark":"LAB21","split":"train"}. Các lệnh phía trên chạy từ thư mục code, với LAB_DATA là đường dẫn tuyệt đối tới dữ liệu. Nhãn chỉ dùng cho video_1.

## Bằng chứng

- evidence/VALIDATION.json: kiểm tra số frame, định dạng MOT, preview được giải mã và notebook.
- evidence/experiments.csv và evidence/trials/: các lượt thử 150 frame, cấu hình, file track và log chạy.
- evidence/EVAL_VIDEO_1.txt, video_1_metrics.json: kết quả chấm chính thức.
- evidence/EVAL_BYTETRACK_VIDEO_1.txt: cấu hình đối chiếu chạy toàn bộ 600 frame.
- evidence/final_runs/: cấu hình và số frame của từng file nộp.
- evidence/images/: ảnh nguồn, ảnh so sánh tracker/ngưỡng và ảnh kết quả nộp.

Các video xem thử đủ frame nằm trong runs/nop_bai của repo gốc. Chúng được giữ trên máy để xem, không đưa vào ZIP.
