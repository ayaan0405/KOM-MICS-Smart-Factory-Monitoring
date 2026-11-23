# -*- coding: utf-8 -*-
"""
Internship Report Text Content - Part 1
Preliminaries, Chapter 1 (Company Overview), Chapter 2 (Role & Responsibilities), Chapter 3 (Project Overview)
"""

METADATA = {
    "title": "SMART FACTORY MONITORING SYSTEM\nINSPIRED BY KOM-MICS",
    "subtitle": "AN INTERNSHIP REPORT",
    "student_name": "AYAAN N",
    "register_no": "230071601037",
    "degree": "BACHELOR OF TECHNOLOGY",
    "branch": "COMPUTER SCIENCE AND ENGINEERING",
    "institution": "B.S. Abdur Rahman Crescent Institute of Science and Technology",
    "institution_short": "B.S. Abdur Rahman Crescent Institute of Science & Technology",
    "location": "Vandalur, Chennai – 600 048",
    "organization": "KOMATSU INDIA PRIVATE LIMITED",
    "org_plant": "Chennai Plant, Plot No. A-1, SIPCOT Industrial Park, Growth Centre, Oragadam, Thenneri (Via), Kanchipuram District, Tamil Nadu – 631 604",
    "internship_period": "22nd June 2026 to 13th July 2026",
    "submission_date": "NOVEMBER 2026",
    "academic_year": "2026–2027",
    "signatory": "Selvakumar J, DGM, HR & GA"
}

PRELIMINARIES = {
    "bonafide": {
        "title": "BONAFIDE CERTIFICATE",
        "body": (
            "Certified that this Internship Report titled \"SMART FACTORY MONITORING SYSTEM "
            "INSPIRED BY KOM-MICS\" is the bonafide work of AYAAN N (RRN : 230071601037), who is pursuing "
            "B.Tech in Computer Science and Engineering at B.S. Abdur Rahman Crescent Institute of Science "
            "and Technology, and who has successfully completed his Internship Training Program at "
            "KOMATSU INDIA PRIVATE LIMITED from 22nd June 2026 to 13th July 2026."
        )
    },
    "viva_voce": {
        "title": "VIVA VOCE EXAMINATION",
        "body": (
            "The viva voce examination of the Internship titled SMART FACTORY MONITORING SYSTEM "
            "INSPIRED BY KOM-MICS submitted by AYAAN N (RRN: 230071601037) is held on ________________."
        )
    },
    "acknowledgement": [
        (
            "I sincerely express my heartfelt gratitude to the Vice Chancellor, B.S. Abdur Rahman Crescent "
            "Institute of Science and Technology, for providing an exemplary academic environment and furnishing "
            "all necessary institutional facilities to carry out my studies and internship training successfully."
        ),
        (
            "I sincerely thank the Registrar for his continued administrative support and for providing every "
            "essential facility throughout the academic curriculum."
        ),
        (
            "I express my sincere thanks to the Dean, School of Computer Information and Mathematical Sciences, "
            "for their encouragement, motivation, and strategic support toward professional industry exposure."
        ),
        (
            "I thank the Professor and Head, Department of Computer Science and Engineering, for providing "
            "visionary oversight, academic direction, and continuous encouragement during the course of my degree program."
        ),
        (
            "I am grateful to the Faculty Members, Technical Staff, and System Administrators of the Department "
            "of Computer Science and Engineering for their academic guidance, constructive feedback, and assistance."
        ),
        (
            "I extend my sincere appreciation and deepest gratitude to the Management and Staff of Komatsu India "
            "Private Limited, Chennai Plant (Oragadam), for granting me the privilege of an observational internship. "
            "I especially thank Mr. Selvakumar J, Deputy General Manager (HR & GA), as well as the supervisory engineers "
            "across the manufacturing, assembly, inspection, and IT divisions for their generous briefings, "
            "operational explanations, and professional mentorship during my plant visits."
        ),
        (
            "Finally, I express my sincere gratitude to my family and peers for their continuous moral support "
            "and encouragement, which motivated me to conceptualize and independently develop this academic "
            "smart factory monitoring prototype."
        )
    ],
    "abstract": [
        (
            "This internship report presents the technical insights, operational observations, and academic prototype "
            "developed following my three-week industrial internship at Komatsu India Private Limited, Chennai Plant, "
            "located in Oragadam, Tamil Nadu, from 22 June 2026 to 13 July 2026. The internship was primarily observational, "
            "focusing on real-world heavy engineering manufacturing methodologies, multi-station fabrication, modular assembly, "
            "quality verification, and industrial information management systems. During this training program, I gained deep "
            "exposure to six major operational divisions: the Welding and Fabrication Shop, Modular and Final Assembly Lines, "
            "Testing and Quality Inspection, Industrial Safety (EHS), Material Handling Logistics, and the Plant Information "
            "Technology Department."
        ),
        (
            "Observing the intricate coordination required across heavy equipment manufacturing lines motivated the development "
            "of an independent academic research prototype titled \"Smart Factory Monitoring System Inspired by KOM-MICS\". "
            "The project draws architectural inspiration from Komatsu’s publicly described KOM-MICS (Komatsu Manufacturing "
            "Innovation & Construction System) concept of \"Mieruka\" (visual management). The prototype is strictly an "
            "independent academic exploration designed to demonstrate how factory-floor telemetry—encompassing machine operational "
            "states, spindle velocities, thermal loads, mechanical vibration levels, shift production targets, and equipment downtime—can "
            "be collected, analyzed, persisted, and visualized through a modern web-based supervisory dashboard."
        ),
        (
            "The system is built on a robust, multi-tier software stack comprising Python 3.12, Flask web micro-framework, SQLite "
            "with Write-Ahead Logging (WAL) for persistent time-series data storage, and an industrial-grade frontend engineered "
            "with HTML5, CSS3, Vanilla JavaScript, and Chart.js. The application integrates a background stochastic telemetry "
            "simulator that models six representative manufacturing assets across three production cells: Robotic Arc Welder and Laser "
            "Cutting CNC (Welding & Fabrication), Automated Screwdriving Cell and Pick & Place Robotics (Assembly), and Coordinate "
            "Measuring Machine and Optical Vision Inspector (Quality Inspection). All data is simulated; the prototype does not interface "
            "with proprietary Komatsu systems or physical factory PLCs."
        ),
        (
            "The completed dashboard incorporates four core modules: a Plant Overview console with high-density KPI metrics, an "
            "Equipment Operating Status Timeline, and a simulated Shift Production Summary with scrap rate tracking; a dense Machine "
            "Matrix with real-time query filtering and an interactive slide-out Inspector Drawer; an Alarms and Events console featuring "
            "threshold alert generation (>75°C thermal, >2.5 mm/s vibration) and an interactive Acknowledge/Resolve lifecycle; and an "
            "Equipment Maintenance & Downtime Tracker that persists downtime events into SQLite. Through this comprehensive effort, "
            "I bridged theoretical computer science principles with industrial smart manufacturing practices, gaining invaluable "
            "practical competence in full-stack web engineering, embedded relational persistence, REST API design, and industrial HMI principles."
        )
    ],
    "abbreviations": [
        ("API", "Application Programming Interface"),
        ("CMM", "Coordinate Measuring Machine"),
        ("CNC", "Computer Numerical Control"),
        ("CSS", "Cascading Style Sheets"),
        ("CSV", "Comma-Separated Values"),
        ("DB", "Database"),
        ("DGM", "Deputy General Manager"),
        ("DOM", "Document Object Model"),
        ("EHS", "Environmental Health and Safety"),
        ("ERD", "Entity-Relationship Diagram"),
        ("ETL", "Extract, Transform, Load"),
        ("FSM", "Finite State Machine"),
        ("HMI", "Human-Machine Interface"),
        ("HTTP", "Hypertext Transfer Protocol"),
        ("IIoT", "Industrial Internet of Things"),
        ("JSON", "JavaScript Object Notation"),
        ("KPI", "Key Performance Indicator"),
        ("KOM-MICS", "Komatsu Manufacturing Innovation & Construction System"),
        ("MICS", "Manufacturing Innovation and Construction System"),
        ("MTBF", "Mean Time Between Failures"),
        ("MTTR", "Mean Time to Repair"),
        ("OEE", "Overall Equipment Effectiveness"),
        ("PLC", "Programmable Logic Controller"),
        ("REST", "Representational State Transfer"),
        ("RMS", "Root Mean Square"),
        ("RPM", "Revolutions Per Minute"),
        ("SCADA", "Supervisory Control and Data Acquisition"),
        ("SQL", "Structured Query Language"),
        ("SQLite", "Self-Contained Serverless Relational Database Engine"),
        ("UI", "User Interface"),
        ("UX", "User Experience"),
        ("WAL", "Write-Ahead Logging"),
        ("WSGI", "Web Server Gateway Interface")
    ]
}

CHAPTER_1 = {
    "title": "COMPANY OVERVIEW",
    "sections": [
        {
            "num": "1.1",
            "title": "Company Overview",
            "paragraphs": [
                (
                    "Komatsu Limited is a global manufacturer of construction, mining, forestry, and industrial "
                    "machinery, founded in 1921 in Komatsu City, Ishikawa Prefecture, Japan. Over more than a century of "
                    "engineering excellence, the enterprise has grown into one of the world's preeminent capital goods "
                    "manufacturers, renowned for uncompromising reliability, technological leadership, and industrial innovation. "
                    "Operating under the guiding philosophy of \"Creating value through manufacturing and technology innovation "
                    "to empower a sustainable future where people, businesses, and our planet thrive together\", Komatsu delivers "
                    "durable equipment and integrated technology solutions to global infrastructure and resource sectors."
                ),
                (
                    "Komatsu India Private Limited (KIPL) was established as a wholly owned subsidiary of Komatsu Limited to serve "
                    "the rapidly modernizing Indian infrastructure, mining, and heavy industrial sectors. Headquartered with its "
                    "flagship manufacturing facility in Tamil Nadu, Komatsu India engineers, manufactures, and supports world-class "
                    "mining dump trucks, hydraulic excavators, and related heavy equipment tailored to withstand rigorous domestic "
                    "operating environments while conforming strictly to Komatsu's uncompromising international quality benchmarks."
                ),
                (
                    "The company operates through an integrated corporate structure encompassing heavy manufacturing plants, specialized "
                    "parts distribution warehouses, certified rebuild centers, and a nationwide technical service network. Through its "
                    "partnership with domestic distribution and support partners such as Larsen & Toubro (L&T), Komatsu equipment "
                    "powers critical national infrastructure initiatives, including major mineral extraction sites, national highway corridors, "
                    "mega-scale irrigation projects, and urban development undertakings."
                )
            ]
        },
        {
            "num": "1.2",
            "title": "Company Website and Digital Infrastructure",
            "paragraphs": [
                (
                    "The primary digital platform of the parent organization is accessible at https://www.komatsu.jp/en and "
                    "https://www.komatsuindia.in. These portals serve as comprehensive repositories detailing Komatsu’s global corporate "
                    "governance, equipment portfolio, research initiatives, sustainability declarations, and investor relations. The online "
                    "presence outlines Komatsu’s comprehensive smart construction and smart manufacturing roadmaps, emphasizing digitized "
                    "mine and factory operations."
                ),
                (
                    "At the industrial technology level, Komatsu has pioneered connected machinery frameworks, most notably through "
                    "KOMTRAX (Komatsu Machine Tracking System) for off-highway fleet management and KOM-MICS (Komatsu Manufacturing "
                    "Innovation & Construction System) for internal factory production optimization. These digital architectures enable "
                    "remote telemetry monitoring, autonomous equipment dispatch, machine health analytics, and fuel efficiency optimization, "
                    "establishing Komatsu as a technology-forward leader in digital industrial operations."
                )
            ]
        },
        {
            "num": "1.3",
            "title": "Chennai Manufacturing Plant (Oragadam Facility)",
            "paragraphs": [
                (
                    "Komatsu India’s primary manufacturing hub is situated at Plot No. A-1, SIPCOT Industrial Park, Growth Centre, "
                    "Oragadam, Thenneri (Via), Kanchipuram District, Tamil Nadu – 631 604. Located within Chennai’s premier industrial "
                    "and automotive corridor, the Oragadam plant represents a state-of-the-art capital investment that incorporates "
                    "advanced Japanese fabrication methodologies, automated welding complexes, heavy machining cells, and specialized "
                    "assembly lines dedicated to off-highway mining dump trucks and hydraulic excavators."
                ),
                (
                    "The Oragadam facility is characterized by high operational precision and stringent quality control. Equipment "
                    "manufactured at this facility includes high-capacity mechanical and electrical drive mining dump trucks (such as the "
                    "HD785 series) and hydraulic mining excavators (such as the PC210 and PC1250 series). The plant comprises distinct "
                    "functional zones, including raw material staging, automated laser cutting and plate preparation, robotic arc welding, "
                    "structural fabrication, shot blasting and automated paint shops, progressive modular assembly bays, and extensive "
                    "end-of-line functional test tracks."
                )
            ]
        },
        {
            "num": "1.4",
            "title": "Manufacturing Operations and Business Context",
            "paragraphs": [
                (
                    "Heavy equipment manufacturing involves substantial engineering complexity, strict structural integrity demands, and "
                    "extended cycle times. Unlike high-volume consumer goods assembly, the production of 100-ton mining dump trucks requires "
                    "the synchronized fabrication of massive steel chassis structures, precision alignment of high-pressure hydraulic circuits, "
                    "heavy-duty powertrain integration, and rigorous testing of electronic control units (ECUs)."
                ),
                (
                    "In this operational context, manufacturing downtime, weld defects, or assembly bottlenecks carry significant cost "
                    "implications. To maintain global competitiveness, Komatsu implements the \"Komatsu Way\"—a unified set of corporate "
                    "values prioritizing quality first (SLQDC: Safety, Law, Quality, Delivery, Cost), gemba-oriented problem solving "
                    "(direct observation of physical workplace realities), and visual management (\"Mieruka\"). The Oragadam plant embodies "
                    "these principles through standardized work procedures, comprehensive Andon status notification networks, and relentless "
                    "Kaizen (continuous improvement) initiatives."
                )
            ]
        }
    ]
}

CHAPTER_2 = {
    "title": "ROLE AND RESPONSIBILITIES",
    "sections": [
        {
            "num": "2.1",
            "title": "Internship Role",
            "paragraphs": [
                (
                    "During the internship period from 22 June 2026 to 13 July 2026, my official role at Komatsu India Private Limited "
                    "was that of an Industrial Observational Trainee. The internship was structured as an immersive academic-industrial "
                    "training program designed to give undergraduate engineering students direct exposure to modern manufacturing operations, "
                    "plant engineering workflows, quality assurance systems, and corporate workplace culture."
                ),
                (
                    "In strict adherence to company safety regulations and intellectual property confidentiality guidelines, my role was "
                    "strictly non-interventional and observational. I was not involved in physical machine operation, hazardous material "
                    "handling, production code modification, or proprietary database administration. Instead, my responsibility was to "
                    "observe, analyze, document, and learn the interconnected disciplines that govern an advanced heavy machinery "
                    "manufacturing plant, translating those observations into foundational engineering insights."
                )
            ]
        },
        {
            "num": "2.2",
            "title": "Manufacturing Departments Observed",
            "paragraphs": [
                (
                    "Under the guidance of plant engineers, supervisory personnel, and HR mentors, I conducted structured rotational "
                    "observations across six vital plant divisions at the Oragadam facility. Table 2.1 summarizes the operational focus "
                    "and engineering observations made within each division."
                )
            ],
            "table": {
                "number": "2.1",
                "title": "Overview of Manufacturing & Operational Divisions Observed at Komatsu India",
                "headers": ["Department", "Core Manufacturing Operations", "Key Engineering Observations"],
                "rows": [
                    ["Welding & Fabrication", "CNC flame/laser plate cutting, heavy multi-pass robotic arc welding, structural chassis fabrication, ultrasonic weld inspection.", "High thermal generation, strict weld penetration standards, fixture clamping precision, robotic path repeatability."],
                    ["Modular & Final Assembly", "Hydraulic piping installation, diesel powertrain mounting, electrical wiring harness routing, cab sub-assembly, final mechanical integration.", "Progressive takt-time management, torque-tightening verification, error-proofing (Poka-Yoke), modular component kitting."],
                    ["Testing & Inspection", "Static pressure hydraulic leak tests, engine dynamic performance analysis, Coordinate Measuring Machine (CMM) dimensional checks, test track trials.", "Stringent tolerance verification, calibration standards, non-destructive testing (NDT), automated sensor inspection."],
                    ["Safety (EHS)", "Safety induction, Personal Protective Equipment (PPE) enforcement, emergency stop protocols, 5S workplace organization, ergonomic assessments.", "Zero-accident philosophy, visual safety signage, pedestrian-forklift segregation, hazardous zone interlocks."],
                    ["Material Handling", "Automated overhead gantry cranes, heavy-capacity forklift logistics, raw material staging, JIT component delivery to assembly bays.", "Inventory staging synchronization, FIFO flow, crane load rigging safety, material routing efficiency."],
                    ["Plant Information Technology", "Industrial networking, server room infrastructure, shop-floor terminal connectivity, ERP system coordination, communication security.", "Isolated operational technology (OT) networks, supervisory data monitoring, IT-OT convergence challenges."]
                ]
            },
            "subsections": [
                {
                    "num": "2.2.1",
                    "title": "Welding and Fabrication Division",
                    "paragraphs": [
                        (
                            "The Welding and Fabrication division represents the foundational stage of heavy machinery production. High-tensile "
                            "structural steel plates are precision-cut using high-definition CNC plasma and laser cutting machines. The cut "
                            "plates are transported to robotic welding cells equipped with articulated industrial manipulators and multi-pass "
                            "submerged arc welding heads. In these cells, structural frames, excavator booms, and dump truck chassis are welded."
                        ),
                        (
                            "My observations centered on how operating parameters—such as welding current, wire feed velocity, thermal input, "
                            "and mechanical clamping vibration—directly dictate weld bead quality and structural integrity. Excessive thermal "
                            "buildup can induce material distortion, while improper wire feed velocity causes porosity. The division employs "
                            "strict ultrasonic and magnetic particle non-destructive testing to verify structural soundness before frames "
                            "proceed to subsequent machining."
                        )
                    ]
                },
                {
                    "num": "2.2.2",
                    "title": "Assembly and Integration Division",
                    "paragraphs": [
                        (
                            "The Assembly division operates on progressive assembly lines where fabricated chassis are systematically outfitted "
                            "with mechanical, hydraulic, pneumatic, and electronic subsystems. Workers and automated equipment operate within "
                            "defined cycle times (takt times), kitting components systematically at each workstation."
                        ),
                        (
                            "Key operations observed included the installation of high-pressure hydraulic cylinders, routing of reinforced hydraulic "
                            "hoses, drop-in mounting of massive diesel power units, and installation of ROPS/FOPS certified operator cabins. "
                            "The critical importance of digital torque wrenches with integrated Bluetooth recording, visual assembly guidance "
                            "monitors, and physical Poka-Yoke fixtures was clearly demonstrated as essential mechanisms to prevent assembly errors."
                        )
                    ]
                },
                {
                    "num": "2.2.3",
                    "title": "Testing and Inspection Division",
                    "paragraphs": [
                        (
                            "The Testing and Inspection division serves as the final quality gate. In enclosed metrology rooms, precision components "
                            "such as hydraulic spool valves, bearing housings, and powertrain gears are measured on high-precision Coordinate "
                            "Measuring Machines (CMM) and optical vision comparators to micrometer tolerances."
                        ),
                        (
                            "On the outdoor dynamic testing area, completed mining trucks and excavators undergo comprehensive functional trials. "
                            "These trials include full-pressure hydraulic relief valve checks, emergency braking distance measurements, steering "
                            "angle calibration, and multi-hour continuous engine running to detect abnormal thermal escalation or excessive structural "
                            "vibration prior to customer delivery certification."
                        )
                    ]
                },
                {
                    "num": "2.2.4",
                    "title": "Industrial Safety, Material Handling, and IT Infrastructure",
                    "paragraphs": [
                        (
                            "Industrial safety at Komatsu is treated as a non-negotiable prerequisite to production. The Environmental Health and "
                            "Safety (EHS) department enforces stringent Personal Protective Equipment (PPE) compliance, pedestrian walkway zoning, "
                            "and mechanical safety interlocks on all automated machinery. The 5S methodology (Sort, Set in order, Shine, Standardize, "
                            "Sustain) is visibly integrated across every square meter of the shop floor."
                        ),
                        (
                            "Material handling logistics relies on synchronized overhead traveling cranes, heavy forklift fleets, and dedicated "
                            "tugger trains supplying parts on a Just-In-Time (JIT) basis. Meanwhile, the Plant IT Department maintains the vital "
                            "communications backbone connecting plant workstations, terminal scanners, and industrial servers, illustrating the "
                            "critical role of robust networking and software infrastructure in maintaining unbroken manufacturing momentum."
                        )
                    ]
                }
            ]
        },
        {
            "num": "2.3",
            "title": "Engineering Responsibilities and Academic Learning",
            "paragraphs": [
                (
                    "Although my role was strictly observational, I maintained disciplined academic responsibilities throughout the internship. "
                    "I maintained daily engineering logbooks documenting plant layout topologies, material flow sequences, inter-departmental "
                    "handshake protocols, and equipment status signaling methods."
                ),
                (
                    "The primary academic takeaways from my internship include: (1) understanding the paramount importance of real-time machine "
                    "operating status awareness; (2) recognizing how undetected thermal and vibration anomalies rapidly propagate into catastrophic "
                    "equipment failure and unplanned downtime; (3) learning that effective plant supervision requires centralized visual telemetry "
                    "rather than fragmented manual clipboards; and (4) appreciating the principles of Komatsu's visual management (\"Mieruka\"). "
                    "These insights provided the comprehensive conceptual foundation for the independent academic monitoring prototype "
                    "developed as the technical project component of this internship."
                )
            ]
        }
    ]
}

CHAPTER_3 = {
    "title": "PROJECT OVERVIEW",
    "sections": [
        {
            "num": "3.1",
            "title": "Project Introduction",
            "paragraphs": [
                (
                    "The technical project component of this internship is an independently developed academic research prototype titled "
                    "\"Smart Factory Monitoring System Inspired by KOM-MICS\". It is a full-stack web-based industrial supervisory console "
                    "designed to demonstrate how manufacturing asset telemetry, operating status transitions, shift production metrics, and "
                    "equipment maintenance history can be ingested, managed, and visually communicated through an authentic SCADA/HMI dashboard."
                ),
                (
                    "The prototype was conceived, architected, coded, and verified independently by the author following the observational "
                    "period at Komatsu India. It serves as an academic bridge connecting core computer science principles—such as database design, "
                    "asynchronous client-server communication, RESTful API architecture, and real-time data visualization—with practical "
                    "manufacturing operations challenges observed in heavy engineering facilities."
                )
            ]
        },
        {
            "num": "3.2",
            "title": "Background and Inspiration from KOM-MICS",
            "paragraphs": [
                (
                    "In high-capital heavy equipment manufacturing, machine downtime is exceptionally costly. When a critical machine such as a "
                    "robotic welding gantry or CNC laser cutter fails unexpectedly, the entire downstream assembly sequence halts. To prevent "
                    "such bottlenecks, leading manufacturing enterprises deploy advanced Supervisory Control and Data Acquisition (SCADA) and "
                    "Industrial IoT (IIoT) platforms."
                ),
                (
                    "In particular, Komatsu has publicly shared its \"KOM-MICS\" (Komatsu Manufacturing Innovation & Construction System) concept. "
                    "KOM-MICS connects machine tools, welding robots, and assembly equipment across Komatsu’s domestic and global plants. By "
                    "gathering operating rate telemetry, cutting loads, and cycle times directly into a centralized platform, KOM-MICS enables "
                    "plant managers to perform \"Mieruka\"—making invisible manufacturing inefficiencies and equipment stresses instantly visible "
                    "and actionable. Inspired by this public industrial paradigm, I designed this prototype to simulate and visualize an "
                    "integrated three-department manufacturing cell."
                )
            ]
        },
        {
            "num": "3.3",
            "title": "Project Objectives",
            "paragraphs": [
                (
                    "The primary objectives of developing the Smart Factory Monitoring System prototype are as follows:"
                )
            ],
            "bullets": [
                ("Centralized Telemetry Aggregation: ", "To engineer a unified relational database schema and background simulation engine capable of capturing and storing continuous time-series sensor data (velocity, thermal load, mechanical vibration) from multiple manufacturing assets."),
                ("Real-Time Visual Management (Mieruka): ", "To design a high-density, professional industrial Human-Machine Interface (HMI) that displays live equipment operational states (Running, Idle, Warning), shift production output, and plant availability at a glance."),
                ("Automated Threshold Exception Monitoring: ", "To establish automatic threshold violation detection for temperature (>75.0 °C) and vibration (>2.5 mm/s), immediately generating timestamped warning alarms in an event audit buffer."),
                ("Interactive Operational Lifecycle Workflows: ", "To implement interactive operator actions for alarm acknowledgement (ACK) and resolution (RESOLVE), as well as equipment maintenance and downtime recording directly linked to SQLite storage."),
                ("Scalable, Lightweight Architecture: ", "To build the entire solution using beginner-friendly, accessible, and production-viable technologies (Python 3.12, Flask, SQLite with WAL mode, Chart.js) without heavyweight or costly third-party enterprise licensing dependencies.")
            ]
        },
        {
            "num": "3.4",
            "title": "Scope and Boundaries of the Prototype",
            "paragraphs": [
                (
                    "To maintain complete academic transparency and professional integrity, the scope and technical boundaries of this "
                    "prototype are explicitly established as follows:"
                )
            ],
            "bullets": [
                ("Independent Academic Work: ", "The software application is entirely an academic prototype created independently by the author. It is NOT an official Komatsu software product, was NOT commissioned by Komatsu India, and is NOT deployed on Komatsu's internal networks or physical machinery."),
                ("Simulated Industrial Telemetry: ", "All sensor telemetry (RPM, temperatures, vibrations) and shift production numbers are mathematically generated by a background stochastic Python simulator (simulator.py). The system does not interface with physical PLCs, live sensors, or operational hardware."),
                ("Standard Factory Scope: ", "The monitoring model encompasses a representative 6-asset manufacturing cell divided across three core departments: Welding & Fabrication, Assembly, and Quality Inspection."),
                ("Absence of Proprietary Data: ", "The prototype contains zero proprietary Komatsu technical blueprints, confidential cycle times, or corporate commercial data. All machine specifications and naming conventions represent generalized industrial equipment categories.")
            ]
        },
        {
            "num": "3.5",
            "title": "Existing Factory Tracking vs. Proposed System",
            "paragraphs": [
                (
                    "Traditional factory environments frequently rely on manual clipboard logging, shift-end spreadsheet entries, and localized "
                    "Andon tower lamps. Table 3.2 contrasts these legacy methodologies with the centralized web-based monitoring architecture "
                    "implemented in this project."
                )
            ],
            "table": {
                "number": "3.2",
                "title": "Comparison Between Traditional Factory Tracking and Proposed Web-Based HMI",
                "headers": ["Evaluation Dimension", "Traditional Factory Methodologies", "Proposed Smart Factory Prototype"],
                "rows": [
                    ["Data Capture Latency", "Delayed; shift-end manual logs or paper clipboards; retrospective discovery of machine failures.", "Real-time; continuous 3-second simulation cycles with 5-second client-side asynchronous polling updates."],
                    ["Telemetry Visibility", "Fragmented; operators must physically walk the shop floor to inspect individual machine consoles.", "Centralized; unified SCADA/HMI console displays all cell machinery simultaneously on one workstation."],
                    ["Threshold Anomaly Alerts", "Auditory horn or physical tower lamp visible only to nearby operators; easily missed in loud shops.", "Automated software alarm generator logs timestamped exceptions, updates badge counters, and tracks lifecycle."],
                    ["Availability Calculation", "Calculated hours or days after shift completion using approximate subjective estimates.", "Dynamically evaluated in real time via mathematically documented formula: (Running Units / Total Units) × 100."],
                    ["Maintenance Logging", "Physical whiteboard or paper maintenance job card; prone to loss and inaccurate downtime records.", "Interactive modal dialog logs maintenance type, technician identity, and downtime minutes directly into SQLite."],
                    ["Production & Scrap Tracking", "Manual count tallies verified only during shift handover; scrap identified retrospectively.", "Real-time shift output versus target comparison with dynamic scrap rate percentage and progress bar visualization."]
                ]
            }
        },
        {
            "num": "3.6",
            "title": "Summary of Core System Features",
            "paragraphs": [
                (
                    "The implemented system delivers a comprehensive suite of practical operational monitoring capabilities organized into "
                    "four dedicated workstation views:"
                )
            ],
            "bullets": [
                ("Plant Overview Console: ", "Displays four contiguous KPI readouts (Monitored Assets, Operating Units, Plant Availability %, and Telemetry Archive Samples), an interactive 6-asset Operating Status Timeline, a Department Operational Status Table, a Department Production Summary table with visual progress bars, a dual-axis Thermal/Vibration line chart, and a Spindle Velocity bar chart."),
                ("Equipment Telemetry Matrix: ", "Presents a high-density equipment table featuring machine tags (#001–#006), model specifications, active operating states, live sensor values, and last synchronization age. Includes real-time text query search and department/state filter chips."),
                ("Slide-Out Machine Inspector Drawer: ", "Clicking any equipment row smoothly slides out a dedicated technical inspection drawer revealing equipment specifications, live velocity/thermal/vibration gauges, historical telemetry samples, and machine-specific maintenance logs with a direct logging action button."),
                ("Alarms and Event Management: ", "A dedicated alarm console displaying active, acknowledged, and resolved fault events with severity tagging. Allows operators to acknowledge (ACK) and resolve (RESOLVE) alarms in real time, updating active badge counters without page reloads."),
                ("Equipment Maintenance & Downtime Tracker: ", "A dedicated maintenance audit console providing total recorded plant downtime analytics, category filter chips (Preventive, Corrective, Tool Change, Inspection, Calibration), and an industrial modal dialog for logging new maintenance events into SQLite.")
            ]
        }
    ]
}
