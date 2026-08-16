# 🗺️ Wayfinder Map: Nâng cấp Skill Table Reconstructor & Markdown Document Processing

> **Mã bản đồ:** `table_reconstructor_upgrade`  
> **Trạng thái:** ✅ Đã hoàn thành 100%  
> **Thời gian cập nhật:** 2026-07-26  

---

## 🎯 1. Điểm đích (Destination)

Đóng gói và nâng cấp Master Skill **`markdown-document-processing`** (đặc biệt là Sub-skill **`table-reconstructor`**) từ Spoke lên Hub (`ccba-agent-platform`). Đảm bảo toàn bộ hệ thống CCBA AI Agent có khả năng:
1. Tự động giải gộp ô (Rowspan/Colspan Unmerging) đối với các bảng phức tạp từ Word (.docx) và HTML.
2. Ngăn ngừa triệt để lỗi lặp tiêu đề `### ### Bảng` gây đứt gãy regex.
3. Tự động xuất đồng thời **3 định dạng (Triple Export Pattern)**: Markdown Pipe Table + JSON Object (`tables/json/`) + CSV Flat File (`tables/csv/`).

---

## 📝 2. Ghi chú (Notes)

- **Bài học thực tế:** Đã kiểm chứng thành công 100% trên bảng 5 cột QCVN 06:2022/BXD tại [legal_docs/02_qcvn/qcvn_06_2022_bxd/](file:///d:/GitHubProjects/ccba-legal-knowledge/legal_docs/02_qcvn/qcvn_06_2022_bxd/).
- **Nguyên tắc:** Plan, Implement & Handoff — Đã đóng gói thành kỹ năng chuẩn hóa tái sử dụng chung cho toàn Platform.

---

## ✅ 3. Quyết định Đã Chốt (Decisions so far)

* [x] **[Giải gộp Ô Bảng 2D Matrix (Rowspan/Colspan Unmerging)](file:///d:/GitHubProjects/ccba-legal-knowledge/scripts/docx_table_extractor.py)**: Xây dựng thành công `docx_table_extractor.py` giải gộp ô dọc và chuẩn hóa 5 cột Bảng 1 trùng khớp 100% layout gốc.
* [x] **[Rào chắn Tiêu đề Trùng lặp (Heading Guardrails)](file:///d:/GitHubProjects/ccba-legal-knowledge/scripts/docx_converter.py)**: Xóa bỏ lỗi tạo nhiều dấu `### ###` trong `docx_converter.py`.
* [x] **[Đóng gói Scripts vào Hub Skill markdown-document-processing](file:///D:/GitHubProjects/ccba-agent-platform/.agents/skills/markdown-processing/scripts/)**: Đã tích hợp `docx_table_extractor.py`, `qcvn_md_table_formatter.py` và `docx_converter.py` vào Hub.
* [x] **[Cập nhật SKILL.md & Quy trình Bảng Ô Gộp tại Hub](file:///D:/GitHubProjects/ccba-agent-platform/.agents/skills/markdown-processing/SKILL.md)**: Đã cập nhật tài liệu `SKILL.md` với hướng dẫn Rowspan Unmerging Checklist và Triple Export.
* [x] **[Thực hiện Proposal Đóng góp Ngược lên Hub (Propose to Hub)](file:///D:/GitHubProjects/ccba-agent-platform/)**: Đã hoàn tất đóng góp nâng cấp tính năng `table-reconstructor` từ Spoke lên Hub.

---

## 🌫️ 4. Chưa xác định rõ (Not yet specified)

- Xây dựng bộ test tự động riêng cho Sub-skill `table-reconstructor` trên Hub (`tests/test_table_reconstructor.py`).

---

## 🚫 5. Ngoài phạm vi (Out of scope)

- Không thay đổi cấu trúc AST `clauses.json` và `qa_benchmark.json` hiện tại vì đã chạy ổn định.
