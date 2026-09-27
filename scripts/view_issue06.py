import json

with open('docs/00_Tablero_Scrumban_Quantux.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'const INITIAL_BACKLOG = (\[[\s\S]*?\]);\s*const EPICS_DATA', text)
if match:
    tasks = json.loads(match.group(1))
    issue06 = next((t for t in tasks if t['id'] == 'ISSUE-06'), None)
    if issue06:
        print(json.dumps(issue06, indent=2, ensure_ascii=False))
