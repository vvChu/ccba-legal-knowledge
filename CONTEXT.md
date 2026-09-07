# CCBA Legal Knowledge Spoke — Domain Context & Ubiquitous Language

Tài liệu này là Từ điển Thuật ngữ miền nghiệp vụ (Ubiquitous Language) của Spoke Tri thức Pháp lý CCBA (`ccba-legal-knowledge`). Mọi tài liệu kỹ thuật, bundle OKF, parser và AI Agent trong hệ thống phải tuân thủ nghiêm ngặt các định nghĩa này.

---

## 1. Thuật ngữ Văn bản Quy phạm Pháp luật (Legal Documents Domain)

- **Văn bản Gốc (Original Legal Document):** Toàn văn văn bản quy chuẩn, tiêu chuẩn hoặc luật/nghị định tại thời điểm ban hành lần đầu (ví dụ: `qcvn_06_2022_bxd.md` theo TT 06/2022/TT-BXD).
- **Văn bản Sửa đổi (Amending Document):** Văn bản pháp lý độc lập ban hành sau nhằm sửa đổi, bổ sung, bãi bỏ hoặc thay thế một số điều khoản của văn bản gốc (ví dụ: `sua_doi_1_2023_qcvn_06_2022_bxd.md` theo TT 09/2023/TT-BXD).
- **Văn bản Hợp nhất (VBHN - Consolidated Legal Text):** Văn bản kỹ thuật tích hợp đầy đủ toàn bộ nội dung sửa đổi, bổ sung vào thân văn bản gốc theo Pháp lệnh số 01/2012/UBTVQH13, phục vụ tra cứu thực thi nhanh (*Fast-RAG*) và thẩm tra thiết kế (ví dụ: `qcvn_06_2022_bxd_hop_nhat_2023.md`).
- **Truy nguyên Lịch sử (Provenance / Point-in-Time):** Khả năng truy vết chính xác từng câu chữ, điều khoản thuộc về văn bản ban hành nào tại từng mốc thời gian hiệu lực pháp lý.
- **Hành vi Lập pháp (Legislative Actions):** 4 hành vi can thiệp điều khoản quy chuẩn theo Nghị định 34/2016/NĐ-CP:
  - `modify` (Sửa đổi): Thay thế cụm từ, câu, đoạn hoặc giá trị số.
  - `add` (Bổ sung): Thêm điều, khoản, điểm, bảng biểu hoặc chú thích mới.
  - `repeal` (Bãi bỏ): Chấm dứt hiệu lực một phần hoặc toàn bộ điều khoản.
  - `replace` (Thay thế): Đổi toàn bộ nội dung của điều/khoản/bảng biểu bằng nội dung mới.

---

## 2. Thuật ngữ Cấu trúc & Kỹ thuật Dữ liệu (OKF & Data Architecture)

- **OKF Bundle (Open Knowledge Format v2.0):** Gói tri thức pháp lý đóng gói độc lập theo cấu trúc đường dẫn nông Cấp 1 (`legal_docs/`), bao gồm Markdown chuẩn hóa, thư mục bảng biểu (`tables/`), cây AST (`clauses.json`), bộ benchmark đối soát (`qa_benchmark.json`) và mục lục điều hướng (`index.md`).
- **Thẻ neo Canonical (Inlined Semantic Anchor):** Thẻ HTML `<a id="..." name="..."></a>` được nhúng trực tiếp trong dòng tiêu đề Markdown (`H1-H5`) để đảm bảo trình xem Markdown và trình duyệt tính toán đúng tọa độ Bounding Box khi cuộn liên kết.
- **CHÚ THÍCH (Table / Clause Note):** Nội dung quy chuẩn mang tính **bắt buộc tuân thủ (Normative)** theo TCVN 1-2:2008, đưa ra các ràng buộc kỹ thuật, điều kiện biên hoặc ngoại lệ áp dụng.
- **GHI CHÚ (Footnote / Remark):** Nội dung mang tính **hướng dẫn, tham khảo (Informative)**, không mang tính chế tài pháp lý bắt buộc.
- **Ma trận Ràng buộc Chú thích (Structured Footnote Binding Matrix):** Cấu trúc dữ liệu JSON biểu diễn ô bảng kỹ thuật có khả năng bóc tách giá trị số thực (*numeric value*), đơn vị đo (*unit*) và con trỏ điều kiện (*condition_refs*) gắn kết chặt chẽ với định danh Chú thích (*Footnote ID*).
- **Điều kiện Quy chuẩn Bắt buộc (Normative Condition):** Điều kiện tiên quyết được quy định trong Chú thích chân bảng mà công trình bắt buộc phải đáp ứng đồng thời để được áp dụng giá trị số tương ứng tại ô bảng đó.
- **Phụ lục Quy định (Normative Annex):** Phụ lục mang tính bắt buộc tuân thủ pháp lý theo Điều 7 TCVN 1-2:2008, có giá trị chế tài tương đương các điều khoản chính của quy chuẩn (`normative_status: "mandatory"`, `legal_enforceability: true`).
- **Phụ lục Tham khảo (Informative Annex):** Phụ lục chỉ mang tính hướng dẫn, minh họa hoặc ví dụ kỹ thuật (`normative_status: "informative"`, `legal_enforceability: false`), không được dùng làm căn cứ bắt lỗi vi phạm pháp quy.
- **Rào chắn Cưỡng chế Pháp lý (Legal Enforceability Guardrail):** Quy tắc trong AI QC Pipeline ngăn chặn tuyệt đối việc sinh mã lỗi sai phạm (*Defect/Violation*) dựa trên các nội dung thuần túy tham khảo.
- **Chỉ số phụ Đa tầng (Multi-index Footnote References):** Trường hợp ô dữ liệu hoặc tiêu đề mang đồng thời nhiều chỉ số tham chiếu (ví dụ: `1 400 <sup>2), 3)</sup>`), trong đó mỗi chỉ số đại diện cho một điều kiện kỹ thuật độc lập.
- **Ràng buộc Mảng Con trỏ (Structured Array Pointer Binding):** Mô hình cấu trúc hóa trong JSON AST phân tách các chỉ số phụ thành mảng con trỏ (`condition_bindings`) kèm toán tử logic (`evaluation_logic: "AND"/"OR"`), cho phép AI QC Agent kiểm tra tuần tự từng điều kiện tiên quyết.
- **Ghi chú Chỉ số Phụ (Item Footnotes Block):** Khối chú thích chân bảng (`_GHI CHÚ CHỈ SỐ PHỤ:_`) chuyên giải nghĩa các ký hiệu `1)`, `2)`, `a)`, `b)` gắn trực tiếp với từng ô dữ liệu riêng lẻ, tách biệt khỏi Chú thích chung của bảng.
- **Giao thức URI Pháp lý Ngữ nghĩa (Semantic Legal URI Scheme):** Chuẩn định danh liên kết độc lập vị trí vật lý theo cú pháp `legal://[doc_id]#[clause_id]`, giúp bảo vệ toàn vẹn các liên kết chéo giữa các văn bản quy chuẩn khác nhau.
- **Bộ Điều hướng Sổ đăng ký (Registry URL Router):** Cơ chế phần mềm ánh xạ tự động từ `legal://` URI sang đường dẫn file Markdown thực tế dựa trên siêu dữ liệu trong `legal_registry.yaml`.
- **Trạng thái Trì hoãn Liên kết (Pending Reference Fallback):** Cơ chế định tuyến an toàn về thẻ thông tin Registry khi văn bản đích được viện dẫn đang ở trạng thái thô (*raw/pending*) chưa được bóc tách sang Markdown, ngăn ngừa lỗi liên kết hỏng (*Broken Links*).
- **Thứ bậc Hiệu lực Pháp lý (Legal Precedence Hierarchy):** Trật tự ưu tiên áp dụng khi thẩm tra thiết kế theo nguyên tắc `Luật > Nghị định > QCVN > TCVN`, bảo đảm quy chuẩn bắt buộc luôn có giá trị pháp lý cao hơn tiêu chuẩn tự nguyện.
- **Nguyên tắc Văn bản Sau (Lex Posterior):** Quy tắc pháp lý áp dụng văn bản mới ban hành thay thế văn bản cũ có cùng cấp hiệu lực (ví dụ: Nghị định 217/2026/NĐ-CP thay thế Nghị định 175/2024/NĐ-CP).
- **Lỗi Vi phạm Cốt tử (Critical Defect):** Nhãn lỗi mức độ cao nhất do AI QC Agent gán khi hồ sơ thiết kế vi phạm trực tiếp các điều khoản bắt buộc của Luật, Nghị định hoặc QCVN mà không có điều kiện giảm trừ.
- **Khuyến nghị Thuyết minh (Verification Required Notice):** Nhãn cảnh báo vàng yêu cầu tư vấn thiết kế cung cấp bản tính toán thuyết minh kỹ thuật tương đương khi áp dụng các ngoại lệ mà QCVN cho phép mở.
- **Rào chắn Kiểm thử Kép (Dual-Layer CI Verification Gate):** Cơ chế cưỡng chế chất lượng 2 lớp (Local Pre-Commit Hook + Remote GitHub Actions Workflow) bảo đảm mọi tài liệu pháp lý mới đều phải vượt qua $100\%$ các bài kiểm toán cấu trúc, thẻ neo, ma trận bảng và độ nguyên vẹn dữ liệu.
- **Cổng Kiểm soát Không Khoan nhượng (Zero-Tolerance Quality Gate):** Chính sách cấm merge mã/dữ liệu vào nhánh chính `main` nếu tồn tại dù chỉ 1 lỗi định dạng, 1 liên kết hỏng hoặc tỷ lệ Parity < 100%.
- **Động cơ Tra cứu Theo Thời gian (Temporal Legal Query Engine):** Mô-đun phân giải tri thức pháp lý tự động dựa trên tham số ngày căn cứ thiết kế (`design_date`), cấp phát chính xác phiên bản quy chuẩn có hiệu lực tại mốc lịch sử đó (*Time-Travel RAG*).
- **Mốc Căn cứ Thiết kế (Design Base Date):** Ngày cấp giấy phép quy hoạch, thẩm duyệt PCCC cơ sở hoặc ngày ký hợp đồng tư vấn thiết kế dùng làm mốc xác định hiệu lực của các quy chuẩn, tiêu chuẩn áp dụng cho công trình.
- **Khoảng Thời gian Hiệu lực (Effective Temporal Interval):** Thuộc tính dữ liệu (`effective_from` $\rightarrow$ `effective_to`) xác định chu kỳ sống pháp lý của từng điều khoản và từng ấn bản quy chuẩn trong `legal_registry.yaml`.
- **Bộ SDK Tri thức Pháp lý (`ccba-legal-sdk`):** Gói thư viện Python chuẩn hóa đóng gói trên Hub (`packages/ccba-legal-sdk`), cung cấp giao diện lập trình kiểu an toàn (*Type-Safe*) cho toàn bộ các dịch vụ AI Agent trên nền tảng CCBA truy xuất điều khoản, bảng số liệu và ma trận ràng buộc điều kiện.
- **Giao diện Truy vấn Nguyên tử (Atomic Table Matrix Lookup API):** Phương thức truy vấn ô bảng kỹ thuật trong SDK cho phép trích xuất độc lập giá trị số học đo lường và danh sách điều kiện quy chuẩn bắt buộc đi kèm.
- **Đóng gói Nguyên tử Cả Điều Khoản (Atomic Clause Chunking - ADR 0011):** Chiến lược phân đoạn dữ liệu RAG trong đó toàn bộ nội dung của một Mục/Điều khoản lớn (bao gồm các điểm `a, b, c...`, gạch đầu dòng `+` và các ý con lồng đa tầng) được bảo toàn nguyên khối trong 1 Document Chunk duy nhất, triệt tiêu rủi ro đứt lìa câu định mức con khỏi câu điều kiện tiên quyết của cấp cha.
- **Danh mục Lồng Đa Tầng (Nested Multi-level Lists):** Cấu trúc phân cấp văn bản quy chuẩn (Điều $\rightarrow$ Khoản/Điểm $\rightarrow$ Gạch đầu dòng `+` $\rightarrow$ Ý con `  -`) tuân thủ nghiêm ngặt quy tắc thụt lề 2 spaces của CommonMark để bảo toàn cây cú pháp AST cho các mô hình AI Vision và RAG Embedding.
- **Kho Tri thức Chuẩn hóa Hiện hành (Clean Unified Repository - ADR 0012):** Bộ dữ liệu 34 nguồn Markdown được chọn lọc nghiêm ngặt phục vụ nạp lên Google NotebookLM và AI Gateway, bao gồm toàn bộ văn bản pháp luật hiện hành, các bản quy chuẩn hợp nhất mới nhất và bảng so sánh thay đổi, loại trừ các bản gốc cũ để bảo đảm 100% độ chính xác thời gian.
- **Rào chắn Ngăn chặn Bản Cũ (Obsolete Source Quarantine Gate):** Cơ chế lọc tự động trong pipeline đồng bộ ngăn không cho các tệp bản gốc cũ và bản sửa đổi rời rạc bị đẩy lên các không gian tìm kiếm RAG hiện hành.
- **Cổng Kiểm Toán Ân Hạn Động (Dynamic Grace Period Compliance Gate - ADR 0013):** Cơ chế phân loại mức độ lỗi kiểm toán tự động theo thời gian (`audit_date`), tự động gán nhãn Cảnh báo vàng trong thời hạn ân hạn chuyển tiếp (ví dụ: 6 tháng từ 15/12/2026 đến 15/06/2027 cho chung cư hiện hữu) và tự động leo thang lên Lỗi đỏ vi phạm bắt buộc sau khi hết hạn chót.
- **Thời hạn Ân Hạn Chuyển Tiếp (Grace Period):** Khoảng thời gian theo luật định cho phép đối tượng áp dụng (công trình hiện hữu) được duy trì trạng thái cũ trong khi chuẩn bị và hoàn thành phương án cải tạo, thích ứng theo quy chuẩn mới.
- **Phân Định Thẩm Quyền Thẩm Định PCCC (Split Jurisdiction - ADR 0014):** Cơ chế phân luồng thẩm tra thiết kế theo Luật 55/2024/QH15 và Nghị định 105/2025/NĐ-CP, trong đó Cơ quan Chuyên môn về Xây dựng (CQXD) thẩm tra phần Kiến trúc/Khói/Ngăn cháy lan, Cơ quan Công an (PC07) thẩm định phần Cơ điện PCCC/Báo cháy/Chữa cháy tự động, và Chủ đầu tư tự thẩm tra theo phân cấp công trình.
- **Siêu Dữ Liệu Thẩm Quyền (Jurisdiction Metadata):** Thuộc tính định tuyến trong AST `clauses.json` (`jurisdiction: 'CQXD' | 'CONG_AN' | 'CHU_DAU_TU_TU_THAM_DINH'`) cho phép AI QC Agent tự động phân tách kết quả audit thành các bộ hồ sơ nộp cơ quan chức năng độc lập.
- **Thẻ Siêu Dữ Liệu Tra Cứu (Metadata Stub Card - ADR 0015):** Thẻ thông tin tự động hiển thị khi người dùng/Agent truy cập một liên kết `legal://` trỏ đến văn bản chưa được số hóa Markdown, cung cấp thông tin xuất xứ, cơ quan ban hành, hiệu lực và nút mở trực tiếp file PDF gốc.
- **Suy Luận Đồ Thị Đa Tài Liệu (Cross-Document Graph Traversal):** Khả năng của AI Agent tự động lần theo các liên kết `legal://` giữa các quy chuẩn và tiêu chuẩn để xây dựng chuỗi lập luận pháp lý logic hoàn chỉnh mà không bị đứt đoạn bởi các tài liệu chưa bóc tách.
- **Động cơ Vá Cấu Trúc Cây Cú Pháp (AST Structural Patching Engine - ADR 0017):** Cơ chế phần mềm tự động hóa việc tạo ra văn bản hợp nhất toàn văn và ma trận đối chiếu bằng cách áp dụng các lệnh thao tác ngữ nghĩa xác định (`REPLACE_CLAUSE`, `INSERT_CLAUSE`, `REPEAL_CLAUSE`, `SUBSTITUTE_PHRASE`) lên cây AST của văn bản gốc, loại bỏ hoàn toàn rủi ro ảo giác của LLM.
- **Thẻ Hành Động Lập Quy (Semantic Action Tokens):** Tập hợp các lệnh thao tác nguyên tử chuẩn hóa đại diện cho các thay đổi hành chính trong văn bản sửa đổi bổ sung của pháp luật Việt Nam.
- **Kiến Trúc Lưu Trữ Tri Thức Kép (Dual-Store Knowledge Topology - ADR 0018):** Mô hình phân phối dữ liệu song hành: lưu trữ văn bản Markdown sạch trên Google NotebookLM để con người tương tác/nghiên cứu ngữ cảnh lớn, kết hợp lưu trữ cây AST `clauses.json` và Vector DB trên Server Spark (:8090) để AI QC Pipeline quét tự động tốc độ cao.
- **Khóa Phiên Bản Đồng Bộ (Sync Version Lock):** Cơ chế đối soát mã băm `commit_sha` giữa Git Remote, NotebookLM và Server Spark nhằm bảo đảm mọi kết luận kiểm toán AI QC đều dựa trên phiên bản quy chuẩn pháp lý mới nhất đang có hiệu lực.
- **Biên Bản Tự Thẩm Định PCCC (PCCC Self-Audit Affidavit - ADR 0019):** Văn bản pháp lý do AI QC Engine tự động kết xuất theo thể thức quy định của Nghị định 105/2025/NĐ-CP và Luật 55/2024/QH15, bao gồm ma trận đối soát quy chuẩn, danh mục sai sót, mã băm SHA-256 của tập bản vẽ và khối ký số điện tử của Chủ đầu tư/Tư vấn thẩm tra.
- **Chế Độ Kiểm Toán Phân Hạng (Tiered Audit Persona):** Cơ chế lọc quy định và tạo lập hồ sơ đa luồng trong AI QC Pipeline (`MODE_CQXD`, `MODE_PC07`, `MODE_CDT_SELF_AUDIT`), cho phép tạo ra các bộ báo cáo chuyên biệt phù hợp với thẩm quyền của từng cơ quan quản lý hoặc nhu cầu lưu trữ nội bộ của dự án.
- **Động Cơ Tính Toán Công Thức Kỹ Thuật Lai Ghép (Hybrid Symbolic Formula Solver Engine - ADR 0020):** Kiến trúc phân tách nhiệm vụ: LLM/AI Vision trích xuất các biến số đầu vào từ bản vẽ; Python engine trong `formulas/` thực thi phép tính số học xác định $100\%$ theo đúng công thức quy chuẩn, triệt tiêu hoàn toàn lỗi tính nhẩm của AI.
- **Mã Định Danh Công Thức (Formula ID / Symbolic Reference):** Nhãn định danh duy nhất (ví dụ: `F_FIRE_WATER_Q06`) gắn kết công thức LaTeX trong văn bản Markdown OKF với hàm Python tính toán tương ứng trong thư viện `formulas/`.
- **Thân Văn Bản Quy Phạm Thuần Khiết (Pure Normative Body - ADR 0021):** Định dạng Markdown chuẩn hóa chỉ chứa nội dung quy phạm pháp luật cốt lõi (từ Chương I đến Điều cuối cùng), loại bỏ hoàn toàn các rác layout hành chính (Quốc hiệu, Tiêu ngữ, Căn cứ thô, Nơi nhận, Chữ ký giấy) để phục vụ nhúng vector không nhiễu (*Noise-Free RAG Embedding*).
- **Đồ Thị Căn Cứ Pháp Lý Có Cấu Trúc (Structured Legal Knowledge Graph - `legal_basis` - ADR 0021):** Mô hình cấu trúc hóa các căn cứ ban hành luật thành mảng đối tượng có liên kết `doc_id` trong `metadata.yaml` và YAML Frontmatter, hỗ trợ AI Agent suy luận bắc cầu đa tài liệu (*Multi-Hop Legal Graph Reasoning*).
- **Kiến Trúc Tách Module Biểu Mẫu Độc Lập (Modular Form Templates Architecture - ADR 0021):** Mô hình phân tách toàn bộ Phụ lục biểu mẫu hành chính thành các tệp Markdown độc lập trong thư mục `templates/` có placeholders `{{ ... }}`, tuân thủ nguyên tắc Một nguồn sự thật (*Single Source of Truth - DRY*).
- **Bộ Lọc Phân Loại Bảng Biểu 3 Lớp (3-Tier Semantic Table Classifier - ADR 0021):** Động cơ Heuristic tự động phân biệt giữa Khung layout Word (bỏ qua), Bảng ma trận dữ liệu tra cứu kỹ thuật (`tables/`), và Biểu mẫu điền thông tin (`templates/`).
- **Kiểm Toán Toàn Vẹn Phân Tán (Distributed Parity Audit Formula - ADR 0021):** Phương pháp đo lường độ bảo toàn dữ liệu bằng tổng hợp thể tích văn bản trên toàn bộ các module phân tán (`Main .md + Templates + Tables`) đối soát với file gốc.

---

## 3. Thuật ngữ Hạ tầng Xe Điện & PCCC Nhà Chung Cư (EV & Fire Safety Domain)

- **Nhà chung cư hiện hữu (Existing Apartment Building - Điều 1.4.31):** Nhà chung cư đã được nghiệm thu, đưa vào sử dụng theo quy định của pháp luật về xây dựng trước ngày Thông tư 31/2026/TT-BXD có hiệu lực thi hành (15/12/2026).
- **Khu vực sạc xe điện (EV Charging Area - Điều 1.4.32):** Khu vực có chức năng chuyên để sạc xe điện, gồm một hoặc nhiều chỗ sạc được bố trí tập trung, được trang bị hệ thống cấp điện, thiết bị sạc, ngắt điện khẩn cấp và các biện pháp an toàn bắt buộc (hút khói cưỡng bức, cảm biến khí CO/HF, hệ thống chữa cháy tự động).
- **Chỗ sạc (EV Charging Bay - Điều 1.4.33):** Vị trí đỗ dành cho một xe để thực hiện sạc điện.
- **Khu vực đổi pin (Battery Swapping Station - Điều 1.4.34):** Khu vực lắp đặt tủ đổi pin cho xe mô tô điện, xe gắn máy điện, xe đạp điện, nơi pin có thể hoán đổi với giới hạn dung lượng lưu trữ nghiêm ngặt: $\le 100\text{ kWh}$ ngoài trời, $\le 35\text{ kWh}$ trên mặt đất, $\le 18\text{ kWh}$ tầng hầm/bán hầm.
- **Khoang cháy Khu vực Sạc (Dedicated Charging Fire Compartment - Điều 2.10.2.1):** Khoang cháy chuyên dụng ngăn cách bằng tường loại 1 hoặc khoảng trống $\ge 6\text{ m}$ (hoặc dải màn nước Drencher kép lưu lượng $1\text{ l/s/m}$), diện tích tối đa $\le 1.500\text{ m}^2$ trên mặt đất hoặc $\le 1.200\text{ m}^2$ trong tầng bán hầm/tầng hầm.
- **Thời hạn Rà soát 6 Tháng (6-Month Compliance Review Period - Điều 2.2 TT 31/2026):** Thời hạn bắt buộc đến ngày 15/06/2027 để toàn bộ các chung cư hiện hữu hoàn thành việc rà soát an toàn PCCC, phân vùng chỗ để xe điện hoặc tiến hành cải tạo công trình theo quy chuẩn.

---

## 4. Thuật ngữ Thu thập Tri thức & Xác thực Dữ liệu (Crawler & Provenance)

- **Cơ chế Cào TVPL 4 Lớp (4-Layer Precision TVPL Crawler):** Pipeline thu thập và đối soát tri thức pháp lý gồm:
  - *Lớp 1 (Định danh URL theo Doc ID):* Phân giải chính xác trang văn bản dựa trên mã định danh số nguyên của TVPL (loại bỏ lỗi rewrite URL).
  - *Lớp 2 (Đối soát Thuộc tính & Lược đồ):* Trích xuất số hiệu, ngày ban hành, cơ quan ban hành và cây quan hệ văn bản từ container `#divThuocTinh`.
  - *Lớp 3 (Kiểm tra Nhãn Hiệu lực):* Phát hiện và cảnh báo văn bản hết hiệu lực hoặc chưa có hiệu lực.
  - *Lớp 4 (Tải 3 Tầng Three-Tier):* Tải và tính toán mã băm SHA-256 bảo vệ tính xác thực tệp gốc.
- **Chiến lược Tải 3 Tầng (Three-Tier Download Fallback):** Cơ chế tìm kiếm và cấp phát file văn bản gốc:
  - *Tier 1:* Kho cục bộ (`.md/extracted_docs/` và `.md/data/cache/`).
  - *Tier 2:* Ổ đĩa chia sẻ / Google Drive API / AWS S3 Bucket.
  - *Tier 3:* Trực tiếp điều khiển Chrome CDP kết nối TVPL, vượt Cloudflare Turnstile và tự động đăng nhập tài khoản VIP.
- **Mã băm Tính Xác Thực (Authenticity SHA-256 Checksum):** Giá trị băm mật mã học được tính trực tiếp trên tệp `.docx`/`.doc` thật tải từ TVPL, lưu trữ bắt buộc trong `legal_registry.yaml` để làm bằng chứng kiểm toán pháp lý không thể chối cãi.
- **Mỏ Neo Pháp Lý Tối Thượng (Legal Anchor of Trust - ADR 0016):** Bản in PDF Công báo có dấu mộc đỏ và chữ ký số chính thức là cơ sở pháp lý cao nhất và duy nhất được công nhận khi giải trình với cơ quan quản lý nhà nước (Cảnh sát PCCC, Sở Xây dựng).
- **Mô hình Trích Xuất & Đối Soát Lai Ghép (Dual-Track Hybrid Model - ADR 0016):** Chiến lược kỹ thuật phân công: file DOCX dùng để trích xuất cấu trúc văn bản/bảng biểu/AST không bị ngắt trang; file PDF Công báo dùng làm mỏ neo kiểm định thị giác (Visual Ground Truth) và bằng chứng pháp lý bất biến.
- **Chiến Lược Nạp Toàn Diện Lên Cloud RAG (Full Comprehensive Cloud RAG Ingestion - ADR 0023):** Kiến trúc đồng bộ hóa 100% tài sản tri thức (Thân văn bản chính + Toàn bộ Biểu mẫu nguyên tử `templates/` + Bảng tra cứu `tables/`) vào 1 Single Unified NotebookLM duy nhất dựa trên hạn ngạch 500-600 nguồn của giấy phép Google AI Ultra, loại bỏ hoàn toàn sự phân mảnh tri thức.
- **Thẻ Viện Dẫn Nguồn Gốc Kép (Dual-Track Provenance Anchor - ADR 0024):** Cơ chế định dạng bắt buộc cho kết quả tra cứu RAG và báo cáo thẩm tra AI QC, trong đó thân câu trả lời là nội dung quy chuẩn hợp nhất mới nhất, nhưng luôn đính kèm mỏ neo chú thích trích dẫn cụ thể điều khoản gốc và số hiệu Thông tư ban hành văn bản sửa đổi.
- **Cổng Kiểm Định Nguồn Gốc Nghiêm Ngặt (Strict Provenance Enactment Gate - ADR 0025):** Rào chắn CI Gate tự động từ chối và chặn đứng mọi văn bản quy phạm pháp luật nạp vào hệ thống nếu thiếu tệp nguồn nhị phân gốc (`.docx`/`.pdf`) hoặc mã băm SHA-256 đối soát từ các cơ quan ban hành chính thức.
- **Phân Phối Tri Thức Qua Gói SDK (Package-Based Knowledge Distribution - ADR 0026):** Mô hình kiến trúc phân định Producer-Consumer giữa Spoke Tri thức (chuyên sản xuất, chuẩn hóa và kiểm định dữ liệu OKF v2.2) và Hub Nền tảng (đóng gói Python Package `ccba-legal-intel` cung cấp API kiểu an toàn cho các downstream agents).

---

## 5. Thuật ngữ Quản trị Hành vi Agent (Agent Behavior Governance — ADR 0032)

- **Cổng Tra Cứu Catalog (Catalog Query Gate - ADR 0032):** Cơ chế cưỡng chế Reuse-First hai lớp, verify-based, được kích hoạt tự động khi agent chuẩn bị tạo code mới liên quan đến Hub capabilities. Chuyển từ mô hình trust-based (agent tự cam kết) sang verify-based (hệ thống kiểm chứng hành động thực tế).
- **Cổng Lập Kế Hoạch (Planning Gate):** Lớp 1 của Catalog Query Gate — kích hoạt một lần duy nhất khi agent nhận yêu cầu và chuẩn bị lập `implementation_plan.md`, bảo vệ *ý định* của agent ngay từ đầu luồng. Output bắt buộc được trích dẫn tường minh trong Implementation Plan.
- **Cổng Tiền Thực Thi (Pre-execution Gate):** Lớp 2 của Catalog Query Gate — kích hoạt ngay trước khi agent tạo file `.py` mới có chứa capability keywords (`fetch`, `crawl`, `convert`, `formula`, `harvest`, `embed`, `registry`...), bảo vệ *hành động thực tế* và chặn drift xảy ra giữa chừng khi thực thi.
- **Từ Khóa Năng Lực (Capability Keywords):** Tập hợp từ khóa Python được phân nhóm theo Hub capability (`fetch_group`, `convert_group`, `formula_group`, `registry_group`, `rag_group`) dùng làm trigger tự động cho Pre-execution Gate. Agent phải scan intent của code sắp viết so với danh sách này trước khi tạo file mới.
- **Ngoại Lệ Có Biên Bản (BYPASS):** Trạng thái kết quả của Catalog Query Gate khi agent xác định Hub tool đã tồn tại nhưng không đáp ứng đủ scope hiện tại. Agent được phép tiếp tục nhưng **bắt buộc** ghi lý do vào `.md/logs/catalog_gate_audit.jsonl`. BYPASS không yêu cầu phê duyệt người dùng nhưng tạo Bypass Debt.
- **Nợ Ngoại Lệ (Bypass Debt):** Số lần BYPASS tích lũy theo thời gian — chỉ số đo mức độ Hub catalog còn thiếu so với nhu cầu thực tế của agent. Bypass Debt > 5 là tín hiệu cần mở rộng Hub catalog, không phải tín hiệu agent sai.
- **Tỷ Lệ Kích Hoạt Cổng (Hit Rate):** Tỷ lệ `(PASS + BLOCK) / total_ops` — đo xem Gate có đang được agent thực sự chạy không. Hit Rate < 80% là dấu hiệu Gate bị bỏ qua.
- **Tỷ Lệ Chặn (Block Rate):** Tỷ lệ `BLOCK / (PASS + BLOCK)` — đo tần suất agent drift khỏi Hub tools. Block Rate > 20% là dấu hiệu agent đang có xu hướng tái tạo code đã có sẵn trong Hub.

---

## 6. Thuật ngữ Kiến trúc Nâng cao & Quy Chuẩn Hiện Đại (ADR 0033 - ADR 0042)

- **Vệ Sinh & Lưu Trữ Thư Mục .md (Directory Hygiene & Archiving - ADR 0033):** Quy chuẩn cấu trúc thư mục `.md/`: cấp gốc chỉ lưu config tối thượng; toàn bộ tài liệu nguồn chuyển vào `.md/extracted_docs/`, scripts thử nghiệm đưa vào `.md/archive/`.
- **Mô Hình Quy Chuẩn Kỹ Thuật Động Cơ Kép (OKF v2.3 Dual-Engine - ADR 0034):** Tiêu chuẩn chuyển đổi TCVN/QCVN tự động nhận diện công thức KaTeX đa dòng và dựng bảng ma trận GFM 2D phức tạp qua `TableMatrixBuilder`.
- **Kho Nhị Phân Đám Mây 3 Tầng & Native Google Docs (Tri-Tier Cloud Binary Vault - ADR 0035):** Kiến trúc lưu trữ tài sản nhị phân nặng (.pdf, .docx) trên Google Drive `CCBA_Legal_Vault`, tự động chuyển đổi sang Native Google Docs sẵn sàng nạp 1-click vào NotebookLM.
- **Đặc Tả Tri Thức Hướng Agent Toàn Cầu (OKF v2.4 Universal Agent-Centric - ADR 0036):** Tiêu chuẩn 5 Invariants: Universal `sources/`, phân tách 4 ngăn kéo (`tables/`, `figures/`, `annexes/`, `templates/`), ma trận VBHN đồng vị, khai báo `source_assets` và giao thức Một Cửa `tab=7`.
- **Hiến Pháp Bảo Tồn Nguyên Văn Quy Phạm (Verbatim Normative Invariant - ADR 0037):** Cấm 100% việc dùng LLM tóm tắt/paraphrase thân văn bản pháp lý; bắt buộc trích xuất xác định 1:1 qua Python-docx AST parser và vượt qua Gate 11 DOCX Verbatim Parity Rate $\ge 98.0\%$.
- **Chuẩn Hóa Cú Pháp Toán Học KaTeX Toàn Cầu (Universal KaTeX Mathematical Syntax Integrity - ADR 0038):** Quy chuẩn bất biến cho công thức toán trong tiêu chuẩn kỹ thuật: bóc tách 100% MathType khối ảnh độc lập trên paragraph rỗng; cô lập ranh giới từ Regex bảo toàn cặp ngoặc `\left[`/`\right]`; dùng `\qquad (X)` trong môi trường đa dòng (`aligned`, `gather`, `cases`) thay cho `\tag` để triệt tiêu lỗi bôi đỏ KaTeX; và tách rời hoàn toàn chú thích hình ảnh khỏi dấu `$$`.
- **Bóc Tách Sơ Đồ Đồ Họa Độ Nét Cao & Bảo Tồn Tuyệt Đối Chú Thích Kẹp Giữa (High-Fidelity Diagram & Sandwiched Annotation Governance - ADR 0039):** Quét và trích xuất text/công thức từ bảng bố cục không viền 2 cột (Layout Diagram Table); bảo tồn 100% các đoạn `CHÚ THÍCH` và `CHÚ DẪN` kẹp giữa ảnh và tiêu đề hình; xếp dọc đa tầng (Vertical Stack) với lề an toàn $\ge 40\text{ px}$; và vượt qua Sub-Gate 11.2 Zero-Dropped Regulatory Notes.
- **Quy Trình Bóc Tách Đa Phương Thức Xác Định Toàn Cầu (Universal Deterministic Multimodal Extraction Pipeline - ADR 0040):** Kiến trúc bóc tách tri thức phi văn bản hợp nhất:
  - *Chuỗi Phân Tầng Công Thức 4 Lớp (4-Tier Formula Fallback Engine):* Pure-Python MTEF Binary Parser $\rightarrow$ Local CLI Fallback (Pandoc/LibreOffice) $\rightarrow$ AI Gateway Vision Harvester $\rightarrow$ `formulas_override.yaml` Ground Truth.
  - *Đồ Họa Kép Vector & Raster (Dual-Format Vector & Raster Pipeline):* Chuyển đổi vector WMF/EMF sang SVG (bảo toàn độ nét vô cực) kèm PNG độ phân giải cao $\ge 300\text{ DPI}$.
  - *Thẻ Thị Giác Tính Toán Tham Số Hóa (Visual Computation Cards - `figures/cards/`):* Decoupling giữa đồ họa tĩnh và thông số tính toán tra cứu, đăng ký tập trung tại `figures/figures_catalog.yaml`.
  - *Mô Hình Biểu Diễn Đường Cong Đa Tầng (Tiered Engineering Curve Representation):* Bảng CSV 2D rời rạc hóa hoặc Python Solver (ADR 0020) làm Chân lý Tối cao; cho phép AI Vision ước lượng ban đầu nhưng bắt buộc gán nhãn `confidence_status: "ESTIMATED_BY_VISION"` và kiểm chứng chéo hai chiều (Mutual Cross-Check).
  - *Cổng Kiểm Định Tài Sản Đa Phương Thức (Master CI Gate 12):* Cưỡng chế $0\text{ stray WMF}$, $100\%$ thẻ thị giác đầy đủ và phân loại nguồn gốc biểu đồ rõ ràng.
- **Kiến Trúc Bóc Tách Tri Thức Bảng Biểu Xác Định Toàn Cầu (Universal Deterministic Table Knowledge Extraction Architecture — ADR 0041):** Kiến trúc bóc tách dữ liệu bảng số liệu 2D chuẩn hóa: thiết lập lưới tọa độ ảo 2D (`tblGrid`); áp dụng Hierarchical Forward-Fill có kiểm soát cho các ô gộp dọc (`vMerge`) trong CSV/JSON; phẳng hóa tiêu đề đa tầng bằng Em-dash ngữ nghĩa (`Tầng 1 — Tầng 2 — Tầng 3`); bóc tách 100% chú thích chân bảng (`footnotes`) ra khỏi ma trận dữ liệu quan hệ; thoát an toàn ký tự pipe trong cell và KaTeX (`\vert `); định tuyến biểu mẫu hành chính sang `templates/`; và cưỡng chế ma trận CSV đạt chuẩn 100% Zero Ragged Rows (Gate 13).
- **Chuẩn Hóa Cấu Trúc OpenXML DOM & Động Cơ Lai Ghép DOCX-PDF Hai Tầng (Canonical OpenXML Sanitization & Hybrid Dual-Engine Architecture — ADR 0042):** Kiến trúc chuyển đổi hai pha hoàn toàn in-memory: Pha 1 tiền xử lý DOM qua `DocxCanonicalSanitizer` (gọt thuộc tính revision `w:rsid*`, loại bỏ `<w:proofErr>`, gộp run phân mảnh về chuẩn Unicode NFC, tiêm `xml:space="preserve"`, giải nén borderless layout tables thành văn xuôi phẳng, thăng cấp heading có cấu trúc) bảo tồn tuyệt đối whitelist `<w:object>`, `<m:oMath>`, `<w:drawing>`; Pha 2 kết hợp DOCX làm khung xương AST ngữ nghĩa phân cấp và PDF làm mỏ neo không gian kiểm chuẩn.
- **Quy Chuẩn Chuẩn Hóa Cấu Trúc OpenXML & Động Cơ Lai Ghép Bất Biến (Universal Canonical OpenXML Sanitization & Hybrid Dual-Engine Invariant — Invariant 14):** Nguyên tắc bất biến cưỡng chế toàn bộ tệp DOCX nạp vào hệ thống bắt buộc phải đi qua Pha 1 tiền xử lý in-memory của `DocxCanonicalSanitizer` trước khi parse AST; bảo tồn 100% khoảng trắng biên; unwrap triệt để bảng layout; không sinh CSV rác; và đạt chuẩn 15/15 Cổng Master CI Gate với 0 Errors và 0 Warnings.










