# 🗺️ Wayfinding Map: Quy trình Xử lý Dữ liệu & Đóng gói OKF v0.2 (OKF Packaging Pipeline)

> **Trạng thái:** Active  
> **Repository:** `d:\GitHubProjects\ccba-legal-knowledge`  
> **Mục tiêu:** Định hình quy trình 4 bước khép kín từ cào/nạp dữ liệu thô $\rightarrow$ Phân rã AST $\rightarrow$ Đóng gói OKF Bundle $\rightarrow$ Đẩy lên Cloud NotebookLM.  

---

## 🎯 1. Điểm đích (Destination)

Xây dựng một **Quy trình Xử lý & Đóng gói OKF v0.2 Chuẩn hóa (OKF Data Processing & Packaging Pipeline)** cho phép:
1. Chuẩn hóa mọi định dạng đầu vào (HTML TVPL, Word `.docx`, PDF) thành Markdown sạch.
2. Phân rã cấu trúc cây VBPL/QCVN (`Chương -> Điều -> Khoản -> Điểm`) thành chỉ mục AST (`clauses.json`).
3. Trích xuất riêng **Bảng số liệu chỉ tiêu kỹ thuật (CSV/JSON)** và **Công thức tính toán (Formulas)** cho QCVN/TCVN.
4. Gắn đầy đủ **5 Tín hiệu Tin cậy (Trust Signals)** vào YAML Frontmatter và tự động cập nhật [legal_registry.yaml](file:///d:/GitHubProjects/ccba-legal-knowledge/legal_registry.yaml) tại Root Level 1.

---

## 📐 2. Quy trình 4 Giai đoạn Xử lý & Đóng gói Dữ liệu

```mermaid
flowchart TD
    subgraph Stage1 ["Stage 1: Intake & Cleansing"]
        Raw[Nguồn thô: HTML TVPL / Docx / PDF] --> Maskara[Maskara Privacy Gate: Redact PII]
        Maskara --> MarkdownClean[Clean Markdown Normalizer]
    end

    subgraph Stage2 ["Stage 2: AST Structural Parsing"]
        MarkdownClean --> ASTParser[ast_parser.py: Split Phần/Chương/Điều/Khoản/Điểm]
        ASTParser --> FullMd[<doc_slug>.md với OKF v0.2 Frontmatter]
        ASTParser --> ClausesJson[clauses.json: Chỉ mục Khoản/Điều]
        ASTParser --> TechnicalData[tables/ CSV & formulas.json (QCVN/TCVN)]
    end

    subgraph Stage3 ["Stage 3: OKF Bundle Packaging & Registry"]
        FullMd --> BundleDir[legal_docs/<category>/<doc_slug>/]
        ClausesJson --> BundleDir
        TechnicalData --> BundleDir
        BundleDir --> MOC[index.md: Map of Content]
        BundleDir --> RootReg[Update legal_registry.yaml at Root]
    end

    subgraph Stage4 ["Stage 4: Cloud Sync & RAG Indexing"]
        BundleDir --> HashCheck[SHA-256 Hash Delta Check]
        HashCheck --> NotebookLMCloud[NotebookLM Cloud: 6dca7e4e-c407-4d1f-882a-e0d9459d1120]
    end
```

---

## 📑 3. Chi tiết Đóng gói 1 OKF Bundle Chuẩn

Mỗi văn bản pháp lý/kỹ thuật sau khi đóng gói sẽ hình thành một thư mục Bundle phẳng nằm tại `legal_docs/<category>/<doc_slug>/`:

```text
legal_docs/01_vbpl/luat_55_2024_qh15_pccc/
├── luat_55_2024_qh15_pccc.md          # 1. Toàn văn sạch có YAML Frontmatter (5 Trust Signals)
├── index.md                            # 2. Map of Content (MOC) chỉ mục tài nguyên
├── clauses.json                        # 3. Structural AST Index (Ánh xạ từng Khoản/Điều tới số dòng)
├── tables/                             # 4. Bảng chỉ tiêu kỹ thuật dạng CSV/JSON (Nếu là QCVN)
│   └── bang_1_gioi_han_chiu_lua.csv
└── formulas.json                       # 5. Công thức PCCC / Kết cấu (Nếu là QCVN)
```

---

## 🚩 4. Các Ticket Triển khai (Action Tickets)

- [x] **[Ticket-OKF-01] [Task AFK]** Chuẩn hóa YAML Frontmatter Schema OKF v0.2 với 5 Trust Signals.
- [x] **[Ticket-OKF-02] [Task AFK]** Thiết lập vị trí đầu ra phẳng tại Root Level 1 (`legal_docs/01_vbpl/`, `02_qcvn/`...).
- [ ] **[Ticket-OKF-03] [Task AFK]** Tích hợp `ast_parser.py` tự động xuất `clauses.json` khi chạy `legal_intelligence.py`.
- [ ] **[Ticket-OKF-04] [Task AFK]** Viết module `table_extractor.py` bóc tách bảng HTML trong QCVN thành các tệp `.csv` trong thư mục `tables/`.

---
*Khởi tạo bởi CCBA Wayfinder Agent — 2026-07-26*
