---
request_id: req-spoke-legal-verification-review-001
verdict: APPROVE_WITH_CONDITIONS
conditions:
- id: COND-01
  description: 'Khai báo bổ sung thuộc tính chính tắc `scope: spoke` vào metadata
    frontmatter của tệp `.agents/skills/ccba-verify-legal-knowledge/SKILL.md` theo
    quy chuẩn phân phối tại ADR-0066.'
  blocking: false
  source_profiles: []
- id: COND-02
  description: 'Chuẩn hóa công thức hiển thị chỉ số GPI trong tài liệu thuyết minh
    đồng bộ theo công thức trọng số chính thức tại ADR-0057: GPI = 2.5S + 2.0K + 2.0A
    - 1.5P = 24.0.'
  blocking: false
  source_profiles: []
- id: COND-03
  description: Bổ sung cấu hình thời gian chờ tối đa (timeout) cho từng tiến trình
    kiểm định con trong harness để triệt tiêu nguy cơ treo vô thời hạn khi đường ống
    I/O gặp tắc nghẽn.
  blocking: false
  source_profiles: []
risk_score: 2
effort: S
summary: Kiến trúc 5 khối của harness ccba-verify-legal-knowledge đáp ứng xuất sắc
  các tiêu chuẩn vận hành cô lập Pstack Upstream, bảo toàn nguyên vẹn ngân sách 15
  kịch bản (ADR-0044) và vượt qua 15 Cổng Master CI. Chấp thuận nghiệm thu kèm các
  điều kiện hoàn thiện nhỏ về thuộc tính scope, công thức GPI và rào chắn timeout.
telemetry:
  session_id: ses-grok-review-20261006-001
  primary_model: grok-4.7
  input_tokens: 18450
  output_tokens: 2860
  reasoning_tokens: 1420
  cached_read_tokens: 7200
  total_tokens: 21310
  model_calls: 1
  turn_count: 1
  cost_usd: 0.042
  cost_mode: estimated
  duration_seconds: 14.8
---

---

## 1. Kết Quả Thẩm Định Tổng Quan

Harness kiểm định chuyên biệt `ccba-verify-legal-knowledge` đạt chất lượng kỹ thuật cao, đáp ứng đầy đủ các yêu cầu cốt lõi về tính toàn vẹn hệ thống và kỷ luật kiểm định phân tầng của nền tảng CCBA:

- **Bảo tồn ngân sách kịch bản (ADR-0044):** Thư mục `scripts/` duy trì chính xác 15/15 tệp theo ratchet budget. Toàn bộ mã nguồn thực thi, điều phối và logic phụ trợ của harness được đóng gói độc lập trong `.agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py`.
- **Hiệu năng rào chắn sức khỏe (Deterministic Health Barrier):** Quá trình phân tích cú pháp 96 văn bản quy chuẩn từ `legal_registry.yaml` và kiểm tra tính hợp lệ của các entrypoint hoàn thành trong $0.087\text{ s}$, vận hành hoàn toàn bằng giải thuật xác định, không sử dụng độ trễ tĩnh.
- **Bảo vệ môi trường Git:** Cấu hình ngoại lệ `.gitignore` bảo vệ mã nguồn kỹ năng kiểm định cục bộ của Spoke, ngăn ngừa nguy cơ bị đồng bộ ghi đè từ Hub trong các chu kỳ `/ccba-update-spoke`.

Phán quyết đưa ra là **`APPROVE_WITH_CONDITIONS`** với mức rủi ro cấp 2 (Thấp). Dưới đây là phân tích chi tiết cho 4 trọng tâm phản biện.

---

## 2. Phân Tích Đối Kháng 4 Trọng Tâm Yêu Cầu

### 2.1. Kiến Trúc 5 Khối & Quản Lý Vòng Đời Tiến Trình (Process Lifecycle)

Cơ chế phân tách 4 chế độ vận hành (`smoke`, `full`, `cleanliness`, `bundle`) phân định ranh giới rõ ràng giữa kiểm tra vệ sinh nhanh trước commit và nghiệm thu toàn diện trước khi phát hành. 

Về cơ chế Process Group trong Khối 2 và Khối 5:
- **Ưu điểm hiện tại:** Việc áp dụng `os.setsid` trên POSIX và `subprocess.CREATE_NEW_PROCESS_GROUP` trên Windows kết hợp cùng khối dọn dẹp `finally:` giúp cô lập tiến trình trực tiếp và giải phóng tài nguyên khi tiến trình kết thúc bình thường.
- **Rủi ro tiến trình phân nhánh sâu (Grandchild Processes):** 
  - Trên POSIX: Lệnh `os.killpg(pgid, signal.SIGTERM)` chỉ tác động tới các tiến trình nằm trong cùng nhóm process group. Trường hợp một công cụ bên thứ ba hoặc kịch bản con chủ động khởi tạo session mới bằng lời gọi hệ thống `setsid()` hoặc `setpgid()`, tiến trình con đó sẽ tách khỏi PGID ban đầu và thoát khỏi tầm kiểm soát của harness.
  - Trên Windows: Cờ `CREATE_NEW_PROCESS_GROUP` điều chỉnh cơ chế nhận tín hiệu ngắt bàn phím. Lệnh `taskkill /F /T /PID <pid>` phụ thuộc vào cây quan hệ cha-con đang hoạt động. Khi tiến trình con trực tiếp thoát đột ngột trước khi các tiến trình cháu kết thúc, `taskkill` theo PID cha sẽ thất bại vì PID không còn tồn tại, để lại các tiến trình cháu mồ côi. Giải pháp tối ưu trên Windows là quản trị tiến trình qua Windows Job Object với cờ `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`.
- **Rủi ro tắc nghẽn I/O (Unbounded I/O Deadlock):** Harness hiện tại sử dụng vòng lặp đồng bộ `for line in proc.stdout:` và gọi `proc.wait()` mà không đặt ngưỡng giới hạn thời gian (timeout). Nếu kịch bản kiểm tra gặp lỗi treo đọc dữ liệu hoặc chờ nhập liệu, toàn bộ quy trình CI sẽ bị đóng băng.

### 2.2. Tuân Thủ ADR-0066 & Cơ Chế Phân Phối Kỹ Năng

Việc chuyển đổi `bundle: _governance` sang `bundle: _core` đã giải quyết được yêu cầu hiển thị gợi ý lệnh gõ nhanh (Slash Command Autocomplete) trên giao diện phát triển. Tuy nhiên, cấu hình hiện tại có điểm cần hoàn thiện:

- **Thiếu thuộc tính `scope` chính tắc:** Theo quy định tại Mục 2 của ADR-0066, mọi tệp `SKILL.md` bắt buộc phải khai báo trường `scope: hub | spoke | universal`. Tệp `SKILL.md` của `ccba-verify-legal-knowledge` hiện đang khuyết trường này.
- **Ranh giới danh mục phân phối:** Thuộc tính `bundle: _core` vốn quy định cho các công cụ điều phối vòng đời dùng chung toàn nền tảng được sao chép từ Hub xuống mọi Spoke. Đối với kỹ năng kiểm định riêng biệt của Spoke `ccba-legal-knowledge`, việc khai báo tường minh `scope: spoke` là bắt buộc để hệ thống linter xác định đây là kỹ năng nội bộ của Spoke, ngăn chặn sự nhầm lẫn với các kỹ năng dùng chung từ Hub.

### 2.3. Hiệu Chuẩn Chỉ Số Độc Lập Tổng Quát (GPI - ADR-0057)

Bản tóm tắt yêu cầu ghi nhận công thức tính điểm:
$$\mathbf{GPI} = S(4.5) + K(4.0) + A(3.5) + P(1.5) = 13.5 \ge 12.0$$

Đây là cách tính cộng gộp đơn giản. Theo định nghĩa chuẩn mực tại ADR-0057 (Mục 2.2) và ADR-0066 (Mục 3.2), công thức tính toán có trọng số chính thức là:
$$\mathbf{GPI} = (S \times 2.5) + (K \times 2.0) + (A \times 2.0) - (P \times 1.5)$$

Áp dụng các tham số đã khai báo trong frontmatter ($S=4.5, K=4.0, A=3.5, P=1.5$):
$$\mathbf{GPI} = (4.5 \times 2.5) + (4.0 \times 2.0) + (3.5 \times 2.0) - (1.5 \times 1.5)$$
$$\mathbf{GPI} = 11.25 + 8.0 + 7.0 - 2.25 = 24.0$$

Giá trị thực tế đạt $24.0$, vượt xa ngưỡng chuẩn $12.0$ dành cho Standalone Kernel Skill (Tier 2B). Antigravity cần cập nhật lại cách trình bày công thức trong các tài liệu bàn giao để phản ánh chính xác chuẩn toán học của nền tảng.

### 2.4. Rào Chắn Nghiệm Thu CI & Phòng Chống Sửa Đổi Bài Kiểm Tra (Anti-Tampering)

Nguyên tắc COND-01 (Pre-Remediation Provenance Check) trong `features/INDEX.md` định hướng rất tốt về mặt quy trình: phân định giữa Lệch Hợp Đồng (Contract Drift) và Lỗi Hồi Quy (Regression), đồng thời cấm sửa mã kiểm tra khi gặp lỗi dữ liệu quy phạm.

Tuy nhiên, rào chắn này hiện là quy ước vận hành, chưa mang tính cưỡng chế cơ học:
- Một tác nhân hoặc nhà phát triển vẫn có thể chỉnh sửa nới lỏng các điều kiện kiểm tra trong `scripts/validate_legal_spoke.py` (chẳng hạn giảm tỷ lệ verbatim parity từ 98% xuống 90%) để vượt qua CI.
- Để biến rào chắn này thành rào chắn bất biến:
  - Áp dụng kiểm tra mã băm toàn vẹn (SHA-256 Checksum Verification) cho các kịch bản kiểm tra cốt lõi trong quy trình CI cấp Hub.
  - Thiết lập Git Diff Guardian: Tự động từ chối các đề xuất commit đồng thời thay đổi cả nội dung văn bản trong `legal_docs/` lẫn logic khẳng định trong `scripts/` hoặc `harness/`.
  - Triển khai cơ chế Ratchet Monotonic: Các chỉ số chất lượng văn bản chỉ được phép giữ nguyên hoặc tăng lên, không cho phép suy giảm qua các phiên bản commit.

---

## 3. Khuyến Nghị Hoàn Thiện Trong Các Chu Kỳ Tiếp Theo

1. **Bổ sung thời gian chờ tối đa (Per-Step Timeout):** Cung cấp tham số `timeout` (mặc định 300 giây) trong hàm `_spawn_process_group` và phương thức gọi thực thi để tự động thu hồi tiến trình nếu xảy ra tắc nghẽn I/O.
2. **Khai mở chế độ quét theo Git Staged (`--staged`):** Tích hợp khả năng tự động phân tích `git diff --name-only --cached` để nhận diện chính xác các bundle văn bản đang chỉnh sửa và tự động kích hoạt `--mode bundle` tương ứng, tối ưu hóa tốc độ kiểm thử trước khi commit.
3. **Song song hóa kiểm định cấp Bundle:** Áp dụng `concurrent.futures.ProcessPoolExecutor` khi quét 96 tài liệu trong chế độ `full`, giúp tận dụng tối đa năng lực phần cứng đa nhân và rút ngắn thời gian nghiệm thu tổng thể.
4. **Chuẩn hóa Telemetry đẩy về Hub:** Bổ sung cấu trúc dữ liệu telemetry vào tệp `.md/reports/evidence_verify_legal_knowledge.json` đồng bộ với định dạng tại ADR-0064, hỗ trợ Hub tổng hợp trạng thái sức khỏe của Spoke một cách tự động.

---

## 4. Danh Mục Điều Kiện Nghiệm Thu (Acceptance Conditions)

| Mã Điều Kiện | Nội Dung Yêu Cầu | Mức Độ | Trạng Thái Đề Xuất |
| :--- | :--- | :---: | :---: |
| `COND-01` | Khai báo bổ sung `scope: spoke` vào metadata frontmatter của `.agents/skills/ccba-verify-legal-knowledge/SKILL.md`. | Khuyến nghị | Thực hiện ngay trong đợt tinh chỉnh này |
| `COND-02` | Chuẩn hóa công thức tính GPI thành $\mathbf{GPI} = 2.5S + 2.0K + 2.0A - 1.5P = 24.0$ trong tài liệu thuyết minh. | Khuyến nghị | Cập nhật tài liệu bàn giao |
| `COND-03` | Cấu hình giới hạn thời gian chạy (timeout) cho các bước kiểm định con trong `verify_legal_harness.py`. | Khuyến nghị | Tích hợp trong chu kỳ bảo trì tiếp theo |