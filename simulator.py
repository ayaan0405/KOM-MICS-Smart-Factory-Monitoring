import time
import random
import threading
from datetime import datetime
from database import get_db_connection, init_db

# 6 Sample Machines across 3 core departments
SAMPLE_MACHINES = [
    # Welding & Fabrication
    {"name": "Robotic Arc Welder #1", "model": "KUKA KR-16 Arc", "department": "Welding & Fabrication"},
    {"name": "Laser Cutting CNC #1", "model": "Trumpf TruLaser 3030", "department": "Welding & Fabrication"},
    # Assembly
    {"name": "Automated Screwdriving Cell", "model": "Atlas Copco Tensor", "department": "Assembly"},
    {"name": "Pick & Place Robotics Cell", "model": "ABB IRB 1200", "department": "Assembly"},
    # Quality Inspection
    {"name": "Coordinate Measuring Machine", "model": "Zeiss Contura CMM", "department": "Quality Inspection"},
    {"name": "Optical Vision Inspector", "model": "Keyence CV-X400", "department": "Quality Inspection"},
]

_stop_event = threading.Event()
_simulator_thread = None

def seed_machines():
    """Seeds the 6 sample machines and baseline sample alarms if not present."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for machine in SAMPLE_MACHINES:
        cursor.execute("SELECT id FROM machines WHERE name = ?", (machine["name"],))
        existing = cursor.fetchone()
        if not existing:
            cursor.execute(
                "INSERT INTO machines (name, model, department, status) VALUES (?, ?, ?, 'IDLE')",
                (machine["name"], machine["model"], machine["department"])
            )
            
    # Seed sample baseline events if alarms table is empty
    cursor.execute("SELECT COUNT(*) FROM alarms")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO alarms (machine_id, code, description, severity, status, timestamp)
            VALUES (1, 'ALM-CAL-DUE', 'Electrode tip wear calibration check recommended', 'INFO', 'ACTIVE', datetime('now', '-2 hours', 'localtime'))
        """)
        cursor.execute("""
            INSERT INTO alarms (machine_id, code, description, severity, status, timestamp, resolved_at)
            VALUES (2, 'ALM-FEED-ERR', 'Optical lens alignment verified and cleared', 'WARNING', 'RESOLVED', datetime('now', '-1 day', 'localtime'), datetime('now', '-18 hours', 'localtime'))
        """)

    # Seed baseline production records if production_records table is empty
    cursor.execute("SELECT COUNT(*) FROM production_records")
    if cursor.fetchone()[0] == 0:
        production_seeds = [
            (1, "Welding & Fabrication", 500, 412, 7),
            (2, "Welding & Fabrication", 650, 585, 12),
            (3, "Assembly", 850, 774, 14),
            (4, "Assembly", 800, 710, 9),
            (5, "Quality Inspection", 550, 489, 4),
            (6, "Quality Inspection", 950, 882, 16),
        ]
        for mid, dept, target, actual, rej in production_seeds:
            cursor.execute("""
                INSERT OR IGNORE INTO production_records (shift_name, department, machine_id, target_units, actual_units, rejected_units, updated_at)
                VALUES ('SHIFT 1 (DAY)', ?, ?, ?, ?, ?, datetime('now', 'localtime'))
            """, (dept, mid, target, actual, rej))

    # Seed baseline maintenance history if maintenance_logs table is empty
    cursor.execute("SELECT COUNT(*) FROM maintenance_logs")
    if cursor.fetchone()[0] == 0:
        maintenance_seeds = [
            (1, "PREVENTIVE", "Torch tip replacement & wire-feed alignment", "K. Takahashi", 45, "COMPLETED", "-2 days"),
            (2, "CORRECTIVE", "Optical lens realign and focal calibration after thermal alert", "M. Sato", 60, "COMPLETED", "-1 day"),
            (3, "TOOL_CHANGE", "Torque driver bit replacement (worn driver)", "H. Tanaka", 15, "COMPLETED", "-14 hours"),
            (4, "INSPECTION", "Pneumatic gripper seal and vacuum sensor check", "T. Yamada", 20, "COMPLETED", "-5 hours"),
            (5, "CALIBRATION", "Probe ruby stylus recalibration against granite standard", "R. Suzuki", 30, "COMPLETED", "-12 hours"),
        ]
        for mid, mtype, desc, tech, down_mins, st, time_offset in maintenance_seeds:
            cursor.execute(f"""
                INSERT INTO maintenance_logs (machine_id, maintenance_type, description, technician, downtime_minutes, status, performed_at)
                VALUES (?, ?, ?, ?, ?, ?, datetime('now', '{time_offset}', 'localtime'))
            """, (mid, mtype, desc, tech, down_mins, st))
    
    conn.commit()
    conn.close()

def generate_cycle():
    """Generates one telemetry reading for each machine and records any warning alarms in SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department FROM machines")
    machines = cursor.fetchall()

    for m in machines:
        machine_id = m["id"]
        # Realistic status probability: 80% RUNNING, 15% IDLE, 5% WARNING
        status = random.choices(["RUNNING", "IDLE", "WARNING"], weights=[80, 15, 5])[0]

        if status == "RUNNING":
            spindle_speed = round(random.uniform(1800.0, 3200.0), 1)
            temperature = round(random.uniform(45.0, 68.0), 2)
            vibration = round(random.uniform(0.6, 1.8), 2)
        elif status == "IDLE":
            # IDLE: Spindle strictly stopped, ambient thermal baseline, minimal vibration
            spindle_speed = 0.0
            temperature = round(random.uniform(22.0, 29.0), 2)
            vibration = round(random.uniform(0.01, 0.12), 2)
        else:  # WARNING
            spindle_speed = round(random.uniform(3200.0, 3600.0), 1)
            temperature = round(random.uniform(75.0, 88.0), 2)
            vibration = round(random.uniform(2.8, 4.5), 2)

            # Record event in alarms table if not already actively logged
            cursor.execute("SELECT id FROM alarms WHERE machine_id = ? AND status = 'ACTIVE'", (machine_id,))
            if not cursor.fetchone():
                code = "ALM-TEMP-HIGH" if temperature > 75.0 else "ALM-VIB-HIGH"
                desc = f"Thermal load exceeded ({temperature} °C)" if temperature > 75.0 else f"Vibration threshold exceeded ({vibration} mm/s)"
                cursor.execute(
                    """INSERT INTO alarms (machine_id, code, description, severity, status, timestamp)
                       VALUES (?, ?, ?, 'WARNING', 'ACTIVE', datetime('now', 'localtime'))""",
                    (machine_id, code, desc)
                )

        # 1. Update current machine status
        cursor.execute("UPDATE machines SET status = ? WHERE id = ?", (status, machine_id))

        # 2. Insert new historical telemetry reading
        cursor.execute(
            """INSERT INTO telemetry (machine_id, spindle_speed, vibration, temperature, timestamp)
               VALUES (?, ?, ?, ?, datetime('now', 'localtime'))""",
            (machine_id, spindle_speed, vibration, temperature)
        )

        # 3. Increment simulated production if operating
        if status == "RUNNING":
            if random.random() < 0.65:
                cursor.execute("""
                    UPDATE production_records 
                    SET actual_units = actual_units + 1, updated_at = datetime('now', 'localtime') 
                    WHERE machine_id = ?
                """, (machine_id,))
            if random.random() < 0.03:
                cursor.execute("""
                    UPDATE production_records 
                    SET rejected_units = rejected_units + 1, updated_at = datetime('now', 'localtime') 
                    WHERE machine_id = ?
                """, (machine_id,))

    conn.commit()
    conn.close()

def _run_loop(interval_seconds):
    """Background loop that periodically executes generate_cycle()."""
    while not _stop_event.is_set():
        try:
            generate_cycle()
        except Exception as e:
            print(f"[Simulator Error] {e}")
        time.sleep(interval_seconds)

def start_background_simulator(interval_seconds=3):
    """Starts the background simulator in a daemon thread."""
    global _simulator_thread
    if _simulator_thread is not None and _simulator_thread.is_alive():
        return
    _stop_event.clear()
    seed_machines()
    _simulator_thread = threading.Thread(target=_run_loop, args=(interval_seconds,), daemon=True)
    _simulator_thread.start()
    print(f"[Simulator] Background telemetry simulator started (interval: {interval_seconds}s).")

def stop_background_simulator():
    """Signals the simulator thread to stop."""
    _stop_event.set()
    if _simulator_thread is not None:
        _simulator_thread.join(timeout=2)
    print("[Simulator] Background telemetry simulator stopped.")

if __name__ == "__main__":
    init_db()
    seed_machines()
    print("Machines seeded. Generating 1 test cycle...")
    generate_cycle()
    print("1 test cycle completed successfully.")
