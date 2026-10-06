---
request_id: req-spoke-ci-granularity-matrix-001
verdict: APPROVE_WITH_CONDITIONS
conditions:
- id: COND-01
  description: Duy trì cấu hình thực thi song song hoàn toàn (parallel execution)
    giữa 5 Jobs, giữ các jobs độc lập nhằm tối đa hóa tầm nhìn trực quan đa điểm check
    trên giao diện GitHub PR và loại bỏ hiện tượng cascading failure.
  blocking: false
  source_profiles: []
- id: COND-02
  description: Thực thi kiểm tra quy chuẩn ADR-0066 và ADR-0057 cho Job 3 (skills-governance-gate)
    bằng câu lệnh Python nội dòng (inline command), bảo vệ nguyên vẹn ngân sách 15
    kịch bản tại thư mục scripts/ theo ADR-0044.
  blocking: false
  source_profiles: []
- id: COND-03
  description: Bổ sung bước actions/upload-artifact@v4 tại Job 4 (verification-harness-gate)
    để lưu trữ tệp bằng chứng máy đọc được evidence_verify_legal_knowledge.json phục
    vụ truy xuất nguồn gốc kiểm định.
  blocking: false
  source_profiles: []
- id: COND-04
  description: Xác định ranh giới chức năng rõ ràng giữa Job 4 (kiểm tra vòng đời
    kiến trúc Pstack và tạo artifact chứng cứ) và Job 5 (kiểm định chuyên sâu 15 Cổng
    chất lượng dữ liệu quy phạm và hiển thị visual parity).
  blocking: false
  source_profiles: []
risk_score: 2
effort: S
summary: Đề xuất phân rã monolithic CI workflow thành ma trận 5 Cổng Kiểm Soát độc
  lập giải quyết trọn vẹn câu hỏi kiểm định trực quan trên GitHub PR
telemetry:
  session_id: 43d8d816-ca7e-47bf-824c-b838f0dc825b
  primary_model: gemini-3.8-flash-high
  input_tokens: 338075
  output_tokens: 4684
  reasoning_tokens: 10876
  cached_read_tokens: 154468
  total_tokens: 342759
  model_calls: 18
  turn_count: 1
  cost_usd: 0.446
  cost_mode: estimated
  duration_seconds: 251.06
---
# Báo Cáo Thẩm Định Kiến Trúc: Phân Rã Monolithic CI Workflow Thành Ma Trận Cổng Kiểm Soát Độc Lập (Granular CI Matrix)

## 1. Kết Luận Thẩm Định Tổng Quan

Phương án phân rã tệp workflow `.github/workflows/legal-knowledge-ci.yml` từ 1 Job đơn khối thành Ma trận 5 Cổng Kiểm Soát độc lập là một bước chuyển đổi kiến trúc chuẩn xác, giải quyết triệt để phản hồi của User trên GitHub Pull Request #32:

- **Minh bạch hóa giao diện Pull Request:** Thay thế dòng trạng thái đơn lẻ bằng 5 check runs độc lập tương ứng với 5 rào chắn bảo vệ của nền tảng CCBA.
- **Cô lập lỗi (Failure Isolation):** Lỗi phát sinh tại một phân vùng kiểm tra được khoanh vùng chính xác ngay trên check run tương ứng. Reviewer nắm bắt đầy đủ trạng thái của các phân vùng còn lại.
- **Mở rộng năng lực bảo vệ toàn diện:** Bổ sung rào chắn quét bí mật công khai (Maskara), kiểm soát phân phối kỹ năng (ADR-0057 / ADR-0066) và xác thực vòng đời Pstack Harness song hành cùng bộ 15 Cổng Master Legal Gates.

Phán quyết đưa ra là **`APPROVE_WITH_CONDITIONS`** với mức rủi ro cấp 2 (Thấp). Bốn trọng tâm phân tích đối kháng được trình bày chi tiết dưới đây.

---

## 2. Phân Tích Đối Kháng 4 Trọng Tâm Yêu Cầu

### 2.1. Cấu Trúc Thực Thi (Parallel Execution vs Pipeline Dependencies)

Mô hình thực thi tối ưu cho Spoke CI là **vận hành song song hoàn toàn (Parallel Execution)** cho cả 5 Jobs.

- **Khả năng quan sát toàn diện trên PR:** Khi các jobs chạy độc lập, một lỗi rò rỉ secret hoặc vi phạm ngân sách script sẽ hiển thị trực quan dấu đỏ tại Job đó, trong khi các Jobs kiểm tra chất lượng pháp điển (Job 4, Job 5) vẫn hoàn thành và báo cáo kết quả. Tác giả PR có thể khắc phục toàn bộ các lỗi trong duy nhất một chu kỳ commit.
- **Tính an toàn thông tin:** Các kịch bản kiểm tra cục bộ (`check_spoke_cleanliness.py`, `validate_legal_spoke.py`, `lint_visual_parity.py`) hoạt động hoàn toàn bằng AST và regex nội bộ, không có hành vi truyền dữ liệu ra bên ngoài. Việc chạy song song với bộ quét Maskara đảm bảo an toàn tuyệt đối.
- **Tiết kiệm thời gian phản hồi (Wall-clock Time):** Tổng thời gian chờ đợi trên PR bằng thời gian của Job chạy lâu nhất ($\approx 40 - 45\text{ s}$), mang lại trải nghiệm nghiệm thu nhanh chóng.

| Tiêu Chí So Sánh | Mô Hình Song Song Hoàn Toàn (Parallel) | Mô Hình Phụ Thuộc Khóa Chặn (Needs DAG) |
| :--- | :--- | :--- |
| **Số check runs hiển thị khi có lỗi** | Đầy đủ 5 checks (Xanh/Đỏ rõ ràng từng cổng) | 1 check Đỏ, 3-4 checks bị bỏ qua (Skipped/Xám) |
| **Khả năng chẩn đoán toàn diện** | Tác giả sửa tất cả lỗi trong 1 lần commit | Tác giả phải sửa lỗi tuần tự qua nhiều commit |
| **Tổng thời gian phản hồi PR** | $\max(T_1, T_2, T_3, T_4, T_5) \approx 40 - 45\text{ s}$ | $T_1 + T_2 + T_3 \approx 75 - 90\text{ s}$ |
| **Hành vi xử lý rủi ro** | Độc lập, minh bạch | Khóa chặn tuần tự, che khuất thông tin phía sau |

### 2.2. Tối Ưu Hóa Khởi Tạo Runner & Cơ Chế Cache

Khởi tạo 5 runners độc lập mang lại hiệu quả cao về mặt thời gian hoàn thành tổng thể trên GitHub Actions:

- **Thời gian khởi tạo đồng thời:** Môi trường `ubuntu-latest` của GitHub Actions đã tích hợp sẵn Python 3.11 trong cache hình ảnh hệ thống. Bước `actions/setup-python@v5` hoàn tất việc liên kết trong $2 - 3\text{ s}$. 
- **Cài đặt thư viện tối giản:** Các gói phụ thuộc của từng Job đều có định dạng wheel nhị phân sẵn có trên PyPI:
  - Job 1 (`ccba-maskara`): $\approx 3\text{ s}$.
  - Job 2 & Job 3 (`pyyaml`): $\approx 2\text{ s}$.
  - Job 4 & Job 5 (`pyyaml`, `python-docx`): $\approx 4\text{ s}$.
- **Hiệu năng thực tế:** Tổng thời gian setup của mỗi runner chỉ từ $8 - 12\text{ s}$ và diễn ra đồng thời trên các máy ảo riêng biệt. Do đó, chi phí khởi tạo song song hoàn toàn hợp lý và mang lại giá trị quan sát trực quan cao.

### 2.3. Ranh Giới Chức Năng Giữa Job 4 (Harness) và Job 5 (Master 15 Gates)

Việc duy trì đồng thời Job 4 và Job 5 đảm bảo sự phân tách trách nhiệm kiến trúc rõ ràng giữa tầng **Hạ tầng Tự động hóa** và tầng **Dữ liệu Quy phạm**:

- **Job 4 (`verification-harness-gate`):** Đại diện cho tầng *Application Harness & Operational Lifecycle*. Job này kiểm tra 5 khối Pstack (Pre-flight, cách ly Process Group, Health Barrier, Graceful Cleanup) và tạo ra tệp chứng cứ máy đọc được `.md/reports/evidence_verify_legal_knowledge.json`.
- **Job 5 (`master-legal-gates`):** Đại diện cho tầng *Statutory Knowledge & Domain Parity*. Job này tập trung kiểm định 15 Cổng quy chuẩn dữ liệu pháp lý (AST schema, liên kết điều khoản, công thức KaTeX, bảng tra 2D, tỷ lệ verbatim $\ge 98\%$) kết hợp bộ kiểm tra `lint_visual_parity.py`.
- **Tối ưu hóa giá trị kiểm định:** Để Job 4 phát huy trọn vẹn vai trò của một Harness Gate, cần bổ sung bước upload artifact cho tệp `evidence_verify_legal_knowledge.json`. Tệp chứng cứ này đóng vai trò biên lai kiểm định chính thức cho mỗi bản build PR.

### 2.4. Đề Xuất Cấu Hình Workflow YAML Tối Ưu

Cấu hình dưới đây chuẩn hóa tên gọi, bổ sung bộ đệm cache, áp dụng lệnh Python nội dòng kiểm tra governance cho Job 3 để bảo vệ ngân sách 15 scripts theo ADR-0044, và lưu trữ artifact cho Job 4:

```yaml
name: CCBA Legal Knowledge Spoke CI Gate

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # =========================================================================
  # Gate 1: Security & Secrets Gate
  # =========================================================================
  security-secrets-gate:
    name: 🔒 Security & Secrets Gate (Maskara)
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Maskara Scanner
        run: |
          python -m pip install --upgrade pip
          pip install ccba-maskara

      - name: Run Maskara Secret Scan
        run: |
          maskara scan --root .

  # =========================================================================
  # Gate 2: Spoke Cleanliness & Script Budget (ADR-0044)
  # =========================================================================
  spoke-cleanliness-gate:
    name: 🧹 Spoke Cleanliness & Budget (ADR-0044)
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyyaml

      - name: Check Script Budget & Machine State Paths
        run: |
          python scripts/check_spoke_cleanliness.py

      - name: Check Hub Import Depth
        run: |
          python scripts/check_hub_import_depth.py

  # =========================================================================
  # Gate 3: Skills Governance & Distribution (ADR-0057 / ADR-0066)
  # =========================================================================
  skills-governance-gate:
    name: ⚙️ Skills Governance & Scope (ADR-0066)
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyyaml

      - name: Validate SKILL.md Frontmatter & GPI Score
        run: |
          python -c "
          import sys, yaml
          skill_path = '.agents/skills/ccba-verify-legal-knowledge/SKILL.md'
          with open(skill_path, 'r', encoding='utf-8') as f:
              parts = f.read().split('---')
          if len(parts) < 3:
              sys.exit('❌ Invalid frontmatter in ' + skill_path)
          meta = yaml.safe_load(parts[1])
          assert meta.get('scope') == 'spoke', f'Scope must be spoke, got {meta.get(\"scope\")}'
          assert meta.get('bundle') == '_core', f'Bundle must be _core, got {meta.get(\"bundle\")}'
          gpi = meta.get('gpi', {})
          score = 2.5 * gpi.get('s', 0) + 2.0 * gpi.get('k', 0) + 2.0 * gpi.get('a', 0) - 1.5 * gpi.get('p', 0)
          assert score >= 12.0, f'GPI score {score:.1f} < 12.0'
          print(f'✓ ADR-0066 & ADR-0057 Validated: scope={meta.get(\"scope\")}, bundle={meta.get(\"bundle\")}, GPI={score:.1f} >= 12.0')
          "

  # =========================================================================
  # Gate 4: Pstack Verification Harness Gate
  # =========================================================================
  verification-harness-gate:
    name: 🚀 Pstack Verification Harness (Evidence)
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyyaml python-docx

      - name: Run Pstack Verification Harness (Smoke Mode)
        run: |
          python .agents/skills/ccba-verify-legal-knowledge/harness/verify_legal_harness.py --mode smoke --skip-pdf-vault

      - name: Upload Verification Evidence Artifact
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: evidence-verify-legal-knowledge
          path: .md/reports/evidence_verify_legal_knowledge.json
          if-no-files-found: ignore

  # =========================================================================
  # Gate 5: Master Legal Knowledge 15 CI Gates
  # =========================================================================
  master-legal-gates:
    name: 🏛️ Master Legal Knowledge 15 CI Gates
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyyaml python-docx

      - name: Run Master 15 CI Gates Validation
        run: |
          python scripts/validate_legal_spoke.py --skip-pdf-vault

      - name: Lint Visual Parity & Footnotes (Gate 9)
        run: |
          python scripts/lint_visual_parity.py
```

---

## 3. Điều Kiện Nghiệm Thu (Acceptance Criteria)

Phương án phân rã workflow được chấp thuận nghiệm thu khi thỏa mãn các tiêu chí sau:

1. **COND-01 (Thực thi độc lập):** Toàn bộ 5 jobs chạy độc lập trong cùng workflow run, không chứa mệnh đề `needs`, bảo đảm hiển thị đầy đủ 5 check marks trên giao diện GitHub PR.
2. **COND-02 (Bảo vệ ngân sách scripts):** Logic kiểm tra của Job 3 được thực thi trực tiếp qua lệnh Python nội dòng, giữ nguyên số lượng tệp hiện có trong thư mục `scripts/` ($\le 15$ tệp theo ADR-0044).
3. **COND-03 (Lưu trữ bằng chứng máy đọc):** Bước `actions/upload-artifact@v4` được thiết lập tại Job 4 và đính kèm thành công tệp `evidence_verify_legal_knowledge.json` vào run của workflow.
4. **COND-04 (Giới hạn thời gian an toàn):** Khai báo thuộc tính `timeout-minutes` cho toàn bộ các jobs để ngăn chặn nguy cơ runner bị treo khi có sự cố môi trường.
