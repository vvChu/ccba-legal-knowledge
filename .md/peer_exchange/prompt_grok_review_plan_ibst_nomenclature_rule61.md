---
request_id: "req-20261107-plan-ibst-nomenclature-rule61-001"
from_agent: "antigravity"
to_agent: "grok"
request_type: "review"
profile: "audit_plan"
max_turns: 6
subject: "Thẩm định Kế hoạch Triển khai: Chuẩn hóa Toàn diện Cụm từ 'Viện IBST' Theo RULE-6.1 Trên 5 Repositories"
timestamp: "2026-11-07T22:18:30+07:00"
source_documents:
  - "/home/vvc/.gemini/antigravity/brain/5054beab-8775-423f-aa9d-57a8bf38524b/implementation_plan.md"
  - "/home/vvc/ccba/ccba-agent-platform/packages/ccba-legal-intel/src/ccba_legal/resources/canonical_construction_taxonomy.yaml"
  - "/home/vvc/ccba/ccba-agent-platform/packages/ccba-ooxml/src/ccba_ooxml/pptx/deck_builder.py"
  - "/home/vvc/ccba/ccba-agent-platform/tests/fixtures/idop_contract/core_lists_snapshot.json"
  - "/home/vvc/ccba/IDOP-CCBA-WAY/tools/eos/seed_eos_initial_catalog.py"
  - "/home/vvc/ccba/IDOP-CCBA-WAY/tools/eos/full_59_list_completion_catalog.py"
  - "/home/vvc/ccba/IDOP-CCBA-WAY/tools/governance/seed_governance_catalog.py"
  - "/home/vvc/ccba/IDOP-CCBA-WAY/tools/storage/bidding_package_creator.py"
output_path: ".md/peer_exchange/grok_review_plan_ibst_nomenclature_rule61.md"
context: "Thẩm định đối kháng kế hoạch chuẩn hóa cụm từ lặp nghĩa 'Viện IBST' theo RULE-6.1 trên 5 repositories (ccba-agent-platform, IDOP-CCBA-WAY, dgx-spark-toolkit, VvC_Notes, ccba-legal-knowledge), đặc biệt là cơ chế chống sinh bản ghi trùng lặp (idempotent upsert) trên SharePoint Online và bảo toàn hợp đồng dữ liệu."
---

# 🎯 Yêu Cầu Thẩm Định Đối Kháng Kế Hoạch Triển Khai (`implementation_plan.md`): Chuẩn Hóa Toàn Diện Cụm Từ `"Viện IBST"` Theo `RULE-6.1`

> ⚠️ **Chỉ Dẫn Quan Trọng Cho Grok (`audit_plan`)**: Toàn văn `implementation_plan.md` và toàn bộ trích đoạn mã nguồn thực tế (`upsert_single_graph_item`, `seed_eos_initial_catalog.py`, `bidding_package_creator.py`, `deck_builder.py`, `core_lists_snapshot.json`, `canonical_construction_taxonomy.yaml`) đã được đính kèm đầy đủ trong prompt này. Grok **KHÔNG CẦN** quét rộng toàn bộ 5 repositories. Hãy thẩm định đối kháng (adversarial review) kế hoạch bên dưới và xuất báo cáo phản biện kèm khối `PeerVerdictBlock` (YAML frontmatter chuẩn với `request_id`, `verdict: APPROVE_PLAN | APPROVE_WITH_CONDITIONS | REVISE_PLAN | REJECT_PLAN`, `risk_score: 1..5`, `conditions: [...]`, `summary`).

---

## I. TOÀN VĂN KẾ HOẠCH TRIỂN KHAI (`implementation_plan.md`)

### 1. Mục Tiêu & Bối Cảnh (`Goal Description`)

Trong tiếng Anh, chữ **`I`** của **`IBST`** (*Vietnam Institute for Building Science and Technology*) đã có nghĩa là **Viện**. Do đó, cụm từ **`"Viện IBST"`** phạm lỗi lặp từ ngữ nghĩa (*tautology*) và đã bị đưa vào danh sách cấm (`vi_forbidden`) theo **`RULE-6.1`** tại `canonical_construction_taxonomy.yaml#L209-L215`.

Kế hoạch này chuẩn hóa triệt để mọi chuỗi hiển thị, tài liệu kiến trúc, skills, dữ liệu mẫu và chỉ mục RAG trên toàn bộ **5 Repositories** (`ccba-legal-knowledge`, `ccba-agent-platform`, `dgx-spark-toolkit`, `IDOP-CCBA-WAY`, `VvC_Notes`) và **Brain Artifact** theo **4 quy tắc ngữ cảnh đích**:

1. **`"Viện"`** *(hoặc `"Cổng Viện"`)*: Khi nói về quy trình hành chính nội bộ, trình ký, nộp lưu, con dấu pháp nhân hoặc các phòng chức năng cấp trên (`KHKT`, `TCKT`, `TCHC`).
2. **`"IBST"`** *(hoặc `"Viện (IBST)"` trên sơ đồ)*: Khi dùng làm mã định danh, tiền tố hệ thống, tiêu đề ngắn gọn, hoặc capsule thương hiệu (`[IBST — CCBA]`).
3. **`"Viện KHCN Xây dựng (IBST)"`** *(hoặc `"Viện KHCNXD"`)*: Khi giới thiệu pháp nhân đầy đủ lần đầu trong văn bản, slide bìa thuyết trình, hoặc địa chỉ trụ sở.
4. **`"Viện/Trung tâm chuyên ngành thuộc IBST"`** *(hoặc `"đơn vị thành viên thuộc IBST"`)*: Khi chỉ nhóm 21 đơn vị thành viên trực thuộc Viện.

> **Seam Capability Audit Receipt (`ADR-0061`):**
> ```json
> {
>   "command": "python3 scripts/governance/compile_catalog.py --in docx_or_md_text --out masked_text --json",
>   "status": "NO_MATCH",
>   "referenced_seam": "legal_lexicon.v1 (ccba_legal.lexicon:LexiconHarvester, ImmutableSpanMasker)",
>   "index_sha256": "fe4c3c11ca879eba54a8790ade072dbd98022f26bb1393585dee90149dddacfc"
> }
> ```

---

### 2. Điểm Cần Lưu Ý & Xác Nhận (`User Review Required`)

1. **Chống sinh bản ghi trùng lặp (Duplicate Rows) trên SharePoint Online (`IDOP-CCBA-WAY`):**
   Trên working tree của `IDOP-CCBA-WAY`, 6 bản ghi mẫu trong `seed_eos_initial_catalog.py`, `full_59_list_completion_catalog.py` và `seed_governance_catalog.py` đã được đổi chuỗi khóa tự nhiên (`SubmissionTitle`, `Title`, `WorkflowName`) từ `"... Viện IBST..."` sang `"... Viện..."`.
   Kế hoạch này sẽ bổ sung cơ chế **khớp fallback theo mã tiền tố định danh ổn định** (`[Gate 1]`, `[SUB-2026-G4-004 | Bước 2]`, `PM-GAMUDA-004:`, `EH-2026-003:`, `DEL-2026-003:`, `WF-GATE2-CONTRACT-IBST:`) trong `upsert_single_graph_item` (`seed_eos_initial_catalog.py#L2585-L2617`) để khi chạy seeder lên SharePoint M365 thật, hệ thống thực hiện `PATCH` cập nhật tại chỗ thay vì `POST` tạo mới bản ghi trùng.

2. **Danh mục Bảo tồn Tuyệt đối (`Must Preserve` — Không sửa):**
   - Các định nghĩa từ khóa bị cấm (`vi_forbidden: ["Viện IBST"]` và ví dụ `❌ Viện IBST`) trong bộ quy tắc `RULE-6.1`.
   - Tên file PDF hóa đơn kế toán vật lý trên OneDrive tại `chung_tu_ke_toan_inventory.json#L8252-L8253`.
   - Mã Enum kỹ thuật nội bộ `"authority_tier": "IBST_INSTITUTE"` trong Neo4j và JSON contract.
   - Các biên bản trao đổi lịch sử trong `.md/peer_exchange/*` và `.md/backups/*`.

---

### 3. Nội Dung Thay Đổi Đề Xuất (`Proposed Changes`)

#### Hạng mục 1: Hub 1 — `/home/vvc/ccba/ccba-agent-platform` (Nguồn gốc Skills, Slide Builder, Test Fixture & ADRs)

- **[MODIFY] `packages/ccba-ooxml/src/ccba_ooxml/pptx/deck_builder.py#L143`**:
  - Chuẩn hóa biến mặc định `org` tại dòng `143` (đồng bộ với dòng `97`):
    - Trước: `org = "TRUNG TÂM TƯ VẤN & ỨNG DỤNG BIM TRONG XÂY DỰNG (CCBA) — VIỆN IBST"`
    - Sau: `org = "TRUNG TÂM TƯ VẤN & ỨNG DỤNG BIM TRONG XÂY DỰNG (CCBA) — VIỆN KHCN XÂY DỰNG (IBST)"`
- **[MODIFY] `.md/seminars/2026/demo_seminar_nd217_luatxd2025.md#L6`**:
  - Chuẩn hóa trường `org:` ở frontmatter dòng `6` sang `"... (CCBA) — VIỆN KHCN XÂY DỰNG (IBST)"`.
- **[MODIFY] `tests/fixtures/idop_contract/core_lists_snapshot.json#L174`**:
  - Chuẩn hóa `8` dòng (`L174–175`, `L870–871`, `L962`, `L1023–1024`, `L1030`) đồng bộ 1:1 với schema SharePoint của `IDOP-CCBA-WAY`:
    - `"Mã dự án quốc gia / Viện IBST"` $\rightarrow$ `"Mã dự án quốc gia / IBST"`
    - `"Đơn vị phối hợp (Viện IBST)"` $\rightarrow$ `"Đơn vị phối hợp (IBST)"`
    - `"Các đơn vị thành viên thuộc Viện IBST..."` $\rightarrow$ `"Các đơn vị thành viên thuộc Viện..."`
    - `"Yêu cầu trình Viện IBST ký"` $\rightarrow$ `"Yêu cầu trình Viện ký"`
    - `"Trạng thái trình Viện IBST (Gateway)"` $\rightarrow$ `"Trạng thái trình Viện (Gateway)"`
    - `"... với Viện IBST"` $\rightarrow$ `"... với Viện"`
- **[MODIFY] 3 Skills gốc & `.md/knowledge/skills_compiled.md#L10544`**:
  - `.agents/skills/ccba-seminar-builder/SKILL.md#L89`: `Eyebrow Capsule [TRUNG TÂM CCBA — VIỆN IBST]` $\rightarrow$ `Eyebrow Capsule [IBST — CCBA]`.
  - `.agents/skills/ccba-sharepoint-iac/SKILL.md#L140` (`L140`, `L152`): `"Yêu cầu trình Viện ký"` và `"Trạng thái trình Viện (Gateway)"`.
  - `.agents/skills/ccba-xu-ly-van-phong/templates/docx-hanh-chinh-quyet-dinh-giao-viec-hdkt.md#L3`: `"giữa Viện KHCN Xây dựng (IBST) và Đơn vị thực hiện (CCBA)"`.
  - Cập nhật `skills_compiled.md` và đồng bộ 3 file skill trên sang `ccba-legal-knowledge`, `IDOP-CCBA-WAY`, `dgx-spark-toolkit`, `VvC_Notes`.
- **[MODIFY] Tài liệu Kiến trúc `CONTEXT.md`, `docs/adr/*` & `.md/knowledge/*` (`10` files)**:
  - `CONTEXT.md#L14` (`L14`, `L365`, `L377`): `"Cổng Giao Tiếp Viện (IBST Gateway)"`, `"trình Viện"`.
  - `docs/adr/0042-tiered-ai-pre-submission-gate-and-tri-repo-sync.md#L4`, `0046-personal-sandbox-lifecycle-and-charter-2026-alignment.md#L45`, `0058-live-collaboration-artifacts-workspace-mirroring-and-charter-alignment.md#L46`, `0060-4hub-federated-spokes-architecture.md#L96`.
  - `.md/knowledge/index.md#L129`, `log.md#L591`, `issues/idop-bridge/map.md#L12`, `issues/doc-auto-evolution/map.md#L33`, `issues/doc-auto-evolution/pr_template_spec.md#L34`.

#### Hạng mục 2: Hub 4 — `/home/vvc/ccba/IDOP-CCBA-WAY` (Hiệu đính Working Tree & Bảo vệ Upsert SharePoint)

- **[MODIFY] `tools/eos/seed_eos_initial_catalog.py#L1699` & `tools/eos/full_59_list_completion_catalog.py#L625` & `tools/governance/seed_governance_catalog.py#L381`**:
  - Tinh chỉnh ngữ nghĩa tại `seed_eos_initial_catalog.py`:
    - `L1699`, `L1711`: `"Tầng 5 Nhà A Viện (Hà Nội)"` $\rightarrow$ `"Tầng 5 Nhà A IBST (Hà Nội)"`.
    - `L1747`: `"Phòng R&D, Nền tảng Số & HTQT — IBST"` $\rightarrow$ `"Phòng R&D, Nền tảng Số & HTQT — CCBA (IBST)"`.
  - Bổ sung prefix-matching fallback trong `upsert_single_graph_item()` cho các bản ghi có tiền tố định danh ổn định (`[Gate 1]`, `[SUB-2026-G4-004 | Bước 2]`, `PM-GAMUDA-004:`, `EH-2026-003:`, `DEL-2026-003:`, `WF-GATE2-CONTRACT-IBST:`) để bảo đảm `PATCH` idempotent trên SharePoint.
- **[MODIFY] `tools/deployment/sp_home_page_deployer.py#L714` & 3 file tài liệu nội bộ**:
  - `sp_home_page_deployer.py:714`: `"Chịu trách nhiệm toàn diện trước Viện trưởng;"` $\rightarrow$ `"Chịu trách nhiệm toàn diện trước Viện trưởng IBST;"`.
  - Chuẩn hóa 2 biến thể thiếu dấu ngoặc tại `.agents/teamwork_preview_explorer_m1/ORIGINAL_REQUEST.md#L9`, `analysis_m1.md#L13` (`"Viện Khoa học Công nghệ Xây dựng (IBST)"`) và 1 dòng tại `.md/scratch/handoffs/handoff-2026-11-01-223700.md#L36`.

#### Hạng mục 3: Spoke (`ccba-legal-knowledge`), Hub 2 (`dgx-spark-toolkit`), Hub 5 (`VvC_Notes`) & Brain Artifact

- **[MODIFY] `.md/knowledge/specs/spec-ccba-unified-context-graph.md#L91` (`ccba-legal-knowledge`) & `brainstorm_session_ccba_unified_context_graph.md#L124`**:
  - Chuẩn hóa `"14 Viện Chuyên Ngành IBST"` $\rightarrow$ `"14 Viện/Trung Tâm Chuyên Ngành Thuộc IBST"`.
- **[MODIFY] `services/rag-service/data/idop_kb/_idop_chunks_cache.json` (`dgx-spark-toolkit`)**:
  - Thực thi `services/rag-service/scripts/index_idop_kb.py` để tái sinh `_idop_chunks_cache.json` từ các file Blueprint đã chuẩn hóa bên `IDOP-CCBA-WAY`, xóa sạch toàn bộ `221` dòng `"Viện IBST"` trong cache RAG.
- **[MODIFY] `04 - Permanent/topics/chuong_11_case_study_toan_canh_ccba_way_va_idop.md#L14` & `scripts/knowledge_graph/graph_data.json` / `graph_data.js` (`VvC_Notes`)**:
  - Sửa dòng `14` (`"thuộc Viện KHCN Xây dựng - IBST"`) và dòng `56` (`"của Viện KHCN Xây dựng (QCTK 2815 và QCCTNB 3209)"`), đồng bộ sang `graph_data.json` và `graph_data.js`.

---

### 4. Kế Hoạch Kiểm Định (`Verification Plan`)

1. **Quét kiểm chứng Regex toàn hệ sinh thái (Xác nhận 0 lỗi ngoài danh sách bảo tồn)**
2. **Kiểm định Skills & Contract Tests trên Hub 1 (`ccba-agent-platform`)**: `pytest tests/ -k "idop or ooxml or lexicon" -q`
3. **Kiểm định RAG Cache & Retriever trên Hub 2 (`dgx-spark-toolkit`)**: `.venv/bin/pytest services/rag-service/tests/ -q`
4. **Kiểm định Seeder Upsert & UCG trên Hub 4 (`IDOP-CCBA-WAY`)**: `pytest tests/ -q`
5. **Kiểm định Guardrails trên Spoke (`ccba-legal-knowledge`)**: `pytest -q && python3 scripts/audits/check_spoke_cleanliness.py`

---

## II. BẰNG CHỨNG MÃ NGUỒN THỰC TẾ ĐỂ GROK THẨM ĐỊNH ĐỐI KHÁNG

### 1. Quy tắc `RULE-6.1` trong `canonical_construction_taxonomy.yaml` (`L209-L215`)
```yaml
  brand_institute:
    canonical_id: INT-GOV-001
    canonical_vi: Viện Khoa học công nghệ xây dựng (IBST)
    domain: brand_nomenclature
    vi_forbidden:
    - Viện IBST
    context_notes: Cấp Viện gọi là Viện, Viện KHCN hoặc IBST theo RULE-6.1
```

### 2. Cơ chế Upsert hiện tại trong `IDOP-CCBA-WAY/tools/eos/seed_eos_initial_catalog.py` (`L2585-L2635` & `L3022-L3082`)
```python
def upsert_single_graph_item(
    graph_client: httpx.Client,
    list_name: str,
    key_field: str,
    serialized_fields: Mapping[str, Any],
    existing_map: dict[str, int],
    *,
    sp_client: httpx.Client | None = None,
    site_url: str = DEFAULT_SITE_URL,
    note_cache: dict[tuple[str, str], str] | None = None,
) -> tuple[str, int]:
    """Create or update a single item in SharePoint via Graph API idempotently."""
    nat_val = str(serialized_fields.get(key_field) or serialized_fields.get("Title") or "").strip()
    base_url = f"https://graph.microsoft.com/v1.0/sites/{EXPECTED_GRAPH_SITE_ID}/lists/{list_name}/items"

    graph_payload: dict[str, Any] = {}
    tax_fields: dict[str, dict[str, Any]] = {}
    for k, v in serialized_fields.items():
        if isinstance(v, dict) and "TermGuid" in v and "Label" in v:
            tax_fields[k] = v
        else:
            graph_payload[k] = v

    if nat_val in existing_map:
        item_id = existing_map[nat_val]
        _http_request_with_retry(
            graph_client,
            "PATCH",
            f"{base_url}/{item_id}/fields",
            json=graph_payload,
        )
        action = "UPDATED"
    else:
        post_resp = _http_request_with_retry(
            graph_client,
            "POST",
            base_url,
            json={"fields": graph_payload},
        )
        item_id = int(post_resp.json()["id"])
        existing_map[nat_val] = item_id
        action = "CREATED"
```

Và đoạn backfill khóa ngoại (`sub_fk_map` và `ApprovalNodes`) ở `seed_eos_initial_catalog.py#L3022-L3082`:
```python
    # 5. Resolve live Submissions & ApprovalWorkflows and backfill Submissions.RelatedId + WorkflowIdLookupId
    existing_sub = fetch_existing_items_by_key(
        graph_client, "Submissions", "SubmissionTitle"
    )
    existing_wf_raw = fetch_existing_items_by_key(
        graph_client, "ApprovalWorkflows", "Title"
    )
    wf_id_by_code: dict[str, int] = {}
    for wf_title, wf_id in existing_wf_raw.items():
        code_prefix = wf_title.split(":", 1)[0].strip()
        wf_id_by_code[code_prefix] = wf_id
...
    sub_fk_map = {
        "[Gate 1] Tờ trình Phê duyệt Tham gia Dự thầu & Đăng ký Đầu mối Viện": (
            21,
            "WF-GATE1-BIDDING",
        ),
...
    }
    for sub_title, (rel_id_val, wf_code) in sub_fk_map.items():
        sub_id = existing_sub.get(sub_title)
        if sub_id is None:
            continue
```
Lưu ý thêm tại `tools/storage/bidding_package_creator.py#L285`:
```python
    submission_domain = {
        "SubmissionTitle": f"[Gate 1] Đăng ký đầu mối & Tham gia đấu thầu - {bidding_code}",
```
*(Cả hai loại bản ghi trong list `Submissions` đều bắt đầu bằng tiền tố `"[Gate 1]"`, chỉ khác phần thân sau `"[Gate 1] Tờ trình Phê duyệt Tham gia Dự thầu..."` vs `"[Gate 1] Đăng ký đầu mối & Tham gia đấu thầu - ..."`).*

### 3. 6 Bản ghi có khóa tự nhiên thay đổi trên `IDOP-CCBA-WAY`
- `seed_eos_initial_catalog.py`:
  1. `Submissions` (`key_field="SubmissionTitle"`): `"[Gate 1] Tờ trình Phê duyệt Tham gia Dự thầu & Đăng ký Đầu mối Viện"` (trước đây: `"... Đầu mối Viện IBST"`)
  2. `ApprovalNodes` (`key_field="Title"`): `"[SUB-2026-G4-004 | Bước 2] Phê duyệt Đóng băng Hồ sơ A1 & Nộp KHKT Viện (ROLE_DIRECTOR)"` (trước đây: `"... Nộp KHKT Viện IBST (ROLE_DIRECTOR)"`)
  3. `ProjectMembers` (`key_field="Title"`): `"PM-GAMUDA-004: Nguyễn Thị Hoa — Quản trị Hồ sơ Pháp lý & Cổng Viện"` (trước đây: `"... Cổng Viện IBST"`)
- `full_59_list_completion_catalog.py`:
  4. `EmployeeHistory` (`key_field="Title"`): `"EH-2026-003: Phân công Trưởng phòng Tổng Hợp & Đầu mối Gateway Viện — Nguyễn Thị Hoa"` (trước đây: `"... Gateway Viện IBST — ..."`)
  5. `Delegations` (`key_field="Title"`): `"DEL-2026-003: Ủy quyền Thừa lệnh Giao dịch Hành chính & Nộp Hồ sơ Cổng Viện (GĐ -> Trưởng phòng Tổng Hợp)"` (trước đây: `"... Cổng Viện IBST (...)"`)
- `seed_governance_catalog.py`:
  6. `ApprovalWorkflows` (`key_field="WorkflowName"`, đồng thời gán `"Title": m_wf.workflow_name`): `"WF-GATE2-CONTRACT-IBST: Phê duyệt HĐKT Vượt hạn mức trình Viện ký"` (trước đây: `"... trình Viện IBST ký"`)

---

## III. CÂU HỎI TRỌNG TÂM CẦN GROK PHẢN BIỆN

1. **Rủi ro va chạm tiền tố (`Prefix Collision`) trong `upsert_single_graph_item()`:**
   - Nếu dùng tiền tố ngắn `"[Gate 1]"` để fallback trong `Submissions`, liệu có nguy cơ khớp nhầm sang các bản ghi `"[Gate 1] Đăng ký đầu mối & Tham gia đấu thầu - {bidding_code}"` do `bidding_package_creator.py` tạo ra trên SharePoint không? Thay vì khớp prefix chung `"[Gate 1]"`, có nên dùng ánh xạ legacy key tường minh (`LEGACY_NATURAL_KEY_ALIASES`) hoặc prefix định danh duy nhất (`"[Gate 1] Tờ trình Phê duyệt Tham gia Dự thầu"`, `"[SUB-2026-G4-004 | Bước 2]"`, `"PM-GAMUDA-004:"`, `"EH-2026-003:"`, `"DEL-2026-003:"`, `"WF-GATE2-CONTRACT-IBST:"`) kèm cập nhật `existing_map[nat_val] = item_id` và xóa khóa cũ khỏi `existing_map` không?
2. **Đồng bộ `Title` vs `key_field` khi `PATCH` trên SharePoint:**
   - Trong `Submissions` (`key_field="SubmissionTitle"`) hoặc `ApprovalWorkflows` (`key_field="WorkflowName"`), khi `PATCH` bản ghi cũ từ `"Viện IBST"` sang `"Viện"`, `graph_payload` đã chứa cả `Title` và `key_field` mới chưa? (Kiểm tra `seed_eos_initial_catalog.py` đối với `Submissions` xem payload có gán đồng thời `Title` và `SubmissionTitle` không).
3. **Tính đầy đủ của 4 Quy tắc Ngữ cảnh Đích & Danh mục Bảo tồn (`Must Preserve`):**
   - Việc sửa các ADR lịch sử (`0042`, `0046`, `0058`, `0060`) và `.md/knowledge/log.md` tại `ccba-agent-platform` có hợp lệ hay cần lưu ý gì về tính toàn vẹn lịch sử không?
   - Các lệnh kiểm thử tự động trong Mục 5 (`Verification Plan`) đã đủ bao phủ hết 5 repositories chưa?
