# Lab Tracking — đã hoàn thành

- Đã chạy notebook: ba câu ôn metric đúng; có output YOLO thật và ảnh phát hiện người.
- Đã kiểm tra toàn bộ 4.137 ảnh, tạo preview nguồn và xem ảnh mẫu của cả năm cảnh.
- Đã thực hiện 34 lượt thử 150 frame, tối thiểu ByteTrack và BoT-SORT cho mỗi video, quét conf/iou cho các cấu hình chọn.
- Đã chọn BoT-SORT conf=0.3 cho video_1; ByteTrack conf=0.15 cho video_2 và video_4, conf=0.3 cho video_3 và video_5. Tất cả dùng iou=0.5.
- Năm file trong runs/nop_bai chạy đủ 600/1050/837/900/750 frame; xác minh định dạng MOT và giải mã đủ toàn bộ frame của video preview.
- Điểm video_1: HOTA 28.228, MOTA 19.800, IDF1 28.517. Bốn video khác chỉ có quan sát, không chấm số khi không có nhãn.
- Báo cáo đã điền trong BAO_CAO.md và submission_template/BAO_CAO_mau.md; phân tích cả năm video, nêu các lỗi còn lại.
- 10 unit test của lab đạt. Bằng chứng kiểm tra nằm trong runs/nop_bai/VALIDATION.json.
- Bài nộp được đóng gói trong K4-Day22-2A202602955-submission.zip và thư mục submission_2A202602955.

Trọng số và dữ liệu giữ trên máy, không đưa vào ZIP. Video có ID nằm trong runs/nop_bai để xem lại. Cách tái lập nằm trong README_NOP_BAI.md.
