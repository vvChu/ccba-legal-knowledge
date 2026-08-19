---
description: Chuyển đổi tài liệu sang Markdown chuẩn OKF v2.0 (tự động xử lý bảng biểu, thẻ neo, hợp nhất sửa đổi và kiểm định CI)
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

## 1. Đối với Văn bản Pháp luật & Quy chuẩn Kỹ thuật (QCVN / TCVN / Luật / Nghị định):
Tuân thủ nghiêm ngặt **Quy trình 3 Bước OKF v2.0**:

1. **Chuyển đổi sang OKF Bundle:**
   ```powershell
   python scripts/docx_converter.py --input "<path_to_docx>" --output-dir "legal_docs/<category>/<doc_slug>"
   ```
2. **Hợp nhất Sửa đổi (nếu có văn bản sửa đổi):**
   ```powershell
   python -m scripts.consolidator `
     --manifest legal_docs/<category>/<doc_slug>/patch_manifest.yaml `
     --base legal_docs/<category>/<doc_slug>/<doc_slug>.md `
     --output legal_docs/<category>/<doc_slug>/
   ```
3. **Chạy 3 Cổng Kiểm định Chất lượng Bắt buộc:**
   ```powershell
   python scripts/validate_legal_spoke.py
   python scripts/verify_knowledge_integrity.py
   python scripts/verify_cross_links.py
   ```

---

## 2. Đối với Tài liệu Hành chính / Kỹ thuật thông thường:
Nạp và thực thi kỹ năng `markdown-document-processing` tại [SKILL.md](../skills/markdown-processing/SKILL.md) thông qua Deep Seam **`ConversionPipeline`** ([`packages/mdconverter`](../../packages/mdconverter)).
