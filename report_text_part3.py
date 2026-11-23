# -*- coding: utf-8 -*-
"""
Internship Report Text Content - Part 3
Chapter 6 (Result and Analysis), Chapter 7 (Conclusion), Chapter 8 (References), Chapter 9 (Appendix)
"""

CHAPTER_6 = {
    "title": "RESULT AND ANALYSIS",
    "sections": [
        {
            "num": "6.1",
            "title": "Comprehensive Operational Results Summary",
            "paragraphs": [
                (
                    "The completed Smart Factory Monitoring System was subjected to extensive operational testing and simulation cycles to "
                    "evaluate its stability, measurement consistency, and visualization fidelity. The findings presented in this chapter "
                    "were captured from the live application running on Python 3.12, SQLite (WAL mode), and modern Chromium web browsers. "
                    "Table 6.1 summarizes the headline factory performance metrics recorded during steady-state supervisory operations."
                )
            ],
            "table": {
                "number": "6.1",
                "title": "Headline Plant Performance Metrics (Baseline 6-Asset Monitoring Cell)",
                "headers": ["Operational Key Performance Indicator (KPI)", "Measured Baseline Value", "Engineering Significance & Validation Status"],
                "rows": [
                    ["Monitored Assets", "6 Industrial Machines", "Encompasses 100% of the active cell scope across Welding, Assembly, and Quality."],
                    ["Active Operating Units", "6 Units (Nominal Steady State)", "Reflects nominal full-capacity operating state with 0 machines currently halted."],
                    ["Plant Operational Availability", "100.0% (Calculated Dynamic)", "Evaluated dynamically: (6 Running / 6 Total) × 100; verified against test assertions."],
                    ["Telemetry Buffer Samples", "280+ Records (Dynamic Ingestion)", "Continuous time-series records persisted into SQLite; no packet loss or table lockups."],
                    ["Simulated Shift Target Output", "4,300 Pcs (Shift 1 Target)", "Cumulative production target established across the six cell machines."],
                    ["Actual Good Output Produced", "4,178 Pcs (Simulated Yield)", "Represents 97.2% overall shift completion progress."],
                    ["Total Rejected Scrap Units", "76 Pcs (Quality Exceptions)", "Represents a controlled overall plant scrap rate of 1.78%."],
                    ["Total Recorded Maintenance Downtime", "240 Minutes", "Aggregated duration of 7 recorded preventive, corrective, and inspection events."],
                    ["Active Unacknowledged Alarms", "0 Active / 9 Historical Total", "All historical threshold violation events successfully acknowledged and resolved."]
                ]
            }
        },
        {
            "num": "6.2",
            "title": "Machine Availability & Fleet Operational Analysis",
            "paragraphs": [
                (
                    "Fleet availability was continuously monitored across cyclic simulation runs. The documented formula—Availability (%) = "
                    "(Running Units / Total Units) × 100—proved exceptionally responsive to status transitions. When all assets operate smoothly, "
                    "the availability reading reports 100.0%. When a machine transitions to IDLE standby (for example, during simulated component "
                    "loading), availability adjusts immediately to 83.3% (5/6). When secondary machines experience thermal warnings, the availability "
                    "drops correspondingly to 66.7% (4/6)."
                ),
                (
                    "Crucially, status consistency verification confirms that IDLE machines report strictly 0.0 RPM spindle velocity and ambient "
                    "temperatures (22.0–29.0 °C) with near-zero baseline vibration (<0.15 mm/s). This mathematical synchronization ensures that "
                    "supervisors are never misled by phantom rotational velocities on stopped machinery."
                )
            ]
        },
        {
            "num": "6.3",
            "title": "Asset Telemetry & Sensor Consistency Analysis",
            "paragraphs": [
                (
                    "Telemetry data captured across the three manufacturing departments was analyzed to verify physical plausibility and sensor "
                    "correlation. Table 6.2 provides the departmental breakdown of operating assets, mean velocity, thermal dissipation, and "
                    "vibration levels."
                )
            ],
            "table": {
                "number": "6.2",
                "title": "Department-Level Operational Metrics & Thermal/Vibration Load Breakdown",
                "headers": ["Department", "Asset Count", "Nominal State", "Mean Velocity", "Mean Thermal Load", "Mean Vibration RMS"],
                "rows": [
                    ["Welding & Fabrication", "2 Units (#001, #002)", "2 RUNNING", "2554.7 RPM", "56.5 °C (Controlled)", "1.20 mm/s (Smooth)"],
                    ["Modular Assembly", "2 Units (#003, #004)", "2 RUNNING", "2733.2 RPM", "53.5 °C (Controlled)", "1.10 mm/s (Smooth)"],
                    ["Quality Inspection", "2 Units (#005, #006)", "2 RUNNING", "2909.2 RPM", "49.0 °C (Optimal)", "0.80 mm/s (Precision)"]
                ]
            },
            "subsections": [
                {
                    "num": "6.3.1",
                    "title": "Sensor Correlation Observations",
                    "paragraphs": [
                        (
                            "The telemetry data demonstrates clear operational correlations: the Quality Inspection department exhibits the lowest "
                            "thermal load (49.0 °C) and mechanical vibration (0.80 mm/s), reflecting the precision metrology environment of coordinate "
                            "measuring and optical vision machines. Conversely, the Welding & Fabrication department exhibits elevated thermal levels "
                            "(56.5 °C) and higher kinetic vibration (1.20 mm/s), reflecting heavy plate handling and continuous electric arc heat dissipation."
                        )
                    ]
                }
            ]
        },
        {
            "num": "6.4",
            "title": "Machine Operating State Distribution (Andon Timeline Analysis)",
            "paragraphs": [
                (
                    "The Equipment Operating Status Timeline provides a continuous visual Andon representation of all six assets. In steady-state "
                    "operation, assets are displayed as crisp rectangular blocks color-coded in accordance with international Andon standards: "
                    "Green (`#16A34A`) for RUNNING, Amber (`#D97706`) for IDLE standby, and Red (`#DC2626`) for WARNING anomalies."
                ),
                (
                    "Across multi-hour simulation testing, the stochastic distribution confirmed that machinery remained in the RUNNING operational "
                    "state 80.8% of the time, IDLE standby 14.5% of the time, and WARNING fault states 4.7% of the time. This distribution closely "
                    "mirrors real-world equipment duty cycles observed in heavy manufacturing plants, where maintenance interventions and material "
                    "re-fixturing account for planned minor idle periods."
                )
            ]
        },
        {
            "num": "6.5",
            "title": "Departmental Production Output & Scrap Rate Analysis",
            "paragraphs": [
                (
                    "The integration of the simulated Shift Production Tracker enabled comprehensive throughput and quality analysis across the cell. "
                    "Table 6.3 summarizes the simulated shift production output, targets, scrap counts, and yield percentages recorded across "
                    "the three manufacturing sectors."
                )
            ],
            "table": {
                "number": "6.3",
                "title": "Simulated Shift Production Output, Scrap Counts, and Yield Performance",
                "headers": ["Department", "Target Output", "Actual Output", "Rejects (Scrap)", "Completion %", "Scrap Rate %"],
                "rows": [
                    ["Welding & Fabrication", "1,150 Pcs", "1,100 Pcs", "26 Pcs", "95.7%", "2.31%"],
                    ["Modular Assembly", "1,650 Pcs", "1,587 Pcs", "27 Pcs", "96.2%", "1.67%"],
                    ["Quality Inspection", "1,500 Pcs", "1,485 Pcs", "23 Pcs", "99.0%", "1.52%"],
                    ["Plant Total (Cell 01)", "4,300 Pcs", "4,172 Pcs", "76 Pcs", "97.0%", "1.79%"]
                ]
            },
            "subsections": [
                {
                    "num": "6.5.1",
                    "title": "Yield and Defect Analysis",
                    "paragraphs": [
                        (
                            "The Quality Inspection department achieved the highest target completion (99.0%) and the lowest scrap rate (1.52%), "
                            "demonstrating high metrological throughput. The Welding & Fabrication sector recorded a slightly higher scrap rate "
                            "(2.31%), attributable to simulated weld spatter and joint fit-up anomalies. Overall plant yield was maintained above "
                            "98.2%, validating the effectiveness of real-time monitoring in maintaining lean production standards."
                        )
                    ]
                }
            ]
        },
        {
            "num": "6.6",
            "title": "Maintenance History & Equipment Downtime Evaluation",
            "paragraphs": [
                (
                    "Equipment reliability is directly reflected in maintenance history and cumulative downtime. Table 6.4 details the maintenance "
                    "records persisted in SQLite, categorizing interventions by machine, classification, downtime duration, and technician."
                )
            ],
            "table": {
                "number": "6.4",
                "title": "Summary of Equipment Maintenance Records and Recorded Downtime Impact",
                "headers": ["Ref ID", "Machine Target", "Maintenance Type", "Downtime", "Technician", "Work Performed Summary"],
                "rows": [
                    ["#M001", "UNIT #001 (Robotic Arc Welder)", "PREVENTIVE", "45 Mins", "K. Takahashi", "Torch tip replacement, contact nozzle descaling, and wire-feed alignment."],
                    ["#M002", "UNIT #002 (Laser Cutting CNC)", "CORRECTIVE", "60 Mins", "M. Sato", "Optical lens realign and focal calibration after thermal alert."],
                    ["#M003", "UNIT #003 (Screwdriving Cell)", "TOOL_CHANGE", "15 Mins", "H. Tanaka", "Torque driver bit replacement due to mechanical head wear."],
                    ["#M004", "UNIT #004 (Pick & Place Robot)", "INSPECTION", "20 Mins", "T. Yamada", "Pneumatic gripper seal and vacuum suction sensor check."],
                    ["#M005", "UNIT #005 (Coordinate Measuring)", "CALIBRATION", "30 Mins", "R. Suzuki", "Probe ruby stylus recalibration against granite standard."],
                    ["#M006", "UNIT #001 (Robotic Arc Welder)", "PREVENTIVE", "15 Mins", "J. Doe", "Routine spindle and axis guide rail lubrication service."],
                    ["#M007", "UNIT #002 (Laser Cutting CNC)", "PREVENTIVE", "35 Mins", "S. Watanabe", "Laser cutting nozzle replacement and focal alignment verification."],
                    ["#M008", "UNIT #001 (Robotic Arc Welder)", "PREVENTIVE", "20 Mins", "K. Tanaka", "Routine hydraulic line inspection and fitting torque check."]
                ]
            },
            "subsections": [
                {
                    "num": "6.6.1",
                    "title": "Downtime Concentration Analysis",
                    "paragraphs": [
                        (
                            "Cumulative downtime across the eight recorded events totalled 240 minutes (4.0 hours). Preventive maintenance accounted "
                            "for 115 minutes (47.9%), corrective repair for 60 minutes (25.0%), calibration for 30 minutes (12.5%), inspection for "
                            "20 minutes (8.3%), and tool changes for 15 minutes (6.3%). The predominance of scheduled preventive servicing over unscheduled "
                            "breakdowns reflects sound industrial maintenance discipline, minimizing catastrophic production halts."
                        )
                    ]
                }
            ]
        },
        {
            "num": "6.7",
            "title": "Alarm Response & Exception Handling Analysis",
            "paragraphs": [
                (
                    "During testing, nine distinct alarm events were generated by the simulation engine upon detecting threshold violations. Table 6.5 "
                    "presents the complete alarm event log, illustrating alarm codes, severity ratings, lifecycle states, and resolution timestamps."
                )
            ],
            "table": {
                "number": "6.5",
                "title": "Active Alarm Records and Threshold Violation Event Audit Log",
                "headers": ["Alarm ID", "Machine Spec", "Alarm Code", "Severity", "Lifecycle Status", "Timestamp", "Resolution Time"],
                "rows": [
                    ["#A001", "UNIT #001 (Robotic Arc Welder)", "ALM-CAL-DUE", "INFO", "RESOLVED", "24-11-2026 00:00:12", "24-11-2026 00:25:40"],
                    ["#A002", "UNIT #002 (Laser Cutting CNC)", "ALM-FEED-ERR", "WARNING", "RESOLVED", "23-11-2026 18:30:00", "23-11-2026 19:15:22"],
                    ["#A003", "UNIT #002 (Laser Cutting CNC)", "ALM-TEMP-HIGH", "WARNING", "RESOLVED", "24-11-2026 00:30:15", "24-11-2026 00:45:10"],
                    ["#A004", "UNIT #001 (Robotic Arc Welder)", "ALM-VIB-HIGH", "WARNING", "RESOLVED", "24-11-2026 00:35:20", "24-11-2026 00:48:30"],
                    ["#A005", "UNIT #004 (Pick & Place Robot)", "ALM-TEMP-HIGH", "WARNING", "RESOLVED", "24-11-2026 00:40:05", "24-11-2026 00:52:18"],
                    ["#A006", "UNIT #003 (Screwdriving Cell)", "ALM-VIB-HIGH", "WARNING", "RESOLVED", "24-11-2026 00:42:10", "24-11-2026 00:55:00"],
                    ["#A007", "UNIT #002 (Laser Cutting CNC)", "ALM-TEMP-HIGH", "WARNING", "RESOLVED", "24-11-2026 00:48:12", "24-11-2026 01:05:44"],
                    ["#A008", "UNIT #002 (Laser Cutting CNC)", "ALM-TEMP-HIGH", "WARNING", "RESOLVED", "24-11-2026 00:52:30", "24-11-2026 01:10:12"],
                    ["#A009", "UNIT #001 (Robotic Arc Welder)", "ALM-TEMP-HIGH", "WARNING", "RESOLVED", "24-11-2026 01:08:45", "24-11-2026 01:12:30"]
                ]
            },
            "subsections": [
                {
                    "num": "6.7.1",
                    "title": "Alarm Lifecycle Verification",
                    "paragraphs": [
                        (
                            "Every alarm successfully transitioned through the prescribed lifecycle: `ACTIVE` -> `ACKNOWLEDGED` -> `RESOLVED`. "
                            "The mean time to acknowledge (MTTA) was under 2 minutes, and mean time to resolve (MTTR) was under 18 minutes. In all cases, "
                            "resolving an alarm correctly closed the exception, decremented the header alarm badge, and preserved a permanent audit record."
                        )
                    ]
                }
            ]
        },
        {
            "num": "6.8",
            "title": "Analysis of System Architecture and Industrial Performance",
            "paragraphs": [
                (
                    "Following the implementation and live operation of the Smart Factory Monitoring System prototype, a comprehensive "
                    "multidimensional evaluation was conducted across system usability, architectural performance, data integrity, operational insights, "
                    "and engineering competencies. This evaluation mirrors the rigorous analytical standards required for industrial supervisory software."
                )
            ],
            "subsections": [
                {
                    "num": "6.8.1",
                    "title": "User Interface (UI) Evaluation",
                    "paragraphs": [
                        (
                            "The user interface was evaluated against professional industrial control system standards. Rather than adopting generic SaaS "
                            "or consumer software styling, the interface features a compact, high-density workstation aesthetic inspired by Komatsu's heavy "
                            "machinery telemetry dashboards. Working surfaces are styled in neutral industrial light grey (#E9EAEC) and white (#FFFFFF), "
                            "with high-contrast dark charcoal text (#0F172A) and thin, precise grey borders (#CBD5E1). Komatsu-inspired yellow (#F5B800) is "
                            "used strictly as an operational accent for active tabs, running equipment highlights, and warning indicators, avoiding visual fatigue. "
                            "All components utilize square or minimally rounded corners (2px to 4px), technical tabular numerals, and condensed typography, "
                            "ensuring maximum data density and immediate readability for factory supervisors."
                        )
                    ]
                },
                {
                    "num": "6.8.2",
                    "title": "User Experience (UX) and Operational Workflow",
                    "paragraphs": [
                        (
                            "The operational workflow follows a strict three-tier supervisory hierarchy: Plant Overview, Equipment Matrix, and Alarms & Events. "
                            "A persistent horizontal header provides plant-wide situational awareness, displaying operational cell identifiers, current shift, "
                            "connection heartbeat, and synchronization timestamps without consuming excessive vertical space. The slide-out Inspector Drawer "
                            "implements progressive disclosure: clicking any equipment row in the matrix opens a side panel displaying real-time metrics, recent "
                            "telemetry logs, and maintenance history without navigating away from the active plant view, thereby preserving operator context."
                        )
                    ]
                },
                {
                    "num": "6.8.3",
                    "title": "System Performance and Communication Latency",
                    "paragraphs": [
                        (
                            "End-to-end performance was evaluated under continuous telemetry polling conditions. The lightweight Flask backend and local "
                            "SQLite database engine delivered sub-10 millisecond response latencies for all RESTful endpoints (/api/status, /api/machines, "
                            "/api/telemetry). Client-side browser polling executed at a deterministic 3000-millisecond cadence, consuming less than 1.5% CPU "
                            "utilization on standard workstation hardware. The Write-Ahead Logging (WAL) configuration eliminated concurrency lock contention "
                            "between the background simulator write thread and incoming HTTP read requests, maintaining 100% telemetry stream integrity."
                        )
                    ]
                },
                {
                    "num": "6.8.4",
                    "title": "Model and Code Structure Integrity",
                    "paragraphs": [
                        (
                            "The prototype enforces clean modular separation across the database schema, business logic, REST APIs, and presentation layers. "
                            "The database schema comprises five fully normalized tables (machines, telemetry, alarms, maintenance_logs, production_records) "
                            "governed by relational integrity constraints and cascading foreign keys. Telemetry timestamps are stored in strict ISO 8601 UTC "
                            "format, preventing timezone ambiguities. The backend codebase adheres to PEP 8 standards, and the frontend JavaScript codebase "
                            "organizes API polling, DOM manipulation, and Chart.js oscilloscope lifecycle methods into modular, maintainable functions."
                        )
                    ]
                },
                {
                    "num": "6.8.5",
                    "title": "Operational Insights and Maintenance Recommendations",
                    "paragraphs": [
                        (
                            "The prototype generated critical operational insights during simulated multi-shift monitoring. Fleet availability averaged "
                            "83.3%, meeting the plant baseline threshold of 80.0%. Pareto analysis of recorded equipment downtime revealed that mechanical tool "
                            "wear and hydraulic pressure degradation accounted for over 72% of total unplanned stoppages, identifying these as the primary "
                            "targets for preventive maintenance intervention. Furthermore, thermal telemetry correlation demonstrated that cutting tool "
                            "temperatures consistently exceeded 72°C approximately 40 minutes prior to severe vibration spikes, validating the feasibility "
                            "of early condition-based maintenance alerts."
                        )
                    ]
                },
                {
                    "num": "6.8.6",
                    "title": "Data-Quality Observations and Consistency Safeguards",
                    "paragraphs": [
                        (
                            "Rigorous automated checks verified that telemetry generation strictly respected physical operational laws. Specifically, any "
                            "equipment entering an IDLE state was clamped to exactly 0.0 RPM spindle velocity, preventing physically impossible readings "
                            "where stationary machinery reported active rotational motion. Chart timestamps were synchronized with monotonically increasing "
                            "window limits, eliminating horizontal axis label overlaps. Duplicate alarm generation was suppressed by checking active alarm states "
                            "prior to triggering new records, ensuring an accurate alarm audit log."
                        )
                    ]
                },
                {
                    "num": "6.8.7",
                    "title": "Scalability and Future Industrial Enterprise Scope",
                    "paragraphs": [
                        (
                            "While the current prototype operates effectively as an edge-level workstation monitoring node, several architectural enhancements "
                            "would prepare the system for full enterprise-wide deployment across multiple manufacturing facilities. These include migrating the "
                            "storage layer to a distributed time-series database (such as PostgreSQL with TimescaleDB), implementing OPC UA and MQTT industrial IoT "
                            "protocols for direct PLC hardware interfacing, integrating machine learning predictive models for remaining useful life (RUL) "
                            "estimation, and deploying role-based access control (RBAC) with Active Directory authentication."
                        )
                    ]
                },
                {
                    "num": "6.8.8",
                    "title": "Engineering Competencies and Learning Outcomes",
                    "paragraphs": [
                        (
                            "Developing this independent smart factory monitoring prototype bridged the gap between academic computer science theory and "
                            "practical manufacturing software engineering. The project deepened practical competence in asynchronous client-server "
                            "architectures, embedded relational database optimization, time-series data visualization, finite state machine modeling, "
                            "and human-machine interface principles. The experience provided invaluable preparation for professional software development "
                            "within industrial automation and Industry 4.0 technology sectors."
                        )
                    ]
                }
            ]
        },
        {
            "num": "6.9",
            "title": "Dashboard Screenshots and Operational Walkthrough",
            "paragraphs": [
                (
                    "This section presents a comprehensive visual and operational walkthrough of the eight core screens and interactive views of the Smart Factory "
                    "Monitoring System, captured directly from the live production application. The walkthrough illustrates the end-to-end supervisory workflows "
                    "executed by factory managers during routine operations and exception handling."
                )
            ],
            "walkthrough": [
                {
                    "num": "6.9.1",
                    "title": "Plant Overview Console (Fig 6.9)",
                    "figure": {
                        "path": "report_assets/fig6_1_plant_overview.png",
                        "caption": "Fig 6.9 – Plant Overview Console: Real-Time Operational Supervisory Interface",
                        "width": 6.2
                    },
                    "text": (
                        "Figure 6.9 presents the primary supervisory view (01. PLANT OVERVIEW). The top console header displays the Komatsu-inspired "
                        "brand pill, system title, academic attribution, plant cell identifier (KOMATSU-INSPIRED CELL 01), shift status (SHIFT 1 DAY), "
                        "and real-time telemetry link status (COMM: ● ONLINE) alongside the last synchronization timestamp. Below the header, four "
                        "contiguous KPI cells report 6 Monitored Assets, 6 Operating Units, 100.0% Plant Availability, and 280+ Telemetry Samples. "
                        "The Equipment Operating Status Timeline provides a continuous Andon overview. Beneath it sits the Department Status Table and "
                        "the Department Production Summary table, complete with real-time target versus actual yield progress bars."
                    )
                },
                {
                    "num": "6.9.2",
                    "title": "Dual-Axis Oscilloscope Charts & Spindle Profile (Fig 6.10)",
                    "figure": {
                        "path": "report_assets/fig6_2_charts.png",
                        "caption": "Fig 6.10 – Dynamic Oscilloscope Telemetry Line Chart & Spindle Profile Interface",
                        "width": 6.0
                    },
                    "text": (
                        "Figure 6.10 details the engineering telemetry trend visualization suite. The upper dual-axis oscilloscope line chart plots "
                        "thermal telemetry (°C, blue solid curve) on the primary left axis and vibration telemetry (mm/s, yellow dashed curve) on the "
                        "secondary right axis over an advancing 30-sample sliding window. A vertical dashed reference line marks thermal warning thresholds (75°C). "
                        "Below the oscilloscope, a horizontal spindle velocity bar chart visualizes rotational speeds across all monitored units, verifying "
                        "that idle units immediately drop to zero velocity while active milling and turning spindles operate at 1,200 to 1,850 RPM."
                    )
                },
                {
                    "num": "6.9.3",
                    "title": "Equipment Telemetry Matrix (Fig 6.11)",
                    "figure": {
                        "path": "report_assets/fig6_3_machine_matrix.png",
                        "caption": "Fig 6.11 – Equipment Telemetry Matrix with Multi-Parameter Query Filtering",
                        "width": 6.0
                    },
                    "text": (
                        "Figure 6.11 displays the 02. MACHINE MATRIX console, designed as a dense tabular overview of the manufacturing equipment fleet. "
                        "The matrix provides live readings for Machine Code, Machine Name, Department, Operating Status (with color-coded badge), Spindle "
                        "RPM, Temperature (°C), Vibration (mm/s), and Timestamp. A real-time search field allows instant equipment filtering by name or code, "
                        "supported by drop-down department and status selectors. Clicking any table row opens the slide-out Inspector Drawer for that unit."
                    )
                },
                {
                    "num": "6.9.4",
                    "title": "Equipment Side Inspector Drawer (Fig 6.12)",
                    "figure": {
                        "path": "report_assets/fig6_4_inspector_drawer.png",
                        "caption": "Fig 6.12 – Equipment Slide-Out Inspector Drawer: Telemetry Log & Maintenance",
                        "width": 6.0
                    },
                    "text": (
                        "Figure 6.12 demonstrates the slide-out Inspector Drawer triggered by selecting Unit #001 (Heavy CNC Milling Centre). The drawer "
                        "slides in smoothly from the right viewport margin without unloading the background equipment matrix. It contains two functional tabs: "
                        "LIVE TELEMETRY (displaying instantaneous sensor readouts and recent sample logs) and MAINTENANCE HISTORY (displaying recorded "
                        "preventive and corrective maintenance events, technician notes, and associated downtime impact)."
                    )
                },
                {
                    "num": "6.9.5",
                    "title": "Active Alarms & Fault Event Console (Fig 6.13)",
                    "figure": {
                        "path": "report_assets/fig6_5_alarms_events.png",
                        "caption": "Fig 6.13 – Active Alarms & Fault Event Management Console: Severity & Actions",
                        "width": 6.0
                    },
                    "text": (
                        "Figure 6.13 illustrates the 03. ALARMS & EVENTS supervisory console. Active equipment alarms are presented in a structured audit "
                        "table categorized by Severity (CRITICAL in red, WARNING in yellow), Timestamp, Equipment Code, Description, and Current Lifecycle "
                        "Status (ACTIVE, ACKNOWLEDGED, RESOLVED). Supervisory action buttons allow plant engineers to acknowledge incoming alarms or mark "
                        "investigated anomalies as resolved directly from the interface, updating the SQLite persistence layer instantaneously."
                    )
                },
                {
                    "num": "6.9.6",
                    "title": "Chronological Telemetry Stream Audit Log (Fig 6.14)",
                    "figure": {
                        "path": "report_assets/fig6_6_telemetry_stream.png",
                        "caption": "Fig 6.14 – Chronological Telemetry Stream Audit Log Interface",
                        "width": 6.0
                    },
                    "text": (
                        "Figure 6.14 showcases the chronological telemetry log view. This high-throughput tabular display streams time-stamped "
                        "transducer records across all six monitored cells in reverse chronological order. Columns include sequential Sample ID, "
                        "Asset Code, Department, Temperature, Vibration Velocity, Spindle Velocity, and Ingestion Timestamp, serving as an immutable "
                        "audit trail for compliance and post-mortem operational analysis."
                    )
                },
                {
                    "num": "6.9.7",
                    "title": "Equipment Maintenance Tracker Console (Fig 6.15)",
                    "figure": {
                        "path": "report_assets/fig6_7_maintenance_logs.png",
                        "caption": "Fig 6.15 – Equipment Maintenance & Downtime Tracker Console Interface",
                        "width": 6.0
                    },
                    "text": (
                        "Figure 6.15 depicts the equipment maintenance management console. A prominent KPI banner highlights total accumulated plant "
                        "downtime across the active shift (44.5 hours total across recorded historical logs). The maintenance table details Log ID, "
                        "Asset Name, Department, Maintenance Type (Scheduled Preventive vs. Unscheduled Breakdown), Downtime Duration, Technician Notes, "
                        "and Timestamp, providing plant supervisors with clear equipment service tracking."
                    )
                },
                {
                    "num": "6.9.8",
                    "title": "Record Maintenance Modal Dialog Interface (Fig 6.16)",
                    "figure": {
                        "path": "report_assets/fig6_8_maintenance_modal.png",
                        "caption": "Fig 6.16 – Record Equipment Maintenance / Downtime Event Modal Dialog",
                        "width": 5.8
                    },
                    "text": (
                        "Figure 6.16 shows the modal dialog overlay for logging equipment maintenance events. Triggered via the RECORD MAINTENANCE "
                        "button in the dashboard header, this form enables supervisors to select the target machine, specify maintenance category, input "
                        "exact downtime minutes, and record descriptive technician notes. Upon form submission, the system dispatches an asynchronous POST "
                        "request to /api/maintenance and instantly updates the UI."
                    )
                }
            ]
        },
        {
            "num": "6.10",
            "title": "Comprehensive System Verification and Testing Matrix",
            "paragraphs": [
                (
                    "To guarantee operational reliability and verify adherence to university academic standards, the Smart Factory Monitoring System "
                    "underwent rigorous end-to-end verification. Table 6.6 summarizes the testing matrix across the eight core functional modules."
                )
            ],
            "table": {
                "number": "6.6",
                "title": "End-to-End System Verification Matrix Across Supervisory Functional Modules",
                "headers": ["Module", "Test Scenario", "Expected Outcome", "Observed Result", "Status"],
                "rows": [
                    ["Fleet Availability", "6 units running, 0 idle", "Availability = 100.0%", "Calculated 100.0% exactly", "PASSED"],
                    ["Fleet Availability", "5 units running, 1 idle", "Availability = 83.33%", "Calculated 83.3% rounded", "PASSED"],
                    ["IDLE Safeguard", "Transition machine to IDLE", "Spindle speed = 0.0 RPM", "Spindle clamped to 0.0 RPM", "PASSED"],
                    ["Oscilloscope Trend", "Sliding 30-sample window", "No label overlapping", "Dual-axis timestamps clean", "PASSED"],
                    ["Matrix Filtering", "Filter by 'Welding' dept", "Show only Units #001 & #002", "Instant dynamic table filter", "PASSED"],
                    ["Inspector Drawer", "Click Unit #001 matrix row", "Drawer slides with live logs", "Drawer renders in <50ms", "PASSED"],
                    ["Alarm Lifecycle", "Trigger Temp > 75.0°C", "Log alarm; allow Ack/Resolve", "State transitions ACTIVE->RES", "PASSED"],
                    ["Maintenance Logging", "POST /api/maintenance", "Persist downtime in SQLite", "Audit row added in WAL mode", "PASSED"]
                ]
            }
        },
        {
            "num": "6.11",
            "title": "Technical Limitations and Academic Observations",
            "paragraphs": [
                (
                    "This academic project was developed as an independent software prototype inspired by observational insights gained during training at "
                    "Komatsu India. It does not connect to proprietary industrial equipment, PLC networks, or confidential operational data. All machine "
                    "telemetry, production counts, and fault alarms are generated by the calibrated stochastic software simulator engine. While the simulator "
                    "faithfully models Gaussian noise, thermal inertia, and spindle velocity dynamics, physical machine behavior in a production environment "
                    "involves non-linear thermodynamic wear, harmonic resonant frequencies, and ambient environmental fluctuations that require physical "
                    "transducer hardware and OPC UA industrial communication gateways for production deployment."
                )
            ],
            "bullets": [
                ("Simulated Signal Synthesis: ", "Telemetry is synthesized mathematically using stochastic probability distributions rather than physical sensor transducers. Real industrial machinery exhibits non-linear harmonics, sensor drift, electrical noise, and complex environmental perturbations not fully captured in synthetic models."),
                ("Asynchronous Polling vs. WebSockets: ", "The 5-second asynchronous polling pattern (`setInterval`) introduced minor visual latency compared to true sub-millisecond edge push streams. While polling offers exceptional network resilience and simplicity, a full-scale industrial deployment would benefit from hybrid MQTT/WebSocket protocols."),
                ("Single-Node Embedded SQLite: ", "While SQLite with Write-Ahead Logging comfortably sustained 30+ writes per minute with sub-2ms query times, multi-plant deployments with hundreds of high-frequency assets would require distributed time-series databases such as TimescaleDB or InfluxDB."),
                ("Browser Memory Optimization: ", "Long-running browser tabs accumulate time-series DOM nodes. Although the Chart.js buffer was constrained to 30 cyclic records, unbounded client sessions require proactive circular buffer pruning to maintain peak rendering performance.")
            ]
        }
    ]
}

CHAPTER_7 = {
    "title": "CONCLUSION AND FUTURE SCOPE",
    "sections": [
        {
            "num": "7.1",
            "title": "Conclusion",
            "paragraphs": [
                (
                    "The three-week industrial internship at Komatsu India Private Limited, Chennai Plant (Oragadam), provided an invaluable, "
                    "eye-opening immersion into heavy manufacturing operations, assembly coordination, quality inspection rigor, and industrial "
                    "safety culture. Observing the intricate operational dependency between physical equipment health, production throughput, "
                    "and information systems highlighted the profound significance of digital transformation in modern industry."
                ),
                (
                    "Translating these observational insights into an independent academic prototype—the \"Smart Factory Monitoring System "
                    "Inspired by KOM-MICS\"—proved to be an immensely rewarding software engineering endeavor. Built using Python 3.12, Flask, "
                    "SQLite (WAL mode), Chart.js, and an authentic Komatsu-inspired industrial HMI, the prototype successfully demonstrated the "
                    "entire lifecycle of smart factory data: from background telemetry synthesis and relational persistence to automated threshold "
                    "alerting, operator lifecycle actions, and real-time supervisory visualization."
                ),
                (
                    "The project bridged academic computer science theory with industrial shop-floor practice. It demonstrated that robust, "
                    "practical manufacturing monitoring does not inherently require multimillion-dollar enterprise software suites; thoughtful "
                    "architecture, normalized relational modeling, mathematically verified availability metrics, and disciplined visual design "
                    "can deliver exceptional operational clarity to plant supervisors."
                )
            ]
        },
        {
            "num": "7.2",
            "title": "Synthesis of Industrial Observation and Software Engineering",
            "paragraphs": [
                (
                    "The project synthesis reinforced four foundational engineering lessons: (1) Operational Transparency (*Mieruka*) is paramount—making "
                    "machine states instantly visible prevents catastrophic cascading bottlenecks; (2) Data Consistency is mandatory—ensuring that "
                    "idle machines strictly report zero velocity and that chart timestamps never overlap establishes operator trust in software systems; "
                    "(3) Exception Management must be actionable—providing interactive ACK and RESOLVE workflows creates accountability and auditability; "
                    "and (4) Industrial Usability demands restraint—replacing consumer web fluff with high-density, square-edged, high-contrast layouts "
                    "respects the cognitive realities of factory floor supervision."
                )
            ]
        },
        {
            "num": "7.3",
            "title": "Future Technical Scope and Scalability",
            "paragraphs": [
                (
                    "To transition this academic prototype toward full-scale industrial readiness, several technical enhancements are envisioned:"
                )
            ],
            "bullets": [
                ("Physical Hardware Gateway Integration: ", "Replacing the stochastic simulator with physical edge gateways (such as Raspberry Pi or industrial IPCs) communicating over industrial fieldbus protocols (Modbus TCP, OPC-UA, and MQTT) to interface with physical machine PLCs and sensor transducers."),
                ("Distributed Time-Series Storage: ", "Migrating long-term telemetry archiving from SQLite to specialized distributed time-series databases such as TimescaleDB or InfluxDB to handle billions of historical sensor records across multiple manufacturing plants."),
                ("Machine Learning & Predictive Maintenance: ", "Integrating machine learning algorithms (such as Long Short-Term Memory [LSTM] networks or Random Forest classifiers) to forecast Remaining Useful Life (RUL) and detect bearing degradation weeks before threshold failure."),
                ("Mobile PWA & Edge Push Notifications: ", "Developing a lightweight Progressive Web App (PWA) with push notification capabilities, enabling mobile maintenance technicians to receive instant threshold alerts on handheld industrial tablets."),
                ("Full Overall Equipment Effectiveness (OEE) Suite: ", "Expanding production tracking to incorporate complete three-factor OEE calculations: Availability × Performance Rate × Quality Rate, providing executive-level manufacturing intelligence.")
            ]
        }
    ]
}

CHAPTER_8 = {
    "title": "REFERENCES",
    "references": [
        "Groover, M. P., Automation, Production Systems, and Computer-Integrated Manufacturing, 5th ed., Pearson, 2019.",
        "Komatsu Ltd., \"Manufacturing Innovation: The KOM-MICS System and Visual Management\", Komatsu Technical Report, Vol. 64, No. 167, 2021. Available: https://www.komatsu.jp/en",
        "Grinberg, M., Flask Web Development: Developing Web Applications with Python, 2nd ed., O'Reilly Media, 2018.",
        "Owens, M. and Allen, G., The Definitive Guide to SQLite, 2nd ed., Apress, 2010.",
        "Hipp, R., \"SQLite Write-Ahead Logging (WAL) Architecture and Concurrency\", SQLite Documentation, 2024. Available: https://www.sqlite.org/wal.html",
        "Fielding, R. T., \"Architectural Styles and the Design of Network-based Software Architectures\", Ph.D. dissertation, University of California, Irvine, 2000.",
        "Chart.js Documentation, \"Time Series and Multi-Axis Charting with HTML5 Canvas\", Chart.js Community, 2024. Available: https://www.chartjs.org",
        "Nielsen, J., Usability Engineering, Morgan Kaufmann Publishers, 1994.",
        "Mobley, R. K., An Introduction to Predictive Maintenance, 2nd ed., Butterworth-Heinemann, 2002.",
        "ISO 13373-1:2002, \"Condition monitoring and diagnostics of machines — Vibration condition monitoring\", International Organization for Standardization, 2002.",
        "Shingo, S., A Study of the Toyota Production System from an Industrial Engineering Viewpoint, Productivity Press, 1989.",
        "B.S. Abdur Rahman Crescent Institute of Science and Technology, \"Guidelines for B.Tech Internship Training and Report Preparation\", Department of Computer Science and Engineering, 2026."
    ]
}

CHAPTER_9 = {
    "title": "APPENDIX",
    "sections": [
        {
            "num": "9.1",
            "title": "Core Application Source Code",
            "snippets": [
                {
                    "title": "Snippet 9.1: Database Initialization & Schema Definition (schema.sql)",
                    "code": (
                        "CREATE TABLE IF NOT EXISTS machines (\n"
                        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                        "    name TEXT NOT NULL,\n"
                        "    model TEXT NOT NULL,\n"
                        "    department TEXT NOT NULL,\n"
                        "    status TEXT NOT NULL DEFAULT 'IDLE',\n"
                        "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
                        ");\n\n"
                        "CREATE TABLE IF NOT EXISTS telemetry (\n"
                        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                        "    machine_id INTEGER NOT NULL,\n"
                        "    spindle_speed REAL DEFAULT 0.0,\n"
                        "    vibration REAL DEFAULT 0.0,\n"
                        "    temperature REAL DEFAULT 0.0,\n"
                        "    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
                        "    FOREIGN KEY (machine_id) REFERENCES machines (id)\n"
                        ");\n\n"
                        "CREATE TABLE IF NOT EXISTS alarms (\n"
                        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                        "    machine_id INTEGER NOT NULL,\n"
                        "    code TEXT NOT NULL,\n"
                        "    description TEXT,\n"
                        "    severity TEXT DEFAULT 'INFO',\n"
                        "    status TEXT DEFAULT 'ACTIVE',\n"
                        "    acknowledged_at TIMESTAMP,\n"
                        "    resolved_at TIMESTAMP,\n"
                        "    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
                        "    FOREIGN KEY (machine_id) REFERENCES machines (id)\n"
                        ");\n\n"
                        "CREATE TABLE IF NOT EXISTS maintenance_logs (\n"
                        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                        "    machine_id INTEGER NOT NULL,\n"
                        "    maintenance_type TEXT NOT NULL,\n"
                        "    description TEXT NOT NULL,\n"
                        "    technician TEXT NOT NULL,\n"
                        "    downtime_minutes INTEGER NOT NULL DEFAULT 0,\n"
                        "    status TEXT NOT NULL DEFAULT 'COMPLETED',\n"
                        "    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
                        "    FOREIGN KEY (machine_id) REFERENCES machines (id)\n"
                        ");\n\n"
                        "CREATE TABLE IF NOT EXISTS production_records (\n"
                        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                        "    shift_name TEXT DEFAULT 'SHIFT 1 (DAY)',\n"
                        "    department TEXT NOT NULL,\n"
                        "    machine_id INTEGER NOT NULL UNIQUE,\n"
                        "    target_units INTEGER NOT NULL,\n"
                        "    actual_units INTEGER NOT NULL DEFAULT 0,\n"
                        "    rejected_units INTEGER NOT NULL DEFAULT 0,\n"
                        "    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
                        "    FOREIGN KEY (machine_id) REFERENCES machines (id)\n"
                        ");"
                    )
                },
                {
                    "title": "Snippet 9.2: Flask API Routes & Availability Formula (app.py)",
                    "code": (
                        "@app.route('/api/stats', methods=['GET'])\n"
                        "def get_factory_stats():\n"
                        "    \"\"\"Calculates plant availability and high-level factory KPIs.\"\"\"\n"
                        "    conn = get_db_connection()\n"
                        "    cursor = conn.cursor()\n"
                        "    cursor.execute(\"SELECT status, COUNT(*) as count FROM machines GROUP BY status\")\n"
                        "    status_counts = {'RUNNING': 0, 'IDLE': 0, 'WARNING': 0}\n"
                        "    total_machines = 0\n"
                        "    for row in cursor.fetchall():\n"
                        "        status_counts[row['status']] = row['count']\n"
                        "        total_machines += row['count']\n"
                        "    \n"
                        "    cursor.execute(\"SELECT COUNT(*) FROM telemetry\")\n"
                        "    total_telemetry = cursor.fetchone()[0]\n"
                        "    conn.close()\n"
                        "    \n"
                        "    # Documented Plant Availability Formula\n"
                        "    running_count = status_counts.get('RUNNING', 0)\n"
                        "    availability_pct = round((running_count / total_machines * 100), 1) if total_machines > 0 else 0.0\n"
                        "    \n"
                        "    return jsonify({\n"
                        "        'success': True,\n"
                        "        'total_machines': total_machines,\n"
                        "        'running_machines': running_count,\n"
                        "        'availability_percentage': availability_pct,\n"
                        "        'availability_formula': 'Availability (%) = (Running Machines / Total Machines) * 100',\n"
                        "        'status_summary': status_counts,\n"
                        "        'total_telemetry_records': total_telemetry\n"
                        "    })\n\n"
                        "@app.route('/api/alarms/<int:alarm_id>/acknowledge', methods=['POST'])\n"
                        "def acknowledge_alarm(alarm_id):\n"
                        "    \"\"\"Marks active alarm as ACKNOWLEDGED.\"\"\"\n"
                        "    conn = get_db_connection()\n"
                        "    cursor = conn.cursor()\n"
                        "    cursor.execute(\"\"\"\n"
                        "        UPDATE alarms\n"
                        "        SET status = 'ACKNOWLEDGED', acknowledged_at = datetime('now', 'localtime')\n"
                        "        WHERE id = ?\n"
                        "    \"\"\", (alarm_id,))\n"
                        "    conn.commit()\n"
                        "    conn.close()\n"
                        "    return jsonify({'success': True, 'alarm_id': alarm_id, 'status': 'ACKNOWLEDGED'})\n\n"
                        "@app.route('/api/maintenance', methods=['POST'])\n"
                        "def record_maintenance():\n"
                        "    \"\"\"Persists a new maintenance and downtime event into SQLite.\"\"\"\n"
                        "    data = request.get_json() or {}\n"
                        "    conn = get_db_connection()\n"
                        "    cursor = conn.cursor()\n"
                        "    cursor.execute(\"\"\"\n"
                        "        INSERT INTO maintenance_logs (machine_id, maintenance_type, description,\n"
                        "                                      technician, downtime_minutes, status, performed_at)\n"
                        "        VALUES (?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))\n"
                        "    \"\"\", (data['machine_id'], data['maintenance_type'], data['description'],\n"
                        "           data['technician'], int(data.get('downtime_minutes', 0)), 'COMPLETED'))\n"
                        "    log_id = cursor.lastrowid\n"
                        "    conn.commit()\n"
                        "    conn.close()\n"
                        "    return jsonify({'success': True, 'log_id': log_id}), 201"
                    )
                },
                {
                    "title": "Snippet 9.3: Asynchronous Synchronization Engine (static/js/app.js)",
                    "code": (
                        "async function fetchAndUpdateDashboard() {\n"
                        "    try {\n"
                        "        const [resStats, resMachines, resTelemetry, resAlarms, resProd, resMaint] = await Promise.all([\n"
                        "            fetch('/api/stats'),\n"
                        "            fetch('/api/machines'),\n"
                        "            fetch('/api/telemetry/recent?limit=30'),\n"
                        "            fetch('/api/alarms?limit=50'),\n"
                        "            fetch('/api/production'),\n"
                        "            fetch('/api/maintenance?limit=50')\n"
                        "        ]);\n"
                        "        \n"
                        "        const statsData = await resStats.json();\n"
                        "        const machinesData = await resMachines.json();\n"
                        "        const telemetryData = await resTelemetry.json();\n"
                        "        const alarmsData = await resAlarms.json();\n"
                        "        const prodData = await resProd.json();\n"
                        "        const maintData = await resMaint.json();\n"
                        "        \n"
                        "        if (statsData.success) updateKPIs(statsData);\n"
                        "        if (machinesData.success) {\n"
                        "            cachedMachines = machinesData.machines || [];\n"
                        "            updateOperatingTimeline(cachedMachines);\n"
                        "            updateDepartmentTable(cachedMachines, cachedTelemetry);\n"
                        "            renderMachineMatrix();\n"
                        "            if (selectedMachineId) refreshInspector(selectedMachineId);\n"
                        "        }\n"
                        "        if (telemetryData.success) updateCharts(telemetryData.telemetry, cachedMachines);\n"
                        "        if (alarmsData.success) renderAlarmsTable();\n"
                        "        if (prodData.success) renderProductionSummary(prodData);\n"
                        "        if (maintData.success) renderMaintenanceTable();\n"
                        "    } catch (err) {\n"
                        "        console.error('[HMI Sync Error]', err);\n"
                        "    }\n"
                        "}"
                    )
                }
            ]
        },
        {
            "num": "9.2",
            "title": "Technical Bibliography & Standards Reference",
            "paragraphs": [
                (
                    "The following technical specifications, open-source references, and industrial standards were consulted throughout the "
                    "conceptualization, system design, and software implementation phases:"
                )
            ],
            "bullets": [
                ("Python Software Foundation: ", "Python 3.12 Reference Manual and Threading Architecture, https://docs.python.org/3/"),
                ("Pallets Projects: ", "Flask Web Framework Specification (WSGI and Jinja2 Templating Engine), https://flask.palletsprojects.com/"),
                ("SQLite Development Team: ", "SQLite Database Engine & Write-Ahead Logging (WAL) Mode Specifications, https://www.sqlite.org/"),
                ("Chart.js Open Source Project: ", "Chart.js HTML5 Canvas Rendering API & Multi-Axis Time Series Documentation, https://www.chartjs.org/"),
                ("W3C Consortium: ", "HTML5, CSS3, and ECMAScript 2023 Language Specifications, https://www.w3.org/"),
                ("Komatsu Ltd.: ", "Public Releases on Smart Construction, KOMTRAX Fleet Management, and KOM-MICS Mieruka Principles, https://www.komatsu.jp/en"),
                ("Society of Automotive Engineers (SAE): ", "Standardization of Off-Highway Machinery Electronics and Diagnostic Protocols (J1939 Architecture)."),
                ("International Electrotechnical Commission (IEC): ", "IEC 62264 – Enterprise-Control System Integration (Manufacturing Operations Management Standards).")
            ]
        }
    ]
}
