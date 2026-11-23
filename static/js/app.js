/**
 * KOM-MICS Industrial Factory Operations Workstation
 * Authentic Industrial HMI Client Controller
 * Pure Vanilla JavaScript + Chart.js
 */

let telemetryChart = null;
let spindleChart = null;
const REFRESH_INTERVAL_MS = 5000;

// Application State
let currentTab = 'overview';
let activeDeptFilter = 'all';
let activeStateFilter = 'all';
let searchQuery = '';
let activeAlarmSev = 'all';
let activeAlarmStatus = 'all';
let activeMaintType = 'all';
let selectedMachineId = null;

let cachedMachines = [];
let cachedStats = null;
let cachedTelemetry = [];
let cachedAlarms = [];
let cachedProduction = null;
let cachedMaintenance = [];
let totalDowntimeMinutes = 0;

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initCharts();
    initMatrixControls();
    initAlarmControls();
    initMaintenanceControls();
    
    // Initial fetch
    fetchAndUpdateDashboard();
    
    // Industrial 5-second polling loop
    setInterval(fetchAndUpdateDashboard, REFRESH_INTERVAL_MS);

    // Sync button
    const btnSync = document.getElementById('btn-refresh');
    if (btnSync) {
        btnSync.addEventListener('click', () => {
            btnSync.textContent = 'SYNCING...';
            fetchAndUpdateDashboard().finally(() => {
                btnSync.textContent = 'SYNC NOW';
            });
        });
    }
});

/**
 * Initializes primary tab navigation across 4 sections.
 */
function initNavigation() {
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            navBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const targetTab = btn.getAttribute('data-tab');
            currentTab = targetTab;
            
            document.querySelectorAll('.view-panel').forEach(panel => {
                panel.classList.remove('active');
            });
            const targetPanel = document.getElementById(`view-${targetTab}`);
            if (targetPanel) targetPanel.classList.add('active');

            // Resize charts if overview tab selected
            if (targetTab === 'overview' && telemetryChart && spindleChart) {
                setTimeout(() => {
                    telemetryChart.resize();
                    spindleChart.resize();
                }, 50);
            }
        });
    });
}

/**
 * Initializes filters and search in Section 2 (Machine Matrix).
 */
function initMatrixControls() {
    // Search input
    const searchInput = document.getElementById('matrix-search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            renderMachineMatrix();
        });
    }

    // Department chips
    document.querySelectorAll('[data-dept-filter]').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('[data-dept-filter]').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            activeDeptFilter = chip.getAttribute('data-dept-filter');
            renderMachineMatrix();
        });
    });

    // State chips
    document.querySelectorAll('[data-state-filter]').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('[data-state-filter]').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            activeStateFilter = chip.getAttribute('data-state-filter');
            renderMachineMatrix();
        });
    });

    // Drawer close button
    const btnClose = document.getElementById('btn-close-inspector');
    if (btnClose) {
        btnClose.addEventListener('click', () => {
            closeInspector();
        });
    }
}

/**
 * Initializes filters in Section 3 (Alarms & Events).
 */
function initAlarmControls() {
    // Severity buttons
    document.querySelectorAll('.alarm-sev-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.alarm-sev-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeAlarmSev = btn.getAttribute('data-sev');
            renderAlarmsTable();
        });
    });

    // Status buttons
    document.querySelectorAll('.alarm-st-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.alarm-st-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeAlarmStatus = btn.getAttribute('data-status');
            renderAlarmsTable();
        });
    });
}

/**
 * Initializes controls and modal for Section 4 (Maintenance Logs).
 */
function initMaintenanceControls() {
    // Category chips
    document.querySelectorAll('.maint-type-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.maint-type-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeMaintType = btn.getAttribute('data-mtype');
            renderMaintenanceTable();
        });
    });

    // Open Modal button
    const btnOpenModal = document.getElementById('btn-open-log-modal');
    if (btnOpenModal) {
        btnOpenModal.addEventListener('click', () => {
            openMaintenanceModal(selectedMachineId || (cachedMachines[0] && cachedMachines[0].id) || 1);
        });
    }

    // Close Modal buttons
    const btnCloseModal = document.getElementById('btn-close-modal');
    if (btnCloseModal) {
        btnCloseModal.addEventListener('click', closeMaintenanceModal);
    }
    const btnCancelModal = document.getElementById('btn-cancel-modal');
    if (btnCancelModal) {
        btnCancelModal.addEventListener('click', closeMaintenanceModal);
    }

    // Backdrop click to close
    const backdrop = document.getElementById('modal-maintenance-backdrop');
    if (backdrop) {
        backdrop.addEventListener('click', (e) => {
            if (e.target === backdrop) closeMaintenanceModal();
        });
    }

    // Form submit
    const form = document.getElementById('form-record-maintenance');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const machineId = parseInt(document.getElementById('maint-machine-select').value, 10);
            const maintType = document.getElementById('maint-type-select').value;
            const downtime = parseInt(document.getElementById('maint-downtime-input').value, 10) || 0;
            const technician = document.getElementById('maint-tech-input').value.trim();
            const desc = document.getElementById('maint-desc-input').value.trim();

            if (!machineId || !technician || !desc) {
                alert('Please complete all maintenance record fields.');
                return;
            }

            try {
                const res = await fetch('/api/maintenance', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        machine_id: machineId,
                        maintenance_type: maintType,
                        downtime_minutes: downtime,
                        technician: technician,
                        description: desc,
                        status: 'COMPLETED'
                    })
                });
                const result = await res.json();
                if (result.success) {
                    closeMaintenanceModal();
                    // Refetch maintenance immediately
                    const mRes = await fetch('/api/maintenance?limit=50');
                    const mData = await mRes.json();
                    if (mData.success) {
                        cachedMaintenance = mData.logs || [];
                        totalDowntimeMinutes = mData.total_downtime_minutes || 0;
                        renderMaintenanceTable();
                    }
                    if (selectedMachineId) {
                        refreshInspector(selectedMachineId);
                    }
                } else {
                    alert('Error saving maintenance record: ' + (result.error || 'Unknown error'));
                }
            } catch (err) {
                console.error('Failed to submit maintenance log:', err);
                alert('Connection failure while submitting maintenance log.');
            }
        });
    }
}

/**
 * Main synchronization routine fetching from backend APIs.
 */
async function fetchAndUpdateDashboard() {
    try {
        const [resStats, resMachines, resTelemetry, resAlarms, resProduction, resMaintenance] = await Promise.all([
            fetch('/api/stats'),
            fetch('/api/machines'),
            fetch('/api/telemetry/recent?limit=30'),
            fetch('/api/alarms?limit=50'),
            fetch('/api/production'),
            fetch('/api/maintenance?limit=50')
        ]);

        const statsData = await resStats.json();
        const machinesData = await resMachines.json();
        const telemetryData = await resTelemetry.json();
        const alarmsData = await resAlarms.json();
        const prodData = await resProduction.json();
        const maintData = await resMaintenance.json();

        if (statsData.success) {
            cachedStats = statsData;
            updateKPIs(statsData);
        }

        if (machinesData.success) {
            cachedMachines = machinesData.machines || [];
            updateOperatingTimeline(cachedMachines);
            updateDepartmentTable(cachedMachines, cachedTelemetry);
            renderMachineMatrix();
            if (selectedMachineId) {
                refreshInspector(selectedMachineId);
            }
        }

        if (telemetryData.success) {
            cachedTelemetry = telemetryData.telemetry || [];
            updateCharts(cachedTelemetry, cachedMachines);
            updateActivityTable(cachedTelemetry);
        }

        if (alarmsData.success) {
            cachedAlarms = alarmsData.alarms || [];
            renderAlarmsTable();
            updateAlarmBadge(cachedAlarms);
        }

        if (prodData.success) {
            cachedProduction = prodData;
            renderProductionSummary(prodData);
        }

        if (maintData.success) {
            cachedMaintenance = maintData.logs || [];
            totalDowntimeMinutes = maintData.total_downtime_minutes || 0;
            renderMaintenanceTable();
        }

        // Clock update
        const clockEl = document.getElementById('last-updated-text');
        if (clockEl) {
            const now = new Date();
            clockEl.textContent = `LAST SYNC: ${now.toLocaleTimeString()}`;
        }

    } catch (err) {
        console.error('[HMI Sync Error]', err);
    }
}

/**
 * Section 1: Updates KPI Summary Banner.
 */
function updateKPIs(stats) {
    document.getElementById('val-total-machines').textContent = stats.total_machines ?? '--';
    
    const running = stats.status_summary?.RUNNING ?? 0;
    const idle = stats.status_summary?.IDLE ?? 0;
    const warning = stats.status_summary?.WARNING ?? 0;
    
    document.getElementById('val-running-machines').textContent = running;
    document.getElementById('sub-running-status').textContent = `${idle} Idle | ${warning} Warning`;
    
    document.getElementById('val-availability').textContent = `${stats.availability_percentage ?? 0}%`;
    document.getElementById('val-telemetry').textContent = Number(stats.total_telemetry_records || 0).toLocaleString();
}

/**
 * Section 1: Renders Machine Operating Status Timeline (Gantt-style blocks).
 */
function updateOperatingTimeline(machines) {
    const container = document.getElementById('operating-status-timeline');
    if (!container) return;

    container.innerHTML = machines.map(m => {
        const stClass = `st-${(m.status || 'idle').toLowerCase()}`;
        return `
            <div class="timeline-unit ${stClass}">
                <div class="tl-id">UNIT #00${m.id}</div>
                <div class="tl-name" title="${escapeHtml(m.name)}">${escapeHtml(m.name)}</div>
                <span class="tl-badge status-${m.status || 'IDLE'}">${escapeHtml(m.status)}</span>
            </div>
        `;
    }).join('');
}

/**
 * Section 1: Renders Department Status Table.
 */
function updateDepartmentTable(machines, telemetry) {
    const tbody = document.getElementById('dept-table-body');
    if (!tbody) return;

    // Group machines by department
    const depts = {};
    machines.forEach(m => {
        const d = m.department;
        if (!depts[d]) {
            depts[d] = { total: 0, running: 0, idle: 0, warning: 0, tempSum: 0, vibSum: 0, count: 0 };
        }
        depts[d].total += 1;
        if (m.status === 'RUNNING') depts[d].running += 1;
        else if (m.status === 'IDLE') depts[d].idle += 1;
        else if (m.status === 'WARNING') depts[d].warning += 1;

        if (m.temperature) {
            depts[d].tempSum += m.temperature;
            depts[d].vibSum += m.vibration;
            depts[d].count += 1;
        }
    });

    const rows = Object.entries(depts).map(([deptName, d]) => {
        const avgTemp = d.count > 0 ? (d.tempSum / d.count).toFixed(1) : '-';
        const avgVib = d.count > 0 ? (d.vibSum / d.count).toFixed(2) : '-';
        return `
            <tr>
                <td><strong>${escapeHtml(deptName)}</strong></td>
                <td style="font-family:var(--font-mono); font-weight:700;">${d.total}</td>
                <td><span class="status-tag status-RUNNING">${d.running} RUNNING</span></td>
                <td><span class="status-tag status-IDLE">${d.idle} IDLE</span></td>
                <td style="font-family:var(--font-mono); font-weight:700; color:${avgTemp > 70 ? 'var(--andon-warn)' : 'inherit'}">${avgTemp} °C</td>
                <td style="font-family:var(--font-mono); font-weight:700; color:${avgVib > 2.5 ? 'var(--andon-warn)' : 'inherit'}">${avgVib} mm/s</td>
            </tr>
        `;
    }).join('');

    tbody.innerHTML = rows || '<tr><td colspan="6" class="loading-td">No department data.</td></tr>';
}

/**
 * Section 1: Renders Department Production Summary Table (Simulated Shift Output).
 */
function renderProductionSummary(prod) {
    const tbody = document.getElementById('production-table-body');
    if (!tbody || !prod || !prod.departments) return;

    const rowsHtml = prod.departments.map(d => {
        const comp = Number(d.completion_percentage || 0);
        const scrap = Number(d.scrap_rate_percentage || 0);
        return `
            <tr>
                <td><strong>${escapeHtml(d.department)}</strong></td>
                <td style="font-family:var(--font-mono); font-weight:700;">${d.machine_count} UNITS</td>
                <td style="font-family:var(--font-mono); font-weight:700;">${Number(d.target_units).toLocaleString()} <small style="color:var(--text-muted)">PCS</small></td>
                <td style="font-family:var(--font-mono); font-weight:700; color:var(--bg-header-band);">${Number(d.actual_units).toLocaleString()} <small style="color:var(--text-muted)">PCS</small></td>
                <td style="font-family:var(--font-mono); font-weight:700; color:${d.rejected_units > 15 ? 'var(--andon-warn)' : 'inherit'}">${d.rejected_units} <small style="color:var(--text-muted)">REJECTS</small></td>
                <td style="font-family:var(--font-mono); font-weight:700; color:${scrap > 2.0 ? 'var(--andon-warn)' : 'inherit'}">${scrap.toFixed(1)}%</td>
                <td>
                    <div class="prod-progress-wrap">
                        <div class="prod-progress-track">
                            <div class="prod-progress-fill" style="width: ${Math.min(comp, 100)}%;"></div>
                        </div>
                        <span class="prod-progress-label">${comp.toFixed(1)}%</span>
                    </div>
                </td>
            </tr>
        `;
    }).join('');

    // Append Plant Summary Row
    const ps = prod.plant_summary || {};
    const plantComp = Number(ps.completion_percentage || 0);
    const plantScrap = Number(ps.scrap_rate_percentage || 0);

    const summaryRow = `
        <tr style="background-color: var(--bg-surface-alt); border-top: 2px solid var(--border-line); font-weight: 800;">
            <td><strong>PLANT TOTAL (CELL 01 SUMMARY)</strong></td>
            <td style="font-family:var(--font-mono); font-weight:800;">6 UNITS</td>
            <td style="font-family:var(--font-mono); font-weight:800;">${Number(ps.total_target_units || 0).toLocaleString()} PCS</td>
            <td style="font-family:var(--font-mono); font-weight:800; color:var(--bg-header-band);">${Number(ps.total_actual_units || 0).toLocaleString()} PCS</td>
            <td style="font-family:var(--font-mono); font-weight:800; color:var(--andon-warn);">${ps.total_rejected_units || 0} REJECTS</td>
            <td style="font-family:var(--font-mono); font-weight:800;">${plantScrap.toFixed(1)}%</td>
            <td>
                <div class="prod-progress-wrap">
                    <div class="prod-progress-track">
                        <div class="prod-progress-fill" style="width: ${Math.min(plantComp, 100)}%; background-color: var(--k-yellow);"></div>
                    </div>
                    <span class="prod-progress-label">${plantComp.toFixed(1)}%</span>
                </div>
            </td>
        </tr>
    `;

    tbody.innerHTML = rowsHtml + summaryRow;
}

/**
 * Section 2: Renders Dense Equipment Matrix Table with Search/Filters.
 */
function renderMachineMatrix() {
    const container = document.getElementById('departments-container');
    if (!container) return;

    let filtered = cachedMachines.filter(m => {
        // Search
        if (searchQuery) {
            const matchName = m.name.toLowerCase().includes(searchQuery);
            const matchModel = m.model.toLowerCase().includes(searchQuery);
            const matchTag = `#00${m.id}`.includes(searchQuery);
            if (!matchName && !matchModel && !matchTag) return false;
        }
        // Dept filter
        if (activeDeptFilter !== 'all' && m.department !== activeDeptFilter) return false;
        // State filter
        if (activeStateFilter !== 'all' && m.status !== activeStateFilter) return false;
        return true;
    });

    if (filtered.length === 0) {
        container.innerHTML = '<div class="empty-inspector-msg">No equipment matches current search or filter criteria.</div>';
        return;
    }

    let tableHtml = `
        <table class="data-table" id="matrix-units-table">
            <thead>
                <tr>
                    <th style="width: 60px;">TAG</th>
                    <th style="width: 240px;">EQUIPMENT NAME & MODEL</th>
                    <th style="width: 170px;">DEPARTMENT</th>
                    <th style="width: 90px;">STATE</th>
                    <th style="width: 110px;">VELOCITY</th>
                    <th style="width: 100px;">THERMAL</th>
                    <th style="width: 100px;">VIBRATION</th>
                    <th style="width: 120px;">LAST SYNC</th>
                    <th style="width: 70px; text-align: center;">ACTION</th>
                </tr>
            </thead>
            <tbody>
    `;

    filtered.forEach(m => {
        const isSelected = selectedMachineId === m.id ? 'selected' : '';
        const isIdle = m.status === 'IDLE';
        const spindleDisplay = isIdle ? '0' : Number(m.spindle_speed).toFixed(0);
        const isOverheat = m.temperature > 70;
        const isHighVib = m.vibration > 2.5;

        tableHtml += `
            <tr class="matrix-row ${isSelected}" data-mid="${m.id}" onclick="selectMachine(${m.id})">
                <td style="font-family:var(--font-mono); font-weight:700; color:var(--bg-header-band);">#00${m.id}</td>
                <td>
                    <strong>${escapeHtml(m.name)}</strong>
                    <span style="font-size:0.68rem; color:var(--text-muted); font-family:var(--font-mono); margin-left:4px;">[${escapeHtml(m.model)}]</span>
                </td>
                <td>${escapeHtml(m.department)}</td>
                <td><span class="status-tag status-${m.status || 'IDLE'}">${escapeHtml(m.status)}</span></td>
                <td style="font-family:var(--font-mono); font-weight:700;">${spindleDisplay} <small style="color:var(--text-muted)">RPM</small></td>
                <td style="font-family:var(--font-mono); font-weight:700;" class="${isOverheat ? 'alert-val' : ''}">${Number(m.temperature).toFixed(1)} °C</td>
                <td style="font-family:var(--font-mono); font-weight:700;" class="${isHighVib ? 'alert-val' : ''}">${Number(m.vibration).toFixed(2)} mm/s</td>
                <td style="font-family:var(--font-mono); font-size:0.7rem; color:var(--text-muted);">${escapeHtml(m.last_reading_time || '-')}</td>
                <td style="text-align: center;">
                    <button class="btn-inspect" onclick="event.stopPropagation(); selectMachine(${m.id})">INSPECT</button>
                </td>
            </tr>
        `;
    });

    tableHtml += `</tbody></table>`;
    container.innerHTML = tableHtml;
}

/**
 * Section 2: Machine Inspector Drawer (Selection, Telemetry Drill-Down & Maintenance).
 */
window.selectMachine = async function(machineId) {
    selectedMachineId = machineId;
    renderMachineMatrix();
    await refreshInspector(machineId);
};

async function refreshInspector(machineId) {
    const m = cachedMachines.find(item => item.id === machineId);
    if (!m) return;

    const titleEl = document.getElementById('inspector-machine-title');
    if (titleEl) titleEl.textContent = `UNIT #00${m.id} | ${m.name.toUpperCase()}`;

    const contentEl = document.getElementById('inspector-content');
    if (!contentEl) return;

    // Fetch historical telemetry & maintenance for this machine
    let historyRows = '';
    let maintRows = '';
    try {
        const [resTel, resMaint] = await Promise.all([
            fetch(`/api/telemetry/recent?machine_id=${machineId}&limit=8`),
            fetch(`/api/maintenance?machine_id=${machineId}&limit=4`)
        ]);

        const dataTel = await resTel.json();
        const dataMaint = await resMaint.json();

        if (dataTel.success && dataTel.telemetry.length > 0) {
            historyRows = dataTel.telemetry.map(t => `
                <tr>
                    <td>${escapeHtml(t.timestamp)}</td>
                    <td>${Number(t.spindle_speed).toFixed(0)} RPM</td>
                    <td class="${t.temperature > 70 ? 'alert-val' : ''}">${Number(t.temperature).toFixed(1)} °C</td>
                    <td class="${t.vibration > 2.5 ? 'alert-val' : ''}">${Number(t.vibration).toFixed(2)}</td>
                </tr>
            `).join('');
        } else {
            historyRows = '<tr><td colspan="4" style="text-align:center;">No history recorded yet.</td></tr>';
        }

        if (dataMaint.success && dataMaint.logs.length > 0) {
            maintRows = dataMaint.logs.map(log => `
                <tr>
                    <td style="font-family:var(--font-mono); font-size:0.68rem;">${escapeHtml(log.performed_at.split(' ')[0] || log.performed_at)}</td>
                    <td><span class="maint-tag maint-${log.maintenance_type}">${log.maintenance_type}</span></td>
                    <td style="font-weight:700;">${log.downtime_minutes}m</td>
                    <td style="font-size:0.68rem;" title="${escapeHtml(log.description)}">${escapeHtml(log.description.length > 25 ? log.description.substring(0, 25) + '...' : log.description)}</td>
                </tr>
            `).join('');
        } else {
            maintRows = '<tr><td colspan="4" style="text-align:center;">No maintenance recorded for this unit.</td></tr>';
        }

    } catch (e) {
        historyRows = '<tr><td colspan="4" style="text-align:center;">Failed to load history.</td></tr>';
        maintRows = '<tr><td colspan="4" style="text-align:center;">Failed to load maintenance.</td></tr>';
    }

    const isIdle = m.status === 'IDLE';
    const spindleDisplay = isIdle ? '0' : Number(m.spindle_speed).toFixed(0);

    contentEl.innerHTML = `
        <div class="inspector-profile">
            <div class="insp-name">${escapeHtml(m.name)}</div>
            <div class="insp-detail-row">
                <span>SPEC / MODEL:</span>
                <strong>${escapeHtml(m.model)}</strong>
            </div>
            <div class="insp-detail-row">
                <span>DEPARTMENT:</span>
                <span>${escapeHtml(m.department)}</span>
            </div>
            <div class="insp-detail-row">
                <span>OPERATING STATE:</span>
                <span class="status-tag status-${m.status || 'IDLE'}">${escapeHtml(m.status)}</span>
            </div>
        </div>

        <div class="inspector-metrics-grid">
            <div class="insp-metric-col">
                <div class="insp-m-label">VELOCITY</div>
                <div class="insp-m-val">${spindleDisplay} <small style="font-size:0.65rem">RPM</small></div>
            </div>
            <div class="insp-metric-col">
                <div class="insp-m-label">THERMAL</div>
                <div class="insp-m-val ${m.temperature > 70 ? 'alert-val' : ''}">${Number(m.temperature).toFixed(1)} °C</div>
            </div>
            <div class="insp-metric-col">
                <div class="insp-m-label">VIBRATION</div>
                <div class="insp-m-val ${m.vibration > 2.5 ? 'alert-val' : ''}">${Number(m.vibration).toFixed(2)}</div>
            </div>
        </div>

        <div style="margin-bottom: 12px;">
            <div style="font-size:0.68rem; font-weight:800; font-family:var(--font-mono); color:var(--text-muted); margin-bottom:4px;">
                HISTORICAL TELEMETRY (RECENT SAMPLES)
            </div>
            <table class="inspector-history-table">
                <thead>
                    <tr>
                        <th>TIME</th>
                        <th>RPM</th>
                        <th>TEMP</th>
                        <th>VIB</th>
                    </tr>
                </thead>
                <tbody>
                    ${historyRows}
                </tbody>
            </table>
        </div>

        <div>
            <div style="font-size:0.68rem; font-weight:800; font-family:var(--font-mono); color:var(--text-muted); margin-bottom:4px; display:flex; justify-content:space-between; align-items:center;">
                <span>MAINTENANCE & DOWNTIME LOG</span>
            </div>
            <table class="inspector-history-table">
                <thead>
                    <tr>
                        <th>DATE</th>
                        <th>TYPE</th>
                        <th>DOWN</th>
                        <th>NOTES</th>
                    </tr>
                </thead>
                <tbody>
                    ${maintRows}
                </tbody>
            </table>
            <button class="drawer-maint-btn" onclick="openMaintenanceModal(${m.id})">+ RECORD MAINTENANCE FOR UNIT #00${m.id}</button>
        </div>
    `;
}

function closeInspector() {
    selectedMachineId = null;
    renderMachineMatrix();
    const titleEl = document.getElementById('inspector-machine-title');
    if (titleEl) titleEl.textContent = 'EQUIPMENT INSPECTOR';
    const contentEl = document.getElementById('inspector-content');
    if (contentEl) {
        contentEl.innerHTML = '<div class="empty-inspector-msg">Click any equipment row in the matrix to inspect live parameters and telemetry history.</div>';
    }
}

/**
 * Section 3: Renders Structured Alarms Table with Acknowledge/Resolve Actions.
 */
function renderAlarmsTable() {
    const tbody = document.getElementById('alarms-table-body');
    if (!tbody) return;

    let filtered = cachedAlarms.filter(a => {
        if (activeAlarmSev !== 'all' && a.severity !== activeAlarmSev) return false;
        if (activeAlarmStatus !== 'all' && (a.status || 'ACTIVE').toUpperCase() !== activeAlarmStatus) return false;
        return true;
    });

    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="loading-td">No alarms matching selected filter criteria.</td></tr>';
        return;
    }

    tbody.innerHTML = filtered.map(a => {
        const st = (a.status || 'ACTIVE').toUpperCase();
        let actionsHtml = '';
        if (st === 'ACTIVE') {
            actionsHtml = `
                <button class="btn-ack" onclick="acknowledgeAlarm(${a.id})">ACK</button>
                <button class="btn-resolve" onclick="resolveAlarm(${a.id})">RESOLVE</button>
            `;
        } else if (st === 'ACKNOWLEDGED') {
            actionsHtml = `
                <button class="btn-resolve" onclick="resolveAlarm(${a.id})">RESOLVE</button>
            `;
        } else {
            actionsHtml = `<span style="color:var(--andon-run); font-family:var(--font-mono); font-size:0.65rem; font-weight:700;">✓ CLOSED</span>`;
        }

        return `
            <tr>
                <td style="font-family:var(--font-mono); font-weight:700;">#A00${a.id}</td>
                <td><span class="sev-tag sev-${a.severity}">${escapeHtml(a.severity)}</span></td>
                <td style="font-family:var(--font-mono); font-size:0.7rem;">${escapeHtml(a.timestamp)}</td>
                <td><strong>${escapeHtml(a.machine_name)}</strong></td>
                <td style="font-family:var(--font-mono); font-weight:700;">${escapeHtml(a.code)}</td>
                <td>${escapeHtml(a.description)}</td>
                <td><span class="alarm-st-tag ast-${st}">${st}</span></td>
                <td style="text-align: right;">${actionsHtml}</td>
            </tr>
        `;
    }).join('');
}

function updateAlarmBadge(alarms) {
    const badge = document.getElementById('badge-alarm-count');
    if (!badge) return;
    const activeCount = alarms.filter(a => (a.status || 'ACTIVE').toUpperCase() === 'ACTIVE').length;
    badge.textContent = activeCount;
    badge.style.display = activeCount > 0 ? 'inline-block' : 'none';
}

window.acknowledgeAlarm = async function(alarmId) {
    try {
        const res = await fetch(`/api/alarms/${alarmId}/acknowledge`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            const item = cachedAlarms.find(a => a.id === alarmId);
            if (item) item.status = 'ACKNOWLEDGED';
            renderAlarmsTable();
            updateAlarmBadge(cachedAlarms);
        }
    } catch (e) {
        console.error('Failed to acknowledge alarm:', e);
    }
};

window.resolveAlarm = async function(alarmId) {
    try {
        const res = await fetch(`/api/alarms/${alarmId}/resolve`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            const item = cachedAlarms.find(a => a.id === alarmId);
            if (item) item.status = 'RESOLVED';
            renderAlarmsTable();
            updateAlarmBadge(cachedAlarms);
        }
    } catch (e) {
        console.error('Failed to resolve alarm:', e);
    }
};

/**
 * Section 4: Renders Maintenance Logs Table.
 */
function renderMaintenanceTable() {
    const tbody = document.getElementById('maintenance-table-body');
    const summaryEl = document.getElementById('maint-downtime-summary');
    if (summaryEl) {
        summaryEl.textContent = `TOTAL RECORDED DOWNTIME: ${totalDowntimeMinutes} MINS`;
    }

    if (!tbody) return;

    let filtered = cachedMaintenance.filter(m => {
        if (activeMaintType !== 'all' && m.maintenance_type !== activeMaintType) return false;
        return true;
    });

    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="loading-td">No maintenance records matching selected category.</td></tr>';
        return;
    }

    tbody.innerHTML = filtered.map(log => {
        return `
            <tr>
                <td style="font-family:var(--font-mono); font-weight:700; color:var(--bg-header-band);">#M00${log.id}</td>
                <td style="font-family:var(--font-mono); font-size:0.7rem;">${escapeHtml(log.performed_at)}</td>
                <td><strong>#00${log.machine_id} ${escapeHtml(log.machine_name)}</strong></td>
                <td>${escapeHtml(log.department)}</td>
                <td><span class="maint-tag maint-${log.maintenance_type}">${escapeHtml(log.maintenance_type)}</span></td>
                <td style="font-family:var(--font-mono); font-weight:700; color:${log.downtime_minutes > 45 ? 'var(--andon-warn)' : 'inherit'}">${log.downtime_minutes} MINS</td>
                <td>${escapeHtml(log.technician)}</td>
                <td>${escapeHtml(log.description)}</td>
                <td><span class="status-tag status-RUNNING">${escapeHtml(log.status)}</span></td>
            </tr>
        `;
    }).join('');
}

/**
 * Opens the Record Maintenance modal.
 */
window.openMaintenanceModal = function(preselectedMachineId) {
    const backdrop = document.getElementById('modal-maintenance-backdrop');
    const select = document.getElementById('maint-machine-select');
    if (!backdrop || !select) return;

    select.innerHTML = cachedMachines.map(m => `
        <option value="${m.id}" ${m.id === preselectedMachineId ? 'selected' : ''}>
            UNIT #00${m.id} - ${escapeHtml(m.name)} [${escapeHtml(m.department)}]
        </option>
    `).join('');

    backdrop.style.display = 'flex';
};

window.closeMaintenanceModal = function() {
    const backdrop = document.getElementById('modal-maintenance-backdrop');
    if (backdrop) backdrop.style.display = 'none';
    const form = document.getElementById('form-record-maintenance');
    if (form) {
        form.reset();
        const downtimeInput = document.getElementById('maint-downtime-input');
        if (downtimeInput) downtimeInput.value = 30;
    }
};

/**
 * Initializes engineering strip charts with authentic industrial HMI styling.
 */
function initCharts() {
    // 1. Oscilloscope Line Chart (Thermal Load & Vibration)
    const ctxTelemetry = document.getElementById('telemetryChart').getContext('2d');
    telemetryChart = new Chart(ctxTelemetry, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'THERMAL LOAD (°C)',
                    data: [],
                    borderColor: '#b45309', // Komatsu Amber
                    backgroundColor: 'transparent',
                    yAxisID: 'yTemp',
                    tension: 0.1, // Linear engineering trace
                    borderWidth: 1.8,
                    pointRadius: 2.5,
                    pointHoverRadius: 4
                },
                {
                    label: 'VIBRATION (mm/s)',
                    data: [],
                    borderColor: '#002d62', // Komatsu Corporate Navy
                    backgroundColor: 'transparent',
                    yAxisID: 'yVib',
                    tension: 0.1,
                    borderWidth: 1.8,
                    pointRadius: 2.5,
                    pointHoverRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    labels: { 
                        color: '#475569', 
                        font: { size: 9, family: 'Consolas, monospace', weight: 'bold' },
                        boxWidth: 10
                    }
                },
                tooltip: {
                    callbacks: {
                        title: (items) => `CYCLE: ${items[0].label}`
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: '#e2e8f0' },
                    ticks: { 
                        color: '#64748b', 
                        maxRotation: 0, 
                        autoSkip: true, 
                        maxTicksLimit: 6,
                        font: { size: 9, family: 'Consolas, monospace' } 
                    }
                },
                yTemp: {
                    type: 'linear',
                    position: 'left',
                    grid: { color: '#e2e8f0' },
                    ticks: { color: '#b45309', font: { size: 9, family: 'Consolas, monospace' } },
                    title: { display: true, text: 'TEMP °C', color: '#b45309', font: { size: 9, weight: 'bold' } }
                },
                yVib: {
                    type: 'linear',
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    ticks: { color: '#002d62', font: { size: 9, family: 'Consolas, monospace' } },
                    title: { display: true, text: 'VIB mm/s', color: '#002d62', font: { size: 9, weight: 'bold' } }
                }
            }
        }
    });

    // 2. Machine Velocity Profile Bar Chart
    const ctxSpindle = document.getElementById('spindleChart').getContext('2d');
    spindleChart = new Chart(ctxSpindle, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'VELOCITY (RPM)',
                data: [],
                backgroundColor: [],
                borderColor: '#cbd5e1',
                borderWidth: 1,
                borderRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { color: '#e2e8f0' },
                    ticks: { color: '#475569', font: { size: 8.5, family: 'Consolas, monospace' } }
                },
                y: {
                    grid: { color: '#e2e8f0' },
                    ticks: { color: '#475569', font: { size: 9, family: 'Consolas, monospace' } },
                    title: { display: true, text: 'RPM', color: '#475569', font: { size: 9, weight: 'bold' } },
                    beginAtZero: true
                }
            }
        }
    });
}

/**
 * Updates telemetry strip-charts with chronological cycle aggregation.
 */
function updateCharts(telemetryList, machines) {
    if (!telemetryChart || !spindleChart) return;

    // Group telemetry by unique cycle timestamp
    const sorted = [...telemetryList].reverse();
    const timeGroups = new Map();

    sorted.forEach(t => {
        const timePart = t.timestamp ? (t.timestamp.includes(' ') ? t.timestamp.split(' ')[1] : t.timestamp) : '';
        if (!timePart) return;

        if (!timeGroups.has(timePart)) {
            timeGroups.set(timePart, { tempSum: 0, vibSum: 0, count: 0 });
        }
        const g = timeGroups.get(timePart);
        g.tempSum += Number(t.temperature) || 0;
        g.vibSum += Number(t.vibration) || 0;
        g.count += 1;
    });

    const labels = [];
    const avgTemps = [];
    const avgVibs = [];

    timeGroups.forEach((g, timeStr) => {
        labels.push(timeStr);
        avgTemps.push(Number((g.tempSum / g.count).toFixed(1)));
        avgVibs.push(Number((g.vibSum / g.count).toFixed(2)));
    });

    telemetryChart.data.labels = labels;
    telemetryChart.data.datasets[0].data = avgTemps;
    telemetryChart.data.datasets[1].data = avgVibs;
    telemetryChart.update();

    // Spindle Bar Chart by Unit
    if (machines && machines.length > 0) {
        spindleChart.data.labels = machines.map(m => `#00${m.id} ${m.name.replace('Robotic ', '').replace('Automated ', '').replace('Cell', '').trim()}`);
        spindleChart.data.datasets[0].data = machines.map(m => (m.status === 'IDLE' ? 0 : m.spindle_speed));
        spindleChart.data.datasets[0].backgroundColor = machines.map(m => {
            if (m.status === 'RUNNING') return '#16a34a'; // Green
            if (m.status === 'WARNING') return '#dc2626'; // Red
            return '#d97706'; // Amber
        });
        spindleChart.update();
    }
}

/**
 * Populates Section 3 historical activity & telemetry stream.
 */
function updateActivityTable(telemetryList) {
    const tbody = document.getElementById('activity-table-body');
    if (!tbody) return;

    if (!telemetryList || telemetryList.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading-td">No sensor samples recorded yet.</td></tr>';
        return;
    }

    const rowsHtml = telemetryList.slice(0, 10).map(t => {
        const status = t.status || (t.spindle_speed > 0 ? 'RUNNING' : 'IDLE');
        const isIdle = status === 'IDLE';
        const isHighTemp = t.temperature > 70;
        const isHighVib = t.vibration > 2.5;

        const statusClass = (isHighTemp || isHighVib) && !isIdle ? 'WARNING' : status;
        const statusBadge = `<span class="status-tag status-${statusClass}">${statusClass}</span>`;
        const spindleDisplay = isIdle ? '0' : Number(t.spindle_speed).toFixed(0);

        return `
            <tr>
                <td style="font-family:var(--font-mono);">${escapeHtml(t.timestamp)}</td>
                <td><strong>${escapeHtml(t.machine_name)}</strong></td>
                <td>${escapeHtml(t.department)}</td>
                <td style="font-family:var(--font-mono); font-weight:700;">${spindleDisplay} RPM</td>
                <td style="font-family:var(--font-mono); font-weight:700;" class="${isHighTemp ? 'alert-val' : ''}">${Number(t.temperature).toFixed(1)} °C</td>
                <td style="font-family:var(--font-mono); font-weight:700;" class="${isHighVib ? 'alert-val' : ''}">${Number(t.vibration).toFixed(2)}</td>
                <td>${statusBadge}</td>
            </tr>
        `;
    }).join('');

    tbody.innerHTML = rowsHtml;
}

/**
 * Utility to escape HTML and prevent XSS.
 */
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
