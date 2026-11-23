from database import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# Check existing columns in alarms
cursor.execute("PRAGMA table_info(alarms)")
existing_cols = [c["name"] for c in cursor.fetchall()]

if "status" not in existing_cols:
    conn.execute("ALTER TABLE alarms ADD COLUMN status TEXT DEFAULT 'ACTIVE'")
    print("Added status column to alarms")

if "acknowledged_at" not in existing_cols:
    conn.execute("ALTER TABLE alarms ADD COLUMN acknowledged_at TIMESTAMP")
    print("Added acknowledged_at column to alarms")

if "resolved_at" not in existing_cols:
    conn.execute("ALTER TABLE alarms ADD COLUMN resolved_at TIMESTAMP")
    print("Added resolved_at column to alarms")

conn.commit()
conn.close()
print("Alarms table schema ready.")
