# ADR 0035: Tri-Tier Cloud Binary Vault Architecture & Universal Ingestion Pipeline 2.0

- **Trạng thái:** ACCEPTED & ADOPTED (Đã chấp thuận & Áp dụng)
- **Ngày quyết định:** 2026-08-27
- **Tác giả:** CCBA Legal Intelligence & Cloud Infrastructure Architecture Team
- **Liên quan:** [ADR 0016: Dual-Track Hybrid PDF Anchor of Trust](0016-dual-track-hybrid-pdf-anchor-of-trust.md), [ADR 0021: OKF v2.2 Pure Normative Body](0021-okf-v2-2-pure-normative-body-legal-graph.md), [ADR 0030: Visual Parity & Footnote Monotonicity](0030-visual-parity-and-2d-navigation-matrix.md), [ADR 0034: OKF v2.3 Dual-Engine Technical Standards](0034-okf-v2-3-dual-engine-technical-standards.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)

Kho tri thức pháp lý xây dựng `ccba-legal-knowledge` đang mở rộng để chứa hàng trăm văn bản quy phạm pháp luật (Luật, Nghị định, Thông tư) và quy chuẩn/tiêu chuẩn kỹ thuật (QCVN, TCVN). Qua đợt nghiên cứu và phản biện thực tế (**Double-Pass Adversarial Review**), chúng tôi ghi nhận 4 điểm nghẽn nghiêm trọng trong pipeline v1.0:

1. **Phình to dung lượng Git Repository (Git Bloat):** Việc commit trực tiếp các tệp PDF Công báo scan nặng (từ 10MB đến 30MB mỗi file) khiến dung lượng repository tăng nhanh lên hàng Gigabyte, làm chậm thao tác `git clone`/`git pull` và cản trở việc phân phối tri thức.
2. **Thiếu tính toàn vẹn của tệp nguồn nhị phân:** Các tệp `.docx` và `.pdf` bị lưu phân tán trong thư mục ẩn `.md/extracted_docs/`, người dùng khó tiếp cận trực quan từ cây thư mục bundle.
3. **Lỗ hổng Crawler TVPL (Single-Asset Bias):** Logic tải dữ liệu từ Thư Viện Pháp Luật (TVPL) ưu tiên file `.docx` dẫn đến việc bỏ qua hoàn toàn file `.pdf` Công báo chính thức, làm thiếu vắng mỏ neo pháp lý tối thượng (ADR 0016).
4. **Lỗi biến dạng bảng Word và đứt gãy chuỗi chú thích:** Thuật toán khử trùng lặp ô ngộp ngang bằng so sánh chuỗi lân cận (`val != row[i-1]`) gây mất cột khi 2 ô có giá trị giống nhau; đồng thời thiếu khả năng xử lý ô gộp dọc (`vMerge`) và làm vỡ dòng tiêu đề Markdown khi ô chứa `\n`.

---

## 2. Quyết Định Kiến Trúc: Mô Hình Lưu Trữ 3 Tầng & Ingestion Pipeline 2.0 (Decision)

Chúng tôi quyết định ban hành kiến trúc **Tri-Tier Cloud Binary Vault & Ingestion Pipeline 2.0** với các quy tắc bắt buộc:

```
                    ┌────────────────────────────────────────────────────────┐
                    │        TRI-TIER CLOUD BINARY VAULT ARCHITECTURE        │
                    └────────────────────────────────────────────────────────┘
                                                 │
          ┌──────────────────────────────────────┼──────────────────────────────────────┐
          ▼                                      ▼                                      ▼
【TẦNG 1: GIT SPOKE】                  【TẦNG 2: GOOGLE DRIVE VAULT】          【TẦNG 3: LOCAL CACHE】
Siêu nhẹ (< 50MB)                      Lưu trữ vĩnh viễn PDF/DOCX             Thư mục `sources/` cục bộ
• Markdown OKF v2.3                    • Thư mục `CCBA_Legal_Vault/`          • Được thêm vào `.gitignore`
• Bảng CSV/JSON & Cards                • OAuth2 Google Account                • Tải On-Demand khi cần
• metadata.yaml & registry             • SHA-256 đối soát bất biến            • Offline fast verification
```

---

### 🏛️ Trụ Cột 1 — Mô Hình Lưu Trữ 3 Tầng (Tri-Tier Storage Invariant)

1. **Tầng 1 — Git Spoke Thuần Khiết:**
   - 100% tệp nhị phân lớn (`legal_docs/**/sources/*.pdf`, `legal_docs/**/sources/*.docx`) được đưa vào `.gitignore`.
   - Git repository chỉ lưu trữ: Thân văn bản Markdown, Bảng tra cứu CSV/JSON số hóa, Thẻ thị giác JSON, Bộ giải Python và file siêu dữ liệu `metadata.yaml` / `legal_registry.yaml`.
2. **Tầng 2 — Google Drive Cloud Binary Vault:**
   - Sử dụng thư mục đám mây tập trung `CCBA_Legal_Vault/` phân cấp theo `01_vbpl/`, `02_qcvn/`, `03_tcvn/`.
   - Mỗi văn bản được liên kết trong `metadata.yaml` thông qua schema chuẩn `source_assets`:
     ```yaml
     source_assets:
       docx:
         sha256: b74016776ef230147524cf7f1b30f57ca51425818502238ed8203d7623c10abf
         gdrive_file_id: 1a2B3c4D5e6F...
         gdrive_view_url: https://drive.google.com/file/d/1a2B3c4D5e6F.../view
       pdf:
         sha256: 0375f3b798e01dfde379710648c8024edc71b5718ec5ee4f0e405764620c7a7d
         gdrive_file_id: 9z8Y7x6W5v4U...
         gdrive_view_url: https://drive.google.com/file/d/9z8Y7x6W5v4U.../view
     ```
3. **Tầng 3 — Local Workspace Cache:**
   - Thư mục `legal_docs/<loai_vb>/<ten_vb>/sources/` hoạt động như một local cache. Người dùng có thể kéo tệp về máy khi cần mở xem offline bằng CLI `python -m ccba_legal pull-source <id>`.

---

### 🔄 Trụ Cột 2 — Thu Thập Song Mã Tự Động (Dual-Asset Ingestion Pipeline)

1. **Crawl 2 Nhịp (Dual-Asset Harvester):**
   - Khi chạy lệnh Ingest, crawler tự động thực hiện:
     * **Nhịp 1:** Tải file `.docx` tại trang chính văn bản (nguồn giàu cấu trúc nhất để parse).
     * **Nhịp 2:** Tự động điều hướng sang `?Tab=TaiVe`, tìm và tải file `.pdf` Công báo chính thức (mỏ neo pháp lý).
2. **Auto Cloud Sync & Google Docs Native Conversion:**
   - Tự động tính mã băm SHA-256 ngay khi tải về và upload trực tiếp lên Google Drive Vault.
   - **Tự động chuyển đổi sang Native Google Docs:** File `.docx` khi tải lên Drive được tự động chuyển đổi sang định dạng Native Google Docs (`application/vnd.google-apps.document`) nhằm tối ưu $100\%$ khả năng nạp nguồn trực tiếp cho **Google NotebookLM** và cho phép mở xem/cộng tác trực tuyến tức thì.
   - Ghi đồng bộ `gdrive_file_id`, `gdrive_view_url` và `sha256` vào `metadata.yaml` và `legal_registry.yaml`.


---

### 🛡️ Trụ Cột 3 — Bộ Chuyển Đổi Bảng Biểu Chống Vỡ (Resilient Table & Footnote Parser)

1. **Lưới 2D Thực Thể (OpenXML Virtual 2D Grid):**
   - Xóa bỏ cơ chế khử trùng lặp chuỗi ngây thơ `val != row[i-1]`.
   - Phân tích trực tiếp thẻ XML `w:gridSpan` (ô gộp ngang) và `w:vMerge` (ô gộp dọc) để dựng ma trận bảng 2 chiều chuẩn xác, không bao giờ bị mất cột hay trượt dữ liệu.
2. **Làm Phẳng Tiêu Đề Bảng (Auto-Flatten Headers):**
   - Loại bỏ triệt để mọi ký tự ngắt dòng `\r`, `\n`, `\x0b` bên trong các ô tiêu đề bảng của Word, đảm bảo $100\%$ dòng tiêu đề và dòng phân cách Markdown không bị gãy dòng.
3. **Cưỡng Chế Đánh Số Chú Thích Đơn Điệu (Monotonic Footnote Enforcement):**
   - Cưỡng chế quy tắc đánh số `**CHÚ THÍCH 1:**`, `**CHÚ THÍCH 2:**` cho toàn bộ ghi chú đa cấp. Bất kỳ văn bản nào có `CHÚ THÍCH 2` mà thiếu `CHÚ THÍCH 1` đều bị CI Gate chặn lại (`MISSING_NOTE_1`).

---

## 3. Hệ Quả & Lợi Ích (Consequences)

- **Dung lượng Repo tối ưu:** Git Spoke duy trì dung lượng dưới 50MB vĩnh viễn, clone về máy trong 2 giây.
- **Tiện ích tối đa cho người dùng:** Mọi thành viên trong tổ chức có thể xem trực tiếp bản PDF/DOCX gốc qua link Google Drive mà không cần cài Git hay clone repo.
- **Tích hợp sâu hệ sinh thái AI:** Các kỹ năng như `notebooklm-connector` có thể import trực tiếp URL PDF từ Drive để tạo Audio Overview hoặc RAG Cloud.
- **Master CI Gate an toàn 100%:** Quá trình kiểm định CI trên máy chủ hoặc máy mới không bị phụ thuộc vào sự tồn tại của các file PDF vật lý trên ổ đĩa.
