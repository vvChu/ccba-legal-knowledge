# CCBA Legal Knowledge Spoke — Workspace Constitution

> [!IMPORTANT]
> **Đây là Repository Spoke Tri thức Pháp lý chính quy của CCBA Agent Platform.**
> Tất cả dữ liệu tri thức được đóng gói theo tiêu chuẩn **OKF v2.0 Native-First**.

---

## 🏛️ Quy tắc Vận hành Spoke Bất Biến (Core Invariants):
1. **Mô hình Đường dẫn Nông (Shallow Path):** Thư mục `legal_docs/` nằm tại Cấp 1 của Spoke. `legal_registry.yaml` nằm tại Root.
2. **Reuse-First Gate:** Mọi thao tác cập nhật dữ liệu phải kế thừa trực tiếp từ package Hub (`packages/ccba-legal-intel`).
3. **Độc lập Mã nguồn:** Không chứa code ứng dụng frontend/backend, tập trung 100% cho OKF Markdown Bundles, RAG Metadata và Pipeline kiểm định.
4. **PDF là Mỏ Neo Pháp Lý Tối Thượng (ADR 0016):** 100% văn bản nạp vào phải có metadata theo dõi PDF Công báo gốc và mã băm SHA-256.

---

## 🚀 Quy trình 3 Bước Xử lý Văn bản Mới (OKF v2.0 Pipeline):

Bất kỳ khi nào tiếp nhận một Luật, Nghị định, Thông tư, QCVN hoặc TCVN mới, Agent **bắt buộc** thực hiện tuần tự 3 bước:

### 1. Nạp & Chuyển đổi sang OKF Bundle:
```powershell
python scripts/docx_converter.py --input "duong/dan/file_goc.docx" --output-dir "legal_docs/02_qcvn/ten_van_ban"
```

### 2. Hợp nhất Văn bản Sửa đổi (nếu có văn bản sửa đổi):
```powershell
python -m scripts.consolidator `
  --manifest legal_docs/02_qcvn/ten_van_ban/patch_manifest.yaml `
  --base legal_docs/02_qcvn/ten_van_ban/ten_van_ban.md `
  --output legal_docs/02_qcvn/ten_van_ban/
```

### 3. Kiểm định Bắt buộc qua 3 Cổng CI Gates (Zero-Tolerance):
```powershell
python scripts/validate_legal_spoke.py
python scripts/verify_knowledge_integrity.py
python scripts/verify_cross_links.py
```
*Tiêu chuẩn nghiệm thu:* `0 Errors, 0 Warnings, 100% Parity, 100% Valid Links`.
