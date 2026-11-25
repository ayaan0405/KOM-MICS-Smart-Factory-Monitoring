# Smart Factory Monitoring System Inspired by KOM-MICS

> **Independent Academic Prototype for B.Tech CSE Internship (Course Code: CSD 4102)**  
> **Student:** Ayaan N (RRN: 230071601037)  
> **Institution:** B.S. Abdur Rahman Crescent Institute of Science and Technology, Chennai  
> **Host Organization:** Komatsu India Private Limited, Chennai Manufacturing Plant (Oragadam)  
> **Internship Period:** 22 June 2026 – 13 July 2026  

---

## 1. Project Overview

The **Smart Factory Monitoring System** is a full-stack industrial supervisory control and data acquisition (SCADA/HMI) web application. The project is an independent academic exploration inspired by observational exposure to manufacturing workflows, robotic welding cells, modular assembly bays, and the **KOM-MICS** (Komatsu Manufacturing Innovation Cloud System) industrial IoT paradigm during training at **Komatsu India Private Limited**.

The system simulates a multi-workcell heavy machinery production facility, providing plant supervisors with real-time equipment telemetry, operating availability tracking, multi-axis oscilloscope trend visualization, automated fault alarm lifecycle management, and downtime maintenance logging.

---

## 2. System Architecture

The application is structured into a robust **4-Tier Cyber-Physical Topology**:

```
[ Edge Simulation Tier ] ---> [ Backend Ingestion & REST Tier ] ---> [ Relational Persistence Tier ] ---> [ Presentation SCADA Tier ]
  - Stochastic Generator        - Python 3.12 / Flask REST APIs       - SQLite in WAL Mode                  - Vanilla JS / Chart.js
  - Gaussian Noise Models       - Non-blocking Background Thread      - 5 Normalized Relational Tables      - Komatsu Industrial UI
  - State Machine Transitions   - Heartbeat & Health Monitoring       - Relational Foreign Keys             - Slide-Out Inspector Drawer
```

1. **Edge Simulation Tier (`simulator.py`):** Runs as an independent daemon thread generating physical telemetry (Temperature °C, Vibration mm/s, Spindle RPM) across six heavy industrial machines with calibrated Gaussian noise and thermodynamic inertia.
2. **Backend Application Tier (`app.py`):** Python 3.12 Flask REST server exposing atomic CRUD endpoints (`/api/status`, `/api/machines`, `/api/alarms`, `/api/maintenance`, `/api/telemetry`).
3. **Persistence Tier (`factory.db`, `schema.sql`):** Embedded SQLite configured in **Write-Ahead Logging (WAL)** mode, eliminating read-write concurrency locks between the simulation engine and web requests.
4. **Presentation & Supervisory HMI Tier (`static/`, `templates/`):** Pure HTML5, CSS3, and JavaScript interface utilizing hardware-accelerated **Chart.js** canvases for dual-axis oscilloscope waveforms and spindle velocity profiles.

---

## 3. Core Functional Capabilities

* **Plant Overview Console:**
  * Real-time KPI banner: Monitored Assets, Operating Units, System Plant Availability %, and Telemetry Ingestion Count.
  * Real-time Andon Operating State Timeline.
  * Department Status and Shift Production Yield vs. Scrap Defect tracking.
* **Equipment Telemetry Matrix:**
  * High-density industrial table displaying live RPM, Temperature, Vibration, and Operational Status badges.
  * Instant multi-parameter search and department/status filtering.
  * Context-preserving slide-out **Inspector Drawer** displaying live sample streams, telemetry logs, and maintenance history.
* **Alarms & Fault Event Management Console:**
  * Threshold-based fault generation (Warning: Temp > 75°C, Vib > 2.0 mm/s; Critical: Temp > 85°C, Vib > 3.0 mm/s).
  * Finite State Machine (FSM) lifecycle: `ACTIVE` $\rightarrow$ `ACKNOWLEDGED` $\rightarrow$ `RESOLVED`.
  * Interactive one-click operator acknowledgment and resolution actions.
* **Equipment Maintenance & Downtime Tracker:**
  * Cumulative plant downtime counter with category filtering (Preventive, Corrective, Tool Change, Inspection, Calibration).
  * Interactive modal dialog to record technician service records, persisting downtime directly to SQLite.
* **Chronological Telemetry Stream Audit Log:**
  * High-throughput reverse-chronological sensor audit log with automatic excursion threshold highlighting.

---

## 4. Key Engineering Safeguards

* **Exact Fleet Availability Formula:**  
  $$\text{Availability} = \left(\frac{\text{Running Machines}}{\text{Total Monitored Machines}}\right) \times 100$$
* **Physical Law Consistency:** Machinery in an `IDLE` state is strictly clamped to **0.0 RPM** spindle velocity, preventing physical anomalies where stationary machines indicate active rotational velocity.
* **Oscilloscope Waveform Stability:** Monotonically advancing sliding time windows prevent horizontal timestamp collisions on dual-axis line charts.
* **High-Concurrency SQLite:** Write-Ahead Logging (`PRAGMA journal_mode=WAL`) enables simultaneous background sensor writes and sub-2ms web dashboard reads.

---

## 5. Formal University Internship Deliverables

Included within this repository are the complete, publication-grade academic report and presentation files prepared for university submission:

### Academic Report
* **[SMART_FACTORY_MONITORING_SYSTEM_INTERNSHIP_REPORT.pdf](SMART_FACTORY_MONITORING_SYSTEM_INTERNSHIP_REPORT.pdf):**  
  * **Length:** Exactly **60 pages** (10 Preliminary Pages + 50 Arabic Chapter Pages).
  * **Typography & Layout:** Adheres strictly to Crescent Institute format and the reference layout of `Musawwir1010.pdf`.
  * **Page Numbering:** Suppressed on preliminary pages; Arabic Page 1 begins at Chapter 1 (`y = 38.2 pt`).
  * **Figures & Tables:** Contains 20 numbered figures (architecture, ERD, state machine, 8 analytical charts, and 8 live dashboard UI captures) and 22 relational data tables.
  * **Official Certificate:** Page ii embeds the original signed Komatsu India Internship Certificate.
* **[SMART_FACTORY_MONITORING_SYSTEM_INTERNSHIP_REPORT.docx](SMART_FACTORY_MONITORING_SYSTEM_INTERNSHIP_REPORT.docx):**  
  * Fully formatted, editable Microsoft Word document matching the PDF layout with customized styles, cell margins, and header tables.

### Viva & Defense Presentation (10 Slides)
* **[Ayaan_Internship_Presentation.pptx](Ayaan_Internship_Presentation.pptx):**  
  * Official 10-slide presentation built from the university template and styled in official Komatsu Blue (`#002D62`).
  * Features the 6-department observational exposure matrix, verified system architecture, source code structure, and embedded certificate.
* **[Ayaan_Internship_Presentation.pdf](Ayaan_Internship_Presentation.pdf):**  
  * 16:9 widescreen ($960 \times 540\text{ pt}$) presentation export ready for review and viva projection.

---

## 6. Installation & Quick Start

### Prerequisites
* Python 3.10+ (Recommended: Python 3.12)
* Modern web browser (Chrome, Edge, Firefox)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ayaan0405/KOM-MICS-Smart-Factory-Monitoring.git
   cd KOM-MICS-Smart-Factory-Monitoring
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application:**
   ```bash
   python app.py
   ```

4. **Access the Supervisory Dashboard:**
   Open your browser and navigate to:  
   `http://localhost:5000`

---

## 7. Running Verification & Test Suites

The repository includes comprehensive automated test suites verifying all backend APIs, database transactions, telemetry clamping, and frontend contracts:

```bash
# Run comprehensive system verification
python test_complete_system.py

# Run backend API contract test suite
python test_api.py

# Run telemetry simulator test suite
python test_simulator.py
```

To recompile the exact 60-page PDF report:
```bash
python build_exact_60p_report.py
```

---

## 8. Repository Structure

```
KOM-MICS-Smart-Factory-Monitoring/
├── app.py                                                # Flask web server & REST API controller
├── simulator.py                                          # Stochastic telemetry simulation daemon
├── database.py                                           # SQLite connection helper (WAL mode)
├── schema.sql                                            # Relational DDL schema & seed data
├── factory.db                                            # Embedded SQLite database
├── requirements.txt                                      # Python package dependencies
├── README.md                                             # Project overview & documentation
│
├── build_exact_60p_report.py                             # Exact 60-page PDF report compiler
├── build_complete_report.py                              # Formatted Word (.docx) compiler
├── report_text_part1.py                                  # Prelims & Chapters 1 - 3 source text
├── report_text_part2.py                                  # Chapters 4 - 5 source text & schemas
├── report_text_part3.py                                  # Chapters 6 - 9 source text & walkthroughs
│
├── SMART_FACTORY_MONITORING_SYSTEM_INTERNSHIP_REPORT.pdf  # Final 60-page PDF internship report
├── SMART_FACTORY_MONITORING_SYSTEM_INTERNSHIP_REPORT.docx # Final editable Word report
├── Ayaan_Internship_Presentation.pptx                    # Official 10-slide PowerPoint presentation
├── Ayaan_Internship_Presentation.pdf                     # Final 16:9 widescreen presentation PDF
│
├── report_assets/                                        # Architecture diagrams, charts & UI screenshots
│   ├── komatsu_logo.png
│   ├── fig4_1_architecture.png
│   ├── fig5_1_schema_erd.png
│   ├── fig5_2_state_machine.png
│   ├── fig6_1_availability_trend.png to fig6_8_telemetry_stream.png
│   └── fig6_1_plant_overview.png to fig6_8_maintenance_modal.png
│
├── templates/
│   └── index.html                                        # Supervisory workstation single-page app
├── static/
│   ├── style.css                                         # Komatsu-inspired industrial stylesheet
│   └── app.js                                            # Client polling & Chart.js controllers
│
└── test_complete_system.py                               # Comprehensive end-to-end test suite
```

---

## 9. Academic Disclaimer

This project is an **independent academic prototype** developed exclusively for educational fulfillment of the **CSD 4102 Internship** curriculum at **B.S. Abdur Rahman Crescent Institute of Science and Technology**. It is inspired by observational training at **Komatsu India Private Limited (Chennai Plant)**. 

This software is **not an official product** of Komatsu Ltd. or Komatsu India Private Limited, does not use proprietary internal intellectual property or live factory network connections, and is not officially endorsed by Komatsu. All telemetry, alarms, and production counts are generated synthetically by the open-source software simulator engine.
