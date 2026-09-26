with open('frontend/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Matriz de Habilitación' in l or 'Buscar cliente por nombre' in l:
        print(f"Line {i+1}: {l.strip()[:100]}")
        for k in range(max(0, i-5), min(len(lines), i+30)):
            print(f"{k+1}: {lines[k]}", end="")
        print("="*60)
