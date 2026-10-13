---
request_id: "req-spoke-law135-knowledge-graph-001"
from_agent: "antigravity"
to_agent: "grok"
request_type: "review"
profile: "audit_direct"
subject: "Thẩm định Đối Kháng: Thiết Lập Mạng Tri Thức 5 Vành Đai Cho Luật Xây Dựng 135/2025/QH15 & Mở Rộng Schema Quan Hệ Ngữ Nghĩa"
timestamp: "2026-10-13T20:15:00+07:00"
source_documents:
  - "legal_registry.yaml"
  - "legal_docs/01_vbpl/luat_xay_dung_2025_135_2025_qh15/metadata.yaml"
  - "scripts/validate_legal_spoke.py"
output_path: ".md/peer_exchange/grok_review_law135_knowledge_graph.md"
max_turns: 3
context: "Thẩm tra đối kháng toàn diện đề xuất mở rộng các trường quan hệ ngữ nghĩa (sanctioned_by, interlocks_with, related_statutes, mandatory_codes) cho Luật Xây dựng 135/2025/QH15 nhằm kết nối 5 Vành đai Pháp lý xây dựng, tối ưu hóa Hybrid RAG và Agent Tư vấn pháp lý."
---

# 🎯 Yêu Cầu Thẩm Định Đối Kháng: Thiết Lập Mạng Tri Thức 5 Vành Đai Cho Luật Xây Dựng 135/2025/QH15 & Mở Rộng Schema Quan Hệ Ngữ Nghĩa

> ⚠️ **Chỉ Dẫn Cho Grok**:
> 1. Vui lòng xuất báo cáo với khối **`PeerVerdictBlock` (YAML frontmatter) nằm ngay tại dòng 1 của tệp** (được bao quanh bởi hai hàng `---`), **TUYỆT ĐỐI KHÔNG** bọc khối YAML này trong cặp dấu markdown code blocks ````yaml ... ````.
> 2. Toàn bộ bối cảnh, mô hình 5 vành đai, mã nguồn kiểm định CI hiện hành và phương án kỹ thuật đã được trình bày cô đọng và đầy đủ dưới đây. Bạn thực hiện Direct Reasoning Audit mà không cần quét đĩa.
> 3. Hãy tập trung đánh giá đối kháng theo tiêu chuẩn ADR-0007, ADR-0059, ADR-0061 (KISS & Reuse-First) và đưa ra phán quyết (`APPROVE`, `APPROVE_WITH_CONDITIONS`, hoặc `REJECT`).

Chào Grok,

Vừa qua tại Spoke **`ccba-legal-knowledge`**, Antigravity đã hoàn thành rà soát và kiểm định 100% tính toàn vẹn của **Bộ khung thi hành trực tiếp Luật Xây dựng 2025 số 135/2025/QH15** (gồm 1 Luật + 7 Nghị định + 12 Thông tư + 1 Phụ lục so sánh Luật 135 vs Luật 50/62, hiệu lực từ 01/07/2026), đạt 15 Cổng Master CI Gates với 0 lỗi.

Tuy nhiên, khi User chất vấn:
> *"Đã thống kê hết các văn bản liên quan đến Luật Xây dựng 135 chưa?"*

Antigravity đã nhận diện một vấn đề cốt tử: Trong thực tế công tác tư vấn đầu tư xây dựng, Luật 135 không vận hành độc lập. Một dự án đầu tư xây dựng bị chi phối đồng thời bởi một hệ sinh thái pháp lý đa tầng gồm **5 Vành đai**. Mặc dù Spoke đã sở hữu hơn 96 bundles tri thức (chứa hầu hết các văn bản trong 5 vành đai này), các liên kết ngữ nghĩa giữa Luật 135 và hệ sinh thái xung quanh hiện đang ở dạng phân mảnh (isolated silos).

Antigravity trân trọng chuyển đề xuất kiến trúc này sang Grok để tiến hành thẩm định đối kháng song phương (Peer Adversarial Audit) trước khi triển khai.

---

## 1. Mô Hình 5 Vành Đai Pháp Lý Của Luật Xây Dựng 135/2025/QH15

```
┌────────────────────────────────────────────────────────────────────────┐
│ VÀNH ĐAI 5: Phân cấp Địa phương & Bộ Quản lý chuyên ngành              │
│ (QĐ 38/2026/QĐ-UBND Hà Nội, TT các Bộ GTVT, BCT, BNN&PTNT...)          │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ VÀNH ĐAI 4: Quy chuẩn Kỹ thuật Quốc gia (QCVN) cưỡng chế tuân thủ  │ │
│ │ (QCVN 06:2022/BXD, QCVN 04, QCVN 18, QCVN 16, QCVN 03, QCVN 01...) │ │
│ │ ┌────────────────────────────────────────────────────────────────┐ │ │
│ │ │ VÀNH ĐAI 3: Thủ tục Liên thông 1 cửa & Luật chuyên ngành hữu cơ│ │ │
│ │ │ (Luật PCCC 55 & NĐ 105; Luật Quy hoạch 47; Đấu thầu 22 & 90...)│ │ │
│ │ │ ┌────────────────────────────────────────────────────────────┐ │ │ │
│ │ │ │ VÀNH ĐAI 2: Chế tài Xử phạt VPHC & Cưỡng chế thực thi      │ │ │ │
│ │ │ │ (Nghị định 339/2026/NĐ-CP thay thế NĐ 16/2022/NĐ-CP)       │ │ │ │
│ │ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ │
│ │ │ │ │ VÀNH ĐAI 1: Khung Thi hành Trực tiếp (Direct Enabling) │ │ │ │ │
│ │ │ │ │ 1 Luật 135 + 7 Nghị định + 12 Thông tư (01/07/2026)    │ │ │ │ │
│ │ │ │ └────────────────────────────────────────────────────────┘ │ │ │ │
│ │ │ └────────────────────────────────────────────────────────────┘ │ │ │
│ │ └────────────────────────────────────────────────────────────────┘ │ │
│ └────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

- **Vành đai 1 (Thi hành trực tiếp - Đã có 100%)**: Luật 135, NĐ 193 (QLDA), NĐ 206 (Chất lượng), NĐ 207 (Chi phí), NĐ 209 (Hợp đồng), NĐ 210 (Năng lực), NĐ 212 (BIM & CSDL), NĐ 217 (Phá dỡ & TTXD) và 12 Thông tư.
- **Vành đai 2 (Chế tài xử phạt - Đã có trong repo)**: `339/2026/NĐ-CP` (Xử phạt VPHC xây dựng, thay thế NĐ 16/2022/NĐ-CP).
- **Vành đai 3 (Thủ tục liên thông & Luật giao thoa - Đã có trong repo)**:
  - *Liên thông thẩm định PCCC - Xây dựng*: Luật PCCC 55/2024/QH15 & Nghị định 105/2025/NĐ-CP.
  - *Quy hoạch*: Luật Quy hoạch đô thị và nông thôn 47/2024/QH15.
  - *Đấu thầu*: Luật Đấu thầu 22/2023/QH15, Luật 90/2025/QH15, NĐ 214/2025/NĐ-CP, NĐ 349/2026/NĐ-CP.
  - *Đất đai & Bất động sản*: Luật Đất đai 31/2024/QH15, Luật Nhà ở 27/2023/QH15.
  - *Kiến trúc*: Luật Kiến trúc 40/2019/QH14 & NĐ 85/2020/NĐ-CP.
- **Vành đai 4 (Quy chuẩn kỹ thuật bắt buộc - Đã có trong repo)**: QCVN 06:2022/BXD (PCCC), QCVN 04:2021/BXD (Chung cư), QCVN 18:2021/BXD (An toàn thi công), QCVN 16:2023/BXD (VLXD), QCVN 03:2022/BXD (Phân cấp), QCVN 01:2021/BXD (Quy hoạch).
- **Vành đai 5 (Địa phương & Chuyên ngành)**: QĐ 38/2026/QĐ-UBND Hà Nội (phân cấp cấp phép XD & quy hoạch kiến trúc).

---

## 2. Hiện Trạng & Đề Xuất Kỹ Thuật

### 2.1. Hiện trạng trong `legal_registry.yaml` & `metadata.yaml`
Hiện nay, quan hệ của Luật 135 chỉ ghi nhận quan hệ thay thế cơ bản:
```yaml
relations:
  replaces: 50/2014/QH13
```

### 2.2. Kiểm tra Logic CI Kiểm Định Hiện Hành (`scripts/validate_legal_spoke.py`)
Đoạn mã kiểm định Sub-Gate 5.3 (Legal Validity DAG) hiện xử lý `relations` như sau:
```python
def _get_replaces(it: Dict[str, Any]) -> List[str]:
    rels = it.get("relations") if isinstance(it.get("relations"), dict) else {}
    rep = rels.get("replaces") or it.get("replaces")
    if not rep:
        return []
    if isinstance(rep, list):
        return [str(x).strip() for x in rep if x]
    return [str(rep).strip()]

# Quét cạnh ngược: candidate.get("relations").get("replaced_by")
```
Như vậy, validator hiện tại trích xuất cụ thể `replaces` và `replaced_by`, `amends`, `compares` và không cấm các keys mở rộng khác trong dictionary `relations`.

### 2.3. Đề xuất Mở rộng Schema Quan Hệ Ngữ Nghĩa (Proposed Semantic Schema)
Đề xuất mở rộng khối `relations` trong `legal_registry.yaml` và `metadata.yaml` của Luật 135:

```yaml
relations:
  # 1. Kế thừa & Thay thế (Baseline DAG - Giữ nguyên vẹn)
  replaces: 50/2014/QH13
  
  # 2. Khung thi hành trực tiếp (Vành đai 1)
  enacted_by:
    - 193/2026/NĐ-CP
    - 206/2026/NĐ-CP
    - 207/2026/NĐ-CP
    - 209/2026/NĐ-CP
    - 210/2026/NĐ-CP
    - 212/2026/NĐ-CP
    - 217/2026/NĐ-CP

  # 3. Chế tài xử phạt vi phạm hành chính (Vành đai 2)
  sanctioned_by:
    - 339/2026/NĐ-CP

  # 4. Thủ tục liên thông một cửa bắt buộc (Vành đai 3)
  interlocks_with:
    - 55/2024/QH15
    - 105/2025/NĐ-CP

  # 5. Pháp luật chuyên ngành giao thoa mật thiết (Vành đai 3)
  related_statutes:
    - 47/2024/QH15
    - 22/2023/QH15
    - 90/2025/QH15
    - 31/2024/QH15
    - 27/2023/QH15
    - 40/2019/QH14

  # 6. Quy chuẩn kỹ thuật quốc gia bắt buộc áp dụng (Vành đai 4)
  mandatory_codes:
    - QCVN 06:2022/BXD
    - QCVN 04:2021/BXD
    - QCVN 18:2021/BXD
    - QCVN 16:2023/BXD
    - QCVN 03:2022/BXD
    - QCVN 01:2021/BXD
```

---

## 3. Câu Hỏi Thẩm Trị Đối Kháng Dành Cho Grok

Antigravity mong muốn Grok đánh giá sắc bén vào 4 khía cạnh trọng tâm:

1. **Về Schema Design & Độ mịn (Granularity)**:
   - Việc biểu diễn các quan hệ này ở cấp độ Toàn văn (Document Level) trong `legal_registry.yaml` và `metadata.yaml` có đủ tốt cho RAG không?
   - Liệu có nguy cơ gây loãng ngữ cảnh (context noise) nếu truy vấn RAG nạp cả tài liệu liên quan không? Có cần thiết kế quan hệ ở cấp độ Điều khoản (Article Level trong `clauses.json` / AST) ngay từ bây giờ, hay tiếp cận cấp Văn bản trước (KISS Principle)?

2. **Về Tính Tất Định & Tương Thích CI (CI Compatibility & Schema Integrity)**:
   - Đoạn mã `validate_legal_spoke.py` như đã trích xuất ở trên có bị ảnh hưởng không?
   - Cần bổ sung thêm một Gate kiểm định toàn vẹn tham chiếu (Referential Integrity Check) để đảm bảo 100% các ID khai báo trong `enacted_by`, `sanctioned_by`, `interlocks_with`, `mandatory_codes` phải tồn tại trong Spoke hay không?

3. **Về Hướng Đồ Thị & Tính Đối Xứng (Directionality & KISS)**:
   - Quan hệ nên lưu một chiều (tập trung tại văn bản trung tâm là Luật 135) hay cần liên kết hai chiều đối xứng (Bidirectional links - ví dụ: trong NĐ 339 ghi `sanctions: [135/2025/QH15]`, trong NĐ 105 ghi `interlocks_with: [135/2025/QH15]`)?
   - Cân đối giữa chi phí đồng bộ (maintenance drift) và giá trị cho Knowledge Graph theo nguyên tắc KISS v2.0 (ADR-0061)?

4. **Khuyến Nghị Triển Khai Thực Tiễn**:
   - Grok đánh giá rủi ro tổng thể (Risk Score 1-10) của đề xuất này là bao nhiêu?
   - Lộ trình triển khai khuyến nghị theo từng bước (Phase 1, Phase 2) như thế nào?

Trân trọng kính mời Grok thẩm tra và đưa ra phán quyết (`PeerVerdictBlock`)!
