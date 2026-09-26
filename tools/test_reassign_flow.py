import sys
import os

# Set standard output to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, 'backend')
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("--- INICIANDO SUITE DE PRUEBAS DE REASIGNACIÓN Y SLA ---")

# 1. Obtener un ticket existente
r = client.get('/api/v1/tickets')
tickets = r.json()
assert len(tickets) > 0, 'No tickets found'
t = tickets[0]
ticket_id = t['id']
req_user = t['requester_username']
print(f"[OK] Ticket cargado: #{ticket_id}, Solicitante: {req_user}")

# 2. Test reasignar al solicitante
r_assign = client.patch(f'/api/v1/tickets/{ticket_id}/assign', json={
    'assignee_username': req_user,
    'support_level': 'SOLICITANTE',
    'reason': 'Derivación al prestador para requerir datos adicionales',
    'changed_by_username': 'soporte'
})
assert r_assign.status_code == 200, f'Assign failed: {r_assign.text}'
updated_t = r_assign.json()
print(f"[OK] Reasignado al solicitante -> Estado: {updated_t['status']}, SLA Pausado: {updated_t['sla_paused']}")
assert updated_t['status'] == 'ESPERANDO_AL_PRESTADOR', f"Esperado ESPERANDO_AL_PRESTADOR, recibido {updated_t['status']}"
assert updated_t['sla_paused'] is True, f"Esperado sla_paused == True, recibido {updated_t['sla_paused']}"

# 3. Test bot interact
r_bot = client.post(f'/api/v1/tickets/{ticket_id}/bot-interact', json={
    'action_type': 'request_requester_info'
})
assert r_bot.status_code == 200, f'Bot interact failed: {r_bot.text}'
bot_res = r_bot.json()
print(f"[OK] Bot Interact ejecutado -> Estado: {bot_res.get('status')}, Acción: {bot_res.get('action')}, Ticket Status: {bot_res.get('ticket_status')}")
assert bot_res.get('status') == 'success'
assert bot_res.get('sla_paused') is True

# 4. Test reasignar de vuelta a un operador N2
r_op = client.patch(f'/api/v1/tickets/{ticket_id}/assign', json={
    'assignee_username': 'soporte',
    'support_level': 'N2',
    'reason': 'Devolución técnica a Mesa N2 tras recepción de antecedentes',
    'changed_by_username': 'admin'
})
assert r_op.status_code == 200, f'Assign to N2 failed: {r_op.text}'
t_n2 = r_op.json()
print(f"[OK] Devuelto a operador N2 -> Asignado: {t_n2['assignee_username']}, Nivel: {t_n2['support_level']}")
assert t_n2['assignee_username'] == 'soporte'
assert t_n2['support_level'] == 'N2'

# 5. Test resolver con workaround -> genera tarjeta en release N3
r_resolve = client.post(f'/api/v1/tickets/{ticket_id}/resolve', json={
    'resolution_summary': 'Reinicio de pasarela y recarga de certificado de firma digital',
    'resolution_notes': 'Se aplicó workaround operativo; requiere parche definitivo de firmware.',
    'is_workaround': True,
    'changed_by_username': 'soporte'
})
assert r_resolve.status_code == 200, f'Resolve failed: {r_resolve.text}'
t_res = r_resolve.json()
print(f"[OK] Ticket resuelto con Workaround -> Estado: {t_res['status']}, Release N3: {t_res.get('release_tag')}")
assert t_res['status'] == 'RESUELTO'
assert bool(t_res.get('release_tag')) is True, f"Esperado release_tag activo, recibido {t_res.get('release_tag')}"

print("\n========================================================")
print(">>> TODAS LAS COMPROBACIONES TÉCNICAS PASARON AL 100% <<<")
print("========================================================")
