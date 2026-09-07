# BÁO CÁO NGHIÊN CỨU CHUYÊN SÂU: KIẾN TRÚC & GIẢI PHÁP BÓC TÁCH TÀI LIỆU PHỨC TẠP TỪ CỘNG ĐỒNG DOCUMENT AI & RAG

**Mã tài liệu:** `RES-COMMUNITY-DOC-AI-2026-09`  
**Chủ đề:** Khảo sát kinh nghiệm cộng đồng quốc tế về bóc tách PDF vs DOCX cho Document AI, đánh giá 7 Framework hàng đầu và xu hướng kiến trúc lai ghép Dual-Engine.  
**Tham chiếu:** IBM Research (Docling), Meta AI (Nougat), OpenDataLab (MinerU), Datalab (Marker), LlamaIndex (LlamaParse), Artifex (PyMuPDF), Unstructured.io, và CCBA Architecture Council (ADR 0016, ADR 0038, ADR 0040, ADR 0041).

---

## 1. Bản Chất Vật Lý & Mô Hình Biểu Diễn Dữ Liệu (PDF vs. DOCX)

Sự khác biệt căn bản giữa PDF và DOCX xuất phát từ mục đích thiết kế ban đầu:

- **PDF (Portable Document Format - ISO 32000):** Được phát triển như một **Ngôn ngữ mô tả trang in (Page Description Language / Display List)** dựa trên PostScript. Mỗi ký tự (glyph) được neo tại tọa độ tuyệt đối $(x, y)$ trên trang giấy ảo.
  * **Thiếu cấu trúc ngữ nghĩa tự nhiên (Semantic Loss):** Khái niệm "đoạn văn", "tiêu đề", "cột", "bảng" không tồn tại trong luồng dữ liệu gốc.
  * **Bài toán nghịch đảo (Inverse Problem / Visual Reconstruction):** Bộ parser buộc phải dùng thị giác máy tính hoặc quy tắc hình học để "đoán" lại xem tác giả ban đầu muốn nhóm các ký tự đó thành bảng, dòng hay tiêu đề như thế nào.
- **DOCX (Office Open XML - ISO/IEC 29500):** Là định dạng đóng gói hướng tài liệu (Document-Oriented Architecture), bao gồm một tập hợp các tệp XML được nén ZIP. Cấu trúc nội tại là một **Cây Cú Pháp Tài Liệu Tường Minh (Explicit DOM Tree)**:
  * Toàn bộ phân cấp văn bản được định nghĩa chuẩn xác: `<w:p>` (đoạn), `<w:pStyle>` (Heading 1, 2, 3), `<w:tbl>` (bảng), `<w:tr>` (hàng), `<w:tc>` (ô), `<w:gridSpan>` (gộp cột ngang), `<w:vMerge>` (gộp hàng dọc).
  * **Giải mã Xác định (Deterministic AST Parsing):** Không cần phỏng đoán, không cần mô hình AI nặng nề, thông tin cấu trúc được đọc thẳng từ cây cú pháp XML với độ tin cậy $100\%$.

---

## 2. Bảng Đối Sánh Đa Chiều 8 Tiêu Chí Kỹ Thuật

| Tiêu chí | DOCX (Office Open XML) | PDF (Vector & Scanned) | Đánh giá cho RAG & Document AI |
| :--- | :--- | :--- | :--- |
| **1. Cấu trúc ngữ nghĩa & Thứ tự đọc** | **Xác định 100%:** Cây DOM XML xác định thứ tự đọc tuyến tính tự nhiên, không bị nhảy cột hay ngắt quãng bởi header/footer. | **Phức tạp:** Phải tính toán ma trận tọa độ $(x, y)$ hoặc dùng mô hình Layout/Vision để tái tạo thứ tự đọc; dễ nhảy đoạn giữa 2 cột. | DOCX vượt trội về độ tin cậy cấu trúc ngữ pháp và trích xuất quan hệ phân cấp. |
| **2. Bảng biểu phức tạp (Table Extraction)** | **Liên tục:** Bảng là ma trận liên tục, ô gộp ngang (`gridSpan`) và gộp dọc (`vMerge`) ghi rõ trong XML. Bảng 50 trang vẫn là 1 thực thể DOM duy nhất. | **Rất khó khăn:** Bảng bị chặt khúc qua các trang. Header lặp lại dễ bị nhầm thành hàng dữ liệu. Ô gộp dọc không viền rất dễ bị vỡ ma trận. | DOCX giữ trọn vẹn 2D matrix; PDF cần mô hình TableFormer hoặc TATR nặng nề và dễ sai sót. |
| **3. Phân cấp Tiêu đề (Headings)** | **Có sẵn trong Style:** Truy vấn trực tiếp từ thuộc tính `w:pStyle` (`Heading 1`, `Heading 2`) hoặc thuộc tính số mục thập phân. | **Heuristic/Thị giác:** Dựa trên kích thước font (font-size clustering), độ đậm chữ hoặc mô hình YOLO/LayoutLMv3; dễ nhầm Title và Header. | DOCX dễ dàng sinh cây AST định danh phân cấp tuyệt đối. |
| **4. Công thức toán học (Equations)** | **Nguyên bản nhị phân:** Lưu dưới dạng MathML (`m:oMath`) hoặc OLE Binary Object (`oleObject.bin` / MTEF của MathType). Giải mã xác định 0 token. | **Mất mát dữ liệu:** Lưu dưới dạng ảnh bitmap hoặc các vector glyph rời rạc. Bắt buộc dùng Vision-to-LaTeX OCR (như UniMERNet), dễ sai lệch chỉ số. | DOCX giải mã trực tiếp ra KaTeX chuẩn xác $100\%$. PDF có nguy cơ hallucination công thức. |
| **5. Độ nguyên vẹn ký tự (Text & Font)** | **Tuyệt đối:** Dữ liệu text luôn ở UTF-8 chuẩn xác, không có lỗi ánh xạ font lạ. | **Rủi ro:** Các file PDF cũ hay bị lỗi font TCVN3/VNI, lỗi font subset thiếu ToUnicode CMap, chữ bị đính dính (ligatures: fi, fl, ffl). | PDF vector cần lớp xử lý ToUnicode CMap và un-ligature; DOCX chạy thẳng. |
| **6. Chi phí & Tốc độ (Latency/Cost)** | **Siêu tốc:** Parsing bằng `python-docx` / `lxml` mất $\sim 5 - 20\text{ ms}$/tài liệu hàng trăm trang trên CPU đơn lõi. Không cần GPU. | **Tốn kém:** Chạy layout deep learning + OCR mất từ $0.5 - 5\text{ giây}$/trang, đòi hỏi GPU chuyên dụng (V100/A100/L4) hoặc Cloud API đắt đỏ. | DOCX tối ưu hóa chi phí ingestion hàng nghìn lần so với PDF Vision Pipeline. |
| **7. Tính toàn vẹn Pháp lý (Anchor of Trust)** | **Kém:** File DOCX dễ bị biên tập, chỉnh sửa nội dung, không có chữ ký số hoặc mộc đỏ đóng dấu của cơ quan nhà nước. | **Tối thượng:** PDF Công báo quét hoặc ký số là căn cứ duy nhất được Tòa án, Viện Kiểm sát, Ban Thanh tra thừa nhận. | **PDF là Mỏ neo Pháp lý Bất biến (Legal Anchor of Trust).** |
| **8. Nguy cơ lỗi đặc thù (Failure Modes)** | Ảnh công thức đặt trên paragraph rỗng dễ bị parser bỏ qua; văn bản copy-paste thủ công bị lệch style XML. | Ảo giác thị giác (Vision Hallucination), cắt đôi bảng qua ngắt trang, mất footnote ở chân trang, đọc nhầm thứ tự văn bản đa cột. | DOCX cần validator cấu trúc; PDF cần visual verification loop. |

---

## 3. Khảo Sát & Đánh Giá 7 Framework Hàng Đầu Hiện Nay

```
       [Các Trường Phái Xử Lý Tài Liệu PDF Phức Tạp]
       
  1. Pure Geometric/Heuristic  --> PyMuPDF / PyMuPDF4LLM (Siêu tốc, CPU, không hallucination)
  2. Modular Vision Pipeline  --> Marker, Docling, Unstructured, MinerU (Cân bằng, chính xác cao)
  3. End-to-End Vision Model  --> Nougat (Meta) (ViT -> Text, chuyên Math, dễ lặp vòng lặp)
  4. GenAI Multimodal Agent   --> LlamaParse (Cloud, GPT-4V/Gemini Vision, chi phí cao)
```

### Ma Trận Năng Lực Kỹ Thuật Của 7 Framework

| Framework | Nhà phát triển | License | Engine Cốt Lõi | Xử lý Tiêu đề phân cấp | Bảng gộp ô & Đa trang | Công thức Toán học | Tốc độ / Yêu cầu Phần cứng | Trường hợp sử dụng tối ưu (Sweet Spot) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Docling** | IBM Research | MIT | DocLayNet + TableFormer | Rất tốt (AST Hierarchy) | Xuất sắc (TableFormer SOTA, nối đa trang) | Khá (Trích xuất ảnh & KaTeX plugin) | Trung bình (1-2s/trang trên GPU/CPU) | Bóc tách tài liệu doanh nghiệp, báo cáo kỹ thuật, RAG Pipeline hiện đại |
| **MinerU** | OpenDataLab | Apache-2.0 | LayoutLMv3 + UniMERNet + StructEqTable | Rất tốt (Đa ngôn ngữ) | Xuất sắc (TableMaster, bảng học thuật) | Xuất sắc nhất (UniMERNet LaTeX SOTA) | Trung bình-chậm (Cần GPU $\ge 8\text{GB}$) | Sách giáo trình, tiêu chuẩn kỹ thuật có dày đặc công thức phức tạp |
| **Marker** | Vik Paruchuri | GPL-3.0 | Surya OCR + Layout + Texify | Tốt (Surya reading order) | Tốt (Xuất Markdown table chuẩn) | Rất tốt (Texify ViT sang LaTeX) | Khá nhanh ($\sim 0.3-0.8\text{s}$/trang trên GPU) | Sách điện tử PDF, tài liệu khoa học, xuất Markdown sạch |
| **Nougat** | Meta AI | MIT | End-to-end Donut (Swin + mBART) | Trung bình (Không có cây AST phân cấp) | Khá (Tốt trên bảng ngắn, hỏng ở bảng dài) | Xuất sắc (Sinh mã LaTeX mượt mà) | Chậm ($\sim 2-5\text{s}$/trang, GPU bắt buộc) | Bài báo khoa học arXiv chuẩn 2 cột |
| **Unstructured** | Unstructured.io | Apache-2.0 | Detectron2/YOLOX + TATR + OCR | Tốt (Element-based Title tagging) | Tốt (TATR HTML Table) | Kém (Chỉ coi Math là ảnh hoặc Text thô) | Tùy chọn (Fast: rất nhanh; Hi-res: chậm) | Hệ thống Ingestion đa nguồn, gom cụm RAG Chunking tự động |
| **PyMuPDF4LLM**| Artifex Software | AGPL-3.0 | C-Engine MuPDF + Font Heuristics | Khá (Font histogram rule-based) | Khá (Tốt trên bảng có kẻ lưới rõ ràng) | Kém (Không chuyển đổi được KaTeX) | Siêu tốc ($< 10\text{ ms}$/trang, CPU nhẹ) | Tài liệu PDF vector chuẩn, cần tốc độ xử lý triệu trang với chi phí 0đ |
| **LlamaParse** | LlamaIndex | Proprietary | Cloud Multi-modal Agentic VLM | Xuất sắc (Prompt-guided context) | Xuất sắc (Đọc hiểu cả biểu đồ và bảng) | Tốt (Prompt chuyển LaTeX) | Phụ thuộc Cloud API latency ($\sim 2-4\text{s}$) | Tài liệu tài chính, biểu đồ, slide thuyết trình nội bộ doanh nghiệp |

---

## 4. Xu Hướng Kiến Trúc Lai Ghép (Dual-Engine Pipeline)

Cộng đồng công nghệ hàng đầu (như các đội ngũ kỹ sư tại Anthropic, OpenAI, LlamaIndex và IBM) đều đồng thuận rằng: **Không có một định dạng đơn độc nào giải quyết trọn vẹn cả hai chiều: Độ chính xác dữ liệu máy học (Machine Accuracy) và Giá trị pháp lý thị giác (Human Verification).**

```
                            [KIẾN TRÚC LAI GHÉP DUAL-ENGINE]
                            
   Tệp DOCX (Biên soạn/VIP)                           Tệp PDF Công Báo (Mộc đỏ)
              │                                                  │
              ▼                                                  ▼
     [DOCX Structure Engine]                           [PDF Visual Anchor Engine]
  - Python XML DOM / AST Parser                     - SHA-256 Hash Invariant
  - Deterministic 2D Table Matrix                   - PyMuPDF / Visual Layout Detector
  - MTEF Binary Formula Decoder                     - Page Image Renderer (DPI 300)
              │                                                  │
              └───────────────────────┬──────────────────────────┘
                                      ▼
                      [GATE 0: CROSS-VERIFICATION ENGINE]
                   - Text Parity Rate (Levenshtein >= 98.5%)
                   - Heading/Chapter Hierarchy Alignment
                   - AI Vision Table Spot-Check (Cell values)
                                      │
                                      ▼
                      [AST KNOWLEDGE GRAPH + PROVENANCE]
                   - Atomic Normative Nodes (Điều/Khoản/Mục)
                   - KaTeX Standardized Formulas
                   - Explicit 2D HTML/Markdown Tables
                   - Spatial Provenance: {source_pdf_page, bbox, cong_bao_no}
```

### Hai Khái Niệm Chân Lý Tách Biệt:
1. **Structural Ground Truth (Chân lý Cấu trúc & Ký tự) $\rightarrow$ Đảm nhận bởi DOCX:**
   - Dữ liệu ký tự không bao giờ dính chữ (no ligatures), không lỗi font encoding.
   - Bảng dài 10–20 trang được bảo toàn thành ma trận 2D duy nhất, không bị phân mảnh bởi lề trang in.
   - Công thức toán học lưu ở dạng byte stream nhị phân (MTEF/MathML), cho phép giải mã toán học xác định.
2. **Spatial & Legal Ground Truth (Chân lý Không gian & Pháp lý) $\rightarrow$ Đảm nhận bởi PDF Công Báo:**
   - Là bằng chứng bất biến có dấu mộc đỏ, chữ ký lãnh đạo và số phát hành Công báo.
   - Định nghĩa số trang vật lý thực tế (`source_pdf_page`) mà thẩm định viên nhà nước yêu cầu khi thanh kiểm tra.
   - Định vị tọa độ hình học (`bbox`) của các sơ đồ, bản vẽ kỹ thuật.

---

## 5. Kinh Nghiệm & Best Practices Thực Chiến Từ Kỹ Sư AI / Data Engineering

1. **Nguyên tắc "Deterministic-First, Vision-Second" (Giải mã xác định trước, AI Vision sau):**
   - Không đẩy mù quáng toàn bộ trang qua Vision LLM (GPT-4V / Gemini) vì nguy cơ ảo giác số học và công thức ($f_{cd}$ bị nhầm thành $f_{ct}$, $\ge$ thành $\le$).
   - Ưu tiên bóc tách MTEF binary/MathML sang KaTeX ($<1\text{ ms}$, 0 token). AI Vision chỉ làm nhiệm vụ đối soát hoặc xử lý fallback ở các tệp scan.
2. **Kỹ thuật Atomic Legal Chunking (Phân đoạn quy phạm nguyên tử vs Fixed-token):**
   - Tuyệt đối không chunking cố định 500–1000 tokens (sẽ cắt đôi điều luật, làm mất điều kiện áp dụng ở nửa đầu).
   - Chunking theo Điều/Khoản/Mục và bắt buộc làm giàu ngữ cảnh bằng Context Breadcrumbs:
     `<!-- CONTEXT: QCVN 06:2022/BXD > Chương 3 > Điều 3.2 > Khoản 3.2.1 -->`
3. **Lan truyền Tiêu đề Cột (Header Propagation) & Table-Footnote Binding:**
   - Phẳng hóa tiêu đề đa tầng thành chuỗi phân cấp ngữ nghĩa (`[Địa hình > B > Hệ số k]: 1.15`) để LLM hiểu được ý nghĩa số liệu.
   - Chú thích chân bảng (Footnotes) là điều kiện biên quy phạm tối quan trọng, bắt buộc phải đóng gói gắn liền vào schema JSON của bảng (`table.footnotes: [...]`) hoặc đặt ngay sát cạnh bảng.
4. **Chuẩn hóa KaTeX Toàn cầu:**
   - Cô lập ranh giới từ Regex (tránh biến `\left[` thành `\le ft[`).
   - Dùng `\qquad (1)` thay cho `\tag{...}` bên trong các môi trường đa dòng (`aligned`, `cases`) để tránh lỗi render đỏ.
5. **Số hóa Đường cong Kỹ thuật thành Deterministic Solver:**
   - Không để AI Vision đoán pixel trên đồ thị tra cứu (sai số $5\% - 30\%$).
   - Số hóa toàn bộ đồ thị đường cong thành **Bảng CSV 2D rời rạc hóa** hoặc **Hàm số giải tích Python (Deterministic Numerical Solver)** để AI Agent gọi trực tiếp với độ chính xác $100\%$.
