import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('report_assets', exist_ok=True)

# ---------------------------------------------------------------------------
# FIG 4.1: Architecture Diagram
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Colors (Komatsu inspired)
c_navy = '#002D62'
c_yellow = '#F5B800'
c_bg_layer = '#F1F5F9'
c_border = '#94A3B8'
c_box = '#FFFFFF'
c_text = '#0F172A'

# Title
ax.text(50, 96, "SYSTEM ARCHITECTURE & MULTI-TIER DATA FLOW", 
        fontsize=13, fontweight='bold', ha='center', color=c_navy, fontfamily='Arial')
ax.text(50, 92.5, "Smart Factory Monitoring System Inspired by KOM-MICS", 
        fontsize=10, fontstyle='italic', ha='center', color='#475569', fontfamily='Arial')

layers = [
    ("TIER 4: PRESENTATION & OPERATOR HMI LAYER", 
     ["Plant Overview (KPIs & Yield)", "Machine Matrix & Inspector Drawer", "Alarms & Event Management", "Maintenance & Downtime Tracker", "Dual-Axis Oscilloscope Charts"],
     71, 16, c_yellow, '#FEF3C7'),
    ("TIER 3: BACKEND REST API & APPLICATION CONTROLLER", 
     ["Flask Application Router (app.py)", "Availability & KPI Engine", "Alarm Lifecycle Controller", "Maintenance Transaction Handler", "Simulated Telemetry Buffer"],
     49, 16, c_navy, '#E2E8F0'),
    ("TIER 2: RELATIONAL DATABASE & PERSISTENCE LAYER", 
     ["SQLite (factory.db)", "Write-Ahead Logging (WAL)", "5 Normalized Tables", "Time-Series Telemetry Store", "ACID Compliant Transactions"],
     27, 16, '#334155', '#F8FAFC'),
    ("TIER 1: INDUSTRIAL ASSET SIMULATION & TELEMETRY ENGINE", 
     ["Background Simulator (simulator.py)", "6 Manufacturing Assets (KUKA, Trumpf, etc.)", "Stochastic Noise & Thermal Profiles", "Automatic Threshold Alert Trigger", "5-Second Polling & Production Loop"],
     5, 16, '#0284C7', '#E0F2FE')
]

for title, items, y_pos, height, border_color, fill_color in layers:
    # Outer Layer Box
    rect = patches.FancyBboxPatch((4, y_pos), 92, height, boxstyle="round,pad=0.5", 
                                  linewidth=1.5, edgecolor=border_color, facecolor=fill_color)
    ax.add_patch(rect)
    # Header label
    ax.text(7, y_pos + height - 3.2, title, fontsize=9.5, fontweight='bold', color=border_color, fontfamily='Arial')
    
    # Inner boxes
    n = len(items)
    box_w = 16.5
    spacing = (92 - 6 - (n * box_w)) / (n - 1) if n > 1 else 0
    start_x = 7
    for i, itm in enumerate(items):
        bx = start_x + i * (box_w + spacing)
        by = y_pos + 2.5
        b_rect = patches.FancyBboxPatch((bx, by), box_w, height - 7.5, boxstyle="round,pad=0.2",
                                        linewidth=1, edgecolor='#CBD5E1', facecolor='#FFFFFF')
        ax.add_patch(b_rect)
        # Word wrap text into box
        words = itm.split(' ')
        if len(words) > 2:
            mid = len(words) // 2
            txt = ' '.join(words[:mid]) + '\n' + ' '.join(words[mid:])
        else:
            txt = itm
        ax.text(bx + box_w/2, by + (height - 7.5)/2, txt, fontsize=7.2, fontweight='bold',
                ha='center', va='center', color=c_text, fontfamily='Arial')

# Vertical interconnecting arrows
for y_arr in [22, 44, 66]:
    ax.annotate('', xy=(50, y_arr + 4.5), xytext=(50, y_arr - 0.5),
                arrowprops=dict(arrowstyle="<->,head_width=0.4,head_length=0.6", lw=2, color=c_navy))

plt.tight_layout()
plt.savefig('report_assets/fig4_1_architecture.png', bbox_inches='tight')
plt.close()
print("Fig 4.1 generated: report_assets/fig4_1_architecture.png")

# ---------------------------------------------------------------------------
# FIG 5.1: Database Schema ERD
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 7), dpi=200)
ax.set_xlim(0, 110)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(55, 96, "RELATIONAL DATABASE SCHEMA & ENTITY-RELATIONSHIP DIAGRAM", 
        fontsize=13, fontweight='bold', ha='center', color=c_navy, fontfamily='Arial')
ax.text(55, 92.5, "SQLite Architecture (factory.db) with Foreign Key Constraints", 
        fontsize=10, fontstyle='italic', ha='center', color='#475569', fontfamily='Arial')

# Center Table: MACHINES
m_x, m_y, m_w, m_h = 42, 54, 26, 32
rect = patches.FancyBboxPatch((m_x, m_y), m_w, m_h, boxstyle="round,pad=0.5", linewidth=2, edgecolor=c_navy, facecolor='#FFFFFF')
ax.add_patch(rect)
header_rect = patches.FancyBboxPatch((m_x, m_y + m_h - 6), m_w, 6, boxstyle="round,pad=0.2", linewidth=0, facecolor=c_navy)
ax.add_patch(header_rect)
ax.text(m_x + m_w/2, m_y + m_h - 3, "MACHINES (Master)", fontsize=10, fontweight='bold', color='#FFFFFF', ha='center', va='center', fontfamily='Arial')

m_fields = [
    ("PK", "id", "INTEGER"),
    ("", "name", "TEXT"),
    ("", "model", "TEXT"),
    ("", "department", "TEXT"),
    ("", "status", "TEXT (RUNNING/IDLE/WARN)"),
    ("", "created_at", "TIMESTAMP")
]
for i, (k, col, typ) in enumerate(m_fields):
    y_line = m_y + m_h - 9.5 - i * 4.2
    ax.text(m_x + 1.5, y_line, k, fontsize=7.5, fontweight='bold', color='#DC2626' if k=='PK' else '#64748b', fontfamily='Consolas')
    ax.text(m_x + 6, y_line, col, fontsize=8, fontweight='bold', color='#0F172A', fontfamily='Consolas')
    ax.text(m_x + m_w - 1.5, y_line, typ, fontsize=7, color='#64748B', ha='right', fontfamily='Consolas')

# Satellite Tables
tables = [
    ("TELEMETRY", 4, 52, 28, 34, "#0284C7", [
        ("PK", "id", "INTEGER"),
        ("FK", "machine_id", "INTEGER"),
        ("", "spindle_speed", "REAL (RPM)"),
        ("", "vibration", "REAL (mm/s)"),
        ("", "temperature", "REAL (°C)"),
        ("", "timestamp", "TIMESTAMP")
    ]),
    ("ALARMS", 78, 52, 28, 34, "#DC2626", [
        ("PK", "id", "INTEGER"),
        ("FK", "machine_id", "INTEGER"),
        ("", "code", "TEXT (e.g. ALM-TEMP)"),
        ("", "description", "TEXT"),
        ("", "severity", "TEXT (WARNING/INFO)"),
        ("", "status", "TEXT (ACTIVE/ACK/RES)"),
        ("", "acknowledged_at", "TIMESTAMP"),
        ("", "resolved_at", "TIMESTAMP"),
        ("", "timestamp", "TIMESTAMP")
    ]),
    ("MAINTENANCE_LOGS", 12, 6, 38, 38, "#D97706", [
        ("PK", "id", "INTEGER"),
        ("FK", "machine_id", "INTEGER"),
        ("", "maintenance_type", "TEXT (PREV/CORR/INSP)"),
        ("", "description", "TEXT"),
        ("", "technician", "TEXT"),
        ("", "downtime_minutes", "INTEGER"),
        ("", "status", "TEXT (COMPLETED)"),
        ("", "performed_at", "TIMESTAMP")
    ]),
    ("PRODUCTION_RECORDS", 60, 6, 38, 38, "#16A34A", [
        ("PK", "id", "INTEGER"),
        ("FK", "machine_id", "INTEGER"),
        ("", "shift_name", "TEXT (SHIFT 1 DAY)"),
        ("", "department", "TEXT"),
        ("", "target_units", "INTEGER"),
        ("", "actual_units", "INTEGER"),
        ("", "rejected_units", "INTEGER (SCRAP)"),
        ("", "updated_at", "TIMESTAMP")
    ])
]

for tname, tx, ty, tw, th, tcolor, tfields in tables:
    rect = patches.FancyBboxPatch((tx, ty), tw, th, boxstyle="round,pad=0.5", linewidth=1.5, edgecolor=tcolor, facecolor='#FFFFFF')
    ax.add_patch(rect)
    hdr = patches.FancyBboxPatch((tx, ty + th - 5.5), tw, 5.5, boxstyle="round,pad=0.2", linewidth=0, facecolor=tcolor)
    ax.add_patch(hdr)
    ax.text(tx + tw/2, ty + th - 2.8, tname, fontsize=9, fontweight='bold', color='#FFFFFF', ha='center', va='center', fontfamily='Arial')

    for i, (k, col, typ) in enumerate(tfields):
        y_line = ty + th - 8.5 - i * 3.4
        ax.text(tx + 1.2, y_line, k, fontsize=7, fontweight='bold', color='#DC2626' if k=='PK' else ('#2563EB' if k=='FK' else '#64748b'), fontfamily='Consolas')
        ax.text(tx + 5.2, y_line, col, fontsize=7.2, fontweight='bold', color='#0F172A', fontfamily='Consolas')
        ax.text(tx + tw - 1.2, y_line, typ, fontsize=6.5, color='#64748B', ha='right', fontfamily='Consolas')

# Draw relationship connector lines (1 to Many from MACHINES)
# Machines to Telemetry (Left)
ax.annotate('', xy=(32, 69), xytext=(42, 69), arrowprops=dict(arrowstyle="<|-", lw=1.5, color='#0284C7'))
ax.text(40, 70.5, "1", fontsize=8, fontweight='bold', color=c_navy)
ax.text(33, 70.5, "N", fontsize=8, fontweight='bold', color='#0284C7')

# Machines to Alarms (Right)
ax.annotate('', xy=(78, 69), xytext=(68, 69), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#DC2626'))
ax.text(69, 70.5, "1", fontsize=8, fontweight='bold', color=c_navy)
ax.text(76, 70.5, "N", fontsize=8, fontweight='bold', color='#DC2626')

# Machines to Maintenance (Bottom Left)
ax.annotate('', xy=(38, 44), xytext=(48, 54), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#D97706'))
ax.text(49, 51, "1", fontsize=8, fontweight='bold', color=c_navy)
ax.text(39, 45, "N", fontsize=8, fontweight='bold', color='#D97706')

# Machines to Production (Bottom Right)
ax.annotate('', xy=(72, 44), xytext=(62, 54), arrowprops=dict(arrowstyle="-|>", lw=1.5, color='#16A34A'))
ax.text(61, 51, "1", fontsize=8, fontweight='bold', color=c_navy)
ax.text(71, 45, "1", fontsize=8, fontweight='bold', color='#16A34A')

plt.tight_layout()
plt.savefig('report_assets/fig5_1_schema_erd.png', bbox_inches='tight')
plt.close()
print("Fig 5.1 generated: report_assets/fig5_1_schema_erd.png")

# ---------------------------------------------------------------------------
# FIG 5.2: State Machine Diagram
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 96, "FINITE STATE MACHINE: MACHINE OPERATING & ALARM LIFECYCLE", 
        fontsize=12, fontweight='bold', ha='center', color=c_navy, fontfamily='Arial')

# Section A: Machine Operating States (Left)
ax.text(25, 88, "A. Machine Operational States (Andon)", fontsize=10, fontweight='bold', ha='center', color='#334155')

st_idle = patches.FancyBboxPatch((6, 56), 18, 18, boxstyle="round,pad=0.3", linewidth=1.8, edgecolor='#D97706', facecolor='#FEF3C7')
st_run = patches.FancyBboxPatch((30, 56), 18, 18, boxstyle="round,pad=0.3", linewidth=1.8, edgecolor='#16A34A', facecolor='#DCFCE7')
st_warn = patches.FancyBboxPatch((18, 20), 18, 18, boxstyle="round,pad=0.3", linewidth=1.8, edgecolor='#DC2626', facecolor='#FEE2E2')
ax.add_patch(st_idle)
ax.add_patch(st_run)
ax.add_patch(st_warn)

ax.text(15, 66, "IDLE", fontsize=10, fontweight='bold', ha='center', color='#92400E')
ax.text(15, 60, "Spindle: 0 RPM\nAmbient Temp", fontsize=7.2, ha='center', color='#78350F')

ax.text(39, 66, "RUNNING", fontsize=10, fontweight='bold', ha='center', color='#166534')
ax.text(39, 60, "1800-3200 RPM\nTemp: 45-68°C", fontsize=7.2, ha='center', color='#14532D')

ax.text(27, 30, "WARNING", fontsize=10, fontweight='bold', ha='center', color='#991B1B')
ax.text(27, 24, "Temp > 75°C OR\nVib > 2.5 mm/s", fontsize=7.2, ha='center', color='#7F1D1D')

# Transitions between machine states
ax.annotate('', xy=(30, 65), xytext=(24, 65), arrowprops=dict(arrowstyle="->", lw=1.5, color='#16A34A'))
ax.text(27, 67, "Start", fontsize=7, ha='center')

ax.annotate('', xy=(24, 63), xytext=(30, 63), arrowprops=dict(arrowstyle="->", lw=1.5, color='#D97706'))
ax.text(27, 59, "Pause", fontsize=7, ha='center')

ax.annotate('', xy=(27, 38), xytext=(36, 56), arrowprops=dict(arrowstyle="->", lw=1.5, color='#DC2626'))
ax.text(35, 45, "Threshold Exceeded", fontsize=6.8, color='#DC2626')

ax.annotate('', xy=(12, 56), xytext=(20, 38), arrowprops=dict(arrowstyle="->", lw=1.5, color='#475569'))
ax.text(11, 44, "Reset/Stop", fontsize=6.8, color='#475569')

# Section B: Alarm Lifecycle States (Right)
ax.text(75, 88, "B. Alarm Exception Lifecycle", fontsize=10, fontweight='bold', ha='center', color='#334155')

alm_act = patches.FancyBboxPatch((55, 48), 18, 20, boxstyle="round,pad=0.3", linewidth=1.8, edgecolor='#DC2626', facecolor='#FEE2E2')
alm_ack = patches.FancyBboxPatch((80, 48), 18, 20, boxstyle="round,pad=0.3", linewidth=1.8, edgecolor='#D97706', facecolor='#FEF3C7')
alm_res = patches.FancyBboxPatch((67, 14), 18, 20, boxstyle="round,pad=0.3", linewidth=1.8, edgecolor='#16A34A', facecolor='#DCFCE7')
ax.add_patch(alm_act)
ax.add_patch(alm_ack)
ax.add_patch(alm_res)

ax.text(64, 61, "ACTIVE", fontsize=10, fontweight='bold', ha='center', color='#991B1B')
ax.text(64, 53, "Event Logged\nUnacknowledged\nBadge Visible", fontsize=7.2, ha='center', color='#7F1D1D')

ax.text(89, 61, "ACKNOWLEDGED", fontsize=8.5, fontweight='bold', ha='center', color='#92400E')
ax.text(89, 53, "Operator Verified\nInvestigation\nIn Progress", fontsize=7.2, ha='center', color='#78350F')

ax.text(76, 27, "RESOLVED", fontsize=10, fontweight='bold', ha='center', color='#166534')
ax.text(76, 19, "Fault Cleared\nCorrective Action\n✓ CLOSED Stamp", fontsize=7.2, ha='center', color='#14532D')

# Transitions for Alarms
ax.annotate('', xy=(80, 58), xytext=(73, 58), arrowprops=dict(arrowstyle="->", lw=1.5, color='#D97706'))
ax.text(76.5, 60.5, "ACK Click", fontsize=7.2, fontweight='bold', ha='center', color='#D97706')

ax.annotate('', xy=(79, 34), xytext=(86, 48), arrowprops=dict(arrowstyle="->", lw=1.5, color='#16A34A'))
ax.text(86, 39, "RESOLVE Click", fontsize=7.2, fontweight='bold', color='#16A34A')

ax.annotate('', xy=(73, 34), xytext=(63, 48), arrowprops=dict(arrowstyle="->", lw=1.5, color='#16A34A'))
ax.text(62, 39, "Direct RESOLVE", fontsize=7.2, fontweight='bold', color='#16A34A')

plt.tight_layout()
plt.savefig('report_assets/fig5_2_state_machine.png', bbox_inches='tight')
plt.close()
print("Fig 5.2 generated: report_assets/fig5_2_state_machine.png")
