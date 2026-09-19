# Copilot Cloud Agent Instructions — CCBA Legal Knowledge Spoke

## 1. Repository Purpose

This is the **CCBA Legal Knowledge Spoke**: a structured knowledge database of Vietnamese construction law, national technical regulations (QCVN), and national standards (TCVN). All content is packaged as **OKF v2.4 Universal Agent-Centric Bundles** (ADR 0021, 0034–0044). There is **no frontend/backend application code** — the repository exists solely to store normative legal knowledge and the Python pipeline that validates and converts it.

---

## 2. Directory Layout (Critical — Read First)

```
ccba-legal-knowledge/
├── legal_docs/                    # All knowledge bundles (Shallow Path — always at Level 1)
│   ├── 01_vbpl/                   # Laws, Decrees, Circulars (văn bản quy phạm pháp luật)
│   ├── 02_qcvn/                   # National Technical Regulations (QCVN)
│   ├── 03_tcvn/                   # National Standards (TCVN)
│   └── 04_appendices/             # Comparative matrices & VBHN appendices
├── legal_registry.yaml            # Master registry: all 53 documents with SHA-256, status, bundle_path
├── scripts/
│   ├── validate_legal_spoke.py    # Master CI validator (15 gates) — run this to check everything
│   ├── lint_visual_parity.py      # Gate 9: visual parity check (ADR 0029/0030)
│   ├── check_spoke_cleanliness.py # Script-count & cleanliness budget
│   └── check_hub_import_depth.py  # ADR 0044 hub import depth check
├── formulas/                      # Parametric engineering formula solvers (Python)
├── tests/                         # pytest suite (unit, integration, e2e)
│   ├── unit/                      # Formula solver tests
│   ├── integration/               # Converter, validator, consolidator tests
│   └── e2e/                       # Full document integrity audits
├── conftest.py                    # Blocks unscoped `pytest` to prevent context explosion
├── pytest.ini                     # pythonpath=., testpaths=tests
└── .github/workflows/legal-knowledge-ci.yml  # CI: validate_legal_spoke + 3 additional checks
```

### Each OKF v2.4 Bundle (`legal_docs/<cat>/<doc_slug>/`) contains:

```
<doc_slug>.md          # 100% verbatim normative body (extracted 1:1 from DOCX)
metadata.yaml          # RAG metadata, legal relationships, source_assets, SHA-256
clauses.json           # AST clause tree with severity ratings
index.md               # 2D navigation table of contents with anchor links
sources/               # REQUIRED: .docx and .pdf source files (git-ignored binaries)
tables/                # 2D lookup tables: *.csv, *.json, tables_catalog.json
figures/               # Visual cards: cards/hinh_*.md, figures_catalog.yaml
annexes/               # Technical normative annexes
templates/             # Atomic administrative form templates (mau_*.md) — NEVER leave empty
bang_so_sanh_thay_doi.md  # (VBHN only) Mandatory comparative change matrix at bundle root
```

---

## 3. Hard Rules — Never Violate

1. **NEVER write Markdown body text from LLM paraphrase.** All `<doc_slug>.md` body text must be extracted verbatim 1:1 from the official DOCX source via `python -m ccba_legal convert`. Paraphrasing normative text is strictly forbidden (ADR 0037, Gate 11 ≥ 98.0% verbatim parity).

2. **NEVER leave `templates/` empty.** Every bundle must contain at least a placeholder template (ADR 0021).

3. **NEVER store `.pdf` or `.docx` files in git.** Binary sources are `.gitignore`d and synced to Google Drive Vault. In the repository they exist only as SHA-256 references in `metadata.yaml` and `legal_registry.yaml`.

4. **NEVER use `\tag{...}` in KaTeX math.** Multi-line environments (`aligned`, `cases`, `gather`) must use `\qquad (X)` numbering to avoid rendering errors (ADR 0038, ADR 0044).

5. **NEVER store `.wmf` or `.emf` files.** Vector graphics must be converted to SVG + PNG ≥ 300 DPI (ADR 0040).

6. **Escape `-` and `+` bullet characters** inside Markdown tables using `\- ` and `&nbsp;&nbsp;\+ ` to preserve literal characters (ADR 0029).

7. **Multi-part documents** (e.g. QCVN 07:2023/BXD) must prefix table filenames with the part ID (e.g. `bang_p01_01.csv`) and declare `part_id` in `tables_catalog.json` (ADR 0044).

---

## 4. How to Run Tests

**Always scope pytest to a specific file.** Running bare `pytest` is blocked by `conftest.py` unless `CI=true` or `--allow-unscoped` is passed.

```bash
# Run a specific test file (required locally)
pytest tests/unit/test_formulas.py
pytest tests/integration/test_validate_legal_spoke.py

# Run full suite (CI only, or explicit override)
pytest --allow-unscoped
# or
CI=true pytest
```

**Available test markers:** `unit`, `solver`, `integration`, `e2e`, `milestone1`, `milestone2`

---

## 5. CI / Validation Workflow

The CI workflow (`.github/workflows/legal-knowledge-ci.yml`) runs on every push/PR to `main` via `ubuntu-latest`, Python 3.11, with dependencies `pyyaml python-docx`.

**To validate locally before committing:**

```bash
# Install minimal dependencies
pip install pyyaml python-docx

# Run all 15 CI gates (Registry, OKF Bundles, Tables, Fake Data, PDF Metadata,
# Pure Body, Cleanliness, Templates, Visual Parity, ADR Traceability,
# DOCX Verbatim Parity, Multimodal Assets, Table Grid, KaTeX, Provenance)
python scripts/validate_legal_spoke.py

# Check spoke cleanliness budget
python scripts/check_spoke_cleanliness.py

# Check hub import depth
python scripts/check_hub_import_depth.py

# Audit visual parity and footnotes (Gate 9)
python scripts/lint_visual_parity.py
```

**Acceptance criteria:** `0 Errors, 0 Warnings, 100% Visual Parity, ≥ 98.0% Verbatim Parity, 100% Valid Links, 100% PDF SHA-256 Match, 100% SVG/Cards Integrity`

---

## 6. Adding a New Legal Document (OKF v2.4 Pipeline)

**Step 0 — Acquire source files** (DOCX + PDF from [thuvienphapluat.vn](https://thuvienphapluat.vn)):
```bash
python -m ccba_legal ingest "<tvpl_url>" --category <01_vbpl|02_qcvn|03_tcvn> --upload-drive
```
If the ingest command is blocked (Cloudflare/Captcha), manually place the `.docx` and `.pdf` files into `legal_docs/<cat>/<doc_slug>/sources/` and proceed to Step 1.

**Step 1 — Convert to OKF v2.4 Bundle** (verbatim extraction, NEVER manual LLM writing):
```bash
python -m ccba_legal convert \
  --docx-path "legal_docs/<cat>/<doc_slug>/sources/<doc_slug>.docx" \
  --target-bundle-dir "legal_docs/<cat>/<doc_slug>"
```

**Step 2 — Consolidate amendments (if applicable)**:
```bash
python -m ccba_legal consolidate \
  --manifest legal_docs/02_qcvn/<slug>/patch_manifest.yaml \
  --base legal_docs/02_qcvn/<slug>/sources/<slug>_goc.md \
  --output legal_docs/02_qcvn/<slug>/
```

**Step 3 — Validate:**
```bash
python scripts/validate_legal_spoke.py
```

**Step 4 — Register** the new document in `legal_registry.yaml` with all required fields: `id`, `document_number`, `type`, `issued_by`, `issued_date`, `effective_date`, `status`, `title`, `bundle_path`, `source_url`, `sha256`, `pdf_sha256`.

---

## 7. Key Conventions

- **CSV encoding:** UTF-8 with BOM (`utf-8-sig`) is accepted by the validator.
- **Table CSV filenames:** `bang_<seq>.csv` (single-part) or `bang_<part_id>_<seq>.csv` (multi-part). Always declare in `tables_catalog.json`.
- **Figure cards:** `figures/cards/hinh_<slug>.md` must be declared 1:1 in `figures_catalog.yaml`.
- **`legal_registry.yaml`** is the single source of truth for all document metadata. The `bundle_path` field must end with `/` and point to a real directory.
- **`sources/` invariant:** Every bundle root must have a `sources/` subdirectory (even if empty in git, due to `.gitignore`).
- **`bang_so_sanh_thay_doi.md`** is mandatory at the bundle root for any `VBHN` (consolidated) document.
- **Heading anchors** follow the pattern `#dieu-X` and `#khoan-Y` (Vietnamese slugified).
- **KaTeX math** uses `$$...$$` blocks; `\left[`/`\right]` delimiters must be preserved exactly; figure captions `<!-- FIGURE: ... -->` must be outside `$$` blocks.

---

## 8. Formula Solvers (`formulas/`)

The `formulas/` package contains parametric engineering solvers (wind load, deflection, fire safety per TCVN 2737:2023, etc.). These are tested with `pytest tests/unit/`. Do not modify these unless the corresponding TCVN standard has been updated.

---

## 9. Archive & Scratch Files

The `.md/` directory (a hidden dotfolder named `.md`) is the processing workspace and is partially `.gitignore`d. The `archive/` directory inside `.md/` contains legacy scripts and audit files — do not modify or delete these.

The `scripts/` folder contains only active pipeline and validation scripts. Do not add utility or one-off scripts there; use `/tmp/` for temporary work.

---

## 10. Common Mistakes to Avoid

| Mistake | Correct Approach |
|---|---|
| Writing normative Markdown body from memory/LLM | Always use `python -m ccba_legal convert` |
| Running bare `pytest` locally | Use `pytest <specific_test_file.py>` |
| Adding new `.pdf`/`.docx` to git | Add SHA-256 to `metadata.yaml`; actual file goes to Google Drive Vault |
| Using `\tag{1}` in KaTeX | Use `\qquad (1)` at end of line instead |
| Leaving `templates/` directory empty | Add at least one `mau_*.md` placeholder |
| Storing `.wmf`/`.emf` graphics | Convert to SVG + PNG ≥ 300 DPI |
| Modifying unrelated tests | Never remove or edit existing tests |
