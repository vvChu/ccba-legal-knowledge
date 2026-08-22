# ADR 0023: Full Comprehensive NotebookLM Ingestion Strategy for Ultra Tier

- **Trạng thái:** ACCEPTED
- **Ngày quyết định:** 2026-08-22
- **Người đề xuất:** CCBA Legal Intelligence Team
- **Phạm vi:** Cloud RAG Sync & Ingestion Architecture (`ccba-update-legal-registry`, NotebookLM API)

---

## 1. Bối cảnh & Vấn đề (Context & Problem Statement)

Trước đây, theo **ADR 0012**, do giả định hạn ngạch miễn phí của Google NotebookLM bị giới hạn ở mức tối đa **50 nguồn (Sources)** trên mỗi Notebook, hệ thống buộc phải áp dụng chiến lược *"Clean Unified Repository (Chỉ nạp 29 tệp Thân văn bản chính và Bảng so sánh)"*, cô lập hơn 90 Biểu mẫu nguyên tử (`templates/`) và hơn 100 Bảng tra cứu số liệu (`tables/`) ở máy cục bộ.

Khi người dùng tra cứu hoặc chất vấn trên giao diện Cloud RAG (NotebookLM) về chi tiết nội dung mẫu đơn hành chính (ví dụ: Mẫu số 01/BXD, Mẫu số 02/BXD), AI Cloud không thể trích xuất trực tiếp nguyên văn biểu mẫu.

---

## 2. Dữ liệu Đo Lường & Năng Lực Hạ Tầng Mới (Infrastructure Baseline)

Theo chính sách hạ tầng Google AI Ultra (Gemini Notebook / NotebookLM Enterprise):
- **Hạn ngạch Nguồn:** Cho phép nạp từ **500 đến 600 nguồn tài liệu độc lập** trên mỗi Single Notebook.
- **Giới hạn mỗi tệp:** Tối đa 500.000 từ (~200 MB) trên mỗi tệp nguồn.
- **Quy mô Kho Tri thức Spoke hiện tại:**
  - 26 tệp Thân văn bản quy phạm thuần khiết (`<slug>.md`)
  - 3 tệp Bảng đối chiếu so sánh (`bang_so_sanh_*.md`)
  - 90 tệp Biểu mẫu nguyên tử hành chính (`templates/`)
  - 105 tệp Bảng tra cứu kỹ thuật 2D (`tables/csv/`)
  - **Tổng cộng: ~224 sources** (chỉ chiếm ~40% dung lượng hạn ngạch 500 sources).

---

## 3. Quyết định Thiết kế (Decision)

1. **Thay thế Chiến lược Tinh giản bằng Chiến lược Nạp Toàn Diện (Full Comprehensive Ingestion):**
   * Cho phép đồng bộ **100% tài sản tri thức OKF v2.2** (Thân văn bản chính + Toàn bộ Biểu mẫu phụ lục + Bảng tra cứu kỹ thuật) vào **1 Single Unified NotebookLM duy nhất**.
2. **Cập nhật Bộ lọc Đồng bộ (`scripts/sync_to_notebooklm.py` & `/ccba-update-legal-registry`):**
   * Loại bỏ bộ lọc cách ly `templates/`, tự động quét và nạp toàn bộ các tệp `.md` trong thư mục `templates/` của 26 gói văn bản.
3. **Bảo tồn Khả năng Tra cứu Đa Chiều:**
   * Người dùng có thể hỏi đáp song song cả về căn cứ pháp lý, điều khoản quy định, số liệu bảng tra cứu và mẫu đơn biểu mẫu hành chính trong cùng một phiên hội thoại duy nhất mà không bị phân mảnh context.

---

## 4. Hệ quả & Đánh đổi (Consequences)

### Tích cực:
* ✅ Trải nghiệm hỏi đáp Cloud RAG đạt độ sâu 100% (Full Normative + Full Forms Coverage).
* ✅ Không cần quản lý phân tán nhiều Notebook (tránh rủi ro đứt gãy liên kết chéo).
* ✅ Tận dụng tối đa giá trị của gói bản quyền Google AI Ultra.

### Thách thức & Biện pháp kiểm soát:
* ⚠️ *Quản lý trùng lặp tên biểu mẫu:* Một số Thông tư có cùng tên biểu mẫu (ví dụ: `mau_01.md`).  
  *Giải pháp:* Tiền tố định danh nguyên tử theo chuẩn OKF v2.2 (ví dụ: `templates/phu_luc_01/mau_01_don_de_nghi_...md`) đã bảo đảm tính duy nhất tuyệt đối.

---

## 5. Tham chiếu (References)
- [ADR 0012: Clean Unified NotebookLM Ingestion Strategy](./0012-clean-unified-notebooklm-ingestion-strategy.md) *(Được cập nhật mở rộng bởi ADR này)*
- [ADR 0021: OKF v2.2 Pure Normative Body & Legal Graph](./0021-okf-v2-2-pure-normative-body-legal-graph.md)
