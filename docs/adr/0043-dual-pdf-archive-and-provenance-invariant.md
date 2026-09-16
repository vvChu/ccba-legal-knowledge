# ADR 0043: Lưu Trữ Song Song & Bảo Tồn Nguồn Gốc PDF (Dual-PDF Archive & Provenance Invariant)

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-09-14)  
*Hội tụ thông qua Chu trình Học tập Kiến trúc `/ccba-grilling` & `/learn` (Mục 46 session_learnings.md).*

---

## 2. Bối Cảnh (Context)
Trong quá trình nạp các văn bản quy chuẩn, tiêu chuẩn kỹ thuật xây dựng từ Thư Viện Pháp Luật và Cổng thông tin điện tử:
1. **Hiện tượng TCVN3 / Scan Mờ Thoái Hóa:** Nhiều tệp PDF Công báo ban hành trước năm 2010 là bản scan chất lượng thấp, chữ mờ nhòe, hoặc tệp PDF tạo bằng bộ phông chữ TCVN3 cũ bị lỗi mã hóa font Unicode nghiêm trọng. Nếu dùng công cụ OCR hoặc AI Vision đọc trực tiếp các tệp này, tỷ lệ lỗi chính tả và sai số kỹ thuật rất cao.
2. **Mâu Thuẫn Giữa Tính Pháp Lý và Khả Năng Khai Thác AI:** Tệp PDF gốc tải từ nguồn chính thống là mỏ neo pháp lý bất khả xâm phạm (Legal Anchor of Trust). Tuy nhiên, file DOCX chính thức đi kèm lại có nội dung văn bản sắc nét và chính xác hơn nhiều. Nếu kết xuất DOCX thành Vector PDF (zero-OCR) qua Word COM, ta thu được tệp PDF chất lượng cao tuyệt đối phục vụ Google NotebookLM và RAG.
3. **Nguy Cơ Mất Dấu Nguồn Gốc (Provenance Drift):** Nếu chỉ lưu bản Vector PDF kết xuất từ Word mà ghi đè lên file PDF gốc, hệ thống sẽ làm mất mã hash SHA-256 đối soát nguồn gốc từ Thư Viện Pháp Luật/Công báo, vi phạm Cổng 5 và ADR 0035.

---

## 3. Quyết Định Thiết Kế (Decision)

Hệ thống thiết lập **Bất biến Lưu trữ Song song & Bảo tồn Nguồn gốc PDF (Dual-PDF Archive & Provenance Invariant - ADR 0043)**:

1. **Lưu Trữ Song Song 2 Tệp PDF:**
   - Đối với các văn bản có tệp PDF tải về là bản scan mờ hoặc lỗi phông chữ: Lưu trữ bản scan gốc dưới tên `sources/<doc_slug>_raw_scan.pdf`.
   - Kết xuất bản Vector PDF độ nét tuyệt đối (zero-OCR) từ tệp DOCX chính quy qua Word COM, lưu làm `sources/<doc_slug>.pdf`.
2. **Ghi Nhận Metadata Nguồn Gốc (Provenance Stamping):**
   - Khai báo trường `pdf_origin: docx_vector_rendered` và `raw_scan_pdf: sources/<doc_slug>_raw_scan.pdf` trong `metadata.yaml`.
   - Ghi nhận đầy đủ mã hash SHA-256 của cả 2 tệp trong `source_assets`.
3. **Đồng Bộ Cloud Vault (ADR 0035):**
   - Cả hai tệp `.pdf` đều được bảo vệ bởi `.gitignore` và tự động đồng bộ lên Google Drive Vault `CCBA_Legal_Vault`.
4. **Kiểm Định Tự Động (Sub-Gate 5.2):**
   - Bộ kiểm định `validate_legal_spoke.py` tự động quét phát hiện các bundle có cờ `docx_vector_rendered`, xác thực sự hiện diện của cả 2 tệp trên disk và đối soát SHA-256.

---

## 4. Hệ Quả & Tác Động (Consequences)

### Tích Cực
- Bảo toàn trọn vẹn 100% tính nguyên gốc pháp lý của tài liệu Công báo từ nguồn thu thập.
- Cung cấp tệp PDF Vector độ nét tối đa (100% chữ máy tính) cho hệ sinh thái RAG, NotebookLM và AI Gateway mà không tốn chi phí OCR.
- Vượt qua toàn diện Gate 5, Gate 15 của Master CI.

### Hạn Chế & Chi Phí Bảo Trì
- Tăng dung lượng lưu trữ trên Google Drive Vault cho các bundle áp dụng cơ chế song song.

---
*Biên soạn bởi CCBA Agent Architecture Council.*  
*Căn cứ thực thi: Invariant 15 `AGENTS.md`, Sub-Gate 5.2 `scripts/validate_legal_spoke.py`.*
