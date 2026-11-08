---
request_id: req-20261107-plan-ibst-nomenclature-rule61-001
verdict: REVISE_PLAN
conditions:
- id: COND-ALIAS-EXACT
  description: Thay fallback prefix trong upsert_single_graph_item bằng bảng LEGACY_NATURAL_KEY_ALIASES
    khóa theo (list_name, key_field, chuỗi cũ nguyên văn). Cấm tiền tố trần '[Gate
    1]'. Chỉ nhận đúng một item; nếu khóa cũ và khóa mới cùng tồn tại thì dừng (fail-closed).
    Sau PATCH gán existing_map[khóa_mới]=item_id và xóa khóa cũ. Nhánh UPDATED hiện
    không rebind map.
  blocking: true
  source_profiles: []
- id: COND-FK-LOOKUP
  description: 'Dùng cùng resolver cho mọi lookup chính xác sau fetch: sub_fk_map
    (seed_eos_initial_catalog.py khoảng L3039), telemetry existing_sub.get Gate 4
    (khoảng L2814), ApprovalNodes/ApprovalHistories theo _SubmissionTitle (khoảng
    L3076-L3100). Thiếu khóa phải fail có log, không continue im lặng để rơi SubmissionLookup
    và WorkflowIdLookupId.'
  blocking: true
  source_profiles: []
- id: COND-LIST-AND-PAYLOAD
  description: 'Alias gắn đúng tên list Graph: Submissions, ApprovalNodes, ProjectMembers,
    EmployeeHistory, ApprovalDelegations (không phải Delegations), ApprovalWorkflows.
    Ghi nhận PATCH Submissions ghi cả SubmissionTitle và Title dạng ''[SUB-2026-Gx-xxx]
    '' + SubmissionTitle (hai chuỗi khác nhau, cắt 255 ký tự). ApprovalWorkflows đã
    ghi đồng thời Title và WorkflowName.'
  blocking: true
  source_profiles: []
- id: COND-RULE4-CONTRACT
  description: 'Sửa 8 chuỗi core_lists_snapshot.json bằng diff với datamodel/sharepoint
    (projects.json đã là ''Mã dự án quốc gia / IBST''). Cụm đơn vị thành viên theo
    RULE-6.1 mục 4: ''thuộc IBST'', không rút thành ''thuộc Viện''. Giữ InternalName,
    choice Submitted_to_IBST / IBST_Approved / IBST_Disbursed và authority_tier IBST_INSTITUTE.'
  blocking: true
  source_profiles: []
- id: COND-SCOPE-LIVE-PATCH
  description: 'Gỡ khỏi đợt này các sửa không chứa cụm cấm và sẽ PATCH SharePoint
    theo khóa ổn định: Location tài sản L1699/L1711 (''Tầng 5 Nhà A Viện'') và L1747
    (''— IBST'' sang ''CCBA (IBST)''), cùng câu ''Viện trưởng'' tại sp_home_page_deployer.py
    L717. AssetCode không đổi nên upsert sẽ ghi đè vị trí đang sống.'
  blocking: true
  source_profiles: []
- id: COND-HISTORY
  description: Giữ nguyên dòng lịch sử trong .md/knowledge/log.md; nếu cần, thêm mục
    đính chính append-only. ADR 0042/0046/0058/0060 chỉ thay token hiển thị, giữ nguyên
    quyết định, kèm một dòng erratum rằng git history giữ nguyên văn cũ.
  blocking: true
  source_profiles: []
- id: COND-VERIFY
  description: 'Bổ sung test upsert với map giả: khóa legacy, một dòng bidding ''[Gate
    1] Đăng ký đầu mối & Tham gia đấu thầu - {code}'', và case cả hai khóa cùng tồn
    tại. Scanner cross-repo có allowlist (vi_forbidden, test docstring, peer_exchange,
    backups, tên file hóa đơn). Gọi test_no_pleonastic_vien_ibst_terminology_in_ssot.
    Khẳng định 0 hit RAG sau index_idop_kb.py, parity skill 4 repo, và một nguồn cho
    graph_data.json/.js. Bổ sung bước VvC_Notes. pytest hiện tại không chạm SharePoint
    sống.'
  blocking: true
  source_profiles: []
risk_score: 4
summary: Hướng RULE-6.1 và danh mục bảo tồn là đúng, nhưng cơ chế prefix '[Gate 1]'
  trong upsert dùng chung có thể PATCH nhầm hồ sơ đấu thầu đang sống. Kế hoạch cần
  chuyển sang alias khóa cũ tường minh, nối resolver đó vào backfill khóa ngoại, và
  cắt các sửa ngữ nghĩa ngoài cụm cấm trước khi triển khai.
telemetry:
  session_id: 873f12b6-24b3-4523-a4a9-c90d4ebf15a1
  primary_model: grok-4.7-build
  input_tokens: 276400
  output_tokens: 18525
  reasoning_tokens: 13651
  cached_read_tokens: 219008
  total_tokens: 294925
  model_calls: 7
  turn_count: 2
  cost_usd: 0.114
  cost_mode: exact
  duration_seconds: 344.94
  degraded_reasoning: false
---

# Phản biện kế hoạch chuẩn hóa "Viện IBST" (RULE-6.1)

## Kết luận

Kế hoạch đúng về mục tiêu và về phần lớn file văn bản. Cơ chế idempotent trên SharePoint, như đang viết ở mục User Review, chưa an toàn để chạy. `upsert_single_graph_item` hiện chỉ khớp nguyên văn (`seed_eos_initial_catalog.py` L2597–L2626). Sáu khóa tự nhiên trên working tree đã bỏ "Viện IBST", nên lần seed lên M365 còn bản ghi cũ sẽ đi nhánh `POST` và tạo dòng trùng. Cách vá bằng tiền tố ngắn `[Gate 1]` sửa đúng triệu chứng đó và mở một lỗi ghi đè khác.

## 1. Va chạm tiền tố — phải đổi thiết kế

`bidding_package_creator.py` L285 và L297–L299 tạo `Submissions` với cả `Title` và `SubmissionTitle` bằng:

`[Gate 1] Đăng ký đầu mối & Tham gia đấu thầu - {bidding_code}`

Tờ trình showcase là chuỗi khác, cùng mở đầu `[Gate 1]`:

`[Gate 1] Tờ trình Phê duyệt Tham gia Dự thầu & Đăng ký Đầu mối Viện`

`fetch_existing_items_by_key` (L2489–L2510) là `dict`: hai dòng cùng khóa thì id sau ghi đè id trước, không báo. Fallback `startswith("[Gate 1]")` trong hàm upsert dùng chung sẽ thấy mọi gói thầu Gate 1. Lấy phần tử đầu tiên rồi `PATCH` nguyên `graph_payload` của tờ trình lên dòng đấu thầu sẽ đổi `SubmissionTitle`, `RelatedEntity`, `SubmissionStatus` của hồ sơ đang sống.

Năm tiền tố còn lại đủ riêng nếu khớp nguyên cụm, gồm cả dấu phân cách:

- `[SUB-2026-G4-004 | Bước 2]` đứng cạnh Bước 1 ở L1538, không nuốt Bước 1
- `PM-GAMUDA-004:`
- `EH-2026-003:`
- `DEL-2026-003:`
- `WF-GATE2-CONTRACT-IBST:`

`wf_id_by_code` (L3030–L3032) đã cắt `Title` tại dấu `:` đầu. Mã `WF-GATE2-CONTRACT-IBST` ổn định khi phần sau dấu hai chấm đổi.

Cách an toàn là alias nguyên văn, theo list:

| List Graph | Khóa | Chuỗi cũ cần alias |
|---|---|---|
| `Submissions` | `SubmissionTitle` | `... Đầu mối Viện IBST` |
| `ApprovalNodes` | `Title` | `... Nộp KHKT Viện IBST (ROLE_DIRECTOR)` |
| `ProjectMembers` | `Title` | `... Cổng Viện IBST` |
| `EmployeeHistory` | `Title` | `... Gateway Viện IBST — ...` |
| `ApprovalDelegations` | `Title` | `... Cổng Viện IBST (...)` |
| `ApprovalWorkflows` | `WorkflowName` | `... trình Viện IBST ký` |

Tên list ủy quyền trong code là `ApprovalDelegations` (`full_59_list_completion_catalog.py` L642), không phải `Delegations`. Alias ghi sai tên list sẽ không bao giờ chạy, và seeder vẫn `POST` dòng mới.

Ba seeder đã hội tụ một hàm: `seed_governance_catalog.py` L39 import `upsert_single_graph_item`; `apply_full_59_completion_lists` nhận `upsert_single_fn`. Sửa một chỗ là phủ ba entrypoint, với điều kiện alias có `list_name`.

Hành vi bắt buộc của resolver:

1. Khớp đúng một id. Nhiều hit thì dừng.
2. Khóa mới và khóa cũ cùng có id thì dừng, để người vận hành gộp tay. `PATCH` một bên sẽ để dòng trùng còn lại.
3. Sau `PATCH`, `existing_map[nat_val] = item_id` và xóa khóa cũ. Nhánh `UPDATED` hiện không ghi map (L2608–L2616); chỉ nhánh `CREATED` ghi (L2625).

## 2. `Title` và `key_field` khi `PATCH`

Payload của sáu bản ghi có cả trường khóa lẫn `Title`. Chi tiết từng list:

**Submissions.** `build_offline_operational_showcase_plan` L778–L780 đặt:

- `SubmissionTitle` = tiêu đề Gate
- `Title` = `[{Code}] {SubmissionTitle}` cắt 255 ký tự, ví dụ `[SUB-2026-G1-001] [Gate 1] ...`

`PATCH` cập nhật cả hai. Cột `Title` trên SharePoint đổi sang dạng có mã `SUB-2026-*`, không chỉ bỏ chữ `IBST`. Bidding creator thì đặt `Title == SubmissionTitle`. Đó là lý do một `PATCH` nhầm Gate 1 phá luôn tiêu đề gói thầu.

**ApprovalWorkflows.** L698: `{"Title": m_wf.workflow_name, **w}` với `w` chứa `WorkflowName`. Hai trường cùng một chuỗi. Backfill ecosystem lại index list này bằng `Title` (L3026–L3028), trong khi governance upsert bằng `WorkflowName` (L383). Hai trường lệch nhau trên dòng legacy thì `wf_id_by_code` đọc `Title` cũ. Alias phải cập nhật cả hai, và lookup workflow nên ưu tiên mã trước dấu `:`.

**ApprovalNodes, ProjectMembers, EmployeeHistory, ApprovalDelegations.** Khóa là `Title` và payload có `Title`. `PATCH` đổi đúng khóa tự nhiên.

**Lỗ hổng nằm ngoài upsert.** Sau showcase, bước 5 fetch lại `existing_sub` rồi `existing_sub.get(sub_title)` với chuỗi mới (L3023–L3060). `None` thì `continue`. Telemetry Gate 4 (L2813–L2816) và `_SubmissionTitle` của ApprovalNodes (L3076–L3079) cùng kiểu. Một lần chạy đủ cờ, showcase chạy trước và `PATCH` xong thì fetch sau thấy khóa mới. Chạy ecosystem hoặc telemetry khi list sống vẫn còn câu cũ thì bỏ qua `RelatedId`, `WorkflowIdLookupId`, `SubmissionLookupLookupId` mà không báo lỗi. Resolver alias phải nằm ở chỗ đọc map, không chỉ ở chỗ ghi.

## 3. Bốn quy tắc ngữ cảnh, danh mục giữ, và kiểm định

`canonical_construction_taxonomy.yaml` L209–L215 đúng như kế hoạch trích: `vi_forbidden: [Viện IBST]`, canonical `Viện Khoa học công nghệ xây dựng (IBST)`. `brand_center` cấm `Trung tâm CCBA`; capsule `[IBST — CCBA]` thoát cả hai lỗi. Canonical đầu văn thư là `IBST - CCBA` (gạch ngang). Dấu `—` trong capsule nên được ghi là biến thể trình bày, hoặc đổi về gạch ngang khi chuỗi đó là đầu văn thư.

`deck_builder.py` L97 đã là `CCBA — Viện KHCN Xây dựng (IBST)`. L143 vẫn là `VIỆN IBST`. Sửa L143 theo rule 3 là đúng. Dạng `(IBST)` không dính regex IDOP, vì regex đòi `ibst` ngay sau khoảng trắng (`test_p6_8_eos_l10_engine.py` L366–L368).

Tám dòng fixture L174, L175, L870, L871, L962, L1023, L1024, L1030 khớp số lượng kế hoạch. `datamodel/sharepoint/lists/process_execution/projects.json` đã dùng `Mã dự án quốc gia / IBST`. Fixture đang lệch SSOT schema; hướng sửa DisplayName là đúng nếu copy từ datamodel. Riêng L871, "Các đơn vị thành viên thuộc Viện" làm mất định danh cha. Rule 4 của chính kế hoạch yêu cầu "đơn vị thành viên thuộc IBST".

Giữ nguyên: dòng `vi_forbidden`, enum `IBST_INSTITUTE`, choice `Submitted_to_IBST`, tên file hóa đơn, `.md/peer_exchange/*`, `.md/backups/*`. Scanner "0 hit" phải nhúng allowlist này. Working tree IDOP hiện chỉ còn cụm cấm trong docstring của test cấm (grep `Viện IBST`).

Ba sửa sau không chứa cụm cấm và không nên đi cùng đợt seed:

- L1699 và L1711: `Tầng 5 Nhà A Viện (Hà Nội)` thành `... IBST ...`. Khóa `AssetCode` ổn định nên sẽ `PATCH` vị trí tài sản đang sống.
- L1747: `Phòng R&D, Nền tảng Số & HTQT — IBST` thành `— CCBA (IBST)`, đổi chủ thể phòng.
- `sp_home_page_deployer.py` L717: `trước Viện trưởng` đã là chức danh đúng. Thêm `IBST` không phải sửa tautology. L709 đã có pháp nhân đầy đủ ở đoạn trên.

ADR và `log.md`: sửa token trong ADR sống được nếu quyết định giữ nguyên và có một dòng erratum. Sửa tay một dòng trong `log.md` làm đổi nhật ký. Phần đính chính nên là mục mới ở cuối.

Kiểm định mục 4 chưa khép 5 repo:

- `pytest tests/ -q` trên IDOP chạy `test_no_pleonastic_vien_ibst_terminology_in_ssot` (chỉ `AGENTS.md`, `datamodel`, `list-formatting`, `specs`, `tools`, `.md/system_blueprint`). Test đó không dựng `existing_map` có cả tờ trình cũ và dòng bidding.
- `pytest -k "idop or ooxml or lexicon"` không đọc ADR, seminar markdown, hay bản sao skill.
- RAG: cần assert 0 hit trong `_idop_chunks_cache.json` sau `index_idop_kb.py`.
- `VvC_Notes` không có bước kiểm. `graph_data.json` và `graph_data.js` sửa tay hai nơi sẽ lệch.
- Spoke `check_spoke_cleanliness.py` không thay cho scanner cụm cấm có allowlist.
- Receipt `compile_catalog` `NO_MATCH` nghĩa là lexicon masker không tự sửa chuỗi này. Cổng hồi quy phải là scanner + test alias, không phải Gate lexicon.

## Phần kế hoạch giữ được

Bảo tồn định nghĩa cấm, enum, hóa đơn, peer_exchange. Đồng bộ L143 với pháp nhân đầy đủ. Đưa fixture về DisplayName đã có trong datamodel. Ba seeder dùng chung một upsert. Mã workflow trước dấu `:` đã là định danh ổn định. Bốn quy tắc ngữ cảnh đủ dùng khi rule 4 được áp đúng cho đơn vị thành viên và các câu không chứa "Viện IBST" được tách khỏi lần seed này.
