import json
from app import app
from simulator import generate_cycle

client = app.test_client()

# Ensure at least one fresh cycle is present
generate_cycle()

print("--- 1. Testing GET /api/machines ---")
res_machines = client.get('/api/machines')
print("Status Code:", res_machines.status_code)
data_machines = res_machines.get_json()
print("Response preview:")
print(json.dumps(data_machines, indent=2))

print("\n--- 2. Testing GET /api/telemetry/recent?limit=3 ---")
res_telemetry = client.get('/api/telemetry/recent?limit=3')
print("Status Code:", res_telemetry.status_code)
data_telemetry = res_telemetry.get_json()
print("Response preview:")
print(json.dumps(data_telemetry, indent=2))

print("\n--- 3. Testing GET /api/stats ---")
res_stats = client.get('/api/stats')
print("Status Code:", res_stats.status_code)
data_stats = res_stats.get_json()
print("Response preview:")
print(json.dumps(data_stats, indent=2))
