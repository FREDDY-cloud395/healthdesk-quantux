import sqlite3

conn = sqlite3.connect('backend/healthdesk.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
counts = {}
for t in tables:
    name = t[0]
    try:
        cur.execute(f"SELECT COUNT(*) FROM {name}")
        counts[name] = cur.fetchone()[0]
    except Exception as e:
        counts[name] = str(e)
print(counts)
