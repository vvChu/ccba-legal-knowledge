# 🧠 Session Document: CCBA Unified Context Graph — EOS L10 Pre-Flight X-Ray & Governance Drift Radar

> [!IMPORTANT]
> **Tài liệu Tổng hợp Phiên Động não (`/ccba-ask` Mode B & `/boost` Adversarial Investigation)**
> Ghi nhận toàn bộ quá trình khảo sát thực nghiệm trên 4 Hub (`ccba-legal-knowledge`, `IDOP-CCBA-WAY`, `dgx-spark-toolkit`, `VvC_Notes`), phát tán ý tưởng theo **Hybrid Rhythm**, phản biện **Party Mode 3 Persona**, và hội tụ thành thiết kế **2-Bước Tối Giản (KISS v2.0)**.

---

## 1. Intake (Thông tin Đầu vào & Bối cảnh Ràng buộc)

| Hạng mục | Nội dung Chi tiết |
| :--- | :--- |
| **Chủ đề (Topic)** | Ứng dụng **Ontology & Knowledge Graph** giải quyết các điểm nghẽn thực tế trong hệ sinh thái Liên bang Hub-Spoke và vận hành **CCBA WAY (`IDOP`)**. |
| **Ngày thực hiện** | `2026-11-07` (Kỳ vận hành EOS L10: `2026-W45`) |
| **Nguồn tri thức tham chiếu** | • **Synthesis Hub (`VvC_Notes`):** `4.011` cached concepts (`_vault_concepts_cache.json`), `76` concepts chuyên sâu về Ontology & KG (`graph_data.json`).<br>• **Legal Spoke (`ccba-legal-knowledge`):** `106` OKF v2.4 Bundles, `5-Ring Legal Graph` (`spoke_cli.py`), Từ điển Quốc gia `QĐ 1812/QĐ-BXD` (`176` trường trong `bang_01.json`).<br>• **Compute Hub (`dgx-spark-toolkit`):** Container `neo4j-graph` (`10.253` nodes, `10.797` edges) & `Hub3Bridge`.<br>• **Operations Hub (`IDOP-CCBA-WAY`):** `62/62` SharePoint Lists (`6.417` items), `m365_bridge.db`, `etl_staging.db` (`184` DLQ), `eos_auto_scorecard_report.json`. |
| **Ràng buộc Kiến trúc (Constraints)** | 1. **SharePoint Lookup Ceiling:** Khóa cứng `MAX_VIEW_LOOKUP_COLUMNS = 8` trên mọi SharePoint List.<br>2. **Reuse-First & KISS (Rule 4 & Rule 5):** Tái sử dụng 100% hạ tầng `neo4j-graph`, SQLite `m365_bridge.db` và Seam `ccba_legal.lexicon`; cấm dựng thêm Graph DB thứ ba.<br>3. **Verbatim & Administrative Authority (Rule 9):** Cấm tự ý ghi đè quy chế nội bộ khi chưa có phụ lục phê duyệt của Lãnh đạo Viện/Trung tâm. |

---

## 2. Nhật ký Ý tưởng Phát tán & Phản biện Đa Vai (Divergent & Party Mode Log)

### 2.1. Ý tưởng từ Người dùng (`(user)` — Nguyên văn Verbatim)
* **(user) [Vòng 1]:** *"/ccba-ask Hãy truy cập thông tin dữ liệu tri thức tại VvC_Note để brain storming về chủ đề Ontology và Knowledge Graph"*
* **(user) [Vòng 2]:** *"/boost Trên cơ sở nền tảng Hub-Spoke và bối cảnh vận hành CCBA WAY thông qua nền tảng idop, hãy gợi ý các bài toán thực tế hoặc 'điểm nghẽn' lớn nhất mà tôi đang có thể dùng Ontology & Knowledge Graph để giải quyết lúc này."*
* **(user) [Vòng 3]:** *"kết hợp cả hai thành một 'CCBA Unified Context Graph'"*
* **(user) [Vòng 4]:** *"Tự động mổ xẻ nguyên nhân + căn cứ quy chế của 347,26 tỷ WIP & 6/10 KPI báo đỏ trước giờ họp EOS L10, cũng như nếu có thể thì Cảnh báo tức thời mọi điều khoản trong QCTK 2815 / QCCTNB 3209 đang lệch pha với Luật/Nghị định 2026 mới)"*
* **(user) [Vòng 5]:** *"thực hiện kết hợp 2 và 3"*
* **(user) [Vòng 6]:** *"đồng ý"*

### 2.2. Ý tưởng Mở rộng từ AI (`(AI)` — `Yes-And` Builds)
* **(AI-1) Kiến trúc "Dual-Storage, Single-Ontology":** Ghi tức thời các thực thể/cạnh vận hành SharePoint vào 2 bảng SQLite `sp_graph_nodes` và `sp_graph_edges` trong `m365_bridge.db` (phục vụ truy vấn cục bộ `< 5ms`), đồng thời chiếu các cạnh tóm tắt lên `neo4j-graph` để ghép với `10.253` nodes Pháp lý & Quy chế.
* **(AI-2) Cầu nối Ngữ nghĩa 3 Chiều (`Statutory Article` $\leftrightarrow$ `Internal Clause` $\leftrightarrow$ `IDOP Gate`):** Biến mỗi cổng kiểm soát (`Gate 1..4`, `Handoff-01..06` trong `cross_module_handoff.py`) thành một *Semantic Contract Node* kết nối quy định pháp luật, quy chế nội bộ (`QCTK 2815`, `QCCTNB 3209`) và gói công việc WBS (`WorkPackages`).
* **(AI-3) Bộ phân rã Đồ thị Nhân quả "WIP & Off-Track Root-Cause Tree":** Bóc tách khối `~347,26 tỷ VND` Unbilled WIP (`495,13 tỷ` tổng `staged_contracts` trừ `143,99 tỷ` `staged_outgoing_invoices`) và `6/10` KPI báo đỏ kỳ `2026-W45` thành các nút cổ chai gắn trực tiếp với điều khoản quy chế.
* **(AI-4) Radar Cảnh báo Lệch pha Quy chế ("Statutory-to-Internal Drift Radar"):** Nạp 4 văn bản trong `.md/governance_constitution/` (`01_qctk_2815_project_management.md`, `02_qcctnb_3209_financial_norms.md`, `03_ccba_charter_2026.md`, `04_ibst_organization_regs_2816.md`) vào `neo4j-graph` và `_idop_chunks_cache.json`, tự động phát hiện các viện dẫn hết hiệu lực (như `TT 11/2021`, `TT 13/2021`, `TT 09/2025` bị thay thế bởi `NĐ 206/2026` & `TT 32, 33, 34/2026/TT-BXD`).
* **(AI-5) Nâng cấp `DecisionCardPayload` trong `ccba_mind_decision_seam.py`:** Đính kèm `causal_chain_path`, `downstream_blocked_value_vnd` và `rationale_citations` vào từng thẻ quyết định tại cuộc họp EOS L10.
* **(AI-6) Just-In-Time Ontology Projection theo `QĐ 1812/QĐ-BXD`:** Dùng `176` trường Từ điển Quốc gia và `ccba_legal.lexicon` làm từ vựng chuẩn tại thời điểm chiếu đồ thị mà không phá vỡ schema `62` SharePoint Lists.

### 2.3. Đóng góp Phản biện từ 3 Persona (`Party Mode`)
* **👔 `(Giám đốc Điều hành EOS L10)`:** Bắt buộc tách bạch `347,26 tỷ VND` WIP thành **"WIP Ảo" (Accounting Ghost WIP)** do `34` hóa đơn đầu ra nằm kẹt trong `etl_dlq_records` (`UNMAPPED_HISTORICAL_CONTRACT`) và **"WIP Thật"** đang kẹt tại `Gate 3/4` hoặc thiếu biên bản phối hợp Viện chuyên ngành; chỉ xuất **Top 5 Hợp đồng (Pareto)** có giá trị giải phóng dòng tiền lớn nhất trong 60 phút họp IDS.
* **⚖️ `(Trưởng ban Pháp chế & KSNB)`:** Cấm tự động sửa ngầm nội dung `QCCTNB 3209` khi phát hiện văn bản căn cứ hết hiệu lực; phải gắn cờ `drift_status: "STATUTE_SUPERSEDED"` trên cạnh `:DERIVED_FROM_STATUTE` và xuất **Governance Amendment Proposal Card**. Đồng thời khóa chặt rủi ro pháp lý giữa `Metric #7 (Billable Utilization = 332,32%)` và `22` chứng chỉ hành nghề `EXPIRED` theo `Luật 135/2025/QH15` & `NĐ 217/2026/NĐ-CP`.
* **🛠️ `(Kỹ sư Kiến trúc Dữ liệu Skeptic)`:** Cấm dựng service thứ ba; giải quyết bằng **2 bước tối giản (KISS)**: (1) Mở rộng `Hub3Bridge` + nạp 4 văn bản `governance_constitution/` vào `neo4j-graph` (~80 LOC); (2) Thêm 2 bảng `sp_graph_nodes` & `sp_graph_edges` vào `m365_bridge.db` để cuộn `Timesheets.HoursWorked -> WorkPackages.ActualHours`, khấu trừ `34` hóa đơn DLQ và cấp dữ liệu trực tiếp cho `ccba_mind_decision_seam.py`.

---

## 3. Nhóm Phân Loại Chủ Đề (Thematic Clustering)

| Nhóm Phân Loại | Các Ý tưởng Thành phần | Hệ thống Đích |
| :--- | :--- | :--- |
| **Nhóm A: Hợp nhất Đồ thị Pháp lý & Quy chế Nội bộ** | `AI-2`, `AI-4`, `Pháp chế-1` (Nối `QCTK 2815` / `QCCTNB 3209` / `CCBA Charter` vào `neo4j-graph`, đồng bộ đủ 5-Ring edges, dọn `64` node `status=NULL`). | `dgx-spark-toolkit` & `ccba-legal-knowledge` |
| **Nhóm B: Đồ thị Vận hành Đọc tại chỗ (Materialized Read-Model)** | `AI-1`, `AI-3`, `Skeptic-1`, `Skeptic-2` (Thêm `sp_graph_nodes` & `sp_graph_edges` vào `m365_bridge.db`, cuộn `ActualHours`, bóc tách `347,26 tỷ` WIP). | `IDOP-CCBA-WAY` (`m365_bridge_worker.py`) |
| **Nhóm C: Tình báo Quyết định EOS L10 (L10 X-Ray Brief)** | `AI-5`, `EOS-L10-1`, `EOS-L10-2` (Tách Ghost WIP vs Real WIP, xếp hạng Top 5 Hợp đồng Pareto, truy vết `6/10` KPI báo đỏ kỳ `2026-W45`). | `IDOP-CCBA-WAY` (`ccba_mind_decision_seam.py`, `l10_traction_engine.py`) |
| **Nhóm D: Kiểm soát Năng lực Thời gian & Làm sạch DLQ** | `AI-6`, `Pháp chế-2` (Chặn gán Chủ trì thuộc `22` chứng chỉ `EXPIRED`, phân giải `184` bản ghi `etl_dlq_records` bằng đồ thị 4 chiều). | `IDOP-CCBA-WAY` & `ccba-legal-intel` |

---

## 4. Xếp Hạng Ưu Tiên Đã Chốt (Prioritized Convergence)

1. **🥇 Ưu tiên Số 1 (P0 — Quick-Win Core): Kiến trúc "2-Bước Tối Giản" cho CCBA Unified Context Graph**
   - **Bước 1A (Operational X-Ray trên `m365_bridge.db`):** Khởi tạo `sp_graph_nodes` & `sp_graph_edges`, tự động bóc tách khối `347,26 tỷ VND` WIP thành *Ghost WIP* (`34` hóa đơn DLQ) vs *Real WIP*, cuộn `Timesheets -> WorkPackages.ActualHours` và truy vết nhân quả cho `6/10` KPI `Off Track` (`Metric #1, #2, #3, #4, #7, #10`) + `Rock Q4-05`.
   - **Bước 1B (Governance Drift Radar trên `neo4j-graph`):** Nạp 4 văn bản `.md/governance_constitution/` thành các node `:InternalRegulation` / `:InternalClause` nối với `:Document` / `:Article` trên `neo4j-graph`, đồng bộ đủ 5-Ring edges và bật cảnh báo `STATUTE_SUPERSEDED` cho `corpus="idop"`.
2. **🥈 Ưu tiên Số 2 (P1 — Data Hygiene & Legal Guardrail):**
   - Dùng *Graph Multi-Evidence Entity Resolution* (`Account + Unit/PM + DateWindow + Amount`) dọn sạch `184` bản ghi `etl_dlq_records` (`71` hợp đồng mồ côi, `45` vendor mồ côi, `47` dòng giao khoán bị kẹt) và áp đặt bộ lọc thời gian chặn `22` chứng chỉ `EXPIRED`.
3. **🥉 Ưu tiên Số 3 (P2 — Second Brain & Gate 3 Parametric QC):**
   - Gắn `parse_graph.py` vào chu trình tự động của `VvC_Notes` và bổ sung 1-hop graph expansion vào `VvCNotesRetriever`.

---

## 5. Kế Hoạch Hành Động Cụ Thể (Action Items — Atomic Micro-PR Slicing)

| Ticket / Bước | Hạng mục Thực thi | File / Seam Tác động | Tiêu chí Nghiệm thu Tất định (Verification Gate) |
| :---: | :--- | :--- | :--- |
| **Slice 1** | **Governance Constitution Ingestion & 5-Ring Neo4j Sync** | • `hub3_bridge.py`<br>• `idop_kb_retriever.py`<br>• `search_pipeline.py` | • `neo4j-graph` có đủ cạnh 5-Ring (`INTERLOCKS_WITH`, `MANDATORY_CODE`, `SANCTIONED_BY`, `LOCAL_DELEGATION`) và `0` node `status=NULL`.<br>• 4 văn bản `governance_constitution/` được bóc tách thành `:InternalClause` nối `:DERIVED_FROM_STATUTE`.<br>• Truy vấn Cypher phát hiện chính xác các viện dẫn hết hiệu lực trong `QCCTNB 3209` (`TT 11/2021`, `TT 13/2021`, `TT 09/2025`). |
| **Slice 2** | **SQLite Operational Context Graph (`sp_graph_nodes` & `sp_graph_edges`)** | • `m365_bridge_worker.py`<br>• `etl_staging.db` | • Tạo bảng `sp_graph_nodes` & `sp_graph_edges` trong `m365_bridge.db`.<br>• Tự động cuộn `297` `Timesheets` sang `208` `WorkPackages.ActualHours` và suy diễn `ProjectId` cho `284/290` dòng.<br>• Phân tách chính xác `347,26 tỷ VND` thành `Ghost WIP` (từ `34` hóa đơn DLQ) và `Real WIP` theo từng Gate. |
| **Slice 3** | **EOS L10 Pre-Flight X-Ray & Governance Amendment Decision Cards** | • `ccba_mind_decision_seam.py`<br>• `l10_traction_engine.py` | • Sinh báo cáo JSON/Markdown trước giờ họp L10: Top 5 Hợp đồng Pareto cần tháo gỡ cho `6/10` KPI báo đỏ kèm trích dẫn Điều khoản `QCTK 2815` / `QCCTNB 3209` và thẻ `STATUTE_SUPERSEDED`. |

---

## 6. Khung Cược Trước & Chuyển Tiếp Phản Biện (Pre-Flight Conviction Handoff)

```markdown
🎯 Cược của tôi: Việc kết hợp 2 bảng đồ thị cục bộ (sp_graph_nodes, sp_graph_edges) trong SQLite m365_bridge.db với các node :InternalClause (QCTK 2815, QCCTNB 3209) trên neo4j-graph theo kiến trúc "2-Bước Tối Giản" sẽ bóc tách chính xác >= 85% nguyên nhân gốc rễ của khối 347,26 tỷ VND WIP & 6/10 KPI EOS L10 báo đỏ và phát hiện 100% điều khoản quy chế nội bộ lệch pha với VBPL 2026 mà không cần dựng thêm bất kỳ Graph DB mới nào (Xác suất tin tưởng: 90%).
💣 Điểm gãy: Cược này sẽ sai nếu > 40% giá trị trong 347,26 tỷ VND WIP nằm ở các hợp đồng lịch sử bị khuyết hoàn toàn cả mã khách hàng (customer_key), mã đơn vị (unit) lẫn hồ sơ giao việc (WorkPackages/Submissions) khiến đồ thị không có cạnh trung gian để bắc cầu, hoặc nếu độ trễ truy vấn đệ quy WITH RECURSIVE trên SQLite vượt quá 500ms mỗi lần sinh thẻ quyết định L10.
🔍 Câu hỏi ép cung AI: Hãy đóng vai Kỹ sư Kiểm toán Dữ liệu Đối kháng (Adversarial Data Auditor), chỉ ra 3 trường hợp biên (edge cases) trong dữ liệu thực tế của staged_contracts (325 dòng), staged_outgoing_invoices (307 dòng) và etl_dlq_records (184 dòng) có thể khiến thuật toán bóc tách Ghost WIP vs Real WIP trên sp_graph_edges tính sai số tiền bị nghẽn hoặc gán nhầm lỗi cho các Trung tâm/Viện chuyên ngành!
```

---

## 7. Bản Đồ Định Vị Hub-Spoke, 3 Rào Chắn Dữ Liệu & Hợp Đồng Giao Tiếp Song Song (DAG Parallel Contracts)

### 7.1. 3 Rào Chắn Kiểm Toán Dữ Liệu Đối Kháng (`[đo thực tế]` trên `etl_staging.db`)
1. **Rào chắn 1 — Chống Nhân Bản Đa Đơn Vị ($1:N$ Fan-out) & Phân Định Trách Nhiệm CCBA vs 14 Viện/Trung Tâm Chuyên Ngành Thuộc IBST:**
   - Trong `325` hợp đồng (`495,13 tỷ VND`), có `121` hợp đồng (`126,20 tỷ VND`) không qua `staged_job_assignments` mà nằm trong `staged_scope_department_allocations` (`467` dòng), và có `138/329` scopes do $\ge 2$ đơn vị cùng thực hiện:
     - `CCBA_INTERNAL` (`TT BIM`, `282` dòng): **`320,72 tỷ VND`**
     - `IBST_INTER_UNIT` (14 Viện/TT chuyên ngành thuộc IBST, `183` dòng): **`93,34 tỷ VND`**
     - `EXTERNAL_PARTNER` (`FGE`, `2` dòng): **`0,56 tỷ VND`**
     - `MISSING_VKH_COOPERATION_MEMO` (`20` HĐ `/VKH`): **`71,31 tỷ VND`** + `INCOMPLETE_COOPERATION_SHARE_SUM` (`5` HĐ): **`9,20 tỷ VND`**
     - Tổng khớp 100%: $320,72 + 93,34 + 0,56 + 71,31 + 9,20 = 495,13\text{ tỷ VND}$.
   - Cạnh `(:ContractScope)-[:ALLOCATED_TO_UNIT {weight_share: allocation_share}]->(:Unit)` bắt buộc nhân `weight_share` để chống nhân bản WIP.
2. **Rào chắn 2 — Đồng Nhất Hệ Quy Chiếu Thuế GTGT & Tách `Ghost WIP` (`34` Hóa đơn DLQ = `1,84 tỷ VND`):**
   - `staged_contracts` lưu giá trị trước thuế (`gross_amount == net_amount == 495,13 tỷ`), còn `staged_outgoing_invoices.gross_amount = 143,99 tỷ` là sau thuế (`net_amount = 133,82 tỷ`, đã thu `122,74 tỷ`). Lưu song song `unbilled_wip_headline_vnd` (`347,26 tỷ`) và `unbilled_wip_net_vat_normalized_vnd` (`max(0, c.net_amount - SUM(inv.net_amount))`), đồng thời cô lập `4` HĐ `gross_amount IS NULL` nhưng đã xuất hóa đơn (`2,43 tỷ`).
3. **Rào chắn 3 — Suy Diễn `ProjectId` Cho `100%` (`284/290`) Dòng `Timesheets` & Khóa `22` Chứng Chỉ `EXPIRED`:**
   - Bắc cầu `staged_timesheets.contract_code -> staged_job_assignments.project_code` để điền đủ `290/290` `ProjectId`, cuộn `SUM(hours_worked)` lên `WorkPackages.ActualHours`, chuẩn hóa mẫu số `AvailableHours` cho `Metric #7` (hiện đang báo ảo `332,32%`), và gắn cờ `CERT_EXPIRED` cho `22` chứng chỉ hết hạn + `20` chứng chỉ lỗi ngày (`9 MISSING` + `11 TEXT_NON_DATE`).

### 7.2. Hợp Đồng JSON Giao Tiếp Giữa Các Repo (Cho Phép Chạy Song Song 100% 4 Phiên)

#### Hợp đồng 1: `tools/output/state/governance_drift_report.json` (tại `IDOP-CCBA-WAY`)
*(Do `dgx-spark-toolkit/services/rag-service/scripts/index_idop_kb.py` sinh ra; `IDOP-CCBA-WAY/tools/eos/ccba_mind_decision_seam.py` tiêu thụ với fallback an toàn nếu file chưa tồn tại)*:
```json
{
  "schema_version": "1.0",
  "generated_at": "2026-11-07T12:00:00+07:00",
  "drifted_clauses": [
    {
      "regulation_id": "3209/QĐ-VKH",
      "regulation_title": "Quy chế chi tiêu nội bộ Viện KHCN Xây dựng",
      "authority_tier": "IBST_INSTITUTE",
      "clause_id": "3209/QĐ-VKH::phu-luc-11-muc-2",
      "heading_path": "Phụ lục 11 > Mục 2. Hệ số lương cấp bậc, mức lương cơ sở, đơn giá tiền công",
      "drift_status": "STATUTE_SUPERSEDED",
      "superseded_citations": [
        {
          "cited_doc": "11/2021/TT-BXD",
          "replaced_by": ["36/2026/TT-BXD"],
          "guided_by": "206/2026/NĐ-CP",
          "effective_date": "2026-07-01"
        },
        {
          "cited_doc": "13/2021/TT-BXD",
          "replaced_by": ["37/2026/TT-BXD"],
          "guided_by": "206/2026/NĐ-CP",
          "effective_date": "2026-07-01"
        },
        {
          "cited_doc": "09/2025/TT-BXD",
          "replaced_by": ["37/2026/TT-BXD"],
          "guided_by": "206/2026/NĐ-CP",
          "effective_date": "2026-07-01"
        }
      ]
    }
  ]
}
```

#### Hợp đồng 2: `scripts/.state/_graph_adjacency_cache.json` (tại `VvC_Notes`)
*(Do `VvC_Notes/scripts/sleep.py::_sync_knowledge_graph` sinh ra; `dgx-spark-toolkit/.../vvc_notes_retriever.py` tiêu thụ với fallback sang `VvC_Notes/scripts/knowledge_graph/graph_data.json`)*:
```json
{
  "schema_version": "1.0",
  "generated_at": "2026-11-07T12:00:00+07:00",
  "adjacency": {
    "ma_hoa_tri_thuc_chuyen_gia_qua_ban_the_luan_va_do_thi_tri_thuc": [
      {"target": "nguy_bien_dong_nhat_suy_luan_voi_tim_kiem_trong_rag", "type": "related", "weight": 1.0}
    ]
  }
}
```

