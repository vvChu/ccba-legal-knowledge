# ADR 0027: Specialized AST Converter for QCVN & TCVN Standards

## 1. Trạng Thái (Status)
**ACCEPTED & ADOPTED** (2026-08-20)

## 2. Bối Cảnh (Context)
Các Quy chuẩn Kỹ thuật Quốc gia (QCVN) và Tiêu chuẩn Quốc gia (TCVN) trong ngành Xây dựng (như QCVN 02:2022/BXD, QCVN 06:2022/BXD, TCVN 2737:2023) có cấu trúc phân cấp phi chuẩn so với VBPL thông thường (Điều/Khoản/Điểm):
- Cấu trúc phân cấp số thập phân nhiều tầng: `1.1`, `1.1.1`, `A.1.2.3`.
- Các Phụ lục (Annexes) mang tính quy chuẩn bắt buộc chứa hàng trăm bảng số liệu tính toán phức tạp và đồ thị.

## 3. Quyết Định Thiết Kế (Decision)
1. **Phân tích Cú pháp AST Chuyên Biệt:** Bổ sung pipeline nhận diện cấu trúc tiêu chuẩn kỹ thuật đa cấp trong `docx_converter.py`.
2. **Neo Định Danh Cực Bộ (Atomic Anchors):** Mọi mục số phân cấp đều được gán anchor `#sec-x-y-z` để phục vụ tra cứu chính xác trong RAG.
3. **Phân Đoạn Quy Chuẩn Mô-đun (Modular Sections):** Tách thân quy chuẩn chính và các phụ lục lớn thành các tệp `.md` chuyên biệt để kiểm soát token.

## 4. Hệ Quả (Consequences)
- Đảm bảo 100% các tiêu chuẩn và quy chuẩn lớn được số hóa nguyên vẹn mà không bị tràn ngữ cảnh LLM.
