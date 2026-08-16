# 🗺️ Wayfinding Map: Chiến lược Kiến trúc & Tra cứu Dữ liệu Tối ưu trên Thư viện Pháp luật (TVPL)

> **Trạng thái:** Approved & In-Progress  
> **Repository:** `d:\GitHubProjects\ccba-legal-knowledge`  
> **Gói công cụ:** `packages/ccba-legal-intel` & `scripts/legal_intelligence.py`  

---

## 🎯 1. Điểm đích (Destination)

Thiết lập một **Chiến lược Tra cứu & Cào Dữ liệu Tối ưu (Optimal TVPL Crawler & RAG Pipeline)** có khả năng:
1. Định danh chính xác và tải 100% toàn văn tài liệu VBPL, QCVN, TCVN theo mã định danh duy nhất `DOC_ID`.
2. Tự động trích xuất Đồ thị Quan hệ Pháp lý (11 nhóm quan hệ) từ Tab `?Tab=LuocDo`.
3. **Cơ chế Cào Tự động Phẳng (Flat Guiding Docs Crawl):** Tự động cào toàn bộ các Nghị định, Thông tư hướng dẫn thi hành đi kèm và lưu phẳng vào thư mục `guiding_docs/` của Luật gốc.
4. Vượt rào cản Cloudflare Turnstile & Giới hạn Tải file Docx bằng Session Auth kế thừa từ Hub (`vuvanchu119`).

---

## ✅ 2. Quyết định Kiến trúc Đã Chốt (Approved Decisions)

- [x] **[Chốt Chiến lược Option 3 - Hybrid Incremental Sync]**:
  - Dùng HTTP DocID Resolver tra cứu siêu tốc cho các tệp đã có.
  - Dùng Chrome CDP (`vuvanchu119`) cào toàn văn, tải `.docx` và trích xuất Lược đồ cho các bộ Luật gốc.
- [x] **[Chốt Cơ chế Cào Tự động Guiding Docs Phẳng]**:
  - Quét Tab `?Tab=LuocDo` $\rightarrow$ Tự động cào tất cả Nghị định/Thông tư hướng dẫn $\rightarrow$ Lưu phẳng tại `guiding_docs/<guiding_doc_slug>.md`.
- [x] **[Chốt Cơ chế Kế thừa Credentials từ Hub]**:
  - Tự động nạp `TVPL_USERNAME` & `TVPL_PASSWORD` từ `D:\GitHubProjects\ccba-agent-platform\.env`.

---

## 🚩 3. Các Ticket Thực thi (Execution Progress)

- [x] **[Ticket-TVPL-01] [Task AFK]** Kế thừa Credentials Hub & Tự động Vượt Cloudflare Turnstile.
- [x] **[Ticket-TVPL-02] [Task AFK]** Cào Toàn văn & Lược đồ Luật PCCC & CNCH 55/2024/QH15 (ID `621347`).
- [ ] **[Ticket-TVPL-03] [Task AFK]** Tự động cào danh mục Nghị định & Thông tư hướng dẫn Luật 55/2024/QH15 từ Tab Lược đồ và lưu phẳng vào `guiding_docs/`.
- [ ] **[Ticket-TVPL-04] [Task AFK]** Cào Toàn văn Luật Xây dựng 2025 số 135/2025/QH15.

---
*Cập nhật bởi CCBA Wayfinder Agent — 2026-07-26*
