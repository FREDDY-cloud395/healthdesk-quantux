import sqlite3
import os

db_path = r"C:\Users\FERO_ADM\.gemini\antigravity\scratch\quantux-v4-dev\backend\healthdesk.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get existing columns
cursor.execute("PRAGMA table_info(tickets)")
existing_cols = [row[1] for row in cursor.fetchall()]

new_cols = [
    ("kcs_data", "TEXT"),
    ("rescue_leader_username", "TEXT"),
    ("rescue_notes", "TEXT"),
    ("rescue_status", "TEXT"),
    ("sla_paused", "BOOLEAN DEFAULT 0"),
    ("sla_paused_at", "DATETIME")
]

for col_name, col_type in new_cols:
    if col_name not in existing_cols:
        cursor.execute(f"ALTER TABLE tickets ADD COLUMN {col_name} {col_type}")
        print(f"Added column {col_name} ({col_type}) to tickets table.")
    else:
        print(f"Column {col_name} already exists.")

conn.commit()
conn.close()
print("Migration completed successfully!")
