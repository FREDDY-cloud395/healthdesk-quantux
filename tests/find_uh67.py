with open('scripts/build_full_scrumban_board.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '"UH-67"' in l:
        print(f"Line {i+1}: {l.strip()}")
        for k in range(max(0, i-2), min(len(lines), i+30)):
            print(f"{k+1}: {lines[k]}", end="")
        break
