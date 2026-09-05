# Báo cáo Nghiên cứu: Hình Mẫu Dữ Liệu Bảng & Chiến Lược Bóc Tách Tri Thức Toàn Diện (Universal Table Knowledge Extraction Architecture)

> **Mã nghiên cứu:** `RESEARCH-TABLE-ARCHETYPE-2026-09`  
> **Chế độ thực thi:** Phản biện Kép (Dual-Agent Adversarial Pattern - `/ccba-research`)  
> **Tác nhân tham gia:** `Table Pattern Explorer` & `Edge Case & Risk Challenger`  
> **Phạm vi đối chiếu:** Toàn bộ kho tri thức `legal_docs/` (`01_vbpl`, `02_qcvn`, `03_tcvn`), OpenXML Specification ISO/IEC 29500, và 12 Cổng kiểm định Master CI Spoke.

---

## 1. Tóm tắt Thực thi (Executive Summary)

Dữ liệu bảng trong hệ thống Văn bản Quy phạm Pháp luật (VBPL), Quy chuẩn Kỹ thuật Quốc gia (QCVN) và Tiêu chuẩn Quốc gia (TCVN) ngành Xây dựng là **mỏ neo tri thức định lượng cốt tử** phục vụ thẩm định thiết kế, kiểm tra an toàn chịu lực, và nghiệm thu công trình. Khảo sát thực tế toàn bộ kho dữ liệu cho thấy bảng biểu kỹ thuật tại Việt Nam sở hữu độ phức tạp hình học và ngữ nghĩa vượt xa các bảng dữ liệu thông thường:
- Từ các bảng số liệu phẳng đơn giản, bảng tiêu đề phân cấp 3-4 tầng (`HIERARCHICAL_GRID`), bảng chứa sơ đồ tiết diện kỹ thuật/công thức toán trong ô (`IN_CELL_MULTIMODAL`), đến các bảng biểu mẫu hành chính (`ADMIN_FORM`) và bảng dàn trang không viền (`BORDERLESS_LAYOUT`).

Qua vòng phản biện độc lập đối kháng (Adversarial Review), hệ thống đã bóc trần **5 bẫy kỹ thuật nguy hiểm** của các bộ parser truyền thống:
1. **Lệch chỉ mục cột (Column Skew)** do duyệt ngây thơ qua thuộc tính `gridSpan` và `vMerge` của Word OpenXML;
2. **Ô nhiễm dữ liệu bảng (Table Clutter)** do bốc nhầm các bảng bố cục dàn trang (quốc hiệu, khung công thức, chữ ký) thành các bảng CSV quy phạm;
3. **Phá vỡ liên kết chú thích (Footnote Corruption)** do nuốt mất ký hiệu tham chiếu (`150(*)`, `H0(1)` biến thành `1501`), tự tiện gán số thứ tự nhân tạo (`CHÚ THÍCH 1..N`), hoặc nhồi khối văn bản chú thích dài ngoặc vào đáy file CSV;
4. **Mất trắng tri thức đa phương thức trong ô (In-Cell Blindness)** khi công thức MathType OLE hoặc hình vẽ vector WMF bị chuyển thành chuỗi rỗng `""`;
5. **Xung đột trực tiếp với 5/12 Cổng kiểm định Master CI** (Gate 3, Gate 8, Gate 9, Gate 11, Gate 12).

Để giải quyết triệt để các tồn tại trên, báo cáo đề xuất **Kiến trúc Bóc tách Bảng Đa tầng Xác định (Deterministic Multi-Tier Table Extraction Pipeline)** dựa trên:
- **Taxonomy 6 Hình mẫu Bảng (6 Table Archetypes)** rõ ràng;
- **Bộ phân loại nhị phân xác định (Binary Layout Classifier)** tách biệt bảng dàn trang và bảng quy chuẩn;
- **Thuật toán Virtual 2D Grid Engine** phục hồi lưới tọa độ $R \times C$ nguyên bản với cơ chế *Hierarchical Forward-Fill* có metadata kiểm soát;
- **Cơ chế Footnote Decoupled & Semantic Binding** bảo tồn $100\%$ ký hiệu gọi chú dẫn;
- **Cấu trúc lưu trữ 4 tầng (Markdown, CSV, Deep Semantic JSON, Metadata Catalog)** tương thích hoàn toàn với Pandas/DuckDB, LLM RAG, và 12 Cổng kiểm định CI.

---

## 2. Kết quả Nghiên cứu Chi tiết (Key Findings)

### 2.1 Hệ Thống Phân Loại Hình Mẫu Bảng (Table Archetype Taxonomy)

Dựa trên khảo sát thực chứng trên 37 văn bản hiện hữu, cấu trúc bảng trong văn bản xây dựng Việt Nam được phân hóa thành 6 nhóm hình mẫu chuẩn:

```
                                  ┌─────────────────────────────┐
                                  │   TẤT CẢ CÁC BẢNG DOCX      │
                                  └──────────────┬──────────────┘
                                                 │
                                     [Bộ Phân Loại Nhị Phân]
                                                 │
                      ┌──────────────────────────┴──────────────────────────┐
                      ▼                                                     ▼
           ┌──────────────────────┐                              ┌──────────────────────┐
           │   BẢNG PHI QUY CHUẨN │                              │   BẢNG QUY CHUẨN 2D  │
           └──────────┬───────────┘                              └──────────┬───────────┘
                      │                                                     │
         ┌────────────┴────────────┐                           ┌────────────┴────────────┐
         ▼                         ▼                           ▼            ▼            ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│BORDERLESS_LAYOUT│       │   ADMIN_FORM    │       │ FLAT_MATRIX │ │HIERARCHICAL │ │  IN_CELL_   │
│ Khung công thức,│       │ Biểu mẫu hồ sơ, │       │ Lưới phẳng  │ │    _GRID    │ │ MULTIMODAL│
│ chữ ký nơi nhận │       │ nghiệm thu QC   │       │ chuẩn 2D    │ │ Tiêu đề đa  │ │ Chứa ảnh /│
│ ➔ Markdown/KaTeX│       │ ➔ templates/    │       │ ➔ CSV/JSON  │ │ tầng lồng   │ │ KaTeX ô   │
└─────────────────┘       └─────────────────┘       └─────────────┘ └─────────────┘ └─────────────┘
                                                                           │
                                                            ┌──────────────┴──────────────┐
                                                            ▼                             ▼
                                                     FOOTNOTE_RICH                 SEMANTIC_BIND
                                                     Chú thích quy phạm            Áp dụng hệ số
                                                     ngoại lệ chân bảng             theo ô dữ liệu
```

1. **`FLAT_MATRIX` (Bảng Tra Cứu 2D Đơn Tầng):**
   - *Đặc điểm:* Header 1 dòng duy nhất, không gộp ô phức tạp, dữ liệu số hoặc chuỗi nguyên tử (ví dụ: Bảng H.1 `qcvn_06_2022_bxd`, Bảng 1 `tcvn_2737_2023`).
   - *Lưu trữ:* Xuất trực tiếp ra Markdown GFM, `tables/csv/{slug}.csv` và `tables/json/{slug}.json`.
2. **`HIERARCHICAL_GRID` (Ma Trận Phân Cấp Đa Tầng):**
   - *Đặc điểm:* Header từ 2 đến 4 tầng (lồng nhau theo nhóm thông số như hướng gió, bề mặt đón/khuất gió, tỷ số hình học), hoặc có hàng phân loại trải dài toàn bộ chiều rộng (Category Partition Rows) (ví dụ: Bảng F.13, F.14, F.15 `tcvn_2737_2023`, Bảng 2.1 `qcvn_09_2017_bxd`).
   - *Lưu trữ:* Header được phẳng hóa có cấu trúc phân cấp (`"Danh mục Cha — Phân nhóm Con"`), JSON lưu cây thuộc tính phân cấp.
3. **`IN_CELL_MULTIMODAL` (Bảng Đa Phương Thức Trong Ô):**
   - *Đặc điểm:* Ô dữ liệu chứa đồng thời văn bản, sơ đồ hình học (vector WMF/EMF hoặc raster PNG), và công thức KaTeX phức tạp (ví dụ: Bảng F.12 `tcvn_2737_2023` chứa sơ đồ tiết diện đa giác đều kèm ảnh `<img ...>` và công thức $Re > 4 \cdot 10^5$).
   - *Lưu trữ:* Bóc tách ảnh sang `figures/images/`, nhúng thẻ `<img>` với đường dẫn tương đối an toàn, công thức đưa về inline KaTeX `$f(x)$`.
4. **`FOOTNOTE_RICH` (Bảng Quy Phạm Chú Thích Rẽ Nhánh):**
   - *Đặc điểm:* Bảng đi kèm hệ thống chú thích chân bảng chứa các quy định pháp lý ngoại lệ (waivers), công thức phụ trợ, hoặc điều kiện nhân hệ số an toàn.
   - *Lưu trữ:* Tách rời hoàn toàn khỏi ô ma trận dữ liệu, bảo tồn $100\%$ ký hiệu gọi (`(*)`, `(1)`), xuất cấu trúc `footnotes` độc lập trong JSON.
5. **`BORDERLESS_LAYOUT` (Bảng Bố Cục Dàn Trang Ẩn Viền):**
   - *Đặc điểm:* Bảng 1 hàng 2 cột không viền dùng để căn lề công thức toán `$$f(x)$$ \tag{1}` hoặc Quốc hiệu - Tiêu ngữ.
   - *Lưu trữ:* **Cấm xuất vào `tables/`**. Giải mã trực tiếp thành các khối Markdown / KaTeX trên thân văn bản chính.
6. **`ADMIN_FORM` (Biểu Mẫu Hành Chính / Biên Bản Nghiệm Thu):**
   - *Đặc điểm:* Bảng biểu mẫu kiểm mục, biên bản nghiệm thu có ô ký tên, checkbox `[ ]`, chỗ điền thông tin chấm lửng `...` (ví dụ: Phụ lục Thông tư 10/2021/TT-BXD, Nghị định 207/2026/NĐ-CP).
   - *Lưu trữ:* Định tuyến về thư mục **`templates/`** (Atomic Form Templates theo ADR 0021 & ADR 0036). Tuyệt đối không xuất file CSV vào `tables/`.

---

### 2.2 Phân Tích Đối Kháng 5 Bẫy Kỹ Thuật (Adversarial Risks & Edge Cases)

#### Bẫy 1: Sự Nhân Bản & Lệch Ma Trận do `w:gridSpan` và `w:vMerge`
- **Cơ chế sự cố trong OpenXML:**
  - `w:gridSpan w:val="K"` gộp $K$ cột. `python-docx` trả về $K$ tham chiếu đến cùng 1 ô nhớ. Nếu parser đọc bằng list comprehension `[c.text for c in row.cells]`, văn bản bị lặp lại $K$ lần trên 1 hàng. Nếu lọc unique cells bằng `set()` hoặc identity, hàng đó chỉ có ít phần tử hơn lưới cơ sở, biến ma trận thành hình răng cưa (jagged array).
  - `w:vMerge`: Các ô tiếp nối (`continue`) hoàn toàn không có text trong XML. Khi xuất ra Pandas/DuckDB, các ô này mang giá trị `NaN` hoặc `""`, khiến thuật toán tra cứu của Agent truy vấn sai ô trống.
- **Giải pháp kiểm soát:**
  - Đọc thẻ `<w:tblGrid><w:gridCol/>` để xác định số cột chuẩn vật lý $C$.
  - Xây dựng **Virtual Grid $R \times C$**.
  - Với ô gộp dọc (`vMerge`): Trong JSON áp dụng cơ chế **Hierarchical Forward-Fill** có kiểm soát (kèm metadata đánh dấu `{"is_merged_continuation": true, "master_cell": [r_start, c]}`).

#### Bẫy 2: Nhầm Lẫn Bảng Dàn Trang (Layout) và Bảng Số Liệu Quy Chuẩn (Normative)
- **Cơ chế sự cố:** Chuyên viên soạn thảo dùng bảng Word 2 cột không viền để kẹp số hiệu công thức `(F.1)` hoặc Quốc hiệu. Nếu parser bốc toàn bộ thẻ `<w:tbl>`, thư mục `tables/csv/` sẽ bị ô nhiễm bởi hàng chục bảng rác chỉ có 1 dòng 2 ô.
- **Giải pháp kiểm soát:** Thiết lập **Rào chắn Phân loại Nhị phân (Binary Deterministic Classifier)** dựa trên:
  1. Kiểm tra thuộc tính đường viền `w:tblBorders` (nếu viền là `none`/`nil` và số dòng $\le 2$ $\rightarrow$ cờ nghi vấn Layout Table);
  2. Kiểm tra nội dung ô (nếu có regex công thức `^\([A-Za-z0-9\.]+\)$` hoặc từ khóa hành chính `CỘNG HÒA XÃ HỘI...` $\rightarrow$ phân loại là `BORDERLESS_LAYOUT`, giải nén thành Markdown/KaTeX, cấm ghi vào `tables/`).

#### Bẫy 3: Phá Vỡ Liên Kết Footnote & Đánh Số Thứ Tự Nhân Tạo
- **Cơ chế sự cố:**
  - Parser ngây thơ tự động đổi các ký hiệu gốc `(*)`, `(**)`, `(1)` thành `CHÚ THÍCH 1:`, `CHÚ THÍCH 2:`.
  - Bộ làm sạch số liệu strip nhầm ký tự superscript trong ô, biến giá trị giới hạn chịu lửa `150(1)` thành `1501` (sai lệch 10 lần!).
  - Nhồi hàng footnote vào ô cuối của file CSV khiến các hàng dữ liệu bị lệch cột.
- **Giải pháp kiểm soát:**
  - Tách rời footnote ra khỏi ma trận số liệu CSV.
  - Bảo tồn $100\%$ ký hiệu gọi chú dẫn trong cell (`(*)`, `(1)`, `a)`).
  - Phân tích cú pháp footnote thành dictionary có cấu trúc trong JSON: `footnotes: {"(*)": "..."}`.

#### Bẫy 4: Mất Trắng Công Thức MathType và Đồ Họa Vector trong Ô
- **Cơ chế sự cố:** Khi gọi `cell.text`, các phần tử `<w:object>` (MathType MTEF) và `<w:drawing>` (WMF/EMF) bị bỏ qua hoàn toàn, dẫn đến ô bảng bị rỗng.
- **Giải pháp kiểm soát:**
  - Kế thừa trực tiếp bộ giải mã **MathType MTEF Binary Parser (`mtef_parser.py` - ADR 0040)**: Quét đệ quy từng đoạn văn trong ô, chuyển đổi trực tiếp sang KaTeX inline `$f(x)$`. Cấm dùng block `$$` trong ô vì sẽ phá vỡ cú pháp bảng Markdown GFM.
  - Trích xuất ảnh trong ô sang `figures/images/`, chuyển đổi WMF/EMF sang SVG và PNG 300 DPI, nhúng vào cell bằng thẻ `<img src="..." width="..." alt="...">`.

#### Bẫy 5: Rủi Ro Xung Đột với 12 Cổng Kiểm Định Master CI
- Nếu thay đổi logic bóc tách bảng mà không kiểm soát:
  - **Gate 3 (Table Attachments):** Sẽ FAIL nếu bảng layout bị xóa bỏ nhưng link trong markdown chưa cập nhật.
  - **Gate 8 (Table Structural Integrity):** Sẽ FAIL nếu bảng bị vỡ pipe (`|`).
  - **Gate 9 (Visual Parity):** Sẽ FAIL nếu footnote bị dồn cục `<br>` trong ô hoặc mất dấu thụt dòng `&nbsp;&nbsp;\- `.
  - **Gate 11 (DOCX-to-Markdown Verbatim Parity):** Sẽ FAIL nếu ô gộp gây nhân bản từ vựng hoặc nuốt mất chữ.
  - **Gate 12 (Multimodal Integrity):** Sẽ FAIL nếu bỏ quên file WMF/EMF trong ô bảng mà không chuyển sang Dual-Format.

---

## 3. Khuyến nghị Triển khai (Implementation Recommendations)

### 3.1 Ma trận Đánh giá Giải pháp: Giá trị × Độ phức tạp × Rủi ro × KISS

| Hạng mục Đề xuất | Giá trị Kỹ thuật | Độ Phức Tạp | Rủi Ro Hệ Thống | Tuân thủ KISS | Phân loại Hành động |
|:---|:---:|:---:|:---:|:---:|:---|
| **1. Binary Layout Table Classifier** | **Rất cao** (Loại bỏ 100% bảng rác trong `tables/`) | Thấp | Rất thấp | ✅ Tối đa (30 dòng code kiểm tra border & keyword) | **Đã có khung, cần hoàn thiện** |
| **2. Virtual 2D Grid Engine** | **Tối thượng** (Ma trận CSV/JSON chuẩn xác 1:1) | Trung bình | Thấp | ✅ Khởi tạo ma trận cố định dựa trên `gridCol` | **Cần nâng cấp trong `table_handler.py`** |
| **3. Decoupled Footnote Engine** | **Rất cao** (Bảo toàn nguyên vẹn điều kiện miễn trừ) | Thấp | Rất thấp | ✅ Tách hàng footnote ra khỏi grid, giữ nguyên header gốc | **Đã áp dụng mẫu ở Bảng 2.1, cần khái quát hóa** |
| **4. In-Cell Multimodal & KaTeX** | **Tối thượng** (Triệt tiêu ô rỗng trong bảng kỹ thuật) | Thấp | Rất thấp | ✅ Tái sử dụng `render_paragraph_with_runs` và `mtef_parser` | **Cần thống nhất giữa handler và extractor** |
| **5. Deep Semantic JSON Schema** | **Rất cao** (Sẵn sàng cho Agent Tool Calling / Pandas) | Thấp | Rất thấp | ✅ Bổ sung trường `archetype`, `headers_hierarchy`, `footnotes` | **Cần chuẩn hóa schema JSON** |

---

### 3.2 Lộ Trình Triển Khai 3 Bước Khả Thi

```
[Bước 1: Khái Quát Hóa Module Hub]
 ├── Hoàn thiện Virtual 2D Grid Engine trong table_handler.py (hỗ trợ N-tier headers & vMerge)
 ├── Thống nhất gọi render_paragraph_with_runs(rid_to_katex) xuyên suốt table_handler & table_extractor
 └── Khóa chặt Binary Layout Table Classifier (định tuyến ADMIN_FORM sang templates/)
          │
          ▼
[Bước 2: Chuẩn Hóa Schema Lưu Trữ Đa Tầng]
 ├── Cập nhật tables_catalog.json bổ sung trường `archetype`
 └── Chuẩn hóa tables/json/{slug}.json tách rời `matrix` và `footnotes`
          │
          ▼
[Bước 3: Tích Hợp Rào Chắn Kiểm Định Master CI]
 ├── Nâng cấp Gate 8: Kiểm tra tính chuẩn tắc ma trận CSV (Zero Jagged Rows)
 ├── Nâng cấp Gate 9: Cưỡng chế bảo tồn ký hiệu footnote gốc trong cell
 └── Chạy toàn trình validate_legal_spoke.py đảm bảo 12/12 Gates PASSED
```

---

## 4. Tài liệu Tham chiếu & Citations (References & Citations)

1. **Hiến pháp Spoke & Kiến trúc Nền tảng:**
   - [`AGENTS.md`](file:///d:/GitHubProjects/ccba-legal-knowledge/AGENTS.md): Core Invariants (ADR 0021, ADR 0036, ADR 0037, ADR 0039, ADR 0040).
   - [`.md/knowledge/session_learnings.md`](file:///d:/GitHubProjects/ccba-legal-knowledge/.md/knowledge/session_learnings.md): Mục 4 (12 Master CI Gates), Mục 38 (In-Cell Schematic Ingestion), Mục 40 (Universal Deterministic Multimodal Pipeline).
2. **Mã nguồn Bộ Chuyển Đổi:**
   - [`table_handler.py`](file:///D:/GitHubProjects/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/standard/handlers/table_handler.py): Logic dựng bảng Markdown, phẳng hóa tiêu đề 2 tầng và trích xuất footnote.
   - [`table_extractor.py`](file:///D:/GitHubProjects/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/table_extractor.py): Bộ lọc phân loại bảng bố cục và thu hoạch caption.
   - [`strategy.py`](file:///D:/GitHubProjects/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/standard/strategy.py): Module render run văn bản và công thức KaTeX nội dòng.
   - [`mtef_parser.py`](file:///D:/GitHubProjects/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/converters/mtef_parser.py): Bộ giải mã nhị phân MathType MTEF v3/v5.
3. **Văn bản Thực Chứng trong Kho Tri Thức:**
   - `legal_docs/02_qcvn/qcvn_09_2017_bxd/`: Bảng 2.1 (Hệ số SHGC và WWR - Footnote giàu công thức toán).
   - `legal_docs/02_qcvn/qcvn_06_2022_bxd/`: Bảng H.1 (Bậc chịu lửa và diện tích khoang cháy - Flat Matrix).
   - `legal_docs/03_tcvn/tcvn_2737_2023/`: Bảng F.12 (Hệ số khí động - In-Cell Multimodal) và Bảng F.15 (Độ mảnh hiệu dụng - Hierarchical Grid 4 cột).
   - `legal_docs/01_vbpl/thong_tu_10_2021_tt_bxd/`: Các mẫu biểu kiểm mục và biên bản nghiệm thu (Admin Form Templates).

---

## 5. Câu hỏi chưa làm rõ & Giả định mầm (Unresolved Questions)

1. **Về việc điền khuyết (Forward-Fill) khi xuất CSV:**
   - *Vấn đề:* Đối với ô gộp dọc (`vMerge`) như tên cột "Loại công trình" gộp qua 5 hàng con, trong file CSV nên để các hàng sau là ô rỗng `""` (bảo toàn trực quan giống bản in) hay tự động copy giá trị từ ô master xuống (để tiện lợi cho thư viện Pandas/SQL query)?
   - *Khuyến nghị:* Trong CSV nên áp dụng **Forward-Fill có kiểm soát** để dữ liệu quan hệ luôn hoàn chỉnh; trong file Markdown hiển thị giữ nguyên bố cục trực quan; trong file JSON lưu rõ metadata `is_merged_continuation`.
2. **Về bảng có chiều rộng vượt quá khổ giấy (Wide Tables):**
   - *Vấn đề:* Một số bảng trong TCVN có từ 12 đến 20 cột, khi render trên Markdown xem trên web bị tràn màn hình (horizontal scrolling).
   - *Khuyến nghị:* Ưu tiên người dùng tra cứu qua file CSV/JSON trong thư mục `tables/` đã được module hóa, trên Markdown giữ cấu trúc GFM chuẩn.

---

*Báo cáo được thực hiện theo quy trình Nghiên cứu Phản biện Kép (`/ccba-research`) của CCBA Agent Platform.*
