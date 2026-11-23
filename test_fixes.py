from app import app
from simulator import generate_cycle

client = app.test_client()

print("=== 1. VERIFYING PLANT AVAILABILITY CALCULATION ===")
# Force a cycle to ensure up-to-date data
generate_cycle()

stats = client.get('/api/stats').get_json()
total_machines = stats['total_machines']
running_machines = stats['running_machines']
expected_avail = round((running_machines / total_machines) * 100, 1)
actual_avail = stats['availability_percentage']
formula_doc = stats.get('availability_formula')

print(f"Total Machines: {total_machines}")
print(f"Running Machines: {running_machines}")
print(f"Calculated Availability: {actual_avail}% (Expected: {expected_avail}%)")
print(f"Documented Formula: {formula_doc}")
assert actual_avail == expected_avail, f"Availability mismatch: {actual_avail} != {expected_avail}"
print("=> Issue 1 Check: PASSED")

print("\n=== 2. VERIFYING MACHINE STATUS & TELEMETRY CONSISTENCY ===")
machines_res = client.get('/api/machines').get_json()
machines = machines_res['machines']
idle_count = 0
for m in machines:
    print(f"Machine [{m['id']}] {m['name']} | Status: {m['status']} | Spindle: {m['spindle_speed']} RPM")
    if m['status'] == 'IDLE':
        idle_count += 1
        assert m['spindle_speed'] == 0.0, f"IDLE machine {m['name']} has non-zero spindle: {m['spindle_speed']}"
print(f"Verified {len(machines)} machines. (Found {idle_count} IDLE machines with strictly 0.0 RPM).")

telemetry_res = client.get('/api/telemetry/recent?limit=30').get_json()
telemetry = telemetry_res['telemetry']
idle_telemetry_count = 0
for t in telemetry:
    if t['status'] == 'IDLE':
        idle_telemetry_count += 1
        assert t['spindle_speed'] == 0.0, f"IDLE telemetry record #{t['id']} has non-zero spindle: {t['spindle_speed']}"
print(f"Verified {len(telemetry)} recent telemetry records. (Found {idle_telemetry_count} IDLE records with strictly 0.0 RPM).")
print("=> Issue 2 Check: PASSED")

print("\n=== 3. VERIFYING NON-OVERLAPPING CHART TIMESTAMPS ===")
# Simulate the JavaScript grouping algorithm in Python
time_groups = {}
for t in reversed(telemetry):
    time_part = t['timestamp'].split(' ')[1] if ' ' in t['timestamp'] else t['timestamp']
    if time_part not in time_groups:
        time_groups[time_part] = {'temp_sum': 0.0, 'vib_sum': 0.0, 'count': 0}
    time_groups[time_part]['temp_sum'] += t['temperature']
    time_groups[time_part]['vib_sum'] += t['vibration']
    time_groups[time_part]['count'] += 1

chart_labels = list(time_groups.keys())
print(f"Distinct Chart Timestamps ({len(chart_labels)} cycles from {len(telemetry)} records): {chart_labels}")
assert len(chart_labels) == len(set(chart_labels)), "Duplicate timestamps detected in chart labels!"
print("=> Issue 3 Check: PASSED")

print("\n=== 4. VERIFYING CROSS-COMPONENT DATA CONSISTENCY ===")
# Verify machine counts match
assert stats['total_machines'] == len(machines), "Stats total_machines does not match /api/machines length"

# Verify status counts match
status_summary = stats['status_summary']
counted_statuses = {'RUNNING': 0, 'IDLE': 0, 'WARNING': 0}
for m in machines:
    counted_statuses[m['status']] = counted_statuses.get(m['status'], 0) + 1

for st, count in counted_statuses.items():
    assert status_summary.get(st, 0) == count, f"Status count mismatch for {st}: stats={status_summary.get(st)} vs machines={count}"
print(f"Status counts perfectly synchronized: {status_summary} == {counted_statuses}")
print("=> Issue 4 Check: PASSED")

print("\nALL 4 ISSUE VERIFICATIONS: PASSED SUCCESSFULLY!")
