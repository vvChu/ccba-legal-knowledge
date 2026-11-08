---
request_id: req-spoke-legal-hygiene-plan-001
verdict: REVISE_PLAN
conditions:
- id: COND-01
  description: Mục 2 phải đổi sàn cứng `doc_count >= 87` và `len(normative_sources)
    >= 106` thành đối soát động với đúng tập khóa mà từng hàm đang đọc. `get_spoke_stats`
    đặt `doc_count = len(laws + standards + documents)` và bỏ qua khóa `decrees`;
    hàm này đếm registry, không đếm thư mục bundle. `get_canonical_manifest(ultra_full=False)`
    chỉ lấy `{slug}.md` khi bundle tồn tại, rồi luôn cộng thêm `legal_docs/<cat>/*.md`
    (trừ index/dead_ends/log). Test phải khẳng định mọi `bundle_path` có `{slug}.md`,
    `doc_count` bằng đúng hợp khóa của `get_spoke_stats`, và phân hoạch 01_vbpl/02_qcvn/03_tcvn/04_appendices
    cộng lại bằng toàn bộ manifest. Sàn 7/11/14/31/491/174/20000/15.0 chỉ được ghi
    sau một lần in `get_spoke_stats` trong cùng PR; 491 phải là số file `figures/cards/*.{md,json}`.
  blocking: true
  source_profiles: []
- id: COND-02
  description: Chưa thêm cả `tests/integration` vào `verification.test_path`. `scripts/spoke/sync/coordinator.py`
    (khoảng dòng 1398) đọc khóa này dạng chuỗi hoặc list và chạy từng path khi `--verify`.
    `test_spoke_validator_pass` gọi `LegalSpokeValidator.run_all_checks()`, gồm Gate
    11 đọc DOCX từng bundle. Đưa nguyên thư mục integration vào post-sync sẽ gắn một
    vòng 15 cổng vào mọi lần đồng bộ. Tách test validator (marker hoặc thư mục fast)
    hoặc giữ `test_path` ở `tests/unit` và để integration cho CI. Sửa test và đổi
    `test_path` trong cùng một thay đổi.
  blocking: true
  source_profiles: []
- id: COND-03
  description: 'Trước `sync_spoke.py --spoke . --apply`, xác nhận chuỗi `[Sync] Error:
    Item not found in Hub catalog.yaml` tại `coordinator.py:659` lấy `sync_item` từ
    manifest copy của Hub, không từ `agent_skills`. Danh sách hiện đã có `ccba-verify-legal-knowledge`
    và nhiều alias ngoài catalog (`grilling`, `maskara-privacy`, `notebooklm-connector`,
    `form-template-cleaner`, `table-reconstructor`) sau các lần sync đã chạy, nên
    việc thêm `ccba-verify-legal-intel` và `ccba-verify-legal-ingest` theo đúng tên
    thư mục skill là cùng một lớp khai báo. Đồng thời xác nhận `--apply` hợp nhất
    `agent_skills` cục bộ, không sinh lại khóa này từ template Hub.'
  blocking: false
  source_profiles: []
- id: COND-04
  description: Mục 3 giữ nguyên diff `\d` trong f-string (hai dấu gạch chéo ngược).
    Chuỗi phát ra JavaScript vẫn là `\d` ở tầng source JS, tức lớp chữ số. Cấm nhân
    thêm thành bốn gạch chéo. Các `\d` ở dòng 66–236 nằm trong raw string; dòng 578
    chỉ dùng escape `\\` hợp lệ. Nghiệm thu bằng `python -W error::SyntaxWarning -m
    compileall -q scripts` để gồm `scripts/_guardrails`, vì glob `scripts/*.py` không
    đệ quy.
  blocking: false
  source_profiles: []
- id: COND-05
  description: Bộ lọc `[VBHN Telemetry]` khớp đúng một chỗ `warnings.append` và chỉ
    khi `verification_scope.type == vbhn_consolidation` (cổng trong code là `type`,
    trường mô tả kế hoạch đang ghi `consolidation_note`). Giữ `success is True` và
    `len(errors)==0`. Khẳng định mọi warning còn lại rỗng, và tập bundle trong telemetry
    trùng metadata có `type == vbhn_consolidation` bị lệch parity, để một warning
    mới tái dùng tiền tố này không bị nuốt.
  blocking: false
  source_profiles: []
risk_score: 3
summary: 'Mục 3 thoát `\d` trong f-string là đúng và có thể làm ngay. Mục 1 đăng ký
  hai skill spoke-local theo tiền lệ `ccba-verify-legal-knowledge`, nhưng cấm gắn
  cả `tests/integration` vào post-sync `--verify` vì `test_spoke_validator_pass` chạy
  đủ 15 cổng. Mục 2 phải viết lại: `doc_count >= 87` đang so cardinality registry
  với số thư mục bundle và để lọt bundle rơi khi số còn trên sàn.'
telemetry:
  session_id: d1375d42-1bb6-4c7b-864a-7dc92aa35aba
  primary_model: grok-4.7-build
  input_tokens: 458528
  output_tokens: 23018
  reasoning_tokens: 18116
  cached_read_tokens: 363392
  total_tokens: 481546
  model_calls: 6
  turn_count: 2
  cost_usd: 0.305
  cost_mode: exact
  duration_seconds: 240.0
  degraded_reasoning: false
---

# Phản biện kế hoạch vệ sinh Spoke — Mục 1, 2, 3

Phạm vi đã đọc: `.md/workspace_context.yaml`, `tests/integration/test_spoke_cli.py`, `scripts/spoke_cli.py` (`get_spoke_stats`), `scripts/sync_notebooklm_knowledge.py` (`get_canonical_manifest`), `scripts/validate_legal_spoke.py` (nhánh telemetry Gate 11), `scripts/verify_formula_visual_matrix.py` (khối f-string quanh dòng 533–579), `features/INDEX.md`, và điểm neo Hub `scripts/spoke/sync/coordinator.py` (dòng 659 và 1398). Chưa chạy `pytest` và chưa chạy `py_compile`, nên báo cáo không đưa số phút đo được.

## Mục 1 — `workspace_context.yaml`

Tệp hiện có `ccba-verify-legal-knowledge` trong `agent_skills` và `verification.test_path` chỉ chứa `tests/unit`. Hai tên cần thêm trùng thư mục skill đã được `features/INDEX.md` trỏ tới (`ccba-verify-legal-intel`, `ccba-verify-legal-ingest`).

**Skill không có trong Hub catalog.** Lần sync kế tiếp không phát sinh một lớp lỗi mới chỉ vì hai tên này. `agent_skills` đã mang `ccba-verify-legal-knowledge` (skill tạo trên Spoke) cùng các alias không nằm catalog Hub: `grilling`, `maskara-privacy`, `notebooklm-connector`, `form-template-cleaner`, `table-reconstructor`. Chuỗi lỗi Hub nằm ở `ccba-agent-platform/scripts/spoke/sync/coordinator.py:659` (`Item '{sync_item}' not found in Hub catalog.yaml`). Điều đó chứng minh có một cửa so catalog; nó chưa chứng minh cửa đó duyệt `agent_skills`. COND-03 yêu cầu đọc hàm chứa dòng 659 trước `--apply`, và xác nhận `--apply` giữ các mục local khi hợp nhất context.

**`test_path` có hiệu lực thật.** Cùng file coordinator, khoảng dòng 1398, đọc `verification.test_path`, tách chuỗi thành list, rồi lặp từng path. Thêm `tests/integration` làm `--verify` hậu đồng bộ chạy thư mục đó.

Chi phí nằm ở `test_spoke_validator_pass`: nó dựng `LegalSpokeValidator(root)` và gọi `run_all_checks()`. Gate 11 (`validate_legal_spoke.py` khoảng 1525–1566) mở từng DOCX dưới `01_vbpl`, `02_qcvn`, `03_tcvn` và so đoạn với Markdown. Một lần `--verify` sau khi thêm path này có khối lượng bằng một lần `python scripts/validate_legal_spoke.py`, cộng 126 unit test. Audit này không bấm giờ suite. Với kho cỡ hiện tại, đó là vòng kiểm định đầy đủ, không phải smoke hậu sync.

COND-02 chặn việc gắn cả thư mục integration. Ba lối an toàn: giữ `test_path: [tests/unit]` và để integration trên CI; đánh marker để sync bỏ `test_spoke_validator_pass`; hoặc trỏ `test_path` tới một nhóm test nhanh đã tách file validator. Sửa assertion và đổi `test_path` trong cùng một commit, vì thứ tự “sửa yaml trước, sửa test sau” làm chính `--verify` đỏ ở ngưỡng cũ `== 60`.

## Mục 2 — Dynamic Scale Invariant

Hướng bỏ `== 60` / `== 370` / `== 128` là đúng bệnh. Diff đang đề xuất thay bằng sàn số tay, và sàn đó lệch nghĩa với hàm đo.

`get_spoke_stats` (`scripts/spoke_cli.py` 84–120):

- `doc_count` = số phần tử `laws` + `standards` + `documents` (dict hoặc list). Không có nhánh `decrees`. Không `iterdir` bundle.
- `categories` lấy `doc["type"]`, thiếu type thì gán `"Khác"`.
- `total_figures` = `figures/cards/*.md` + `figures/cards/*.json`.
- `total_templates` = `templates/**/*.md`.
- `total_clauses` / `total_qa` = độ dài JSON tương ứng.
- `total_size_mb` = tổng byte mọi `legal_docs/**/*.md`.

`get_canonical_manifest(..., ultra_full=False)` (`sync_notebooklm_knowledge.py` 31–202):

- Đọc thêm khóa `decrees`.
- Bỏ qua registry item khi thiếu `bundle_path`, thiếu thư mục, hoặc thiếu `{slug}.md` (`continue` im lặng).
- Nhánh template/csv/annex/`bang_so_sanh_thay_doi.md` chỉ chạy khi `ultra_full=True`.
- Vòng `legal_docs/<cat>/*.md` (dòng 175–200) chạy cả khi `ultra_full=False`, trừ `index.md`, `dead_ends.md`, `log.md`.

Hệ quả trực tiếp trên diff:

| Assertion trong kế hoạch | Hàm thực tế đang đếm |
|---|---|
| `stats["doc_count"] >= 87` | Cardinality registry (laws+standards+documents), trong khi 87 là số bundle vật lý được nêu ở đề bài |
| `len(normative_sources) >= 106` | Số `{slug}.md` còn file cộng markdown nằm ngay dưới thư mục category |
| `state >= 103`, `appendix >= 3`, tổng bằng manifest | Category = `bundle_path` segment `[1]` sau `strip("/")`, tức `legal_docs/<cat>/<slug>` → `<cat>` |
| `normative_tcvn >= 33` | Cùng category `03_tcvn` hoặc `rel_path` chứa chuỗi đó |
| `categories["Tiêu chuẩn quốc gia"] >= 31` | Đếm field `type`, một predicate khác với folder `03_tcvn` |
| `total_figures >= 491` | Số card `.md` + `.json`, không phải số mục `figures_catalog.yaml` |

Sàn `>= 87` trên `doc_count` để lọt đúng ca Mục 2 muốn chặn: registry tụt từ mức hiện hành xuống còn trên 87 vẫn xanh. Sàn `>= 106` trên manifest cũng xanh khi một thân quy phạm biến mất mà một file `.md` lỏng ở cấp category bù chỗ, hoặc khi số nguồn còn trên 106. Phép cộng `state + appendix == len(normative_sources)` giữ được: nó bắt nguồn có category ngoài bốn thư mục. Nó không bắt bundle biến mất khi tổng vẫn trên sàn. Khoảng cách 31 (type) với 33 (folder `03_tcvn`) cần một dòng giải thích trong PR; hai số này đang được chép từ hai phép đếm khác nhau.

`get_spoke_stats` và manifest còn lệch khóa `decrees`. Hai assertion `>= 87` và `>= 106` vì thế không cùng một tập văn bản.

Điều kiện hoàn chỉnh cho test, thay cho sàn tay:

1. Nạp `legal_registry.yaml` trong test. Mọi item có `bundle_path` phải có thư mục và `{slug}.md`. Đây là lưới bắt bundle rơi, độc lập với số đếm.
2. `stats["doc_count"]` bằng `len(laws + standards + documents)` tính lại trong test — cùng hợp khóa với `get_spoke_stats`. Thêm văn bản mới thì test vẫn xanh; xóa một entry thì đỏ.
3. Với `ultra_full=False`, tập manifest bằng các `{slug}.md` ấy cộng các markdown cấp category. Giữ phép cộng bốn category. Suy `03_tcvn` và `04_appendices` từ segment đường dẫn, bỏ sàn 103/3/33.
4. `stats["categories"]` bằng `Counter(doc["type"] or "Khác")` trên cùng tập với mục 2.
5. `total_figures` và `total_templates` bằng glob độc lập cùng pattern với hàm (`cards/*.md`, `cards/*.json`, `templates/**/*.md`). Pattern này khóa định nghĩa bộ đếm. Một file ratchet tăng đơn điệu chỉ dùng thêm nếu muốn bắt “registry và đĩa cùng bị xóa”; số 491, 174, 20000, 15.0 chỉ ghi vào ratchet sau khi PR dán output một lần chạy `get_spoke_stats`.

Lọc warning ở `test_spoke_validator_pass` đi đúng hướng. Chỗ duy nhất gắn tiền tố là:

```1563:1566:scripts/validate_legal_spoke.py
                    if is_vbhn_consolidation:
                        self.warnings.append(f"[VBHN Telemetry] {msg} — Delta expected per verification_scope.consolidation_note.")
                    else:
                        self.errors.append(msg)
```

Cờ `is_vbhn_consolidation` bật khi `verification_scope.type == "vbhn_consolidation"`. Bundle chỉ có `consolidation_note` mà sai `type` vẫn thành `errors`, và `assert len(errors)==0` vẫn bắt được. `warnings` đang là `str`, nên `startswith` dùng được. Đề bài nói test đang vướng ở `len(warnings)==0` trong khi `success` và `errors` đã qua, nghĩa là `run_all_checks()` trả `True` khi chỉ còn telemetry. Giữ hai assert đó. COND-05 siết thêm: warning ngoài tiền tố phải rỗng, và các slug trong telemetry khớp các bundle metadata `type == vbhn_consolidation` bị fail parity — một warning mới mượn tiền tố `[VBHN Telemetry]` sẽ không bị lọc trắng.

## Mục 3 — `SyntaxWarning` `\d`

Chẩn đoán dòng 552–553 đúng. Khối HTML là f-string thường (`{bundle_name}`, `{{` cho ngoặc JS). Trong f-string, `\d` là escape không hợp lệ với Python 3.12 và phát `SyntaxWarning` ngay lúc compile (kể cả khi `check_spoke_cleanliness.py` chỉ `ast`/compile file). Giá trị chuỗi vẫn giữ dấu `\`, nên JS hiện vẫn nhận lớp chữ số; cảnh báo là lỗi compile, hành vi regex hiện chưa sai.

Diff đề xuất:

```python
fid.match(/_C(\\d+(?:_\\d+)+)_/)
fid.match(/_ANNEX_([A-Z](?:_\\d+)+)_/)
```

`\\` trong f-string thành một `\`. JavaScript nhận lại `/_C(\d+(?:_\d+)+)_/`. Đây là bản vá tối thiểu đúng. Bốn dấu gạch chéo (`\\\\d`) sẽ đẩy `\\d` sang JS và biến lớp chữ số thành gạch chéo + chữ `d`.

Trong cùng file, các `\d` dòng 66, 77, 81, 100, 141, 147, 224, 227, 232, 236 nằm trong raw string `r"..."`. Dòng 578 `replace(/\\\\tag\\{{[^}}]+\\}}/g` chỉ gồm cặp `\\` và `{{`/`}}`, là escape hợp lệ, không phát `SyntaxWarning`. Grep `\d` trên `scripts/**/*.py` còn lại cũng nằm trong raw string (`lint_visual_parity.py`, `verify_all_docs_against_pdf.py`, `validate_legal_spoke.py`, `spoke_cli.py`, `check_spoke_cleanliness.py`). Audit chưa chạy compiler và chưa quét hết `\s`, `\w`, `\(` trong literal không raw. COND-04 lấy `compileall` đệ quy làm cửa đóng Mục 3; glob `scripts/*.py` bỏ sót `scripts/_guardrails/`.

Đổi cả template sang raw f-string `rf"""` sẽ làm lệch các chuỗi `\\\\` đã cân ở dòng 578. Giữ f-string thường và chỉ nhân đôi gạch chéo tại hai regex.

## Thứ tự làm sau khi sửa kế hoạch

1. Vá hai regex (Mục 3) và `compileall` dưới `-W error::SyntaxWarning`.
2. Viết lại `test_spoke_cli.py` theo COND-01 và COND-05; chạy riêng file này.
3. Thêm hai skill vào `agent_skills` sau bước xác nhận COND-03.
4. Chỉ mở rộng `test_path` theo một trong ba lối ở COND-02, cùng commit với test đã xanh.

Mục 3 và tên hai skill giữ nguyên được. Mục 2 trong diff hiện tại và việc gắn nguyên `tests/integration` vào `--verify` cần sửa trong kế hoạch trước khi code.