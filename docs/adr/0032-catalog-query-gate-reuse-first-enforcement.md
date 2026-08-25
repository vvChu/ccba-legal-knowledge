# ADR 0032 — Catalog Query Gate: Cưỡng Chế Reuse-First bằng Cơ Chế Verify-Based

**Ngày:** 2026-08-24  
**Trạng thái:** Accepted  
**Tác giả:** CCBA Platform Team (đúc kết qua Grilling Session 2026-08-24)

---

## 1. Bối Cảnh (Context)

Quy tắc **Reuse-First Gate** đã được ghi nhận trong `AGENTS.md` từ lâu: trước khi viết bất kỳ utility/script nào, agent phải kiểm tra Hub catalog xem đã có tool tương tự chưa. Tuy nhiên cơ chế thực thi hiện tại là **trust-based** — agent đọc quy tắc, tự cam kết tuân thủ, không có gì kiểm tra lại hành động thực tế.

Khoảng trống này dẫn đến các anti-pattern đã được ghi nhận trong `session_learnings.md`:
- **AP-01:** Agent tự viết `requests.get(tvpl_url)` thay vì gọi `ccba_legal fetch`
- **AP-02:** Agent tự viết `extract_formula_from_docx()` thay vì dùng `formula_harvester.py`
- **AP-03:** Agent viết script helper 20 dòng mà Hub đã có sẵn

Tất cả đều có dấu hiệu chung: agent tạo ra Python code mới thực hiện một *capability* đã tồn tại trong Hub.

---

## 2. Quyết Định (Decision)

Triển khai **Catalog Query Gate** — cơ chế verify-based 2 lớp cưỡng chế Reuse-First trước khi agent tạo bất kỳ code mới nào liên quan đến Hub capabilities.

### Lớp 1 — Planning Gate (Bảo vệ Ý định)

**Khi nào:** Ngay khi agent nhận yêu cầu xử lý tài liệu pháp lý và chuẩn bị lập `implementation_plan.md`.

**Hành động bắt buộc:**
```bash
python scripts/query_hub_catalog.py --intent "<mô tả task>"
# Output JSON: [{tool, skill_path, triggers_matched}]
```

**Kết quả:** Implementation Plan phải trích dẫn tường minh tool Hub sẽ dùng tại mỗi bước.

---

### Lớp 2 — Pre-execution Gate (Bảo vệ Hành động)

**Khi nào:** Ngay trước khi agent tạo file `.py` mới có chứa bất kỳ **capability keyword** nào sau đây:

```yaml
capability_keywords:
  fetch_group:    [fetch, crawl, download, requests.get, urllib]
  convert_group:  [convert, extract, parse, docx, document.xml]
  formula_group:  [formula, harvest, vision, ocr, VML, imagedata]
  registry_group: [legal_registry, registry.yaml, update_registry]
  rag_group:      [embed, rag, vector, chunking, retrieval]
```

**Hành động bắt buộc:**
```bash
python scripts/query_hub_catalog.py --intent "<capability>" --layer pre_exec
```

**Kết quả có thể:**
- `PASS` → Hub tool tìm thấy, agent dùng tool đó thay vì viết mới
- `BLOCK` → Hub tool tìm thấy nhưng agent sắp viết trùng lặp → dừng lại
- `BYPASS` → Agent xác định Hub tool không đáp ứng đủ, ghi lý do vào audit log và tiếp tục

---

### BYPASS Protocol

Agent được phép BYPASS Gate nếu:
1. Hub tool đã tồn tại nhưng **không đáp ứng đủ scope hiện tại** (ví dụ: cần xử lý edge case chưa có trong Hub)
2. **Bắt buộc** ghi log BYPASS vào `.md/logs/catalog_gate_audit.jsonl`:

```json
{
  "ts": "2026-08-24T15:27:00+07:00",
  "layer": "pre_exec",
  "intent": "extract formula with custom heuristic",
  "matched_keyword": "formula",
  "catalog_result": "formula_harvester.py",
  "action": "BYPASS",
  "bypass_reason": "Cần heuristic width > 380pt cho TCVN 2737 — Hub chưa hỗ trợ"
}
```

BYPASS không yêu cầu phê duyệt người dùng nhưng **tạo Bypass Debt** — được đo và review định kỳ.

---

## 3. Audit Log & Observability

**File:** `.md/logs/catalog_gate_audit.jsonl` (JSONL, Append-Only per ADR Logger skill)

**3 chỉ số theo dõi hiệu quả:**

| Chỉ số | Công thức | Ngưỡng cảnh báo |
|:--|:--|:--|
| **Hit Rate** | `(PASS + BLOCK) / total_ops` | < 80% → Gate bị bỏ qua |
| **Block Rate** | `BLOCK / (PASS + BLOCK)` | > 20% → Agent drift nhiều |
| **Bypass Debt** | `SUM(BYPASS)` tích lũy | > 5 → Cần review & tối ưu capability_keywords |

**Script phân tích:**
```bash
python scripts/analyze_gate_audit.py --since "7 days ago"
```

---

## 4. Hệ Quả (Consequences)

### Tích cực
- **Verify-based** thay vì trust-based: hành động thực tế được kiểm soát, không chỉ ý định
- **BYPASS có biên bản:** Mọi ngoại lệ đều để lại dấu vết → nguồn dữ liệu tối ưu capability_keywords
- **Reuse-First có bằng chứng:** Hit Rate và Block Rate là số liệu đo thực tế `[đo thực tế]`, không phải ước lượng
- **Feedback loop:** Bypass Debt tích lũy → tín hiệu để mở rộng Hub catalog đúng nơi cần thiết

### Đánh đổi
- Thêm bước bắt buộc vào mỗi task xử lý tài liệu pháp lý (~5-10s overhead)
- Agent phải tự scan intent trước khi viết code — thêm cognitive load
- `query_hub_catalog.py` và `analyze_gate_audit.py` cần được xây dựng (chưa có)

### Phụ thuộc
- `catalog.yaml` phải được duy trì cập nhật (đã có, AUTO-COMPILED)
- `Append-Only Logger` skill từ Hub (đã có)
- CI Gate `validate_legal_spoke.py` cần được mở rộng để kiểm tra audit log tồn tại sau mỗi session xử lý tài liệu

---

## 5. Phương Án Đã Loại Bỏ

| Phương án | Lý do loại |
|:--|:--|
| **A — Trust-based (AGENTS.md text only)** | Không verify hành động thực tế, đã thất bại thực tế |
| **C — Pre-commit CI Hook only** | Reactive (phát hiện sau khi sai), không phòng ngừa drift |
| **1 lớp duy nhất (chỉ Planning Gate)** | Không chặn drift xảy ra trong quá trình thực thi |
| **1 lớp duy nhất (chỉ Pre-execution Gate)** | Friction cao với task đơn giản, không định hướng sớm |

---

## 6. Liên Kết

- `AGENTS.md` — Mục Reuse-First Gate (sẽ được cập nhật để tham chiếu ADR này)
- `session_learnings.md` — Mục 4A (Anti-Pattern AP-01, AP-02, AP-03)
- `scripts/query_hub_catalog.py` — **[CHƯA XÂY]** Cần implement
- `scripts/analyze_gate_audit.py` — **[CHƯA XÂY]** Cần implement
- `.md/logs/catalog_gate_audit.jsonl` — **[CHƯA TỒN TẠI]** Tạo khi Gate lần đầu kích hoạt
- ADR 0007 — Dual-Layer CI Verification Gate (tiền lệ kiến trúc 2 lớp)
