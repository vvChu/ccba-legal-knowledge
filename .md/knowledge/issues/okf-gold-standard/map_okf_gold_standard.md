# 🗺️ Wayfinding Map: Triển khai Quy trình Xử lý Dữ liệu OKF v0.2 Đạt Chuẩn Hoàn hảo (Gold Standard 100%)

> **Trạng thái:** Active  
> **Repository:** `d:\GitHubProjects\ccba-legal-knowledge`  
> **Chủ sở hữu:** CCBA Agent Platform  
> **Chuẩn áp dụng:** Open Knowledge Format v0.2 (OKF v0.2 Spec)  

---

## 🎯 1. Điểm đích (Destination)

Xây dựng và vận hành **Quy trình Xử lý & Đóng gói Dữ liệu OKF v0.2 Đạt Chuẩn Hoàn hảo (Gold Standard Pipeline)** cho CCBA Legal Knowledge Spoke, đảm bảo 100% dữ liệu VBPL, QCVN, TCVN được làm sạch sang Pure Markdown, gắn Inline Semantic Anchors (`<a id="..."></a>`), bóc tách bảng số liệu kỹ thuật CSV, tích hợp 5 Tín hiệu Tin cậy (Trust Signals) kèm bộ kiểm thử RAG `qa_benchmark.json` và đồng bộ tự động lên Cloud NotebookLM (`6dca7e4e-c407-4d1f-882a-e0d9459d1120`).

---

## 📝 2. Ghi chú (Notes)

- **Tuân thủ Hiến pháp Spoke:** Giữ nguyên cấu trúc thư mục nông tại Root Level 1 (`legal_docs/01_vbpl`, `02_qcvn`, `03_tcvn`, `04_appendices`) và tệp [legal_registry.yaml](file:///d:/GitHubProjects/ccba-legal-knowledge/legal_registry.yaml) tại Root.
- **Nguyên tắc KISS & Code Quality:** Mọi module Python viết mới phải có docstring Google style, type hints 100%, không dài quá 50 dòng/hàm.
- **Model Target:** Gemini 3.6 Flash / Pro & LiteLLM AI Gateway (`ccba-ai`).

---

## ✅ 3. Quyết định Đã chốt (Decisions so far)

- [x] **[Phân tách Thư mục Nông Root Level 1](file:///d:/GitHubProjects/ccba-legal-knowledge/legal_docs/)**: Triển khai 4 nhóm tri thức phẳng `01_vbpl`, `02_qcvn`, `03_tcvn`, `04_appendices` tại Root level 1.
- [x] **[Đồ thị Quan hệ Registry Trung tâm](file:///d:/GitHubProjects/ccba-legal-knowledge/legal_registry.yaml)**: Quản lý mối quan hệ *Parent-Child*, *Guiding*, *Superseded* bằng YAML metadata tại Root.
- [x] **[Kế thừa Credentials Hub & Chrome CDP 9222](file:///d:/GitHubProjects/ccba-legal-knowledge/scripts/legal_intelligence.py)**: Nạp `vuvanchu119` từ Hub `.env` tự động vượt Cloudflare Turnstile.
- [x] **[Khởi tạo Notebook Cloud Chuyên biệt](file:///d:/GitHubProjects/ccba-legal-knowledge/.md/workspace_context.yaml)**: Tạo Notebook `CCBA_Legal_Knowledge_Base_2026` (`6dca7e4e-c407-4d1f-882a-e0d9459d1120`).
- [x] **[Nạp & Đồng bộ Luật PCCC 2024 (2.406 dòng / 124 KB)](file:///d:/GitHubProjects/ccba-legal-knowledge/legal_docs/01_vbpl/luat_phong_chay_chua_chay_cuu_nan_cuu_ho_2024_so_55_2024_qh1/)**: Cào toàn văn chính xác và upload thành công lên NotebookLM Cloud.

---

## 🚩 4. Các Ticket ở Biên giới (Frontier Unblocked Tickets)

### 🎫 [Ticket-GS-01] [Task AFK] Pure Markdown Cleansing Engine
- **Mục tiêu:** Viết module làm sạch 100% thẻ HTML thô (`<table>`, `<tr>`, `<td>`, `<br>`) từ Thư viện Pháp luật sang **Markdown Tables** sạch.
- **Loại:** `Task [AFK]` | **Assignee:** Unassigned

### 🎫 [Ticket-GS-02] [Task AFK] Inline Semantic Anchoring Injector
- **Mục tiêu:** Tự động chèn thẻ neo HTML ẩn `<a id="dieu-XX-khoan-YY"></a>` trực tiếp vào trước tiêu đề từng Điều/Khoản trong file `.md` chính để hỗ trợ Citation RAG chính xác.
- **Loại:** `Task [AFK]` | **Assignee:** Unassigned

### 🎫 [Ticket-GS-03] [Task AFK] AST Structural Parsing & clauses.json Generator
- **Mục tiêu:** Tích hợp `ast_parser.py` tự động xuất chỉ mục cấu trúc Khoản/Điều (`clauses.json`) kèm số dòng offset.
- **Loại:** `Task [AFK]` | **Assignee:** Unassigned

### 🎫 [Ticket-GS-04] [Task AFK] Technical Table CSV & Formula JSON Extractor
- **Mục tiêu:** Bóc tách các bảng giới hạn chịu lửa & khoảng cách an toàn PCCC trong QCVN 06/QCVN 04 thành các file CSV phẳng trong thư mục `tables/`.
- **Loại:** `Task [AFK]` | **Assignee:** Unassigned

### 🎫 [Ticket-GS-05] [Task AFK] Ground Truth QA Benchmark Generator
- **Mục tiêu:** Tự động khởi tạo tệp `qa_benchmark.json` chứa 5-10 cặp câu hỏi-đáp Ground Truth cho mỗi bộ Luật/QCVN để phục vụ kiểm thử tự động độ chính xác RAG.
- **Loại:** `Task [AFK]` | **Assignee:** Unassigned

---

## 🌫️ 5. Chưa xác định rõ (Not yet specified - In the Fog)

- **Tự động hóa Đánh giá RAG Accuracy (Evaluation Harness):** Xây dựng runner đo lường điểm precision/recall của NotebookLM RAG theo bộ `qa_benchmark.json`.

---

## ⛔ 6. Ngoài phạm vi (Out of scope)

- Giữ nguyên các thẻ HTML thô trong tệp Markdown tri thức.
- Lưu trữ file PDF/Word quét ảnh chưa được OCR.

---
*Cập nhật bởi CCBA Wayfinder Agent — 2026-07-26*
