import time
from database import init_db, get_db_connection
from simulator import seed_machines, generate_cycle, start_background_simulator, stop_background_simulator
from app import app

# 1. Initialize schema and seed machines
init_db()
seed_machines()

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, name, model, department, status FROM machines")
machines = cursor.fetchall()
print(f"=== SEEDED MACHINES ({len(machines)}) ===")
for m in machines:
    print(f"ID {m['id']}: {m['name']} ({m['model']}) - Dept: {m['department']} - Status: {m['status']}")

# 2. Test single telemetry cycle
generate_cycle()
cursor.execute("SELECT COUNT(*) FROM telemetry")
print(f"Telemetry count after 1 cycle: {cursor.fetchone()[0]}")

# 3. Test background simulator thread for 3 seconds
print("Running background simulator for 3 seconds...")
start_background_simulator(interval_seconds=1)
time.sleep(3.2)
stop_background_simulator()

cursor.execute("SELECT COUNT(*) FROM telemetry")
total_telemetry = cursor.fetchone()[0]
print(f"Total telemetry count after background simulation: {total_telemetry}")

# 4. Inspect latest readings
cursor.execute("""
    SELECT t.id, m.name, t.spindle_speed, t.temperature, t.vibration, t.timestamp
    FROM telemetry t
    JOIN machines m ON t.machine_id = m.id
    ORDER BY t.id DESC LIMIT 3
""")
print("=== LATEST 3 TELEMETRY SAMPLES ===")
for row in cursor.fetchall():
    print(f"Row {row['id']}: {row['name']} | Spindle: {row['spindle_speed']} RPM | Temp: {row['temperature']} C | Vibration: {row['vibration']} mm/s | Time: {row['timestamp']}")

conn.close()

# 5. Verify Flask health endpoint
client = app.test_client()
res = client.get('/api/health')
print("Flask Health Response:", res.get_json())
