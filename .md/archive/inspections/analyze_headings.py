import json

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\md_all_headings.json', 'r', encoding='utf-8') as f:
    headings = json.load(f)

with open(r'd:\GitHubProjects\ccba-legal-knowledge\.md\md_headings_sample.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total headings in MD: {len(headings)}\n\n")
    for h in headings:
        out.write(f"L{h['line_num']} [H{h['level']}]: {h['text']}\n")

print(f"Written {len(headings)} headings to md_headings_sample.txt")
