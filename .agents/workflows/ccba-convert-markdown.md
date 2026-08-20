---
description: Chuyển đổi tài liệu sang Markdown chuẩn OKF v2.2 (Pure Normative Body, Legal Knowledge Graph, Atomic Form Templates, 3-Tier Table Classifier và kiểm định CI)
applies_to:
  - "Phần mềm"
  - "Thẩm tra thiết kế"
  - "Thiết kế"
  - "Kiểm định"
bundle: "_core"
disable-model-invocation: true
---
# Workflow: Convert to Markdown (/ccba-convert-markdown)

Khi người dùng kích hoạt lệnh này, Agent hãy phân loại loại hình tài liệu đầu vào để thực thi đúng quy trình:

## 1. Đối với Văn bản Pháp luật & Quy chuẩn Kỹ thuật (QCVN / TCVN / Luật / Nghị định / Thông tư):
Tuân thủ nghiêm ngặt **Quy trình 3 Bước OKF v2.2 (ADR 0021)**:

### Bước 1: Nạp & Chuyển đổi sang OKF v2.2 Bundle (Universal Converter):
```powershell
python scripts/docx_converter.py "<path_to_docx>" "legal_docs/<category>/<doc_slug>"
```
*Đặc tính xử lý tự động của Engine:*
- **VBPL (Luật / Nghị định / Thông tư):**
  * Tự động trích xuất **Thân Quy Phạm Thuần Khiết (Pure Normative Body)** từ Chương I đến Điều cuối cùng vào file `.md` chính.
  * Tự động chuẩn hóa số thứ tự khoản `**1.**`, `**2.**` (chống lỗi thụt lề so le CommonMark).
  * Tự động cấu trúc hóa Đồ thị Căn cứ Pháp lý (`legal_basis`) vào `metadata.yaml`.
  * Tự động bóc tách **Biểu Mẫu Nguyên Tử (Atomic Form Templates)** vào thư mục `templates/phu_luc_XX/mau_YY_...md`.
  * Tự động lọc khung layout hành chính, trích xuất Bảng số liệu ma trận kỹ thuật vào `tables/csv/` và `tables/json/`.
- **QCVN / TCVN (Quy chuẩn kỹ thuật):**
  * Tự động trích xuất bảng biểu 2D GFM Pipe Tables, ma trận chú thích ràng buộc chân bảng.

### Bước 1.5: Tiêu Chuẩn Hóa Cấu Trúc Khối Chú Thích & QA Benchmark (OKF v2.2 Processor):
```powershell
python scripts/gold_standard_processor.py "legal_docs/<category>/<doc_slug>"
```
*Đặc tính xử lý:*
* Tự động chuẩn hóa **Binary Note Standard** (Khử trùng lặp header `_CHÚ THÍCH:_`).
* Tự động giải phóng chú thích kẹp chân bảng thành `_GHI CHÚ CHỈ SỐ PHỤ:_` và chuẩn hóa thẻ `<sup>X)</sup>`.
* Tự động đồng bộ danh sách gạch đầu dòng mã (`LT`, `BC`, `SK`, `ĐT`, `K0..3`, `R-E-I-W`) và thụt lề ý con `a), b), c)` thuộc chú thích.
* Tự động sinh `clauses.json` (AST) và `qa_benchmark.json` (phân quyền `CQXD` vs `CONG_AN`).

### Bước 2: Hợp nhất Sửa đổi (nếu có văn bản sửa đổi):
```powershell
python -m scripts.consolidator `
  --manifest legal_docs/<category>/<doc_slug>/patch_manifest.yaml `
  --base legal_docs/<category>/<doc_slug>/<doc_slug>.md `
  --output legal_docs/<category>/<doc_slug>/
```

### Bước 3: Kiểm định Bắt buộc qua 4 Cổng CI Gates (Zero-Tolerance):
```powershell
python scripts/validate_legal_spoke.py
python scripts/verify_knowledge_integrity.py
python scripts/verify_cross_links.py
python scripts/audit_visual_parity.py
```
*Tiêu chuẩn nghiệm thu:* `0 Errors, 0 Warnings, 100% Parity, 100% Valid Links, 100% Visual Parity`.

---

## 2. Đối với Tài liệu Hành chính / Kỹ thuật thông thường:
Nạp và thực thi kỹ năng `markdown-document-processing` tại [SKILL.md](../skills/markdown-processing/SKILL.md) thông qua Deep Seam **`ConversionPipeline`** ([`packages/mdconverter`](../../packages/mdconverter)).
