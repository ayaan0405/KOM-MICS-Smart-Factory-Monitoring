# -*- coding: utf-8 -*-
"""
Internship Report Text Content - Part 2
Chapter 4 (Theoretical Analysis) and Chapter 5 (Design and Implementation)
"""

CHAPTER_4 = {
    "title": "THEORETICAL ANALYSIS",
    "sections": [
        {
            "num": "4.1",
            "title": "Introduction to Smart Manufacturing and Industry 4.0",
            "paragraphs": [
                (
                    "Smart manufacturing represents the convergence of advanced information technology, data science, and physical industrial "
                    "operations. Broadly defined under the global banner of Industry 4.0, smart manufacturing transforms traditional, "
                    "isolated production machinery into interconnected, self-reporting cyber-physical systems. In heavy equipment manufacturing, "
                    "where capital equipment costs are enormous and component failure can jeopardize human safety and production targets, "
                    "the transition toward digitized, transparent manufacturing operations is no longer optional—it is a strategic necessity."
                ),
                (
                    "At the core of smart manufacturing is the concept of end-to-end operational visibility. Historical industrial paradigms "
                    "treated manufacturing machinery as black boxes: machines operated until an unexpected mechanical breakdown occurred, "
                    "triggering corrective maintenance after catastrophic damage had already halted the production line. Conversely, a smart "
                    "factory framework continuously captures operational parameters, tracks degradation trends, alerts supervisors to minor "
                    "thermal or vibrational variances, and enables predictive intervention long before equipment failure manifests."
                )
            ]
        },
        {
            "num": "4.2",
            "title": "Industrial IoT and Machine Health Monitoring",
            "paragraphs": [
                (
                    "The Industrial Internet of Things (IIoT) refers to the specialized application of networked sensors, edge compute gateways, "
                    "and analytical software within industrial environments. Unlike commercial or consumer IoT, IIoT demands exceptional data "
                    "reliability, deterministic communication, high environmental ruggedness, and strict protocol standards."
                ),
                (
                    "In heavy machining and fabrication environments, asset health is characterized by physical phenomena: motor rotational "
                    "velocity, bearing temperature gradients, acoustic emissions, and structural vibration levels. By instrumenting equipment "
                    "with high-frequency telemetry transducers, plant managers can capture the vital signs of industrial machinery in real time. "
                    "This continuous data stream forms the evidentiary basis for Condition-Based Monitoring (CBM), Overall Equipment Effectiveness "
                    "(OEE) evaluations, and lean manufacturing visual management."
                )
            ]
        },
        {
            "num": "4.3",
            "title": "Core Telemetry Variables in Industrial Equipment",
            "paragraphs": [
                (
                    "To construct an accurate, realistic monitoring framework, this prototype focuses on three primary telemetry variables "
                    "commonly monitored across CNC machining centers, robotic welding cells, and automated assembly fixtures. Table 4.1 "
                    "delineates the technical significance, physical dynamics, and engineering units associated with each monitored variable."
                )
            ],
            "table": {
                "number": "4.1",
                "title": "Industrial Telemetry Variables, Sampling Dynamics, and Engineering Units",
                "headers": ["Telemetry Variable", "Engineering Unit", "Industrial Significance", "Typical Operating Profile", "Failure Threshold"],
                "rows": [
                    ["Spindle Velocity", "Revolutions Per Minute (RPM)", "Indicates mechanical tool motion, cutting speed, and operational loading. Zero RPM denotes stopped/idle status.", "1800.0 – 3200.0 RPM during active machining/welding; strictly 0.0 RPM when Idle.", "> 3400.0 RPM (Overspeed hazard)"],
                    ["Thermal Load (Temperature)", "Degrees Celsius (°C)", "Reflects friction in bearings, motor windings, and weld heat dissipation. Heat buildup signals lubrication failure.", "45.0 – 68.0 °C under steady operating loads; 22.0 – 29.0 °C ambient standby.", "> 75.0 °C (Thermal degradation limit)"],
                    ["Mechanical Vibration", "Millimeters per second (mm/s)", "Measures kinematic oscillations, spindle imbalance, tool wear, and bearing race defects (RMS velocity).", "0.60 – 1.80 mm/s smooth running; < 0.15 mm/s baseline background noise.", "> 2.50 mm/s (Mechanical fault boundary)"]
                ]
            }
        },
        {
            "num": "4.4",
            "title": "Web Application Framework: Python 3.12 and Flask",
            "paragraphs": [
                (
                    "Python has emerged as the premier language for industrial data science, automation, and backend engineering due to its "
                    "clean syntax, extensive standard library, and robust ecosystem. In this project, Python 3.12 was chosen for its enhanced "
                    "execution speed, refined exception handling, and native support for background daemon threads."
                ),
                (
                    "To deliver web-based supervisory monitoring, the Flask micro-framework was selected. Unlike monolithic frameworks such as "
                    "Django, Flask provides an unopinionated, lightweight WSGI (Web Server Gateway Interface) environment that allows engineers "
                    "to construct modular RESTful APIs with minimal architectural overhead. Flask’s minimalist design makes it exceptionally "
                    "suited for embedded industrial dashboards, edge computing appliances, and supervisory microservices where rapid request-response "
                    "cycles and low memory footprints are paramount."
                )
            ]
        },
        {
            "num": "4.5",
            "title": "Relational Database Management: SQLite Architecture & Write-Ahead Logging",
            "paragraphs": [
                (
                    "Industrial monitoring requires a reliable, zero-configuration persistence engine capable of handling concurrent read and write "
                    "transactions without requiring cumbersome client-server database administration. SQLite was selected as the embedded relational "
                    "database engine (`factory.db`). SQLite is an in-process, serverless library that implements a complete, self-contained, "
                    "ACID-compliant SQL database engine."
                ),
                (
                    "A critical architectural requirement in real-time telemetry systems is managing concurrency: the background simulation engine "
                    "continuously writes new sensor samples, production tallies, and alarm events, while multiple web clients concurrently read "
                    "data to refresh dashboard visualizations. In default rollback journal mode, SQLite locks the entire database during write operations, "
                    "which can cause read timeouts and thread contention. To eliminate this bottleneck, this project configures SQLite in "
                    "Write-Ahead Logging (WAL) mode via `PRAGMA journal_mode=WAL;`. Table 4.2 contrasts the performance characteristics of standard "
                    "rollback journaling against Write-Ahead Logging."
                )
            ],
            "table": {
                "number": "4.2",
                "title": "Comparison of Relational Database Modes (Rollback Journal vs. Write-Ahead Logging)",
                "headers": ["Performance Characteristic", "Default Rollback Journal Mode", "Write-Ahead Logging (WAL) Mode"],
                "rows": [
                    ["Concurrency Mechanism", "Single-writer OR single-reader; writes block all concurrent reads completely.", "Concurrent reader-writer model; readers never block writers, and writers never block readers."],
                    ["Disk I/O Operations", "Directly writes modified database pages to main database file with dual-write overhead.", "Appends changes sequentially to separate `-wal` file; periodic atomic checkpoints commit changes."],
                    ["Query Response Latency", "Subject to intermittent latency spikes when write transactions are executing.", "Consistently ultra-low response latency (< 2 ms) for concurrent analytical read queries."],
                    ["Suitability for IIoT Telemetry", "Poor; high-frequency sensor ingestion causes `database locked` operational errors.", "Exceptional; seamlessly accommodates continuous time-series sensor ingestion alongside concurrent web queries."]
                ]
            }
        },
        {
            "num": "4.6",
            "title": "RESTful API Design & Asynchronous Client Polling Patterns",
            "paragraphs": [
                (
                    "Communication between the Python backend and the web browser conforms strictly to Representational State Transfer (REST) "
                    "architectural principles. All data exchanges are executed over standard HTTP protocols utilizing predictable URIs and standard "
                    "HTTP methods (`GET` for resource retrieval, `POST` for transaction creation). Payloads are serialized in lightweight, human-readable "
                    "JavaScript Object Notation (JSON)."
                ),
                (
                    "For telemetry synchronization, the client-side controller utilizes a controlled asynchronous polling pattern (`setInterval` at 5,000 ms). "
                    "While WebSockets represent an alternative for full-duplex streaming, asynchronous REST polling provides superior operational "
                    "resilience in industrial factory networks: it is stateless, easily traverses industrial network firewalls and proxy servers, "
                    "requires zero persistent socket maintenance, automatically recovers from intermittent network drops, and allows granular, "
                    "independent caching of statistics, machine rosters, alarm buffers, and maintenance logs."
                )
            ]
        },
        {
            "num": "4.7",
            "title": "Dynamic Engineering Data Visualization: Chart.js Canvas Rendering",
            "paragraphs": [
                (
                    "Visual representation of high-frequency engineering telemetry requires a charting library capable of smooth, hardware-accelerated "
                    "rendering without taxing client CPU resources. Chart.js (version 4.4.1) was selected for this project. Chart.js renders "
                    "visualizations onto the HTML5 `<canvas>` element using hardware-accelerated rasterization, providing superior performance over "
                    "DOM-heavy SVG libraries when updating real-time time-series streams."
                ),
                (
                    "The dashboard deploys two specialized engineering charts: (1) an Oscilloscope-style Dual-Axis Line Chart that simultaneously "
                    "plots thermal load (°C) on the left Y-axis and mechanical vibration (mm/s) on the right Y-axis against cyclic timestamps; and "
                    "(2) a Machine Velocity Profile Bar Chart that plots spindle speeds (RPM) with dynamic Andon color-coding (Green for Running, "
                    "Amber for Idle, Red for Warning). To guarantee offline operational independence on isolated factory networks, Chart.js is bundled "
                    "locally (`chart.umd.min.js`), eliminating dependencies on external Content Delivery Networks (CDNs)."
                )
            ]
        },
        {
            "num": "4.8",
            "title": "Human-Machine Interface (HMI) & Industrial UI/UX Principles",
            "paragraphs": [
                (
                    "Industrial supervisory interfaces serve a fundamentally different purpose than consumer software applications. In a factory control "
                    "room, operators must interpret mission-critical equipment statuses within seconds. Interfaces cluttered with decorative drop shadows, "
                    "animated floating cards, pastel gradients, and oversized marketing banners impede rapid cognitive processing and induce operator fatigue."
                ),
                (
                    "Inspired by Komatsu’s operational visual identity and real-world industrial workstation standards, the user interface follows strict "
                    "design heuristics: (1) High Information Density—maximizing meaningful operational data per square pixel; (2) Square-Edged Components—crisp, "
                    "technical borders (`#D0D3D6`) rather than generic bubbly rounded cards; (3) Authentic Color Palette—Komatsu Safety Yellow (`#F5B800`) "
                    "reserved exclusively for active states and critical alerts, Komatsu Corporate Navy (`#002D62`) for headers, Light Industrial Grey "
                    "(`#E9EAEC`) for the workstation chassis, and White (`#FFFFFF`) for working data tables; (4) Standard Andon Color Coding—Green for Running, "
                    "Amber for Idle/Standby, and Red for Fault/Warning; and (5) Technical Monospace Typography (Consolas) for numeric telemetry readouts."
                )
            ]
        },
        {
            "num": "4.9",
            "title": "Chapter Summary",
            "paragraphs": [
                (
                    "This theoretical analysis establishes the comprehensive engineering framework underpinning the Smart Factory Monitoring System. "
                    "By combining Python 3.12, Flask RESTful microservices, SQLite in Write-Ahead Logging mode, asynchronous client polling, "
                    "hardware-accelerated Chart.js rendering, and authentic industrial HMI design principles, the architecture provides a robust, "
                    "extensible, and lightweight foundation for real-time manufacturing supervisory monitoring. The practical translation of these "
                    "theoretical concepts into working code is detailed in the subsequent chapter."
                )
            ]
        }
    ]
}

CHAPTER_5 = {
    "title": "DESIGN AND IMPLEMENTATION",
    "sections": [
        {
            "num": "5.1",
            "title": "System Architecture & Multi-Tier Topology",
            "paragraphs": [
                (
                    "The Smart Factory Monitoring System is architectured as an integrated, multi-tier software system designed to decouple data "
                    "generation, persistence, business logic, and presentation. Figure 4.1 illustrates the four-tier architectural topology of the "
                    "entire platform."
                )
            ],
            "figure": {
                "path": "report_assets/fig4_1_architecture.png",
                "caption": "Fig 4.1 – Four-Tier System Architecture of the Smart Factory Monitoring System",
                "width": 6.2
            },
            "subsections": [
                {
                    "num": "5.1.1",
                    "title": "Architectural Tier Decomposition",
                    "paragraphs": [
                        (
                            "The system operates across four discrete layers: (1) Tier 1 – Industrial Asset Simulation Engine: an asynchronous, "
                            "daemon-threaded Python engine (`simulator.py`) that models six physical machines, generating realistic stochastic telemetry "
                            "and updating shift production progress every 3 seconds; (2) Tier 2 – Relational Persistence Layer: an embedded SQLite database "
                            "(`factory.db`) configured in Write-Ahead Logging (WAL) mode containing five normalized relational tables; (3) Tier 3 – Backend "
                            "Application & REST API Controller: a Flask application (`app.py`) providing transactional endpoints, computing plant availability "
                            "formulas, managing alarm state lifecycles, and formatting JSON responses; and (4) Tier 4 – Presentation & Operator HMI Layer: "
                            "a single-page, multi-tab industrial workstation interface built with HTML5, CSS3, Vanilla JavaScript (`app.js`), and Chart.js."
                        )
                    ]
                }
            ]
        },
        {
            "num": "5.2",
            "title": "Relational Database Schema Design",
            "paragraphs": [
                (
                    "The persistence layer is structured to maintain strict relational integrity, ensure third normal form (3NF) compliance, and "
                    "support high-frequency append-only time-series telemetry. Figure 5.1 provides the complete Entity-Relationship Diagram (ERD), "
                    "illustrating the primary and foreign key constraints linking the central `machines` master table to its satellite operational tables."
                )
            ],
            "figure": {
                "path": "report_assets/fig5_1_schema_erd.png",
                "caption": "Fig 5.1 – Relational Database Schema & Entity-Relationship Diagram (factory.db)",
                "width": 6.2
            },
            "table": {
                "number": "5.1",
                "title": "Normalized Database Schema Structure of factory.db",
                "headers": ["Table Name", "Primary Key", "Foreign Keys", "Key Operational Columns", "Data Storage Role"],
                "rows": [
                    ["machines", "id (INTEGER AUTO)", "None", "name, model, department, status, created_at", "Master equipment roster holding machine tags, model specs, and current operational states."],
                    ["telemetry", "id (INTEGER AUTO)", "machine_id -> machines(id)", "spindle_speed, vibration, temperature, timestamp", "Append-only time-series telemetry archive recording high-frequency sensor readings."],
                    ["alarms", "id (INTEGER AUTO)", "machine_id -> machines(id)", "code, description, severity, status, acknowledged_at, resolved_at, timestamp", "Event exception buffer recording threshold violation alarms and operator audit trail."],
                    ["maintenance_logs", "id (INTEGER AUTO)", "machine_id -> machines(id)", "maintenance_type, description, technician, downtime_minutes, status, performed_at", "Audit log tracking equipment downtime events, maintenance classifications, and technicians."],
                    ["production_records", "id (INTEGER AUTO)", "machine_id -> machines(id) [UNIQUE]", "shift_name, department, target_units, actual_units, rejected_units, updated_at", "Shift production tracking table storing output targets, actual good units, and scrap tallies."]
                ]
            }
        },
        {
            "num": "5.3",
            "title": "Python Flask Backend & RESTful API Implementation",
            "paragraphs": [
                (
                    "The backend server is implemented in `app.py`. Upon startup, the Flask application initializes the SQLite database schema "
                    "via `init_db()` and seeds initial equipment, baseline alarms, maintenance history, and production records via `seed_machines()`. "
                    "The application then launches the background simulator in a daemon thread and serves the single-page dashboard at route `/`."
                ),
                (
                    "To support client-side data requirements, `app.py` exposes eleven robust RESTful endpoints. Table 5.2 outlines the complete "
                    "API specification, detailing HTTP methods, URL patterns, query parameters, and functional responsibilities."
                )
            ],
            "table": {
                "number": "5.2",
                "title": "RESTful Application Programming Interface (API) Route Specification",
                "headers": ["HTTP Method", "Route Endpoint", "Parameters", "Payload Format", "Operational Role & Response Summary"],
                "rows": [
                    ["GET", "/", "None", "HTML5", "Renders the complete industrial workstation console view (templates/index.html)."],
                    ["GET", "/api/health", "None", "JSON", "Verifies database connectivity, checks table integrity, and reports asset/record tallies."],
                    ["GET", "/api/stats", "None", "JSON", "Computes high-level KPIs: monitored assets, operating units, availability %, and recent sensor averages."],
                    ["GET", "/api/machines", "None", "JSON", "Returns all 6 assets with latest telemetry; strictly enforces 0 RPM spindle speed for IDLE status."],
                    ["GET", "/api/telemetry/recent", "limit (int), machine_id (int)", "JSON", "Returns chronological telemetry samples; supports filtering to a specific machine for the drawer view."],
                    ["GET", "/api/alarms", "limit (int), status (str), severity (str)", "JSON", "Returns alarms buffer filtered by state (ACTIVE, ACKNOWLEDGED, RESOLVED) or severity."],
                    ["POST", "/api/alarms/<id>/acknowledge", "alarm_id (URL path)", "JSON", "Transitions alarm from ACTIVE to ACKNOWLEDGED; stamps `acknowledged_at` with local timestamp."],
                    ["POST", "/api/alarms/<id>/resolve", "alarm_id (URL path)", "JSON", "Transitions alarm to RESOLVED; stamps `resolved_at` with local timestamp and closes exception."],
                    ["GET", "/api/production", "None", "JSON", "Returns shift production summary, department-level targets/actuals/scrap, and progress percentages."],
                    ["GET", "/api/maintenance", "limit (int), machine_id (int)", "JSON", "Returns maintenance history logs and aggregates total plant downtime minutes recorded in SQLite."],
                    ["POST", "/api/maintenance", "machine_id, maintenance_type, downtime_minutes, technician, description", "JSON", "Inserts a new maintenance and downtime event record into `maintenance_logs` with HTTP 201 Created."]
                ]
            }
        },
        {
            "num": "5.4",
            "title": "Stochastic Asset Telemetry Simulator Engine",
            "paragraphs": [
                (
                    "Because physical access to live factory PLCs and production machinery is prohibited during an observational internship, a "
                    "dedicated background simulator engine (`simulator.py`) was engineered to generate mathematically sound, stochastic industrial telemetry. "
                    "The simulator runs within a persistent Python `threading.Thread(daemon=True)` managed by a threading event lock."
                ),
                (
                    "Every 3 seconds, `generate_cycle()` iterates over the six monitored assets, stochastically evaluating operational state transitions "
                    "using realistic industrial probability weightings: 80% probability of RUNNING, 15% probability of IDLE (standby), and 5% probability "
                    "of WARNING (threshold anomaly). Telemetry parameters are synthesized within defined physical ranges with Gaussian jitter. "
                    "Table 5.3 summarizes the operational parameter profiles assigned to each equipment model."
                )
            ],
            "table": {
                "number": "5.3",
                "title": "Stochastic Parameter Profiles for Simulated Asset Telemetry Generation",
                "headers": ["Unit Tag", "Equipment Name", "Model Specification", "Department", "Operating Velocity", "Thermal Range", "Vibration Profile"],
                "rows": [
                    ["UNIT #001", "Robotic Arc Welder #1", "KUKA KR-16 Arc", "Welding & Fabrication", "1800 – 3200 RPM", "45.0 – 68.0 °C", "0.60 – 1.80 mm/s"],
                    ["UNIT #002", "Laser Cutting CNC #1", "Trumpf TruLaser 3030", "Welding & Fabrication", "2000 – 3200 RPM", "48.0 – 68.0 °C", "0.70 – 1.80 mm/s"],
                    ["UNIT #003", "Automated Screwdriving Cell", "Atlas Copco Tensor", "Assembly", "1800 – 3000 RPM", "42.0 – 65.0 °C", "0.50 – 1.60 mm/s"],
                    ["UNIT #004", "Pick & Place Robotics Cell", "ABB IRB 1200", "Assembly", "2200 – 3200 RPM", "44.0 – 66.0 °C", "0.60 – 1.70 mm/s"],
                    ["UNIT #005", "Coordinate Measuring Machine", "Zeiss Contura CMM", "Quality Inspection", "1800 – 2800 RPM", "38.0 – 58.0 °C", "0.40 – 1.20 mm/s"],
                    ["UNIT #006", "Optical Vision Inspector", "Keyence CV-X400", "Quality Inspection", "2400 – 3200 RPM", "40.0 – 60.0 °C", "0.50 – 1.40 mm/s"]
                ]
            }
        },
        {
            "num": "5.5",
            "title": "Plant Availability Calculation Logic & Formula Derivation",
            "paragraphs": [
                (
                    "In world-class manufacturing frameworks such as Total Productive Maintenance (TPM) and Overall Equipment Effectiveness (OEE), "
                    "Availability measures the proportion of planned operating time that equipment is actually running and productive. In this "
                    "prototype, the Plant Availability ratio is calculated and displayed dynamically on the primary KPI banner."
                ),
                (
                    "The operational formula implemented within `/api/stats` is defined as:"
                ),
                (
                    "$$\\text{Plant Availability (\\%)} = \\left( \\frac{\\text{Number of Operating (RUNNING) Machines}}{\\text{Total Monitored Machines}} \\right) \\times 100$$"
                ),
                (
                    "For example, when all 6 cell machines are actively operating, Plant Availability evaluates to strictly 100.0%. If one machine "
                    "transitions to IDLE standby and one machine enters a thermal WARNING state, the availability dynamically adjusts to "
                    "$(4 / 6) \\times 100 = 66.7\\%$. This exact formula is mathematically verified and asserted during every test suite execution."
                )
            ]
        },
        {
            "num": "5.6",
            "title": "Machine Matrix & Slide-Out Inspector Drawer Implementation",
            "paragraphs": [
                (
                    "The Machine Matrix (`view-matrix`) provides a high-density, tabular SCADA equipment overview. The client controller (`app.js`) "
                    "renders equipment rows containing equipment tags, model specifications, department badges, active operational status tags, "
                    "spindle velocity, thermal load, and vibration levels. A real-time text query input filters rows instantly by searching across "
                    "machine names, models, and tag numbers, while department filter chips (`ALL`, `WELDING`, `ASSEMBLY`, `QUALITY`) and status "
                    "chips (`ALL`, `RUNNING`, `IDLE`, `WARNING`) allow multidimensional slice-and-dice filtering."
                ),
                (
                    "To support detailed machine investigation without navigating away from the matrix view, an interactive slide-out Inspector Drawer "
                    "(`matrix-inspector-drawer`) was implemented. Clicking any equipment row or its dedicated `INSPECT` action button updates the "
                    "selected machine state, highlights the active row, and issues asynchronous requests to `/api/telemetry/recent?machine_id=<id>&limit=8` "
                    "and `/api/maintenance?machine_id=<id>&limit=4`. The drawer smoothly expands to present real-time velocity/thermal/vibration gauges, "
                    "a historical telemetry table, a machine-specific maintenance audit list, and a direct `+ RECORD MAINTENANCE FOR UNIT #00X` action button."
                )
            ]
        },
        {
            "num": "5.7",
            "title": "Alarm Lifecycle Management & Finite State Machine",
            "paragraphs": [
                (
                    "Exception management is vital in manufacturing operations to prevent machine damage and quality defects. The monitoring system "
                    "implements a Finite State Machine (FSM) governing equipment operational states and alarm exception lifecycles, as illustrated "
                    "in Figure 5.2."
                )
            ],
            "figure": {
                "path": "report_assets/fig5_2_state_machine.png",
                "caption": "Fig 5.2 – Finite State Machine: Equipment Operating State & Alarm Exception Lifecycle",
                "width": 6.2
            },
            "subsections": [
                {
                    "num": "5.7.1",
                    "title": "Alarm Thresholds and State Transitions",
                    "paragraphs": [
                        (
                            "When an asset's thermal sensor exceeds 75.0 °C, the simulator flags code `ALM-TEMP-HIGH` with description "
                            "\"Thermal load exceeded (XX.X °C)\". When vibration exceeds 2.5 mm/s, code `ALM-VIB-HIGH` is generated with description "
                            "\"Vibration threshold exceeded (X.XX mm/s)\". If an active alarm does not already exist for that asset, a new record is "
                            "inserted into SQLite with status `ACTIVE`."
                        ),
                        (
                            "On the dashboard, active alarms are highlighted with red status tags and activate an unacknowledged badge counter on the "
                            "navigation bar. Clicking `ACK` issues `POST /api/alarms/<id>/acknowledge`, updating the record to `ACKNOWLEDGED` and stamping "
                            "`acknowledged_at`. Clicking `RESOLVE` issues `POST /api/alarms/<id>/resolve`, transitioning the state to `RESOLVED`, stamping "
                            "`resolved_at`, decrementing the navigation badge, and displaying a permanent `✓ CLOSED` audit stamp."
                        )
                    ]
                }
            ]
        },
        {
            "num": "5.8",
            "title": "Equipment Maintenance & Downtime Tracking Module",
            "paragraphs": [
                (
                    "To bridge the gap between real-time telemetry and physical plant maintenance practices, a dedicated Maintenance Logging module "
                    "was integrated. The module tracks six standardized industrial maintenance classifications: `PREVENTIVE` (scheduled servicing), "
                    "`CORRECTIVE` (breakdown repair), `TOOL_CHANGE` (tool/fixture replacement), `INSPECTION` (safety checks), `CALIBRATION` (sensor alignment), "
                    "and `EMERGENCY` (emergency stop recovery)."
                ),
                (
                    "The module features a high-visibility summary banner calculating total recorded plant downtime minutes (`TOTAL RECORDED DOWNTIME: XX MINS`). "
                    "Operators can filter records using category chips and record new maintenance events via an industrial modal dialog overlay. "
                    "The modal provides validated input fields for machine selection, maintenance category, downtime duration (minutes), technician name, "
                    "and work performed description, persisting the transaction into `maintenance_logs` via `POST /api/maintenance`."
                )
            ]
        },
        {
            "num": "5.9",
            "title": "Simulated Shift Production & Scrap Rate Progress Tracking",
            "paragraphs": [
                (
                    "In lean manufacturing, machine availability is directly correlated with production throughput. The monitoring system implements "
                    "a dedicated Shift Production Tracker that models output across the active shift (`SHIFT 1 (DAY)`). For each manufacturing cell, "
                    "production targets, actual good units produced, and rejected scrap units are recorded in the `production_records` table."
                ),
                (
                    "During active simulation, operating machines increment actual output units, while occasional quality defects increment scrap units. "
                    "The `/api/production` endpoint aggregates completion percentages and scrap rates ($[\\text{Rejects} / (\\text{Actual} + \\text{Rejects})] \\times 100$), "
                    "which are rendered in the Plant Overview tab using dual-tone industrial progress bars. In strict conformance with academic ethics, "
                    "all production panels are explicitly badged with notice: `[SIMULATED SHIFT PRODUCTION DATA — NON-BENCHMARK RESEARCH TELEMETRY]`."
                )
            ]
        },
        {
            "num": "5.10",
            "title": "Testing, Verification & Regression Test Suites",
            "paragraphs": [
                (
                    "To guarantee operational reliability and prevent regression defects, a comprehensive automated testing framework was implemented. "
                    "The test suite consists of three specialized test modules: (1) `test_frontend.py`: validates all HTTP routes, verifies asset MIME types, "
                    "and asserts the binding of all 15 required DOM element IDs; (2) `test_fixes.py`: mathematically asserts Plant Availability calculations, "
                    "verifies strict 0.0 RPM spindle speeds for IDLE machinery, verifies chart timestamp deduplication, and confirms cross-component status "
                    "synchronization; and (3) `test_complete_system.py`: tests end-to-end API workflows including production retrieval, maintenance POST "
                    "transactions, and alarm ACK/RESOLVE state transitions."
                ),
                (
                    "In addition to automated Python test suites, live visual and interactive verification was executed using a headless browser subagent, "
                    "validating search filtering, inspector drawer expansion, modal dialog form submission, and real-time Chart.js trace rendering "
                    "with zero JavaScript console errors."
                )
            ]
        },
        {
            "num": "5.11",
            "title": "Technical and Engineering Skills Acquired",
            "paragraphs": [
                (
                    "Developing this complete smart factory monitoring prototype enabled me to acquire and strengthen essential engineering competencies:"
                )
            ],
            "bullets": [
                ("Full-Stack Web Engineering: ", "Mastery of Python 3.12, Flask routing, WSGI application structures, and clean RESTful API endpoint design."),
                ("Embedded Relational Database Engineering: ", "Practical expertise in relational schema design, third normal form normalization, foreign key integrity constraints, and SQLite Write-Ahead Logging (WAL) configuration."),
                ("Asynchronous Client Controller Architecture: ", "Advanced proficiency in Vanilla JavaScript (ES6+), `fetch` API asynchronous concurrency, DOM manipulation, and resilient polling mechanisms."),
                ("Industrial Data Visualization: ", "Expertise in Chart.js canvas rendering, multi-axis scaling, real-time data streaming, and non-overlapping time-series grouping algorithms."),
                ("Industrial HMI & SCADA Usability: ", "Application of authentic industrial visual design heuristics, Andon color standards, high information density, and ergonomic workstation layouts."),
                ("Software Verification & Quality Assurance: ", "Design and execution of automated regression test suites, unit testing with test clients, and live browser automation testing.")
            ]
        }
    ]
}
