import re
import subprocess
import os
import sys

def fix_and_validate():
    file_path = 'scripts/build_full_scrumban_board.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix unescaped newlines in appendObservationFromModal
    bad_pattern = r"const updatedVal = prevVal \? \(prevVal \+ '(?:\n|\\n){1,2}\["
    # Let's inspect line 6168
    content = re.sub(
        r"const updatedVal = prevVal \? \(prevVal \+ '(\\n|\n){1,2}\[",
        r"const updatedVal = prevVal ? (prevVal + '\\n\\n[",
        content
    )
    # Also in case it's written as \\\\n
    content = content.replace(
        "prevVal + '\\n\\n['",
        "prevVal + '\\\\n\\\\n['"
    )

    # Add automated post-generation validation into build_full_scrumban_board.py
    # At the end of build_full_scrumban_board.py, make it test the output with node --check
    validator_code = '''
    # VALIDACIÓN AUTOMÁTICA PRE-DESPLIEGUE (CERO ROTURAS)
    try:
        import subprocess
        # Extraer script para verificación sintáctica estricta con Node.js
        s_idx = html_content.find('<script>')
        e_idx = html_content.rfind('</script>')
        if s_idx != -1 and e_idx != -1:
            js_code = html_content[s_idx + 8:e_idx]
            tmp_js = os.path.join(docs_dir, '_tmp_check.js')
            with open(tmp_js, 'w', encoding='utf-8') as f_tmp:
                f_tmp.write(js_code)
            res = subprocess.run(['node', '--check', tmp_js], capture_output=True, text=True)
            if os.path.exists(tmp_js):
                os.remove(tmp_js)
            if res.returncode != 0:
                print("FATAL ERROR: JavaScript Syntax Error detectado en el tablero generado:")
                print(res.stderr)
                raise RuntimeError("El tablero generado contiene errores de sintaxis JavaScript. Despliegue abortado.")
            else:
                print("VERIFICACIÓN SINTÁCTICA JS: EXITOSA (0 errores sintácticos)")
    except Exception as err:
        if isinstance(err, RuntimeError):
            raise
        print("Aviso en validación JS:", err)
'''
    if 'VERIFICACIÓN SINTÁCTICA JS' not in content:
        # Insert before writing the file or right after writing the file
        needle = "with open(output_path, 'w', encoding='utf-8') as f:"
        content = content.replace(needle, validator_code + "\n    " + needle)
        print("Automated syntax validation hook installed into build_full_scrumban_board.py")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("build_full_scrumban_board.py updated.")

if __name__ == '__main__':
    fix_and_validate()
