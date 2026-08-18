import sys
sys.stdout.reconfigure(encoding='utf-8')
import ast
from pathlib import Path

tests_dir = Path(r"d:\GitHubProjects\ccba-legal-knowledge\tests")

for py_file in tests_dir.glob("test_*.py"):
    text = py_file.read_text(encoding="utf-8")
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            # Check args
            args = [arg.arg for arg in node.args.args]
            if "qa_benchmark_data" in args or "clauses_ast_data" in args or "qa_benchmark" in node.name or "clause" in node.name:
                doc = ast.get_docstring(node) or ""
                print(f"{py_file.name}::{node.name}")
                print(f"   Args: {args}")
                print(f"   Doc: {doc.strip()}")
