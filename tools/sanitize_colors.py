import os

files_to_clean = [
    os.path.join('frontend', 'index.html'),
    os.path.join('frontend', 'js', 'app.js'),
    os.path.join('frontend', 'css', 'styles.css')
]

for fp in files_to_clean:
    if not os.path.exists(fp):
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Emerald / saturated teal
    content = content.replace('#00A896', '#0F172A')
    content = content.replace('#008F80', '#1E293B')
    content = content.replace('#009684', '#1E293B')
    content = content.replace('#00875A', '#0F172A')
    content = content.replace('#006644', '#0F172A')
    content = content.replace('rgba(0,168,150,', 'rgba(15,23,42,')
    content = content.replace('rgba(0, 168, 150,', 'rgba(15, 23, 42,')
    content = content.replace('rgba(0,135,90,', 'rgba(15,23,42,')

    # Electric Blue
    content = content.replace('#0052CC', '#0F172A')
    content = content.replace('#2563EB', '#0F172A')
    content = content.replace('rgba(0,82,204,', 'rgba(15,23,42,')
    content = content.replace('rgba(0, 82, 204,', 'rgba(15, 23, 42,')
    content = content.replace('rgba(37,99,235,', 'rgba(15,23,42,')
    content = content.replace('rgba(37, 99, 235,', 'rgba(15, 23, 42,')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Sanitized: {fp}")

print("All non-Quantux colors successfully replaced with Slate Neutral #0F172A / #1E293B.")
