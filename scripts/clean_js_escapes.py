def clean():
    with open('scripts/build_full_scrumban_board.py', 'r', encoding='utf-8') as f:
        text = f.read()

    # In triggerDemonRework, avoid literal multiline escapes inside single quotes:
    text = text.replace("join('\\n• ')", "join(' | ')")
    text = text.replace("join('\\\\n• ')", "join(' | ')")
    text = text.replace(
        "notes: actionsSummary ? ('Solución técnica ejecutada efectivamente:\\n• ' + actionsSummary) :",
        "notes: actionsSummary ? ('Solución técnica ejecutada efectivamente: ' + actionsSummary) :"
    )
    text = text.replace(
        "notes: actionsSummary ? ('Solución técnica ejecutada efectivamente:\\\\n• ' + actionsSummary) :",
        "notes: actionsSummary ? ('Solución técnica ejecutada efectivamente: ' + actionsSummary) :"
    )
    text = text.replace(
        "const fileMsg = filesList.length > 0 ? ('\\n\\nArchivos modificados en caliente:\\n• ' + filesList.join('\\n• ')) : '';",
        "const fileMsg = filesList.length > 0 ? (' (Archivos: ' + filesList.join(', ') + ')') : '';"
    )
    text = text.replace(
        "const fileMsg = filesList.length > 0 ? ('\\\\n\\\\nArchivos modificados en caliente:\\\\n• ' + filesList.join('\\\\n• ')) : '';",
        "const fileMsg = filesList.length > 0 ? (' (Archivos: ' + filesList.join(', ') + ')') : '';"
    )

    with open('scripts/build_full_scrumban_board.py', 'w', encoding='utf-8') as f:
        f.write(text)

    print("Cleaned string escapes.")

if __name__ == '__main__':
    clean()
