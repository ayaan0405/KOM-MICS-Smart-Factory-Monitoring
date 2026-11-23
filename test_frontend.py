from app import app

client = app.test_client()

routes = [
    ('/', 'text/html'),
    ('/static/css/style.css', 'text/css'),
    ('/static/js/chart.umd.min.js', 'text/javascript'),
    ('/static/js/app.js', 'text/javascript'),
    ('/api/health', 'application/json'),
    ('/api/stats', 'application/json'),
    ('/api/machines', 'application/json'),
    ('/api/telemetry/recent?limit=5', 'application/json')
]

print("=== TESTING ALL APPLICATION ROUTES & ASSETS ===")
all_ok = True
for url, expected_type in routes:
    res = client.get(url)
    content_type = res.headers.get('Content-Type', '')
    match = expected_type in content_type
    clean_type = content_type.split(';')[0]
    print(f"Route: {url:35} | Status: {res.status_code} | Type: {clean_type} | Size: {len(res.data)} bytes")
    if res.status_code != 200:
        all_ok = False

# Validate expected DOM element IDs in index.html
html = client.get('/').data.decode('utf-8')
required_ids = [
    'kpi-total-machines', 'val-total-machines',
    'kpi-running-machines', 'val-running-machines', 'sub-running-status',
    'kpi-availability', 'val-availability',
    'kpi-telemetry', 'val-telemetry',
    'telemetryChart', 'spindleChart',
    'departments-container', 'last-updated-text',
    'activity-table-body', 'btn-refresh'
]

print("\n=== VALIDATING DOM ELEMENT BINDINGS ===")
missing_ids = [elem_id for elem_id in required_ids if elem_id not in html]
if missing_ids:
    print("Missing DOM IDs:", missing_ids)
    all_ok = False
else:
    print(f"All {len(required_ids)} required DOM element IDs successfully bound in index.html.")

print("\nOVERALL VERIFICATION RESULT:", "PASSED" if all_ok else "FAILED")
