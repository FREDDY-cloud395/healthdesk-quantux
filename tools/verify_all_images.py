import os
import re
import urllib.request

def check_all_images():
    with open('docs/00_Tablero_Scrumban_Quantux.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all attachment_image values
    pattern = re.compile(r'"attachment_image":\s*"([^"]+)"')
    images = set(pattern.findall(content))
    print(f"Total de imagenes unicas adjuntas en INITIAL_BACKLOG: {len(images)}")

    missing_docs = []
    missing_frontend = []
    http_errors = []

    for img in sorted(images):
        clean_rel = img.replace("docs/", "")
        
        # 1. Verificar en docs/
        doc_full = os.path.join("docs", clean_rel)
        if not os.path.exists(doc_full):
            missing_docs.append((img, doc_full))

        # 2. Verificar en frontend/
        front_full = os.path.join("frontend", clean_rel)
        if not os.path.exists(front_full):
            missing_frontend.append((img, front_full))

        # 3. Probar peticion HTTP 200 en vivo al servidor FastAPI
        url = "http://127.0.0.1:8000/" + clean_rel
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req) as resp:
                if resp.status != 200:
                    http_errors.append((url, resp.status))
        except Exception as e:
            http_errors.append((url, str(e)))

    print(f"Faltantes en docs/: {len(missing_docs)}")
    if missing_docs:
        for m in missing_docs:
            print("  -", m)

    print(f"Faltantes en frontend/: {len(missing_frontend)}")
    if missing_frontend:
        for m in missing_frontend:
            print("  -", m)

    print(f"Errores HTTP (404, etc.): {len(http_errors)}")
    if http_errors:
        for err in http_errors:
            print("  -", err)

    if not missing_docs and not missing_frontend and not http_errors:
        print("\n>>> AUDITORIA EXITOSA: 100% DE LAS IMAGENES EXISTEN Y CARGAN CON HTTP 200 SIN ERRORES! <<<")
        return True
    return False

if __name__ == '__main__':
    ok = check_all_images()
    exit(0 if ok else 1)
