# 📚 CCBA Legal Knowledge Spoke

Cơ sở dữ liệu Tri thức Pháp luật và Quy chuẩn Kỹ thuật Xây dựng chính quy của **CCBA Agent Platform**, được đóng gói theo tiêu chuẩn **OKF v2.4 Universal Agent-Centric (ADR 0034 - ADR 0037)**.

---

## 🏛️ Cấu Trúc Thư Mục Tri Thức Cấp 1 (`legal_docs/`):

* **`legal_docs/01_vbpl/`** — Văn bản quy phạm pháp luật (Luật Xây dựng 2025, Luật PCCC 2024, Luật Đấu thầu 2023, 7 Nghị định & 12 Thông tư hướng dẫn mới nhất 2026).
* **`legal_docs/02_qcvn/`** — Quy chuẩn Kỹ thuật Quốc gia (QCVN 01:2021, QCVN 02:2022, QCVN 03:2022, QCVN 04:2021 SĐ 1:2026, QCVN 06:2022 SĐ 1:2023).
* **`legal_docs/03_tcvn/`** — Tiêu chuẩn Quốc gia (TCVN 2737:2023 Tải trọng & tác động, TCVN 7336:2021 Chữa cháy tự động Sprinkler/Bọt).
* **`legal_docs/04_appendices/`** — Bảng so sánh đối chiếu đổi mới và ma trận VBHN độc lập.

---

## 📦 Cấu Trúc Gói Tri Thức OKF v2.4 (Universal Agent-Centric Bundle):

```text
legal_docs/<category>/<doc_slug>/
├── <doc_slug>.md          # Thân văn bản Markdown nguyên văn 100% (ADR 0037)
├── metadata.yaml          # RAG Metadata, quan hệ pháp lý & source_assets
├── clauses.json           # Cây điều khoản AST & severity rating
├── index.md               # Mục lục điều hướng 2D & anchor links
├── sources/               # Universal sources invariant: chứa bản gốc .docx và .pdf
├── tables/                # Bảng số liệu 2D (CSV, JSON, tables_catalog.json)
├── figures/               # Thẻ thị giác tính toán tham số hóa (cards/, figures_catalog.yaml)
├── annexes/               # Phụ lục kỹ thuật quy phạm (Technical Normative Annexes)
└── templates/             # Biểu mẫu hành chính nguyên tử (mau_*.md)
```

---

## 🚀 Lệnh Vận Hành & Kiểm Định CI:

* **Nạp tự động 1 lệnh toàn trình:**
  ```powershell
  python -m ccba_legal ingest "<tvpl_url>" --category <01_vbpl|02_qcvn|03_tcvn> --upload-drive
  ```
* **Chuyển đổi thủ công:**
  ```powershell
  python -m ccba_legal convert --docx-path "legal_docs/<cat>/<slug>/sources/<slug>.docx" --target-bundle-dir "legal_docs/<cat>/<slug>"
  ```
* **Kiểm định toàn diện 11 Cổng Master CI Gate:**
  ```powershell
  python scripts/validate_legal_spoke.py
  ```
