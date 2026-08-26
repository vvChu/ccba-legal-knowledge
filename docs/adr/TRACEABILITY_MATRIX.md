# 🗺️ Living Architecture Traceability Matrix & Skill Radar

> **Mục tiêu:** Ma trận tự động theo dõi mối quan hệ giữa các **Quyết định Kiến trúc (ADR)** và các **Kỹ năng (Skills) / Hiến pháp Vận hành**.

*(Tệp này được biên dịch tự động bởi `scripts/sync_adr_matrix.py` — Không chỉnh sửa thủ công)*

---

| Mã ADR | Tiêu đề Quyết Định | Trạng thái | Tài Liệu & Skills Đang Tuân Thủ / Viện Dẫn |
| :--- | :--- | :---: | :--- |
| [ADR 0001](0001-vbhn-dual-track-provenance.md) | **Chiến lược Quản lý Văn bản Hợp nhất (VBHN) Dual-Track Provenance cho RAG & Thẩm tra Thiết kế** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0002](0002-structured-table-footnote-binding.md) | **Chuẩn hóa Ma trận Ràng buộc Footnote Bảng biểu (Structured Footnote Binding Matrix) cho AI QC Audit** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0003](0003-annex-normative-guardrails.md) | **Phân loại Siêu dữ liệu Phụ lục Bắt buộc vs. Tham khảo & Rào chắn Cưỡng chế Pháp lý** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0004](0004-structured-array-pointer-binding.md) | **Structured Array Pointer Binding Cho Chỉ Số Phụ Đa Tầng Trong Bảng Kỹ Thuật** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0005](0005-semantic-legal-uri-scheme.md) | **Semantic Legal URI Scheme & Registry Resolver Cho Viện Dẫn Đa Văn Bản** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0006](0006-legal-precedence-conflict-arbitration.md) | **Thứ Bậc Hiệu Lực Pháp Lý & Cơ Chế Phân Xử Xung Đột Trong AI QC Audits** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0007](0007-dual-layer-ci-verification-gate.md) | **Dual-Layer CI Verification Gate & Zero-Tolerance Quality Enforcement** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0008](0008-temporal-query-engine-point-in-time-auditing.md) | **Temporal Legal Query Engine & Point-in-Time Auditing Protocol** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0009](0009-ccba-legal-sdk-package-distribution.md) | **Phân Phối Tri Thức Pháp Lý Qua Monorepo Package `ccba-legal-sdk`** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0010](0010-four-layer-tvpl-vip-crawler-three-tier-fallback.md) | **Cơ Chế Cào TVPL 4 Lớp Tự Động Kết Hợp Đăng Nhập VIP Chrome CDP & Fallback 3 Tầng** | ✅ ACCEPTED | `.agents/skills/ccba-adr-lifecycle/SKILL.md`<br>`.agents/skills/ccba-ai-qc-batch-orchestrator/SKILL.md`<br>`.agents/skills/ccba-ai-qc-pccc-audit/SKILL.md`<br>`.agents/skills/excalidraw-diagram/SKILL.md`<br>`.agents/skills/improve-codebase-architecture/SKILL.md` |
| [ADR 0011](0011-atomic-clause-rag-chunking-strategy.md) | **Atomic Clause RAG Chunking Strategy for Clause-Based Standards** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0012](0012-clean-unified-notebooklm-ingestion-strategy.md) | **Clean Unified Repository Strategy for Google NotebookLM Ingestion** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0013](0013-dynamic-grace-period-compliance-gate.md) | **Dynamic Grace Period Compliance Gate for Retroactive Transition Auditing** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0014](0014-split-jurisdiction-pccc-audit-routing.md) | **Split Jurisdiction PCCC Audit Routing & Metadata Binding (Luật 55/2024 & NĐ 105/2025)** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0015](0015-unresolved-reference-metadata-fallback.md) | **Unresolved Normative Reference Fallback & Metadata Card Resolution** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0016](0016-dual-track-hybrid-pdf-anchor-of-trust.md) | **Dual-Track Hybrid Extraction & PDF Anchor of Trust Protocol** | ✅ ACCEPTED | `.agents/skills/ccba-legal-ingest/SKILL.md`<br>`AGENTS.md`<br>`CONTEXT.md`<br>`.md/knowledge/session_learnings.md` |
| [ADR 0017](0017-ast-structural-patching-consolidation-engine.md) | **AST Structural Patching via Semantic Action Tokens for Legislative Consolidation** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0018](0018-git-ratchet-multi-platform-knowledge-sync.md) | **Git-Ratchet Multi-Platform Knowledge Sync & Dual-Store Topology** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0019](0019-tiered-audit-persona-and-self-audit-affidavit.md) | **Tiered Audit Persona & Client Self-Audit Affidavit Engine** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0020](0020-hybrid-symbolic-formula-solver-engine.md) | **Hybrid Symbolic Formula Solver Engine for Normative Engineering Calculations** | ✅ ACCEPTED | `CONTEXT.md`<br>`.md/knowledge/session_learnings.md` |
| [ADR 0021](0021-okf-v2-2-pure-normative-body-legal-graph.md) | **OKF v2.2 Pure Normative Body & Legal Knowledge Graph Topology** | ✅ ACCEPTED | `.agents/skills/ccba-legal-ingest/SKILL.md`<br>`.agents/skills/ccba-legal-intel/SKILL.md`<br>`AGENTS.md`<br>`CONTEXT.md`<br>`.md/knowledge/session_learnings.md` |
| [ADR 0022](0022-okf-v2-2-qcvn-modular-annexes.md) | **OKF v2.2 QCVN Modular Technical Annexes & Active Core Pattern** | ✅ ACCEPTED | `.agents/skills/ccba-legal-ingest/SKILL.md`<br>`.md/knowledge/session_learnings.md` |
| [ADR 0023](0023-full-comprehensive-notebooklm-ultra-ingestion.md) | **Full Comprehensive NotebookLM Ingestion Strategy for Ultra Tier** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0024](0024-dual-track-provenance-footnote-anchoring.md) | **Dual-Track Provenance with Footnote Anchor for Consolidated Legal Norms** | ✅ ACCEPTED | `.agents/skills/legal-advisor/SKILL.md`<br>`CONTEXT.md` |
| [ADR 0025](0025-strict-provenance-enactment-gate.md) | **Strict Zero-Tolerance Provenance Enactment Gate for Legal Ingestion** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0026](0026-package-based-downstream-knowledge-distribution.md) | **Package-Based Downstream Legal Knowledge Distribution via ccba-legal-intel SDK** | ✅ ACCEPTED | `CONTEXT.md` |
| [ADR 0027](0027-tcvn-qcvn-specialized-ast-converter.md) | **Specialized AST Converter for QCVN & TCVN Standards** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0028](0028-atomic-template-form-extraction.md) | **Atomic Template Form Extraction & Table Isolation** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
| [ADR 0029](0029-verbatim-bullet-parity-and-escaping.md) | **Verbatim Bullet Parity & Markdown Escaping Protocol** | ✅ ACCEPTED | `.agents/skills/ccba-legal-ingest/SKILL.md`<br>`AGENTS.md`<br>`.md/knowledge/session_learnings.md` |
| [ADR 0030](0030-visual-parity-and-2d-navigation-matrix.md) | **Visual Parity & 2D Annex Navigation Matrix for Large Standards** | ✅ ACCEPTED | `.agents/skills/ccba-legal-ingest/SKILL.md`<br>`AGENTS.md`<br>`.md/knowledge/session_learnings.md` |
| [ADR 0031](0031-tvpl-vip-digital-pdf-priority-and-session-engine.md) | **TVPL VIP Digital Vector PDF Priority & Persistent Session Engine** | ✅ ACCEPTED | `.agents/skills/ccba-legal-ingest/SKILL.md`<br>`.agents/skills/ccba-legal-intel/SKILL.md`<br>`.md/knowledge/session_learnings.md` |
| [ADR 0032](0032-catalog-query-gate-reuse-first-enforcement.md) | **— Catalog Query Gate: Cưỡng Chế Reuse-First bằng Cơ Chế Verify-Based** | ✅ ACCEPTED | `.agents/skills/ccba-adr-lifecycle/SKILL.md`<br>`CONTEXT.md`<br>`.md/knowledge/session_learnings.md` |
| [ADR 0033](0033-spoke-md-directory-hygiene-and-archiving.md) | **Spoke .md Directory Hygiene & Archiving Structure** | ✅ ACCEPTED | `.md/knowledge/session_learnings.md` |
| [ADR 0034](0034-okf-v2-3-dual-engine-technical-standards.md) | **OKF v2.3 Dual-Engine Technical Standards Paradigm (Parametric Visual Cards, Lossless Table Matrices & Deterministic Solvers)** | ✅ ACCEPTED | *Chưa có liên kết trực tiếp* |
