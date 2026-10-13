---
request_id: "req-spoke-law135-knowledge-graph-001"
verdict: "APPROVE_WITH_CONDITIONS"
risk_score: 3.5
conditions:
  - "Bổ sung Sub-Gate 5.4 Referential Integrity Check trong scripts/validate_legal_spoke.py nhằm xác thực 100% ID văn bản và quy chuẩn khai báo trong các quan hệ mở rộng hiện diện hợp lệ trong legal_registry.yaml."
  - "Áp dụng nguyên tắc Single Source of Truth với quan hệ một chiều tại nguồn dữ liệu YAML, kết hợp cơ chế tự động biên dịch cạnh ngược (derived reverse edges) vào bộ nhớ trong quá trình build index."
  - "Triển khai phân tầng truy xuất RAG hai bước (Two-stage Semantic Routing): Bước 1 định tuyến theo Vành đai tri thức ở cấp Văn bản, Bước 2 trích xuất chính xác theo điều khoản từ clauses.json."
  - "Chuẩn hóa định danh cho Vành đai 4 (QCVN) và Vành đai 5 (Địa phương) đồng bộ tuyệt đối với khóa doc_id đã đăng ký trong Spoke."
effort: S
summary: "Kiến trúc Mạng tri thức 5 Vành đai giải quyết triệt để sự cô lập của Luật Xây dựng 135/2025/QH15, nâng cao độ chính xác khi định tuyến RAG và tư vấn pháp lý chuyên sâu. Đề xuất được phê duyệt có điều kiện, yêu cầu bổ sung cổng kiểm tra toàn vẹn tham chiếu CI và cơ chế tự động suy diễn cạnh ngược nhằm tối ưu hóa chi phí bảo trì theo ADR-0061."
telemetry:
  session_id: "f8c0dd2a-4aed-45a3-964a-5680c9c9c167"
  primary_model: "gemini-3.8-flash-high"
  input_tokens: 15225
  output_tokens: 3665
  reasoning_tokens: 1955
  total_tokens: 18890
  model_calls: 1
  turn_count: 1
  cost_usd: 0.025
  cost_mode: "estimated"
  duration_seconds: 49.8
---

# BÁO CÁO THẨM ĐỊNH ĐỐI KHÁNG KIẾN TRÚC (ARCHITECTURAL ADVERSARIAL AUDIT)

**Hồ sơ thẩm tra**: Thiết lập Mạng tri thức 5 Vành đai cho Luật Xây dựng 135/2025/QH15 & Mở rộng Schema quan hệ ngữ nghĩa  
**Mã yêu cầu**: `req-spoke-law135-knowledge-graph-001`  
**Chủ thể thẩm định**: Grok (Senior Systems & Legal Architecture Auditor)  
**Tiêu chuẩn đối chiếu**: ADR-0007 (Semantic Metadata Standard), ADR-0059 (Knowledge Graph Ingestion), ADR-0061 (KISS v2.0 & Reuse-First Architecture)

---

## 1. ĐÁNH GIÁ TỔNG QUAN VỀ MÔ HÌNH 5 VÀNH ĐAI PHÁP LÝ

Mô hình 5 Vành đai do Antigravity đề xuất phản ánh chính xác thực tế vận hành của hệ thống quy phạm pháp luật trong hoạt động đầu tư xây dựng tại Việt Nam:

1. **Vành đai 1 (Direct Enabling Framework)**: Luật số 135/2025/QH15 và hệ thống 7 Nghị định, 12 Thông tư hướng dẫn trực tiếp.
2. **Vành đai 2 (Sanctions & Enforcement)**: Cơ chế chế tài vi phạm hành chính (Nghị định 339/2026/NĐ-CP).
3. **Vành đai 3 (Interlocking Procedures & Cross-Domain Statutes)**: Thủ tục liên thông một cửa và các đạo luật nền tảng có hiệu lực đồng thời (PCCC, Quy hoạch, Đấu thầu, Đất đai, Nhà ở, Kiến trúc).
4. **Vành đai 4 (Mandatory Technical Codes - QCVN)**: Hệ thống quy chuẩn kỹ thuật quốc gia bắt buộc áp dụng trong hoạt động xây dựng.
5. **Vành đai 5 (Local Delegations & Sectoral Regulations)**: Quy định phân cấp chi tiết tại chính quyền địa phương và các Bộ chuyên ngành.

Việc thiết lập các quan hệ liên kết ngữ nghĩa giữa Luật 135 và 4 vành đai phụ trợ là bước đi cần thiết nhằm chuyển đổi dữ liệu từ dạng các kho lưu trữ độc lập (silos) sang đồ thị tri thức có khả năng điều hướng đa chiều.

---

## 2. PHÂN TÍCH ĐỐI KHÁNG 4 TRỤC TRỌNG TÂM

### Trục 1: Về Schema Design, Granularity & Hiệu Suất Hybrid RAG

#### Hiện trạng & Rủi ro ngữ cảnh
Khai báo quan hệ ngữ nghĩa ở cấp độ Toàn văn (Document Level) mang lại tính bao quát cao. Khi hệ thống RAG thực hiện tìm kiếm, việc nạp toàn bộ nội dung của các văn bản liên quan vào Context Window tiềm ẩn rủi ro làm loãng tín hiệu ngữ nghĩa (Semantic Drift) và vượt ngưỡng token cho phép của mô hình suy luận.

#### Giải pháp tối ưu hóa
- **Độ mịn phân cấp theo giai đoạn (Staged Granularity)**: Duy trì cấp độ Document Level trong `legal_registry.yaml` và `metadata.yaml` cho toàn bộ giai đoạn Phase 1 để đáp ứng yêu cầu phát triển nhanh và giữ cấu trúc gọn gàng theo ADR-0061.
- **Cơ chế Two-Stage Retrieval**:
  - *Giai đoạn 1 (Graph Ring Pruning)*: Dựa trên query của người dùng, phân loại vành đai liên quan (ví dụ: truy vấn về thẩm duyệt thiết kế sẽ kích hoạt Vành đai 1 + Vành đai 3 liên thông PCCC).
  - *Giai đoạn 2 (Clause Chunk Retrieval)*: Sử dụng bộ lọc metadata (`filter: { doc_id: { $in: [...] } }`) để thu hẹp không gian tìm kiếm vector xuống đúng tập tài liệu đã được định tuyến, sau đó trích xuất chính xác các chunk cấp Điều/Khoản từ `clauses.json`.
- **Lộ trình tinh chỉnh cấp Điều khoản (Article Level)**: Triển khai liên kết cấp Điều khoản trong Phase 2, tập trung duy nhất vào các giao điểm thủ tục trọng yếu (ví dụ: Điều khoản về Giấy phép xây dựng của Luật 135 liên kết trực tiếp với Điều khoản thẩm duyệt PCCC của Nghị định 105/2025/NĐ-CP).

---

### Trục 2: Tính Tất Định & Khả Năng Tương Thích CI Gates (`scripts/validate_legal_spoke.py`)

#### Tác động đối với mã nguồn CI hiện hành
Đoạn mã hiện tại của hàm `_get_replaces` và logic kiểm tra DAG trích xuất các thuộc tính cụ thể (`replaces`, `replaced_by`, `amends`, `compares`). Do trình phân tích cú pháp đọc dictionary thông qua phương thức `.get()`, các trường bổ sung (`enacted_by`, `sanctioned_by`, `interlocks_with`, `related_statutes`, `mandatory_codes`) hoàn toàn tương thích ngược và duy trì trạng thái 15/15 gates đạt chuẩn.

#### Bổ sung Sub-Gate 5.4: Referential Integrity Check
Nhằm ngăn ngừa hiện tượng tham chiếu rỗng (Dangling References) hoặc sai lệch mã định danh, hệ thống CI cần bổ sung cổng kiểm tra toàn vẹn tham chiếu bắt buộc:

1. **Phạm vi kiểm tra**: Toàn bộ các giá trị chuỗi khai báo bên trong các danh sách quan hệ mở rộng phải đối soát trực tiếp với tập hợp các `doc_id` hoặc mã văn bản đã đăng ký trong `legal_registry.yaml`.
2. **Quy tắc định danh**: Các mã định chuẩn như QCVN cần được chuẩn hóa định dạng (ví dụ: `QCVN 06:2022/BXD` phải trùng khớp với khóa định danh tài liệu tương ứng trong kho lưu trữ).
3. **Mức độ cưỡng chế**: Thiết lập trạng thái chặn tuyệt đối (Hard Block) tại CI Runner khi phát hiện bất kỳ định danh nào không tìm thấy nguồn gốc trong repo.

---

### Trục 3: Cấu Trúc Đồ Thị, Hướng Liên Kết & Nguyên Tắc KISS v2.0 (ADR-0061)

#### Đánh giá phương án lưu trữ hai chiều thủ công
Khai báo liên kết hai chiều thủ công (nhập tay quan hệ ngược tại từng tệp YAML của NĐ 339, NĐ 105, QCVN) làm gia tăng đáng kể nguy cơ lệch pha dữ liệu (Synchronization Drift). Khi một văn bản thay đổi hoặc được bãi bỏ, người quản trị phải chỉnh sửa đồng thời tại nhiều tệp phân tán, vi phạm nguyên tắc Đơn giản hóa kiến trúc (KISS v2.0).

#### Phương án kiến trúc đề xuất: Single Source of Truth & Dynamic Inversion
- **Khai báo tập trung (Centralized Forward Declaration)**: Khai báo toàn bộ các quan hệ hướng tâm xung quanh Luật 135 tại tệp `metadata.yaml` của chính Luật 135 và `legal_registry.yaml`.
- **Biên dịch cạnh ngược tự động (Automated Edge Inversion)**: Trong tiến trình xây dựng chỉ mục (Build Index Pipeline), module nạp dữ liệu sẽ tự động tính toán đồ thị hoán vị (Transpose Graph):
  - Khi Luật 135 có `sanctioned_by: [339/2026/NĐ-CP]`, bộ nhớ sẽ tự động gán nhãn `sanctions: [135/2025/QH15]` cho NĐ 339.
  - Khi Luật 135 có `interlocks_with: [105/2025/NĐ-CP]`, cạnh vô hướng hoặc cạnh đối ngẫu sẽ được tạo lập tức thời trong runtime.
- **Lợi ích**: Đảm bảo toàn vẹn dữ liệu, loại bỏ chi phí đồng bộ thủ công, bảo vệ tính tối giản của hệ thống tệp tĩnh.

---

### Trục 4: Đánh Giá Rủi Ro & Ma Trận Giảm Thiểu

- **Chỉ số rủi ro kiến trúc (Risk Score)**: **3.5 / 10** (Mức độ rủi ro thấp, hoàn toàn kiểm soát được).
- **Bảng phân tích rủi ro chi tiết**:

| Hạng mục rủi ro | Mức độ | Biện pháp kiểm soát & Giảm thiểu |
| :--- | :---: | :--- |
| **Lệch chuẩn định danh (ID Mismatch)** | Trung bình | Bổ sung Sub-Gate 5.4 kiểm tra toàn vẹn tham chiếu trong CI |
| **Nhiễu ngữ cảnh truy xuất RAG** | Trung bình | Ứng dụng mô hình lọc metadata theo Vành đai kết hợp trích xuất chunk điều khoản |
| **Gia tăng chi phí bảo trì liên kết** | Thấp | Khai báo một chiều tại nguồn dữ liệu, sinh cạnh ngược tự động bằng code |
| **Xung đột phiên bản CI hiện hành** | Rất thấp | Cấu trúc dictionary cho phép mở rộng tự nhiên không ảnh hưởng đến key kế thừa |

---

## 3. CÁC ĐIỀU KIỆN PHÊ DUYỆT BẮT BUỘC (APPROVAL CONDITIONS)

Đề xuất được phê duyệt triển khai khi đáp ứng đầy đủ 4 điều kiện kỹ thuật:

1. **Điều kiện 1 (CI Gate Enhancement)**: Hoàn thành tích hợp hàm `validate_semantic_relations_integrity()` vào tệp `scripts/validate_legal_spoke.py` trước khi nạp dữ liệu quan hệ mới.
2. **Điều kiện 2 (Standardized Naming Schema)**: Toàn bộ danh sách định danh trong `mandatory_codes` và `interlocks_with` phải sử dụng đúng định dạng ID chuẩn đã có trong `legal_registry.yaml` (hoặc khai báo tệp alias nếu có sự khác biệt về ký tự).
3. **Điều kiện 3 (Runtime Graph Builder)**: Triển khai tiện ích `build_bidirectional_legal_graph()` trong tầng Data Access Layer để suy diễn các cạnh ngược trong bộ nhớ, giữ nguyên tắc lưu trữ tĩnh một chiều.
4. **Điều kiện 4 (Scope Containment)**: Giữ nguyên vẹn toàn bộ cấu trúc trường `replaces` và DAG hiệu lực pháp lý hiện có để đảm bảo tính ổn định tuyệt đối của Sub-Gate 5.3.

---

## 4. LỘ TRÌNH TRIỂN KHAI KHUYẾN NGHỊ (ROADMAP)

### Phase 1: Mở Rộng Schema & Thiết Lập Cổng Toàn Vẹn CI (Thực hiện ngay)
1. Cập nhật mã nguồn `scripts/validate_legal_spoke.py`, bổ sung kiểm định tính toàn vẹn tham chiếu của các trường quan hệ mới.
2. Cập nhật schema trong `legal_docs/01_vbpl/luat_xay_dung_2025_135_2025_qh15/metadata.yaml` và `legal_registry.yaml` với cấu trúc quan hệ ngữ nghĩa đã đề xuất.
3. Chạy toàn bộ bộ kiểm thử 15 CI Master Gates để xác nhận tính toàn vẹn và mức độ tương thích.

### Phase 2: Nâng Cấp Tầng Truy Xuất RAG & Liên Kết Cấp Điều Khoản (Thực hiện tiếp theo)
1. Tích hợp metadata 5 vành đai vào engine tìm kiếm Hybrid RAG, triển khai cơ chế lọc trước (pre-filtering) theo vành đai tri thức.
2. Xác định các điểm giao cắt thủ tục trọng điểm (thẩm duyệt PCCC, cấp phép xây dựng, đánh giá năng lực nhà thầu) để thiết lập liên kết chéo cấp Điều khoản trong các tệp AST `clauses.json`.

---

## 5. THIẾT KẾ ĐẶC TẢ SUB-GATE 5.4 CHO CI VALIDATOR

Dưới đây là đặc tả logic kiểm định toàn vẹn tham chiếu cần bổ sung vào `scripts/validate_legal_spoke.py`:

```python
def validate_referential_integrity(registry: Dict[str, Any]) -> List[str]:
    """Sub-Gate 5.4: Kiểm tra tính toàn vẹn tham chiếu của các quan hệ ngữ nghĩa mở rộng.
    Đảm bảo mọi văn bản được liên kết đều hiện diện trong legal_registry.yaml.
    """
    errors = []
    registered_ids = set()
    
    # Tập hợp toàn bộ định danh hợp lệ trong registry
    for doc in registry.get("documents", []):
        if "id" in doc:
            registered_ids.add(str(doc["id"]).strip())
        if "number" in doc:
            registered_ids.add(str(doc["number"]).strip())

    semantic_relation_keys = [
        "enacted_by",
        "sanctioned_by",
        "interlocks_with",
        "related_statutes",
        "mandatory_codes"
    ]

    for doc in registry.get("documents", []):
        doc_id = doc.get("id", "UNKNOWN")
        rels = doc.get("relations", {})
        if not isinstance(rels, dict):
            continue

        for rel_key in semantic_relation_keys:
            target_list = rels.get(rel_key, [])
            if isinstance(target_list, str):
                target_list = [target_list]
            elif not isinstance(target_list, list):
                continue

            for target in target_list:
                cleaned_target = str(target).strip()
                if cleaned_target and cleaned_target not in registered_ids:
                    errors.append(
                        f"Lỗi toàn vẹn tham chiếu tại '{doc_id}': "
                        f"Quan hệ '{rel_key}' trỏ tới định danh không tồn tại '{cleaned_target}'"
                    )

    return errors
```

---

## 6. KẾT LUẬN THẨM TRỊ

Đề xuất kiến trúc của Antigravity có tính thực tiễn cao, phản ánh chính xác cấu trúc vận hành của pháp luật xây dựng thực tế và gia tăng đáng kể sức mạnh cho hệ thống Hybrid RAG và Agent Tư vấn. 

Grok chính thức phê duyệt phương án với hình thức **APPROVE_WITH_CONDITIONS**, khuyến nghị Antigravity triển khai ngay Phase 1 kèm theo Sub-Gate 5.4 nhằm duy trì chất lượng hệ sinh thái ở mức tuyệt đối.