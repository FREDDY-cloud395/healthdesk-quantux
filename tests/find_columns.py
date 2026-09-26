import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_full_scrumban_board.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'En Revisi' in l or 'Revisión (Aceptación' in l or ('column' in l.lower() and ('qa' in l or 'progress' in l)):
        print(f"{i+1}: {l.strip()[:140]}")
