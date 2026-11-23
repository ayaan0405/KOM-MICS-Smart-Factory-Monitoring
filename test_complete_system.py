import json
from app import app
from simulator import generate_cycle

client = app.test_client()

print("=" * 60)
print("COMPREHENSIVE SMART FACTORY SYSTEM VERIFICATION SUITE")
print("=" * 60)

# 1. Test Navigation & Endpoints
endpoints = [
    ('/', 200),
    ('/api/health', 200),
    ('/api/stats', 200),
    ('/api/machines', 200),
    ('/api/telemetry/recent?limit=10', 200),
    ('/api/alarms?limit=20', 200),
    ('/api/production', 200),
    ('/api/maintenance?limit=20', 200),
]

print("\n--- 1. Testing System Routes & Endpoints ---")
for url, expected_status in endpoints:
    res = client.get(url)
    assert res.status_code == expected_status, f"Endpoint {url} failed with status {res.status_code}"
    print(f"GET {url:35} -> HTTP {res.status_code} [OK]")

# 2. Test Production Tracking API
print("\n--- 2. Testing Production Tracking API ---")
prod_res = client.get('/api/production')
prod_data = prod_res.get_json()
assert prod_data['success'] is True, "Production API call unsuccessful"
assert prod_data['is_simulated'] is True, "Production data must be marked as simulated"
assert len(prod_data['departments']) == 3, f"Expected 3 departments, got {len(prod_data['departments'])}"
assert len(prod_data['machines']) == 6, f"Expected 6 machines in production, got {len(prod_data['machines'])}"

ps = prod_data['plant_summary']
print(f"Shift: {prod_data['shift_name']}")
print(f"Total Target Units: {ps['total_target_units']}")
print(f"Total Actual Units: {ps['total_actual_units']}")
print(f"Total Rejected Units: {ps['total_rejected_units']}")
print(f"Shift Completion: {ps['completion_percentage']}%")
print(f"Scrap Rate: {ps['scrap_rate_percentage']}%")
for d in prod_data['departments']:
    print(f"  > Dept: {d['department']:25} | Target: {d['target_units']:4} | Actual: {d['actual_units']:4} | Rejects: {d['rejected_units']:2} | Yield: {d['completion_percentage']}%")

# 3. Test Maintenance Logging & Downtime API
print("\n--- 3. Testing Maintenance Logging & Downtime API ---")
maint_get = client.get('/api/maintenance')
maint_data = maint_get.get_json()
assert maint_data['success'] is True
initial_count = maint_data['count']
initial_downtime = maint_data['total_downtime_minutes']
print(f"Initial Maintenance Logs: {initial_count} | Total Downtime: {initial_downtime} mins")

# Post a new maintenance record
new_record = {
    'machine_id': 2,
    'maintenance_type': 'PREVENTIVE',
    'description': 'Laser cutting nozzle replacement and alignment test',
    'technician': 'S. Watanabe',
    'downtime_minutes': 35,
    'status': 'COMPLETED'
}
maint_post = client.post('/api/maintenance', json=new_record)
assert maint_post.status_code == 201
post_data = maint_post.get_json()
assert post_data['success'] is True
log_id = post_data['log_id']
print(f"POST /api/maintenance -> HTTP 201 Created log #{log_id}")

# Verify log is retrievable
maint_verify = client.get(f'/api/maintenance?machine_id=2')
v_data = maint_verify.get_json()
assert any(log['id'] == log_id for log in v_data['logs']), "New maintenance log not found in machine 2 records"
print(f"Verified new maintenance log #{log_id} recorded in SQLite and linked to machine #2.")

# 4. Test Alarm Workflow (Thresholds, ACK, RESOLVE)
print("\n--- 4. Testing Alarm Workflow ---")
alarms_res = client.get('/api/alarms')
alarms = alarms_res.get_json()['alarms']
active_alarms = [a for a in alarms if a['status'] == 'ACTIVE']
print(f"Found {len(alarms)} total alarms, {len(active_alarms)} ACTIVE.")

if active_alarms:
    test_alarm = active_alarms[0]
    alarm_id = test_alarm['id']
    # Acknowledge
    ack_res = client.post(f'/api/alarms/{alarm_id}/acknowledge')
    assert ack_res.status_code == 200
    assert ack_res.get_json()['status'] == 'ACKNOWLEDGED'
    print(f"Alarm #{alarm_id} ({test_alarm['code']}) successfully ACKNOWLEDGED.")
    
    # Resolve
    res_res = client.post(f'/api/alarms/{alarm_id}/resolve')
    assert res_res.status_code == 200
    assert res_res.get_json()['status'] == 'RESOLVED'
    print(f"Alarm #{alarm_id} ({test_alarm['code']}) successfully RESOLVED.")

print("\n" + "=" * 60)
print("ALL SYSTEM VERIFICATION TESTS PASSED SUCCESSFULLY!")
print("=" * 60)
