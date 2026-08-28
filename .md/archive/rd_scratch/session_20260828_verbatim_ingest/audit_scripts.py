import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

hub_root = Path(r"D:\GitHubProjects\ccba-agent-platform")
wf_dir = hub_root / ".agents" / "workflows"
skill_dir = hub_root / ".agents" / "skills"

# Match python commands in markdown codeblocks
python_cmd_pattern = re.compile(r"python(?:3)?\s+([^\n\r]+)")

all_files = list(wf_dir.glob("*.md")) + list(skill_dir.glob("**/SKILL.md"))
findings = []

for f in all_files:
    lines = f.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines, 1):
        m = python_cmd_pattern.search(line)
        if m:
            cmd = m.group(1).strip()
            findings.append({
                "file": f.relative_to(hub_root).as_posix(),
                "line": idx,
                "cmd": cmd,
                "line_text": line.strip()
            })

print(f"Total python command references found: {len(findings)}")

# Filter workflows specifically
wf_findings = [x for x in findings if x["file"].startswith(".agents/workflows")]
print(f"Workflow python commands: {len(wf_findings)}")
print("=" * 80)
for w in sorted(wf_findings, key=lambda x: (x["file"], x["line"])):
    print(f"{w['file']}:{w['line']} -> python {w['cmd']}")
