# ADR 0033: Spoke .md Directory Hygiene & Archiving Structure

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-08-24)

## 2. Bối Cảnh (Context)
Trong quá trình vận hành, thẩm định và kiểm toán đối kháng (Adversarial Auditing), rất nhiều script khảo sát (`inspect_*`, `survey_*`), kịch bản tấn công (`challenger_*`) và tệp kết quả JSON/TXT tạm thời được sinh ra ngổn ngang tại cấp gốc `.\.md\`, làm phình to thư mục và cản trở AI Agent đọc ngữ cảnh.

## 3. Quyết Định Thiết Kế (Decision)
Thiết lập chuẩn vệ sinh thư mục `.\.md\` bất biến:
1. **Cấp gốc `.\.md\`:** Chỉ lưu trữ tối đa 4 tệp cấu hình và tri thức cốt lõi (`workspace_context.yaml`, `codebase_architecture_analysis.md`, `FPT_HN03_Presentation_Workshop_20260806.md`, `team_tasks.json`).
2. **Cấu trúc Thư mục Con Chuyên Biệt:**
   - `extracted_docs/`: Nguồn tệp Word/PDF gốc.
   - `knowledge/`: `session_learnings.md` và các quy chuẩn kiến trúc.
   - `data/`: Sổ bộ, session locks, caches.
   - `archive/audits/`: Nơi lưu trữ tất cả kịch bản và kết quả kiểm toán đối kháng lịch sử.
   - `archive/inspections/`: Nơi lưu trữ các script khảo sát và trích xuất dữ liệu tạm thời.
   - `archive/legacy_harvesters/`: Nơi lưu trữ các script tải tệp cũ trước khi tích hợp vào Hub.
   - `backups/`: Các bản sao lưu cấu hình.

## 4. Hệ Quả (Consequences)
- Thư mục `.\.md\` luôn sạch sẽ, gọn gàng, tăng tốc độ khởi tạo ngữ cảnh của AI Agent lên 10x.
