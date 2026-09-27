# -*- coding: utf-8 -*-
with open("scripts/build_full_scrumban_board.py", "r", encoding="utf-8") as f:
    code = f.read()

# Buscamos function init() { hasta function syncIssueInBacklog
start_idx = code.find("    function init() {")
end_idx = code.find("    function syncIssueInBacklog(issueId) {{")

if start_idx != -1 and end_idx != -1:
    init_chunk = code[start_idx:end_idx]
    # Reemplazamos llaves simples por dobles en init_chunk
    # primero cuidamos si alguna ya era doble
    doubled_chunk = init_chunk.replace("{{", "SINGLE_O").replace("}}", "SINGLE_C")
    doubled_chunk = doubled_chunk.replace("{", "{{").replace("}", "}}")
    doubled_chunk = doubled_chunk.replace("SINGLE_O", "{{").replace("SINGLE_C", "}}")
    
    code = code[:start_idx] + doubled_chunk + code[end_idx:]
    with open("scripts/build_full_scrumban_board.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Braces fixed in init() function!")
else:
    print(f"Could not find init() bounds! start={start_idx}, end={end_idx}")
