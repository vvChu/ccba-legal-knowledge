# Specification: Deterministic Zero-Data-Loss & OKF Legal Knowledge Pipeline

## Problem Statement

Currently, when ingesting complex Vietnamese legal, technical, and building code documents (such as QCVN 06:2022/BXD, circulars, and national standards) from official `.docx` files into Markdown-based Open Knowledge Format (OKF) bundles, legacy parsers operate on a "best-effort" heuristic approach. This leads to critical silent failures:
1. **Silent Data Loss:** Approximately 25% of body paragraphs (e.g., short clauses, mathematical explanations, bullet lists) and split tables across page breaks are silently dropped during parsing.
2. **Table Syntax Bleed & Destruction:** Complex tables with merged footnote rows are flattened into broken single-line markdown strings or duplicate footnotes across columns.
3. **Empty Anchor Navigation Failure:** Inserting empty HTML anchor tags (`<a id="..."></a>`) on separate lines causes Chromium-based WebViews to calculate bounding boxes with 0px height, causing link jumps to abort.
4. **Sub-dot Heading Truncation:** Paragraph number tokens like `1.4.1` lose their intermediate dot (`1.41`), corrupting AST tree generation and search indexing.
5. **Lack of Integrated Legal Consolidation (VBHN):** Original texts and amendment circulars remain completely disconnected, forcing AI agents to perform fragile runtime map-reduction which causes hallucinations and severe context waste.
6. **Loss of Table Condition Bindings:** Numerical values tied to mandatory footnote conditions (e.g., `1 400 5)`) are stripped into flat strings or raw numbers, causing AI QC Audit pipelines to evaluate parameters without enforcing requisite safety conditions.

---

## Solution

Build and standardize a **Deterministic Zero-Data-Loss Legal Knowledge Processing Pipeline** across the CCBA platform. The pipeline replaces heuristic parsing with a strict 4-stage deterministic engine:
1. **Sequential Body Element Trace:** Sequentially iterates 100% of paragraph (`CT_P`) and table (`CT_Tbl`) elements directly from the document XML tree, guaranteeing zero dropped text.
2. **Inlined Semantic Anchor Injection:** Embeds canonical anchors directly into markdown header lines (`##### <a id="muc-x-y-z" name="muc-x-y-z"></a>X.Y.Z`) ensuring pixel-perfect browser and IDE scroll navigation.
3. **2D GFM Table Engine with Footnote Isolation:** Converts complex tables into valid GitHub Flavored Markdown 2D pipe grids with blank line isolation, extracts merged footnote rows into standalone markdown text, and turns single-column layout tables into clean bulleted text.
4. **Structured Footnote Binding Matrix (ADR 0002):** Enriches table JSON schemas with structured cell metadata (`numeric_value`, `unit`, `condition_refs`) coupled to classified footnote conditions (`normative_condition`, `exception`, `definition`).
5. **Dual-Track Provenance & Auto-VBHN Consolidation (ADR 0001):** Generates pre-consolidated legal text (`*_hop_nhat_*.md`) embedding amendment directives into base clauses with standard GFM callouts while preserving standalone original and amendment files.
6. **Annex Legal Enforceability Guardrails (ADR 0003):** Annotates AST clause nodes with `normative_status` (`mandatory` vs `informative`) to prevent AI QC agents from raising false positive defects against informative guidelines.
7. **Deterministic Zero Data Loss Verification Gate:** Enforces an automated counter-check asserting that 100% of paragraphs, headings, and table cells from the source document exist in the generated bundle before passing CI/CD.

---

## User Stories

1. As a Legal Knowledge Engineer, I want the document parser to sequentially extract every paragraph and table without regex filtering, so that zero regulatory clauses are dropped.
2. As an AI Agent developer, I want all markdown anchors to be inlined within heading tags, so that clicking clause links in IDEs and WebViews accurately navigates to the exact target line.
3. As a Construction QC Auditor, I want technical tables to render as clean 2D GFM pipe tables with isolated footnotes, so that building parameters are legible and machine-parseable.
4. As an AI QC Audit Engine, I want table cells to provide structured numbers, units, and condition references, so that I can automatically verify both numerical limits and prerequisite safety conditions.
5. As a Legal Researcher, I want access to pre-consolidated legal texts (VBHN) with callouts for amended clauses, so that I can immediately review current in-force regulations without manually cross-referencing multiple circulars.
6. As a Compliance Officer, I want original and amending legal documents to remain preserved alongside the consolidated text, so that historical point-in-time legal provenance is maintained.
7. As an AI Agent performing automated drawing checks, I want AST clause nodes to clearly flag informative annexes as non-enforceable, so that I do not flag false-positive compliance violations based on illustrative diagrams.
8. As a Spoke Maintainer, I want an automated integrity verification script that validates paragraph counts, table cell counts, and anchor resolution, so that broken or incomplete bundles are immediately caught and rejected.
9. As a Platform Core Developer, I want parser scripts to be reusable across all legal spokes via a standardized CLI interface, so that new regulations can be ingested with zero manual code modifications.
10. As an LLM RAG Pipeline, I want high-speed access to a unified tables catalog, so that table schemas and normative conditions can be retrieved in sub-millisecond time.

---

## Implementation Decisions

### 1. Document Parsing & Structure Preservation Engine
- The parser must traverse document body elements strictly in document order (`CT_P` and `CT_Tbl`).
- Text paragraphs that do not match primary section heading patterns must be preserved as standard body paragraphs rather than silently discarded.
- Numbering normalization routines must protect multidot sequences (`1.4.1` through `1.4.72`), preventing truncation to two-level numbers.

### 2. Markdown & Inlined Semantic Anchor Standardization
- Anchor tags must be formatted as `<a id="slug" name="slug"></a>` and placed directly inside the markdown heading prefix (`#`, `##`, `###`, `####`, `#####`).
- Headings and tables must be surrounded by blank lines (`\n\n`) to conform to RFC markdown rendering specifications.

### 3. Structured Footnote Binding Matrix (ADR 0002)
- Table JSON schemas will retain backward compatibility with raw string rows while introducing `structured_rows`:
  ```json
  {
    "raw": "1 400 5)",
    "numeric_value": 1400.0,
    "unit": "m2",
    "condition_refs": [5]
  }
  ```
- Footnotes will be categorized into `normative_condition`, `exception`, and `definition`.

### 4. Consolidated Legal Text Generation (ADR 0001)
- VBHN generation will parse amendment directives categorized into 4 legal actions: `modify`, `add`, `repeal`, `replace`.
- Modifications will be injected in-place with `> [!NOTE]` callouts; repeals will be marked with `> [!WARNING]`.

### 5. Legal Enforceability Guardrails (ADR 0003)
- All clause AST nodes will include `normative_status` (`mandatory` or `informative`) and `legal_enforceability` (`true` or `false`).
- Normative annexes (e.g., Annexes A to H) are marked mandatory; informative annexes (e.g., Annex I - Illustrations) are marked informative.

---

## Testing Decisions

### Seam Architecture
- **Highest Seam: `LegalSpokeValidator` & `KnowledgeIntegrityAuditor`**
  Testing must occur at the boundary of the complete OKF bundle output rather than internal parser private functions.

### Good Test Principles
- **Black-Box Determinism:** Tests verify that given a canonical `.docx`, the produced markdown, JSON tables, and AST clauses match exact mathematical counts and schema invariants.
- **Zero Tolerance on Data Loss:** Assertions require `retained_paragraphs == total_docx_paragraphs` and `retained_cells == total_docx_cells`.
- **Bidirectional Link Soundness:** Assertions require `broken_links == 0` across all cross-references.

---

## Out of Scope
- Direct extraction from scanned raster images (OCR of non-searchable PDF scans is handled upstream by dedicated Vision Preprocessor skills).
- Automatic legal interpretation or reasoning on conflicting inter-ministerial circulars (reserved for legal experts).

---

## Further Notes
- This specification formalizes the architectural decisions approved in ADR 0001, ADR 0002, and ADR 0003.
- All tools and skills updated under this spec will follow the CCBA Platform Reuse-First Gate.
