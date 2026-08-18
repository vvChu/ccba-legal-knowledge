# E2E Test Infra: QCVN 06:2022/BXD & Amendment 1:2023 OKF Legal Knowledge Bundle

## Test Philosophy
- **Opaque-Box & Requirement-Driven**: Tests are formulated purely from the ground truth authoritative legal documents (`qcvn_06_2022_bxd.docx`, `sua_doi_1_2023_qcvn_06_2022_bxd.docx`) and regulatory specifications. No reliance on intermediate conversion scripts or implementation internal heuristics.
- **Zero Data Loss Invariant**: 100% preservation of all normative text paragraphs, technical tables, footnotes, and amendment directives.
- **Methodology**: Systematic 4-tier test architecture using Category-Partition Testing, Boundary Value Analysis (BVA), Pairwise Combinatorial Testing, and Real-World Workload Scenarios.

## Feature Inventory & Test Coverage Matrix
| # | Feature | Requirement Source | Tier 1 (Count) | Tier 2 (Count) | Tier 3 (Pairwise) | Tier 4 (Scenario) |
|---|---------|--------------------|:--------------:|:--------------:|:-----------------:|:-----------------:|
| F1 | Base Text & Appendix Complete Extraction | ORIGINAL_REQUEST §R1 | 10 | 10 | ✓ | ✓ |
| F2 | Heading & Numbering Normalization | ORIGINAL_REQUEST §R1 | 8 | 8 | ✓ | ✓ |
| F3 | Heading Hierarchy Structuring (H1-H5) | ORIGINAL_REQUEST §R1 | 6 | 6 | ✓ | ✓ |
| F4 | 64 Canonical Table Extraction | ORIGINAL_REQUEST §R2 | 10 | 10 | ✓ | ✓ |
| F5 | JSON & CSV Clean Schemas | ORIGINAL_REQUEST §R2 | 8 | 8 | ✓ | ✓ |
| F6 | Missing Tables Addition (E.4a/b, G.2a/b) | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| F7 | Embedded Markdown Table Repair | ORIGINAL_REQUEST §R2 | 8 | 8 | ✓ | ✓ |
| F8 | Footnote Preservation | ORIGINAL_REQUEST §R2 | 6 | 6 | ✓ | ✓ |
| F9 | Amendment Text & Directives | ORIGINAL_REQUEST §R3 | 8 | 8 | ✓ | ✓ |
| F10 | Amendment Table 10 GFM Grid | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| F11 | Amendment Clause Anchors & Cross-links | ORIGINAL_REQUEST §R3 | 6 | 6 | ✓ | ✓ |
| F12 | AST Clause Tree Synchronization | ORIGINAL_REQUEST §R4 | 6 | 6 | ✓ | ✓ |
| F13 | QA Benchmark Synchronization | ORIGINAL_REQUEST §R4 | 6 | 6 | ✓ | ✓ |
| F14 | Verification Script Refinement | ORIGINAL_REQUEST §R5 | 5 | 5 | ✓ | ✓ |
| F15 | E2E Spoke & Integrity Gate | ORIGINAL_REQUEST §R5 | 5 | 5 | ✓ | ✓ |
| F16 | Forensic Integrity Audit & Matrix | ORIGINAL_REQUEST §R5 | 5 | 5 | ✓ | ✓ |
| **Total** | **16 Features** | | **107 tests** | **107 tests** | **16 pairs** | **8 scenarios** |

## Test Architecture

### Directory Layout
```
tests/
├── conftest.py                      # Shared fixtures (DOCX parser helpers, bundle path resolvers, AST loaders)
├── test_tier1_feature_coverage.py   # Tier 1: Feature Coverage (Text parity, 64 tables, directives, schemas)
├── test_tier2_boundaries.py         # Tier 2: Boundary, corner-cases, precision, footnotes, escape characters
├── test_tier3_cross_features.py     # Tier 3: Cross-feature combinations (Table-to-clause, SD1-to-Base cross-links)
├── test_tier4_real_world.py         # Tier 4: Real-world RAG retrieval, chunking, full bundle spoke validation
└── run_e2e_tests.py                 # Standalone CLI test runner and report generator
```

### Test Invocation & Semantics
1. Standard Pytest Runner:
   ```powershell
   python -m pytest tests/ -v --tb=short
   ```
2. Custom Comprehensive Test Runner:
   ```powershell
   python tests/run_e2e_tests.py
   ```
   - Exit code `0` = All tests pass (100% Zero Data Loss & Parity).
   - Exit code `1` = One or more test failures detected (with detailed failure analysis).

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Complexity | Description |
|---|----------|--------------------|------------|-------------|
| S1 | End-to-End Fire Compartment Query | F1, F3, F4, F12, F13 | High | RAG retrieval simulation for fire resistance ratings of fire separation walls (Bảng 1, Điều 2.3). |
| S2 | Smoke Control & Extraction Formula Lookup | F1, F3, F7, F8, F12 | High | Retrieval of Appendix D formula calculations and technical limits for smoke evacuation fans. |
| S3 | Technical Table Parameter Extraction (Bảng E.4a/E.4b) | F4, F5, F6, F7, F8 | High | Querying fire separation distances for industrial and residential buildings across varying fire hazard categories. |
| S4 | Amendment 1:2023 Water Flow Override (Bảng 10) | F9, F10, F11, F15 | High | Verifying that queries on fire water flow rates correctly resolve to the replacement Bảng 10 grid in Sửa đổi 1:2023. |
| S5 | Bidirectional Legal Cross-Reference Navigation | F2, F3, F11, F12, F13 | Medium | Navigating from Sửa đổi 1:2023 modified clauses back to base QCVN 06:2022 anchors and vice versa. |
| S6 | AST Clause Tree Hierarchy Traversal | F1, F2, F3, F12 | Medium | Validating hierarchical tree traversal from Chapter 1 down to 4-level leaf subclauses. |
| S7 | Footnote Regulatory Interpretation | F4, F5, F8, F13 | Medium | Querying special conditions and exceptions specified in technical table footnotes. |
| S8 | Full OKF Spoke & Registry Verification | F14, F15, F16 | High | Complete automated gate execution via `validate_legal_spoke.py` and `verify_knowledge_integrity.py`. |

## Coverage Thresholds
- **Tier 1 (Feature Coverage)**: ≥5 test cases per feature (Total: ≥100 test cases).
- **Tier 2 (Boundary & Corner Cases)**: ≥5 test cases per feature (Total: ≥100 test cases).
- **Tier 3 (Cross-Feature Combinations)**: Pairwise coverage across all 16 major feature interactions.
- **Tier 4 (Real-World Scenarios)**: 8 realistic application scenarios (RAG retrieval, table lookup, amendment override, spoke validation).
- **Total Minimum Test Count**: ≥230 test assertions.
