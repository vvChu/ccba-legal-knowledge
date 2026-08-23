# CCBA Legal Knowledge Spoke — Workspace Constitution

> [!IMPORTANT]
> **Đây là Repository Spoke Tri thức Pháp lý chính quy của CCBA Agent Platform.**
> Tất cả dữ liệu tri thức được đóng gói theo tiêu chuẩn **OKF v2.2 Native-First (Pure Normative Body & Atomic Templates - ADR 0021)**.

---

## 🏛️ Quy tắc Vận hành Spoke Bất Biến (Core Invariants):
1. **Mô hình Đường dẫn Nông (Shallow Path):** Thư mục `legal_docs/` nằm tại Cấp 1 của Spoke. `legal_registry.yaml` nằm tại Root.
2. **Reuse-First Gate:** Mọi thao tác cập nhật dữ liệu phải kế thừa trực tiếp từ package Hub (`packages/ccba-legal-intel`).
3. **Độc lập Mã nguồn:** Không chứa code ứng dụng frontend/backend, tập trung 100% cho OKF Markdown Bundles, RAG Metadata, Atomic Templates và Pipeline kiểm định.
4. **PDF là Mỏ Neo Pháp Lý Tối Thượng (ADR 0016):** 100% văn bản nạp vào phải có metadata theo dõi PDF Công báo gốc và mã băm SHA-256.
5. **Thân Văn Bản Thuần Khiết & Biểu Mẫu Nguyên Tử (ADR 0021):** Thân văn bản chính loại bỏ 100% rác layout hành chính; Phụ lục biểu mẫu được tách thành Atomic Form Templates (`templates/phu_luc_XX/mau_YY_...md`); Bảng số liệu tra cứu đưa vào `tables/`.

---

## 🚀 Quy trình 4 Bước Chuẩn Hóa Văn Bản Mới (Universal OKF v2.2 Pipeline):

Bất kỳ khi nào tiếp nhận một Luật, Nghị định, Thông tư, QCVN hoặc TCVN mới (hoặc khi phát hiện file nguồn DOCX bị thiếu/lỗi), Agent **bắt buộc** thực hiện tuần tự 4 bước:

### 0. Thu thập & Xác thực Nguồn gốc (Acquisition Gate — Bắt buộc qua ccba-legal-intel):
* Tuyệt đối cấm cào HTML web tự do bằng `read_url_content` hay `requests`.
* Kích hoạt Deep Seam `TVPLCrawler` từ `ccba-legal-intel` (hoặc Cổng Dữ liệu Mở Quốc gia `vbpl.vn`, `quochoi.vn`):
```powershell
python scripts/fetch_tvpl_doc.py "<url_or_doc_number>"
```

### 1. Nạp & Chuyển đổi sang OKF v2.2 Bundle (ADR 0021):
```powershell
python scripts/docx_converter.py ".md/extracted_docs/ten_van_ban/ten_file.docx" "legal_docs/01_vbpl/ten_van_ban"
```

### 2. Hợp nhất Văn bản Sửa đổi (nếu có văn bản sửa đổi):
```powershell
python -m scripts.consolidator `
  --manifest legal_docs/01_vbpl/ten_van_ban/patch_manifest.yaml `
  --base legal_docs/01_vbpl/ten_van_ban/ten_van_ban.md `
  --output legal_docs/01_vbpl/ten_van_ban/
```

### 3. Kiểm định Bắt buộc qua 5 Cổng CI Gates (Zero-Tolerance):
```powershell
python scripts/validate_legal_spoke.py
python scripts/test_converter_regression.py
python scripts/audit_visual_parity.py
python scripts/verify_cross_links.py
python scripts/verify_all_docs_against_pdf.py
```
*Tiêu chuẩn nghiệm thu:* `0 Errors, 0 Warnings, 100% Valid Links, 100% PDF SHA-256 Match, 100% Visual Parity`.
