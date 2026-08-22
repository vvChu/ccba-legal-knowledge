# ADR 0024: Dual-Track Provenance with Footnote Anchor for Consolidated Legal Norms

- **Trạng thái:** ACCEPTED
- **Ngày quyết định:** 2026-08-22
- **Người đề xuất:** CCBA Legal Intelligence Team
- **Phạm vi:** Legal Query Engine, AI QC Pipeline, RAG Grounding Gate, OKF Bundles

---

## 1. Bối cảnh & Vấn đề (Context & Problem Statement)

Trong thực tiễn tư vấn xây dựng và thẩm duyệt pháp lý (Cảnh sát PCCC & CNCH, Cục Giám định Nhà nước về Chất lượng Công trình Xây dựng, Sở Xây dựng), một văn bản hợp nhất (VBHN) tuy cung cấp nội dung thực thi liền mạch nhưng **không có giá trị ban hành độc lập** về mặt chế tài pháp quy (theo Pháp lệnh 01/2012/UBTVQH13). Khi kỹ sư lập Thuyết minh Thiết kế hoặc giải trình thẩm duyệt, họ bắt buộc phải trích dẫn chính xác:
1. Số hiệu điều khoản trong Văn bản Quy chuẩn Gốc.
2. Số hiệu văn bản quy phạm pháp luật sửa đổi, bổ sung (Thông tư ban hành Sửa đổi).

Nếu hệ thống RAG chỉ trả về nội dung hợp nhất phẳng (Pure Fast-RAG), kỹ sư sẽ thiếu căn cứ viện dẫn chính thức. Ngược lại, nếu chỉ trả về các văn bản sửa đổi rời rạc, AI sẽ dễ rơi vào bẫy áp dụng các điều khoản cũ đã bị bãi bỏ hoặc sửa đổi từ ngữ.

---

## 2. Quyết định Thiết kế (Decision)

1. **Chuẩn Hóa Mô Hình Viện Dẫn Lai Ghép (Dual-Track Provenance with Footnote Anchor):**
   * Mọi câu trả lời tra cứu pháp lý, khuyến nghị kỹ thuật và báo cáo kiểm toán AI QC (`Defect Audit Report`) khi trích dẫn các điều khoản đã qua sửa đổi, bổ sung **bắt buộc** phải tuân thủ cấu trúc kép:
     - **Thân Quy chuẩn Thực thi (Normative Body):** Nội dung toàn văn đã được hợp nhất mới nhất.
     - **Mỏ neo Truy nguyên Nguồn gốc (Provenance Anchor):** Khối chú thích hoặc Callout đính kèm chỉ rõ:
       * Điều khoản gốc.
       * Văn bản sửa đổi, số Thông tư và ngày hiệu lực.
       * Hành vi lập pháp can thiệp (`sửa đổi`, `bổ sung`, `thay thế`, `bãi bỏ`).

2. **Quy Chuẩn Định Dạng Thẻ Viện Dẫn (Standardized Provenance Tag):**
   ```markdown
   > [!NOTE]
   > 🏛️ **Căn cứ Pháp lý Kép:** [Tên Quy chuẩn Gốc - Điều X] (Được [sửa đổi/bổ sung] theo Mục Y [Tên Văn bản Sửa đổi] - Ban hành kèm [Thông tư Z]).
   ```

3. **Tích Hợp Vào Cây AST `clauses.json`:**
   * Mỗi AST Node bị can thiệp bởi văn bản sửa đổi bắt buộc phải có thuộc tính:
     ```json
     {
       "clause_id": "dieu-2-6-3",
       "amendment_history": [
         {
           "amending_doc_id": "sua_doi_1_2023_qcvn_06_2022_bxd",
           "amending_circular": "09/2023/TT-BXD",
           "action": "replace",
           "effective_date": "2023-12-01"
         }
       ]
     }
     ```

---

## 3. Hệ quả & Đánh đổi (Consequences)

### Tích cực:
* ✅ Bảo vệ 100% tính hợp pháp cho Thuyết minh Thiết kế và Hồ sơ Giải trình Thẩm tra của kỹ sư CCBA.
* ✅ Triệt tiêu rủi ro áp dụng nhầm các câu từ cũ đã hết hiệu lực.
* ✅ Cung cấp khả năng truy vết lịch sử (Point-in-Time Traceability) tự động cho toàn bộ hệ thống.

---

## 4. Tham chiếu (References)
- [ADR 0001: VBHN Dual-Track Provenance](./0001-vbhn-dual-track-provenance.md)
- [ADR 0006: Legal Precedence Conflict Arbitration](./0006-legal-precedence-conflict-arbitration.md)
- [ADR 0017: AST Structural Patching Consolidation Engine](./0017-ast-structural-patching-consolidation-engine.md)
- [ADR 0021: OKF v2.2 Pure Normative Body & Legal Graph](./0021-okf-v2-2-pure-normative-body-legal-graph.md)
