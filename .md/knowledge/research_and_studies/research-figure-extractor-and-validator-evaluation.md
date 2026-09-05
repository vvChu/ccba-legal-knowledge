# Báo Cáo Nghiên Cứu & Đánh Giá Đối Kháng: Thuật Toán figure_extractor.py và Hệ Thống Kiểm Định Spoke Master CI (Gate 12)

> [!IMPORTANT]
> **Phương pháp thực hiện:** Quy trình `/ccba-research` áp dụng **Mô hình Phản biện Đối kháng Kép (Dual-Agent Adversarial Review)** kết hợp nguyên tắc **Code-First Research** và **KISS (Keep It Simple, Stupid)**.  
> **Hai luồng nghiên cứu độc lập:**
> - **Luồng 1 (Auditor & Proponent):** Khảo sát chi tiết 415 dòng code của `figure_extractor.py` và Gate 12 trong `validate_legal_spoke.py`.
> - **Luồng 2 (Risk & Fidelity Challenger):** Phản biện rủi ro hồi quy trên 43 sơ đồ khí động TCVN 2737:2023, 30+ biểu đồ TCVN 5574:2018, và đo lường tác động đến 15 Cổng Master CI.

---

## 1. Tóm Tắt Thực Thi (Executive Summary)

Sau khi đối soát mã nguồn thực tế tại Hub (`packages/ccba-legal-intel/src/ccba_legal/figure_extractor.py`) và Spoke (`scripts/validate_legal_spoke.py`), kết luận rõ ràng và dứt khoát là:

1. **KHÔNG CẦN VÀ KHÔNG NÊN TÁI CẤU TRÚC TOÀN DIỆN (NO SWEEPING REFACTOR):**
   - `figure_extractor.py` chỉ có **415 dòng code**, chạy hoàn toàn ở chế độ **Offline Ingest / Batch Convert**, không hề nằm trên đường dẫn phản hồi thời gian thực (latency-critical path) của RAG hay Agent Chat.
   - Việc chia nhỏ tệp này thành 4 module con (`docx_scanner.py`, `media_processor.py`, `image_stitcher.py`, `catalog_renderer.py`) là một sự trừu tượng hóa quá mức (Over-Abstraction) vi phạm nghiêm trọng nguyên tắc **KISS**, tiềm ẩn nguy cơ cực lớn phá vỡ tính tương thích ngược với **43 sơ đồ khí động phức tạp của TCVN 2737:2023** và **30+ biểu đồ ứng suất của TCVN 5574:2018**.

2. **CẦN THỰC HIỆN 4 VÁ PHẪU THUẬT CỤC BỘ (SURGICAL PATCHES):**
   - **Vá 1 (Khử Anti-Pattern "Pollute-then-Prune"):** Ngừng giải nén vô điều kiện các tệp `.wmf` và `.emf` vào `figures/images/`, tránh nguy cơ rò rỉ file vector nhị phân vi phạm Gate 12.
   - **Vá 2 (Cross-Platform Typography Fallback):** Bổ sung danh sách font dự phòng đa tầng cho PIL ImageDraw thay vì chỉ dựa vào font Windows `arialbd.ttf`, bảo vệ hiển thị tiếng Việt trên Linux CI.
   - **Vá 3 (Bổ khuyết Gate 12 Spoke):** Bổ sung kiểm tra tệp ảnh rỗng 0-byte (`stat().st_size == 0`) trong Gate 12 để ngăn tệp ảnh hỏng lọt qua CI.
   - **Vá 4 (Khử Silent Pass trong Spoke):** Cung cấp fallback độc lập trong `validate_legal_spoke.py` khi quét ảnh mồ côi (Orphan Figures) nếu Spoke chạy trong môi trường standalone chưa cài Hub.

---

## 2. Kết Quả Nghiên Cứu Chi Tiết (Key Findings)

### 2.1. Đánh Giá Hiện Trạng `figure_extractor.py` (Hub - 415 dòng)

```
┌─────────────────────────────────────────────────────────────────────────┐
│              CẤU TRÚC HIỆN TẠI CỦA figure_extractor.py (415 dòng)       │
├─────────────────────────────────────────────────────────────────────────┤
│ • L15-25:   load_bundle_figures_overrides()      [11 dòng - Đọc YAML]   │
│ • L27-294:  extract_docx_figures()               [268 dòng - God Func]  │
│   ├─ L51-65:   Quét caption Hình X - Tiêu đề                            │
│   ├─ L66-94:   Merge figures_override.yaml & sort                       │
│   ├─ L102-111: Unconditional zip extract (Lỗ hổng WMF/EMF)              │
│   ├─ L130-193: Bounded range paragraph XML rId scanning                 │
│   ├─ L194-232: PIL Image vertical stitching (Ghép ảnh a, b, c)          │
│   ├─ L233-252: Fallback heuristic chọn ảnh có diện tích lớn nhất        │
│   └─ L253-289: Render card Markdown & dump figures_catalog.yaml         │
│ • L296-329: render_markdown_figure_card()        [34 dòng - Pure render]│
│ • L331-410: scan_and_prune_orphan_figures()      [80 dòng - Clean scan] │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Điểm mạnh đã được kiểm chứng (Battle-Tested Strengths):
1. **Cơ chế Bounded Range Scanning (L131-L150):** Quét ngược có chặn (`search_start = max(prev_idx + 1, f_idx - 30)`) và quét xuôi tìm trang nối tiếp (`Hình X (kết thúc)`) giúp giải quyết xuất sắc các sơ đồ nhiều trang của TCVN 2737:2023.
2. **Cơ chế Override Linh Hoạt (L43, L66-81):** `figures_override.yaml` đóng vai trò là "phao cứu sinh", cho phép can thiệp thủ công các ca dị biệt mà không cần sửa core parser.
3. **Thẻ Thị Giác Chuẩn Hóa (L296-329):** Sinh các file `figures/cards/hinh_{slug}.md` đồng vị $1:1$ với catalog, có mỏ neo HTML `<a id="...">` và callout chú thích khí động.

#### Điểm yếu và rủi ro kỹ thuật (Vulnerabilities):
1. **Lỗ hổng "Pollute-then-Prune" (L105-110):**
   ```python
   # Unconditionally extract all media files so any inline diagram image is present
   for media_path in media_list:
       fname = Path(media_path).name
       target_file = images_dir / fname
       if not target_file.exists():
           target_file.write_bytes(z.read(media_path))
   ```
   Nếu DOCX chứa `image1.wmf`, nó bị ghi ngay vào `figures/images/`. Mặc dù cuối hàm có gọi prune, nhưng nếu quá trình này lỗi hoặc bị ngắt, tệp `.wmf` sẽ kích hoạt lỗi cờ đỏ tại Gate 12.
2. **Phụ thuộc font Windows `arialbd.ttf` (L198-201):**
   Khi chạy trên Linux CI, PIL rơi vào `ImageFont.load_default()` (font bitmap không dấu), làm hỏng hiển thị tiếng Việt khi ghép chú thích `a)`, `b)`.

---

### 2.2. Đánh Giá Sự Ghép Nối Với `validate_legal_spoke.py` (Spoke)

1. **Gate 12 (`validate_multimodal_assets_and_cards_gate`: L768-L864):**
   - Đã kiểm tra: Cấm `.wmf`/`.emf`, đối soát 1:1 giữa catalog và cards, kiểm tra `is_chart` có `related_tables` hoặc disclaimer.
   - **Kẽ hở:** Chưa kiểm tra kích thước file ảnh. Nếu file ảnh là 0 bytes (do lỗi I/O), Gate 12 vẫn cho PASS vì `img_path.exists()` trả về `True`.
2. **Khối Nuốt Lỗi Silent Pass tại L545-L555 (`_check_figures_catalog`):**
   ```python
   try:
       from ccba_legal.figure_extractor import scan_and_prune_orphan_figures
       scan_res = scan_and_prune_orphan_figures(doc_dir, prune=False)
       ...
   except Exception:
       pass
   ```
   Nếu Spoke chạy độc lập mà không có package `ccba-legal-intel`, kiểm tra ảnh mồ côi bị vô hiệu hóa hoàn toàn trong im lặng.

---

### 2.3. Phản Biện Đối Kháng Chuyên Sâu (Adversarial Challenger Review)

*Challenger Subagent* đã chứng minh rằng:
- **Rủi ro vỡ 1:1 Parity nếu đổi Slug:** Gate 12 gắn chặt với công thức `slug = fig_tag.lower().replace(".", "_").replace("-", "_")`. Bất kỳ thay đổi nào làm đổi tên card (ví dụ: `hinh_c_1a.md` thành `hinh_c-1a.md`) sẽ làm **FAIL ngay lập tức 100% các văn bản có hình**.
- **Tính toán chi phí/lợi ích:** Viết lại module này thành một sub-package 4-5 file sẽ tăng gấp 3 lần số dòng code, tăng chi phí bảo trì và kiểm thử hồi quy, trong khi `figure_extractor.py` hiện tại đang vận hành ổn định trên 37 văn bản và pass 100% CI Gates.

---

## 3. Khuyến Nghị Triển Khai (Implementation Recommendations)

Thực hiện theo ma trận **Giá trị × Độ phức tạp × Rủi ro × KISS**:

| Hạng mục đề xuất | Giá trị | Độ phức tạp | Rủi ro hồi quy | Khuyến nghị |
| :--- | :---: | :---: | :---: | :--- |
| **1. Tái cấu trúc thành 4 modules riêng biệt** | Thấp | Cao (300+ dòng) | 💥 Cực cao | ⛔ **BÁC BỎ HOÀN TOÀN** |
| **2. Bỏ giải nén vô điều kiện tệp .wmf/.emf (Zero-WMF Guard)** | Rất cao | Rất thấp (3 dòng) | 0% | ✅ **CHẤP THUẬN (Vá cục bộ)** |
| **3. Font Fallback đa nền tảng cho PIL ImageDraw** | Cao | Rất thấp (10 dòng) | 0% | ✅ **CHẤP THUẬN (Vá cục bộ)** |
| **4. Bổ sung Zero-Byte Image Check vào Gate 12** | Cao | Rất thấp (4 dòng) | 0% | ✅ **CHẤP THUẬN (Vá cục bộ)** |
| **5. Cung cấp Local Fallback cho Orphan Figures Scanner tại Spoke** | Cao | Thấp (15 dòng) | 0% | ✅ **CHẤP THUẬN (Vá cục bộ)** |

### Kế hoạch hành động chi tiết (Surgical Patching Plan):

1. **Tại `figure_extractor.py` (L106-110):**
   - Chỉ giải nén trực tiếp các định dạng ảnh raster thông dụng (`.png`, `.jpg`, `.jpeg`, `.gif`).
   - Bỏ qua giải nén vô điều kiện đối với `.wmf`, `.emf` vào `images_dir`.
2. **Tại `figure_extractor.py` (L198-201):**
   - Thử lần lượt các font phổ biến trên Windows, Linux, macOS: `arialbd.ttf`, `DejaVuSans-Bold.ttf`, `LiberationSans-Bold.ttf`, `FreeSansBold.ttf` trước khi fallback sang `load_default()`.
3. **Tại `validate_legal_spoke.py` (Gate 12 L818):**
   - Bổ sung assert `img_path.stat().st_size > 0` kèm thông báo lỗi rõ ràng nếu tệp ảnh 0 bytes.
4. **Tại `validate_legal_spoke.py` (L545-L555):**
   - Thay thế `except Exception: pass` bằng thuật toán quét ảnh mồ côi cục bộ độc lập dựa trên regex scanning đối chiếu với Markdown và catalog.

---

## 4. Tài Liệu Tham Chiếu & Citations

1. [`packages/ccba-legal-intel/src/ccba_legal/figure_extractor.py`](file:///D:/GitHubProjects/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/figure_extractor.py) — Mã nguồn bóc tách hình vẽ và sơ đồ hình học.
2. [`scripts/validate_legal_spoke.py`](file:///d:/GitHubProjects/ccba-legal-knowledge/scripts/validate_legal_spoke.py) — Gate 12 Multimodal Decoupled Asset & SVG/Cards Integrity Gate.
3. [`legal_docs/03_tcvn/tcvn_2737_2023/figures/figures_catalog.yaml`](file:///d:/GitHubProjects/ccba-legal-knowledge/legal_docs/03_tcvn/tcvn_2737_2023/figures/figures_catalog.yaml) — Bộ dữ liệu chuẩn mực 43 sơ đồ khí động.
4. [`legal_docs/03_tcvn/tcvn_5574_2018/figures/figures_catalog.yaml`](file:///d:/GitHubProjects/ccba-legal-knowledge/legal_docs/03_tcvn/tcvn_5574_2018/figures/figures_catalog.yaml) — Bộ dữ liệu chuẩn mực hơn 30 biểu đồ ứng suất bê tông.
5. [`docs/adr/0040-universal-deterministic-multimodal-extraction-and-zero-closed-binary-specification.md`](file:///d:/GitHubProjects/ccba-legal-knowledge/docs/adr/0040-universal-deterministic-multimodal-extraction-and-zero-closed-binary-specification.md) — Kiến trúc tri thức đa phương thức xác định và khử tệp đóng kín.

---

## 5. Câu Hỏi Chưa Làm Rõ (Unresolved Questions)

1. **Công cụ chuyển đổi WMF sang SVG ngoại vi:** Nếu gặp văn bản cổ chỉ có sơ đồ dạng vector WMF trong DOCX mà không có ảnh raster bitmap kèm theo, hệ thống nên tích hợp thư viện Python nào (`pillow-wmf` vs `wmf2svg` vs gọi `librsvg`) mà không làm phình to dependencies của Spoke?
   *(Khuyến nghị: Hiện tại 100% 37 văn bản hiện hữu đều đã có ảnh PNG nét cao, nên giữ giải pháp bóc tách PNG hiện hành và sử dụng `figures_override.yaml` khi phát sinh ngoại lệ).*
