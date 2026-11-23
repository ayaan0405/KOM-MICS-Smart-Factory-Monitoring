import os
from flask import Flask, jsonify, render_template, request
from database import get_db_connection, init_db
from simulator import seed_machines, start_background_simulator

app = Flask(__name__)

# Initialize database schema and seed machines
with app.app_context():
    init_db()
    seed_machines()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
        
        cursor.execute("SELECT COUNT(*) FROM machines")
        machine_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM telemetry")
        telemetry_count = cursor.fetchone()[0]

        conn.close()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'tables': tables,
            'machine_count': machine_count,
            'telemetry_count': telemetry_count
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/machines', methods=['GET'])
def get_machines():
    """Returns all factory machines with their current status, department, and latest telemetry."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                m.id, 
                m.name, 
                m.model, 
                m.department, 
                m.status, 
                m.created_at,
                t.spindle_speed,
                t.temperature,
                t.vibration,
                t.timestamp as last_reading_time
            FROM machines m
            LEFT JOIN (
                SELECT machine_id, spindle_speed, temperature, vibration, timestamp
                FROM telemetry
                WHERE id IN (SELECT MAX(id) FROM telemetry GROUP BY machine_id)
            ) t ON m.id = t.machine_id
            ORDER BY m.id ASC
        """)
        rows = cursor.fetchall()
        conn.close()

        machines = []
        for row in rows:
            status = row['status']
            # Strict consistency: IDLE machines strictly have 0.0 RPM spindle speed and baseline vibration
            if status == 'IDLE':
                spindle_speed = 0.0
                vibration = round(min(row['vibration'] or 0.0, 0.15), 2)
            else:
                spindle_speed = row['spindle_speed'] or 0.0
                vibration = row['vibration'] or 0.0

            machines.append({
                'id': row['id'],
                'name': row['name'],
                'model': row['model'],
                'department': row['department'],
                'status': status,
                'created_at': row['created_at'],
                'spindle_speed': spindle_speed,
                'temperature': row['temperature'] or 0.0,
                'vibration': vibration,
                'last_reading_time': row['last_reading_time'] or '-'
            })

        return jsonify({
            'success': True,
            'count': len(machines),
            'machines': machines
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/telemetry/recent', methods=['GET'])
def get_recent_telemetry():
    """Returns recent telemetry readings, optionally filtered by machine_id."""
    try:
        limit = request.args.get('limit', default=24, type=int)
        limit = max(1, min(limit, 100))
        machine_id = request.args.get('machine_id', default=None, type=int)

        conn = get_db_connection()
        cursor = conn.cursor()

        if machine_id:
            cursor.execute("""
                SELECT 
                    t.id, 
                    t.machine_id, 
                    m.name AS machine_name, 
                    m.department, 
                    m.status,
                    t.spindle_speed, 
                    t.vibration, 
                    t.temperature, 
                    t.timestamp
                FROM telemetry t
                JOIN machines m ON t.machine_id = m.id
                WHERE t.machine_id = ?
                ORDER BY t.id DESC
                LIMIT ?
            """, (machine_id, limit))
        else:
            cursor.execute("""
                SELECT 
                    t.id, 
                    t.machine_id, 
                    m.name AS machine_name, 
                    m.department, 
                    m.status,
                    t.spindle_speed, 
                    t.vibration, 
                    t.temperature, 
                    t.timestamp
                FROM telemetry t
                JOIN machines m ON t.machine_id = m.id
                ORDER BY t.id DESC
                LIMIT ?
            """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        data = []
        for row in rows:
            status = row['status']
            spindle = 0.0 if status == 'IDLE' else (row['spindle_speed'] or 0.0)
            data.append({
                'id': row['id'],
                'machine_id': row['machine_id'],
                'machine_name': row['machine_name'],
                'department': row['department'],
                'status': status,
                'spindle_speed': spindle,
                'vibration': row['vibration'] or 0.0,
                'temperature': row['temperature'] or 0.0,
                'timestamp': row['timestamp']
            })

        return jsonify({
            'success': True,
            'count': len(data),
            'telemetry': data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_factory_stats():
    """Returns aggregated high-level KPIs and machine metrics for the factory.
    
    Plant Availability Formula:
      Availability (%) = (Active Operating Machines / Total Machines) * 100
      In standard KOM-MICS / OEE frameworks, Availability reflects the proportion of
      planned equipment currently in the RUNNING operational state.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Status summary
        cursor.execute("SELECT status, COUNT(*) as count FROM machines GROUP BY status")
        status_rows = cursor.fetchall()
        status_counts = {'RUNNING': 0, 'IDLE': 0, 'WARNING': 0}
        total_machines = 0
        for row in status_rows:
            status_counts[row['status']] = row['count']
            total_machines += row['count']

        # Department breakdown
        cursor.execute("SELECT department, COUNT(*) as count FROM machines GROUP BY department")
        department_counts = {row['department']: row['count'] for row in cursor.fetchall()}

        # Total telemetry records
        cursor.execute("SELECT COUNT(*) FROM telemetry")
        total_telemetry = cursor.fetchone()[0]

        # Recent averages across active telemetry
        cursor.execute("""
            SELECT 
                ROUND(AVG(spindle_speed), 1) as avg_spindle,
                ROUND(AVG(temperature), 2) as avg_temp,
                ROUND(AVG(vibration), 2) as avg_vib
            FROM (
                SELECT spindle_speed, temperature, vibration 
                FROM telemetry 
                ORDER BY id DESC 
                LIMIT 30
            )
        """)
        avg_row = cursor.fetchone()

        conn.close()

        # Correct & Documented Availability Formula
        running_count = status_counts.get('RUNNING', 0)
        availability_pct = round((running_count / total_machines * 100), 1) if total_machines > 0 else 0.0

        return jsonify({
            'success': True,
            'total_machines': total_machines,
            'running_machines': running_count,
            'availability_percentage': availability_pct,
            'availability_formula': 'Availability (%) = (Running Machines / Total Machines) * 100',
            'status_summary': status_counts,
            'departments': department_counts,
            'total_telemetry_records': total_telemetry,
            'recent_averages': {
                'avg_spindle_speed_rpm': avg_row['avg_spindle'] or 0.0,
                'avg_temperature_c': avg_row['avg_temp'] or 0.0,
                'avg_vibration_mm_s': avg_row['avg_vib'] or 0.0
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/alarms', methods=['GET'])
def get_alarms():
    """Returns factory alarms and events from SQLite."""
    try:
        limit = request.args.get('limit', default=50, type=int)
        status_filter = request.args.get('status', default=None, type=str)
        severity_filter = request.args.get('severity', default=None, type=str)

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                a.id, 
                a.machine_id, 
                m.name AS machine_name, 
                m.department, 
                a.code, 
                a.description, 
                a.severity, 
                COALESCE(a.status, 'ACTIVE') AS status,
                a.acknowledged_at,
                a.resolved_at,
                a.timestamp
            FROM alarms a
            JOIN machines m ON a.machine_id = m.id
            WHERE 1=1
        """
        params = []

        if status_filter and status_filter.lower() != 'all':
            query += " AND UPPER(a.status) = ?"
            params.append(status_filter.upper())

        if severity_filter and severity_filter.lower() != 'all':
            query += " AND UPPER(a.severity) = ?"
            params.append(severity_filter.upper())

        query += " ORDER BY a.id DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()

        alarms = [
            {
                'id': row['id'],
                'machine_id': row['machine_id'],
                'machine_name': row['machine_name'],
                'department': row['department'],
                'code': row['code'],
                'description': row['description'],
                'severity': row['severity'],
                'status': row['status'],
                'acknowledged_at': row['acknowledged_at'],
                'resolved_at': row['resolved_at'],
                'timestamp': row['timestamp']
            }
            for row in rows
        ]

        return jsonify({'success': True, 'count': len(alarms), 'alarms': alarms})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/alarms/<int:alarm_id>/acknowledge', methods=['POST'])
def acknowledge_alarm(alarm_id):
    """Marks an active alarm as ACKNOWLEDGED."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE alarms 
               SET status = 'ACKNOWLEDGED', acknowledged_at = datetime('now', 'localtime') 
               WHERE id = ?""",
            (alarm_id,)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'alarm_id': alarm_id, 'status': 'ACKNOWLEDGED'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/alarms/<int:alarm_id>/resolve', methods=['POST'])
def resolve_alarm(alarm_id):
    """Marks an alarm as RESOLVED."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE alarms 
               SET status = 'RESOLVED', resolved_at = datetime('now', 'localtime') 
               WHERE id = ?""",
            (alarm_id,)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'alarm_id': alarm_id, 'status': 'RESOLVED'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/production', methods=['GET'])
def get_production_data():
    """Returns shift production targets, actual output, rejected units, and department summaries.
    Clearly identifies the data as simulated research telemetry.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                p.id,
                p.shift_name,
                p.department,
                p.machine_id,
                m.name as machine_name,
                m.model as machine_model,
                m.status as machine_status,
                p.target_units,
                p.actual_units,
                p.rejected_units,
                p.updated_at
            FROM production_records p
            JOIN machines m ON p.machine_id = m.id
            ORDER BY m.id ASC
        """)
        rows = cursor.fetchall()
        conn.close()

        total_target = 0
        total_actual = 0
        total_rejected = 0
        departments = {}
        machines_list = []

        for row in rows:
            dept = row['department']
            target = row['target_units']
            actual = row['actual_units']
            rejected = row['rejected_units']
            
            total_target += target
            total_actual += actual
            total_rejected += rejected

            if dept not in departments:
                departments[dept] = {
                    'department': dept,
                    'target_units': 0,
                    'actual_units': 0,
                    'rejected_units': 0,
                    'machine_count': 0
                }
            
            departments[dept]['target_units'] += target
            departments[dept]['actual_units'] += actual
            departments[dept]['rejected_units'] += rejected
            departments[dept]['machine_count'] += 1

            comp_pct = round((actual / target * 100), 1) if target > 0 else 0.0
            total_produced = actual + rejected
            scrap_pct = round((rejected / total_produced * 100), 2) if total_produced > 0 else 0.0

            machines_list.append({
                'machine_id': row['machine_id'],
                'machine_name': row['machine_name'],
                'machine_model': row['machine_model'],
                'department': dept,
                'status': row['machine_status'],
                'target_units': target,
                'actual_units': actual,
                'rejected_units': rejected,
                'completion_percentage': comp_pct,
                'scrap_rate_percentage': scrap_pct,
                'updated_at': row['updated_at']
            })

        dept_summary_list = []
        for dept, data in departments.items():
            comp_pct = round((data['actual_units'] / data['target_units'] * 100), 1) if data['target_units'] > 0 else 0.0
            tot_prod = data['actual_units'] + data['rejected_units']
            scrap_pct = round((data['rejected_units'] / tot_prod * 100), 2) if tot_prod > 0 else 0.0
            dept_summary_list.append({
                'department': dept,
                'target_units': data['target_units'],
                'actual_units': data['actual_units'],
                'rejected_units': data['rejected_units'],
                'machine_count': data['machine_count'],
                'completion_percentage': comp_pct,
                'scrap_rate_percentage': scrap_pct
            })

        overall_comp = round((total_actual / total_target * 100), 1) if total_target > 0 else 0.0
        tot_all = total_actual + total_rejected
        overall_scrap = round((total_rejected / tot_all * 100), 2) if tot_all > 0 else 0.0

        return jsonify({
            'success': True,
            'is_simulated': True,
            'shift_name': 'SHIFT 1 (DAY)',
            'simulation_notice': '[SIMULATED SHIFT PRODUCTION DATA — NON-BENCHMARK RESEARCH TELEMETRY]',
            'plant_summary': {
                'total_target_units': total_target,
                'total_actual_units': total_actual,
                'total_rejected_units': total_rejected,
                'completion_percentage': overall_comp,
                'scrap_rate_percentage': overall_scrap
            },
            'departments': dept_summary_list,
            'machines': machines_list
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/maintenance', methods=['GET'])
def get_maintenance_logs():
    """Returns factory equipment maintenance and downtime history from SQLite."""
    try:
        limit = request.args.get('limit', default=50, type=int)
        machine_id = request.args.get('machine_id', default=None, type=int)

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                ml.id,
                ml.machine_id,
                m.name as machine_name,
                m.model as machine_model,
                m.department,
                ml.maintenance_type,
                ml.description,
                ml.technician,
                ml.downtime_minutes,
                ml.status,
                ml.performed_at
            FROM maintenance_logs ml
            JOIN machines m ON ml.machine_id = m.id
            WHERE 1=1
        """
        params = []
        if machine_id:
            query += " AND ml.machine_id = ?"
            params.append(machine_id)

        query += " ORDER BY ml.id DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        # Compute total downtime minutes recorded
        cursor.execute("SELECT COALESCE(SUM(downtime_minutes), 0) FROM maintenance_logs")
        total_downtime = cursor.fetchone()[0]

        conn.close()

        logs = [
            {
                'id': row['id'],
                'machine_id': row['machine_id'],
                'machine_name': row['machine_name'],
                'machine_model': row['machine_model'],
                'department': row['department'],
                'maintenance_type': row['maintenance_type'],
                'description': row['description'],
                'technician': row['technician'],
                'downtime_minutes': row['downtime_minutes'],
                'status': row['status'],
                'performed_at': row['performed_at']
            }
            for row in rows
        ]

        return jsonify({
            'success': True,
            'count': len(logs),
            'total_downtime_minutes': total_downtime,
            'logs': logs
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/maintenance', methods=['POST'])
def record_maintenance():
    """Records a maintenance and downtime log for a machine."""
    try:
        data = request.get_json() or {}
        machine_id = data.get('machine_id')
        maintenance_type = (data.get('maintenance_type') or 'PREVENTIVE').strip().upper()
        description = (data.get('description') or '').strip()
        technician = (data.get('technician') or '').strip()
        downtime_minutes = int(data.get('downtime_minutes') or 0)
        status = (data.get('status') or 'COMPLETED').strip().upper()

        if not machine_id:
            return jsonify({'success': False, 'error': 'machine_id is required'}), 400
        if not description:
            return jsonify({'success': False, 'error': 'description is required'}), 400
        if not technician:
            return jsonify({'success': False, 'error': 'technician is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check machine exists
        cursor.execute("SELECT id, name FROM machines WHERE id = ?", (machine_id,))
        machine = cursor.fetchone()
        if not machine:
            conn.close()
            return jsonify({'success': False, 'error': f'Machine #{machine_id} not found'}), 404

        cursor.execute("""
            INSERT INTO maintenance_logs (machine_id, maintenance_type, description, technician, downtime_minutes, status, performed_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
        """, (machine_id, maintenance_type, description, technician, downtime_minutes, status))
        
        log_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'log_id': log_id,
            'machine_id': machine_id,
            'message': f'Maintenance record logged for {machine["name"]}'
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    start_background_simulator(interval_seconds=3)
    app.run(debug=True, host='127.0.0.1', port=5000)
