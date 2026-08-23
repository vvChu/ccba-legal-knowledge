"""CCBA Legislative Consolidator Package — Deterministic Legal Document Patching & VBHN Generation.

Thin Spoke wrapper delegating 100% to Hub SDK `ccba_legal.consolidator`.
"""

from __future__ import annotations

from ccba_legal.ast_parser import ASTNode
from ccba_legal.consolidator import (
    ConsolidationResult,
    DocMode,
    DualModeASTParser,
    LegislativeConsolidator,
    ManifestGenerator,
    PatchAction,
    PatchItem,
    PatchManifest,
    load_manifest,
)

__all__ = [
    "DocMode",
    "PatchAction",
    "PatchItem",
    "PatchManifest",
    "load_manifest",
    "ASTNode",
    "DualModeASTParser",
    "ConsolidationResult",
    "LegislativeConsolidator",
    "ManifestGenerator",
]
