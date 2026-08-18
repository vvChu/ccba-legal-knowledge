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






