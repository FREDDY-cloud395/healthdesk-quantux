import urllib.request
import json
import re

url = 'http://127.0.0.1:8000/api/v1/ai/triage'

with open('frontend/js/typeahead.js', 'r', encoding='utf-8') as f:
    text = f.read()

queries = re.findall(r'query:\s*"([^"]+)"', text)
print(f'Total de queries oficiales en Typeahead: {len(queries)}')

success_count = 0
for i, q in enumerate(queries, 1):
    data = json.dumps({'query': q, 'user_fullname': 'Tester', 'platform_code': 'CD2', 'institution_code': 'OSDE'}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as r:
            res = json.loads(r.read().decode())
            top = res.get('top_articles', [{}])[0] if res.get('top_articles') else {}
            title = top.get('title', 'SIN MATCH')
            if 'SIN MATCH' not in title:
                success_count += 1
            else:
                print(f'[FAIL MATCH] Query {i}: {q}')
    except Exception as e:
        print(f'[ERROR] Query {i}: {q} -> {e}')

print(f'TOTAL EVALUADOS: {len(queries)} | COINCIDENCIAS EXITOSAS: {success_count}')

# Test caso desconocido (Cero Alucinaciones)
data_unknown = json.dumps({'query': 'palabra inventada zzz999 no existe en ningun lado', 'user_fullname': 'Tester', 'platform_code': 'CD2', 'institution_code': 'OSDE'}).encode('utf-8')
req_u = urllib.request.Request(url, data=data_unknown, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req_u) as r:
    res_u = json.loads(r.read().decode())
    act = res_u.get('recommended_action', '')
    print('Respuesta para consulta desconocida:', act)
    assert any(term in act.lower() for term in ['desarrollo', 'funcional'])
    print('[OK] Politica CERO Alucinaciones validada con éxito.')
