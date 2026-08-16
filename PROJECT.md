# Project: ccba-legal-knowledge Architecture & Governance Analysis

## Architecture
- Knowledge Base Spoke (OKF v2.0 Native-First)
- Shallow Path Structure (`legal_docs/`, `legal_registry.yaml`)
- Helper Scripts & Test Suite (`scripts/`, `tests/`)
- Platform Integration & Governance (`AGENTS.md`, `workspace_context.yaml`, `.agents/skills`, `.agents/workflows`, Hub Reuse-First Gate, AI Gateway)

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Knowledge Data Model & OKF v2.0 | Directory structure, legal_registry.yaml, OKF bundles, sync flow | M1 | R1 |
| 2 | Helper Scripts & Test Suite | scripts/, tests/, safe_pytest.py, validate_docs.py, update_legal_registry.py | M2 | R2 |
| 3 | Governance & Platform Integration | AGENTS.md, workspace_context.yaml, workflows, skills, Hub Reuse-First Gate, AI Gateway | M3 | R3 |
| 4 | Architecture Report Synthesis | Generate .md/codebase_architecture_analysis.md with Mermaid diagrams and compliance assessment | M4 | Final |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Survey Knowledge Data Model (R1) | Survey legal_docs/, legal_registry.yaml, OKF bundles, NotebookLM sync | none | DONE |
| 2 | Survey Helper Scripts & Test Suite (R2) | Survey scripts/, tests/, safe_pytest.py, validate_docs.py, update_legal_registry.py | none | DONE |
| 3 | Survey Governance & Platform (R3) | Survey AGENTS.md, workspace_context.yaml, skills, workflows, Hub gate, AI Gateway | none | DONE |
| 4 | Synthesize & Review Architecture Analysis Report | Produce .md/codebase_architecture_analysis.md and audit/review report | M1, M2, M3 | DONE |

## Code Layout
- `.md/codebase_architecture_analysis.md` (Target Report Output)
- `.agents/orchestrator/` (Orchestrator Workspace)
- `.agents/explorer_r1/`, `.agents/explorer_r2/`, `.agents/explorer_r3/` (Survey Workspaces)
- `.agents/writer_1/` (Writer Workspace)
- `.agents/reviewer_1/`, `.agents/reviewer_2/`, `.agents/auditor_1/` (Review & Audit Workspaces)
