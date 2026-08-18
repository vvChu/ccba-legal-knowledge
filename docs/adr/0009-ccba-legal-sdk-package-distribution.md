# ADR 0009: Phân Phối Tri Thức Pháp Lý Qua Monorepo Package `ccba-legal-sdk`

- **Trạng thái:** Accepted (Đã chấp thuận)
- **Ngày quyết định:** 2026-08-18
- **Tác giả:** CCBA Legal Intelligence Architecture Team
- **Liên quan:** [ADR 0001: Dual-Track VBHN](0001-vbhn-dual-track-provenance.md), [ADR 0002: Structured Footnote Matrix](0002-structured-table-footnote-binding.md), [ADR 0008: Temporal Engine](0008-temporal-query-engine-point-in-time-auditing.md), [CONTEXT.md](../../CONTEXT.md)

---

## 1. Bối Cảnh (Context)
Spoke `ccba-legal-knowledge` chứa toàn bộ dữ liệu chuẩn hóa OKF v2.0 của các quy chuẩn xây dựng và PCCC. Trên Hub `ccba-agent-platform` và các Spoke dự án chuyên ngành, hàng loạt dịch vụ tự động hóa (như `ccba-ai-qc`, `bigbim-vbpl-digest`, `completion-checklist`) cần truy xuất và so khớp các điều khoản, bảng số liệu và điều kiện chú thích pháp lý.

Nếu để các tác vụ tự viết lại logic đọc file thô (`json.loads`, `re.search`):
1. **Phân mảnh mã nguồn:** Logic bóc tách điều kiện, xử lý chỉ số phụ và phân giải mốc thời gian sẽ bị trùng lặp ở hàng chục nơi.
2. **Thiếu an toàn kiểu dữ liệu (Type-Safety):** Dễ gây lỗi runtime khi schema thay đổi hoặc dữ liệu không đồng nhất.

---

## 2. Quyết Định Kiến Trúc (Decision)

Chúng tôi quyết định đóng gói toàn bộ logic truy vấn và bộ bóc tách dữ liệu thành package Python chính quy **`ccba-legal-sdk`** (cài đặt dạng editable qua Hub: `pip install -e packages/ccba-legal-sdk`):

1. **Giao Diện Lập Trình Thống Nhất (`Unified Python API`):**
   ```python
   from ccba_legal import legal

   # 1. Tra cứu điều khoản theo dòng thời gian (Point-in-Time)
   clause = legal.get_clause(
       doc_id="qcvn_06_2022_bxd",
       clause_id="1.1.2",
       design_date="2023-05-20"
   )
   print(clause.title, clause.content, clause.normative_status)

   # 2. Tra cứu bảng ma trận và điều kiện ràng buộc
   table = legal.get_table("bang_4")
   cell = table.lookup(fire_resistance="R120", component="cot_chiu_luc")
   print(cell.numeric_value, cell.unit, cell.condition_bindings)
   ```

2. **Cung cấp Type Hints & Pydantic Data Models:**
   - Định nghĩa các data model chuẩn hóa: `LegalClause`, `TableMatrix`, `TableCell`, `FootnoteBinding`, `TemporalInterval`.

3. **Tích hợp Sẵn CI Testing:**
   - Bộ SDK đi kèm test suite kiểm tra toàn vẹn dữ liệu từ các bundle OKF của Spoke.

---

## 3. Hệ Quả & Đánh Đổi (Consequences & Trade-offs)

### Tích cực:
- **Tái sử dụng triệt để (Reuse-First Gate):** Toàn bộ nền tảng CCBA chỉ sử dụng 1 SDK duy nhất để làm việc với dữ liệu pháp quy.
- **Tốc độ thực thi cực nhanh:** Bộ nhớ đệm (*In-memory Caching*) giúp các bài toán batch audit hàng trăm bản vẽ diễn ra trong tích tắc.
- **Trải nghiệm lập trình cao cấp:** Tự động hoàn thành code (IntelliSense) và kiểm tra lỗi tĩnh qua `mypy` / `ruff`.

### Đánh đổi:
- Cần đồng bộ phiên bản SDK khi có các cập nhật mới về schema hoặc quy chuẩn.
