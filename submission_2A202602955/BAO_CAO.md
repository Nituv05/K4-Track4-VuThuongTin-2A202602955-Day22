# Báo cáo lab: chọn tracker cho 5 video

**Nhóm:** 2A202602955
**Thành viên:** Vũ Thượng Tin — 2A202602955

Detector cố định: `yolo26n.pt`, ảnh đầu vào 640 px, chỉ lớp người (`class_id=0`); Re-ID cố định `osnet_x0_25_msmt17.pt`. Không huấn luyện hoặc đổi các mô hình này, không sửa tham số bên trong tracker.

## 1. Cấu hình đã chọn

| Video | Tracker | conf | iou | Frame đã chạy | Quan sát khi xem kết quả | Đã thử nhưng loại |
|---|---|---|---|---|---|---|
| video_1 | botsort | 0.3 | 0.5 | 600 | Các nhóm gần camera có track; vẫn bỏ sót nhiều người nhỏ ở xa. BoT-SORT có HOTA/MOTA/IDF1 tốt hơn ByteTrack trên toàn bộ 600 frame, dù số lần đổi ID lớn hơn. | ByteTrack conf=0.3, iou=0.5: HOTA 26.912, MOTA 17.292, IDF1 25.713; thấp hơn cấu hình chọn. |
| video_2 | bytetrack | 0.15 | 0.5 | 1050 | Các ID chính ở phần gần camera giữ được qua frame 30/75/150. conf=0.15 giữ thêm hộp qua đoạn điểm tin cậy thấp; conf=0.5 làm mất người ở vùng xa tại frame 150. | ByteTrack conf=0.5, iou=0.5: nhiều hộp xa biến mất; BoT-SORT conf=0.3 có thêm track nhưng chưa có ưu thế đủ rõ về giữ ID ở các người chính. |
| video_3 | bytetrack | 0.3 | 0.5 | 837 | Hai người gần camera giữ ID 1 và 2 ở frame 30/75/150 với cả hai tracker. Chưa thấy lợi ích rõ của Re-ID trên đoạn thử; vẫn có track ngắn khi người bị cắt ở biên ảnh. | BoT-SORT conf=0.3, iou=0.5: hai ID chính cũng ổn định, nhưng có thêm các track ngắn; chi phí Re-ID cao hơn trên CPU. |
| video_4 | bytetrack | 0.15 | 0.5 | 900 | Người áo đỏ và áo trắng gần camera được giữ track. Người phía sau bên trái còn ID 7 ở frame 75 và 150 với conf=0.15, trong khi conf=0.3 cho ID 16 rồi 23 tại vị trí tương ứng. | ByteTrack conf=0.5: còn track ở người lớn nhưng hộp người phía sau kém liên tục; BoT-SORT conf=0.3 chưa vượt rõ hai track chính. |
| video_5 | bytetrack | 0.3 | 0.5 | 750 | Các hộp ở người nhỏ trên vỉa hè còn thiếu; camera tiến và rẽ làm người ra/vào khung hình. Ở đoạn đầu, ByteTrack giữ các ID 2 và 14 qua frame 30/75; Re-ID chưa loại bỏ hiện tượng sinh track mới. | ByteTrack conf=0.5: đoạn thử chỉ có 518 dòng track so với 673 ở conf=0.3, đồng thời mất một số người nhỏ nhìn thấy; BoT-SORT sinh nhiều ID hơn. |

Cả năm file nộp được chạy trên ảnh `img1/` với toàn bộ frame, không dùng `--max-frames`. Các lượt thử dùng 150 frame đầu, mỗi lần đổi một ngưỡng. Mỗi video so sánh ByteTrack với BoT-SORT; thử ByteTrack tại `conf=0.15/0.3/0.5`, `iou=0.4/0.5/0.7`. Với BoT-SORT được chọn cho video_1, cũng thử các ngưỡng này trước khi giữ cấu hình `conf=0.3, iou=0.5` có số liệu chấm toàn chuỗi. Thay IoU trong các lượt thử ảnh hưởng nhỏ đến các track chính, nên giữ 0.5. Bảng toàn bộ lượt thử và số frame nằm ở `evidence/experiments.csv`.

Việc quan sát dùng ảnh gốc, video có vẽ ID và ảnh so sánh tại các frame 30, 75, 150; bản chạy toàn chuỗi được kiểm tra thêm tại các frame trải đều từ đầu tới cuối. Số dòng track hoặc số ID là mô tả file kết quả, không phải độ chính xác hay số lần đổi ID. Các lượt chạy có thể đồng thời, nên FPS trong log là tốc độ của lần chạy này, không phải benchmark CPU độc lập.

## 2. Số liệu video_1

Chấm bằng `scripts/evaluate_practice.py` trên toàn bộ 600 frame; chỉ dùng nhãn được phát cho video_1. Kết quả chọn và cấu hình đối chiếu đều chấm trên cùng detector, dữ liệu và toàn chuỗi:

| Cấu hình | HOTA | MOTA | IDF1 | TP | FN | FP | Đổi ID |
|---|---:|---:|---:|---:|---:|---:|---:|
| **BoT-SORT, conf=0.3, iou=0.5 — nộp** | **28.228** | **19.800** | **28.517** | 4043 | 14538 | 338 | 26 |
| ByteTrack, conf=0.3, iou=0.5 | 26.912 | 17.292 | 25.713 | 3332 | 15249 | 107 | 12 |

HOTA, MOTA và IDF1 ở bảng là điểm theo thang phần trăm do TrackEval in ra. Kết quả còn nhiều bỏ sót; không diễn giải các điểm này thành chất lượng tracking tốt tuyệt đối. BoT-SORT tăng recall từ 17.932 lên 21.759 nhưng cũng tăng hộp giả và số lần đổi ID. Trong trường hợp này, ba điểm tổng tốt hơn không đồng nghĩa với việc đổi ID ít hơn.

Output gốc của lệnh chấm cấu hình nộp:

```text
HOTA: submission_2A202602955-pedestrianHOTA      DetA      AssA      DetRe     DetPr     AssRe     AssPr     LocA      OWTA      HOTA(0)   LocA(0)   HOTALocA(0)
video_1                            28.228    18.083    44.309    18.587    78.832    48.622    77.754    83.649    28.65     34.399    78.398    26.968
COMBINED                           28.228    18.083    44.309    18.587    78.832    48.622    77.754    83.649    28.65     34.399    78.398    26.968

CLEAR: submission_2A202602955-pedestrianMOTA      MOTP      MODA      CLR_Re    CLR_Pr    MTR       PTR       MLR       sMOTA     CLR_TP    CLR_FN    CLR_FP    IDSW      MT        PT        ML        Frag
video_1                            19.8      81.477    19.94     21.759    92.285    12.903    19.355    67.742    15.769    4043      14538     338       26        8         12        42        99
COMBINED                           19.8      81.477    19.94     21.759    92.285    12.903    19.355    67.742    15.769    4043      14538     338       26        8         12        42        99

Identity: submission_2A202602955-pedestrianIDF1      IDR       IDP       IDTP      IDFN      IDFP
video_1                            28.517    17.62     74.732    3274      15307     1107
COMBINED                           28.517    17.62     74.732    3274      15307     1107
```

Log đầy đủ: `evidence/EVAL_VIDEO_1.txt`; bảng máy đọc được: `evidence/video_1_metrics.json`. video_2 đến video_5 không có nhãn trong gói lab, chỉ ghi quan sát, không điền HOTA/MOTA/IDF1.

## 3. Phân tích

### video_1 — camera tĩnh, ban ngày

Cảnh có người đi cắt nhau và nhiều người nhỏ ở sâu trong quảng trường, nên vừa cần giữ danh tính vừa cần phát hiện đủ người. Chọn BoT-SORT vì trên toàn bộ 600 frame, HOTA tăng 1.316 điểm và IDF1 tăng 2.804 điểm so với ByteTrack. Mô hình có Re-ID cho thêm khả năng dùng ngoại hình, nhưng kết quả ở đây chủ yếu thể hiện giảm bỏ sót: FN giảm 711 trong khi FP tăng 231 và số lần đổi ID tăng từ 12 lên 26. Do đó không kết luận Re-ID luôn tốt hơn về gán danh tính; detector cố định vẫn bỏ sót nhiều người nhỏ, giới hạn cả hai tracker.

### video_2 — camera tĩnh trên cao, ban đêm

Camera tĩnh giúp chuyển động của hộp qua các frame tương đối đều, nên ByteTrack là lựa chọn đủ hợp lý cho các người ở vùng gần camera đã quan sát. Chọn conf=0.15 vì ngưỡng này giữ các hộp tin cậy thấp để tracker nối tiếp track, trong khi conf=0.5 làm mất một số người ở xa tại frame 150. Đoạn thử có 1377 dòng track và 15 ID với conf=0.15, so với 1313 dòng và 16 ID ở conf=0.3; đây là bằng chứng về thay đổi đầu ra, không chứng minh độ chính xác khi không có nhãn. Cột đèn, xe và các nhóm người che khuất nhau vẫn là nguồn mất track; Re-ID được thử nhưng chưa cho ưu thế đủ rõ ở các ID chính để chọn nó cho cảnh này.

### video_3 — camera di chuyển, ảnh 640×480

Camera và người cùng di chuyển, người gần camera có hộp lớn, bị cắt ở biên và thay đổi tỉ lệ nhanh. Trong đoạn thử, cả ByteTrack và BoT-SORT giữ ID 1 cho người áo kẻ và ID 2 cho người áo xám ở frame 30, 75 và 150. Chọn ByteTrack conf=0.3 vì lợi ích giữ ID của Re-ID chưa thể hiện rõ ở hai track này, còn ngưỡng 0.5 giảm các hộp yếu. Đây là kết luận từ đoạn thử và video nộp đã xem mẫu, không đảm bảo không có đổi ID ở phần khác của toàn chuỗi.

### video_4 — trong nhà, camera tiến tới

Người áo đỏ và người áo trắng đi trước camera là hai track chính cần giữ liên tục. Chọn ByteTrack conf=0.15 vì ở người phía sau bên trái, ID 7 giữ từ frame 75 tới 150, trong khi cấu hình conf=0.3 cho các ID 16 và 23 ở vị trí tương ứng. Kính và mặt sàn phản chiếu khiến ngưỡng thấp có nguy cơ thêm hộp nhầm; qua các frame mẫu chưa thấy lợi ích rõ của tăng conf lên 0.5 cho hai track chính. Vì không có nhãn, ưu tiên liên tục ở người nhìn thấy và ghi rõ nguy cơ phản chiếu, thay vì suy diễn số lần đổi ID cho cả video. Ở ảnh kiểm tra toàn chuỗi, người áo đỏ vẫn đổi ID qua các đoạn sau (ID 25 tại frame 338 và ID 54 tại frame 562), nên cấu hình này chưa giải quyết được che khuất dài.

### video_5 — camera trên phương tiện, giao lộ

Camera tiến và rẽ làm nền, kích thước người và vị trí hộp biến đổi, đồng thời cột và biển báo che khuất người. Chọn ByteTrack conf=0.3 vì ở đoạn đầu các ID 2 và 14 được giữ qua frame 30 và 75, còn conf=0.5 mất thêm người nhỏ thấy được ở vỉa hè. BoT-SORT có thêm hộp và ID trong đoạn thử nhưng chưa loại bỏ việc sinh track mới khi đối tượng bị che hoặc ra/vào vùng nhìn. Cấu hình chọn cân bằng số hộp được giữ với độ ổn định quan sát được; vẫn còn bỏ sót và không coi số ID ít hơn là bằng chứng tự động của chất lượng tốt hơn.

## 4. Nếu có thêm thời gian

Tôi sẽ thử các đoạn có che khuất dài và camera rẽ, rồi quét conf mịn hơn quanh cấu hình đã chọn để kiểm tra tính ổn định. Phần mở rộng có thể thử Re-ID khác, nhưng bài nộp chính này giữ nguyên Re-ID của đề.

## 5. Kiểm tra và tái lập

- Ôn metric trong notebook: True / False / True; ba câu đều đúng. Detector ở một frame video_1 cho 14, 6 và 5 hộp ở conf=0.15, 0.3 và 0.5.
- Dữ liệu gồm 600 / 1050 / 837 / 900 / 750 frame; tổng 4137 ảnh đã đọc, không ảnh hỏng.
- Môi trường thực tế: Python 3.12, Ultralytics 8.4.174, BoxMOT 10.0.42, PyTorch 2.5.1, NumPy 1.26.4; chạy CPU. Dùng venv trong workspace vì máy không có Conda; giữ nguyên tracker và trọng số theo đề.
- BoxMOT cũ cần setuptools 79.0.1 để có pkg_resources. Cài NumPy riêng vì metadata của BoxMOT ghim NumPy 1.23.1 không có wheel Python 3.12; không đổi thuật toán tracker.
- Gói dữ liệu thiếu eval_config.json: thêm cấu hình benchmark cục bộ LAB21/train cho video_1, giữ nguyên nội dung nhãn và chuẩn hóa tên sequence trong bản sao metadata. Không thêm nhãn cho các video còn lại.
- Script chấm dùng backend Agg và alias NumPy trong đúng tiến trình con. Unit test của lab được giới hạn ở thư mục tests để không chạy bộ test của TrackEval vốn cần dữ liệu khác.
- Video preview các chuỗi không có metadata dùng 20 FPS để xem; không suy luận FPS nguồn từ giá trị này. File MOT ghi frame theo thứ tự ảnh, nên việc này không thay đổi kết quả nộp.

Các lệnh tái lập nằm ở README_NOP_BAI.md. Trọng số, ảnh dữ liệu và video lớn không được đưa vào gói nộp.
