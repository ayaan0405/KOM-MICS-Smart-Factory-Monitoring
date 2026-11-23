# -*- coding: utf-8 -*-
"""
PDF Document Compiler: Smart Factory Monitoring System Internship Report
Generates SMART_FACTORY_MONITORING_SYSTEM_INTERNSHIP_REPORT.pdf adhering strictly to Crescent & Komatsu guidelines.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, Preformatted
)
from reportlab.pdfgen import canvas

from report_text_part1 import METADATA, PRELIMINARIES, CHAPTER_1, CHAPTER_2, CHAPTER_3
from report_text_part2 import CHAPTER_4, CHAPTER_5
from report_text_part3 import CHAPTER_6, CHAPTER_7, CHAPTER_8, CHAPTER_9

OUTPUT_PDF = "SMART_FACTORY_MONITORING_SYSTEM_INTERNSHIP_REPORT.pdf"

# Komatsu Colors
COLOR_NAVY = colors.HexColor("#002D62")
COLOR_YELLOW = colors.HexColor("#F5B800")
COLOR_TEXT = colors.HexColor("#0F172A")
COLOR_MUTED = colors.HexColor("#64748B")
COLOR_BORDER = colors.HexColor("#CBD5E1")
COLOR_LIGHT_BG = colors.HexColor("#F8FAFC")

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to calculate page counts and draw professional running footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Page 1 is Cover (no header/footer)
        if self._pageNumber == 1:
            return
        
        # Preliminaries: Pages 1 to 11 (Cover, Bonafide, Cert, Viva, Ack, TOC 1-2, Abbr, Figs, Tables, Abstract)
        # As per faculty note: "Don't put numbers for upto abstract. Page no starts from chapter 1"
        # We start Arabic numbering at Chapter 1!
        # Chapter 1 starts at page 12 in PDF
        chap1_page = 12
        if self._pageNumber >= chap1_page:
            arabic_num = self._pageNumber - chap1_page + 1
            self.saveState()
            self.setFont("Helvetica", 9)
            self.setFillColor(COLOR_TEXT)
            self.drawCentredString(letter[0] / 2.0, 0.65 * inch, str(arabic_num))
            
            # Subtle running header rule
            self.setStrokeColor(COLOR_BORDER)
            self.setLineWidth(0.5)
            self.line(1.25 * inch, letter[1] - 0.75 * inch, letter[0] - 1.0 * inch, letter[1] - 0.75 * inch)
            
            self.setFont("Helvetica", 8)
            self.setFillColor(COLOR_MUTED)
            self.drawString(1.25 * inch, letter[1] - 0.70 * inch, "SMART FACTORY MONITORING SYSTEM INSPIRED BY KOM-MICS")
            self.drawRightString(letter[0] - 1.0 * inch, letter[1] - 0.70 * inch, "B.TECH CSE INTERNSHIP")
            self.restoreState()

print("Building PDF Report...")

doc = SimpleDocTemplate(
    OUTPUT_PDF,
    pagesize=letter,
    leftMargin=1.25 * inch,
    rightMargin=1.0 * inch,
    topMargin=1.0 * inch,
    bottomMargin=1.0 * inch
)

styles = getSampleStyleSheet()

# Custom Typographic Styles
style_title = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=17,
    leading=22,
    alignment=1, # Center
    textColor=COLOR_NAVY,
    spaceAfter=12
)

style_subtitle = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=16,
    alignment=1,
    textColor=COLOR_TEXT,
    spaceAfter=24
)

style_h1 = ParagraphStyle(
    'ChapterH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=15,
    leading=20,
    alignment=1, # Center
    textColor=COLOR_NAVY,
    spaceBefore=14,
    spaceAfter=12,
    keepWithNext=True
)

style_h2 = ParagraphStyle(
    'SectionH2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12.5,
    leading=17,
    alignment=1, # Center (as per guidelines)
    textColor=COLOR_NAVY,
    spaceBefore=12,
    spaceAfter=6,
    keepWithNext=True
)

style_h3 = ParagraphStyle(
    'SubSectionH3',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=15,
    alignment=0, # Left
    textColor=COLOR_NAVY,
    spaceBefore=10,
    spaceAfter=4,
    keepWithNext=True
)

style_body = ParagraphStyle(
    'BodyTextCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    leading=14.5,
    alignment=4, # Justified
    textColor=COLOR_TEXT,
    spaceAfter=6
)

style_bullet = ParagraphStyle(
    'BulletCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    leading=14.5,
    alignment=4,
    textColor=COLOR_TEXT,
    leftIndent=18,
    spaceAfter=4
)

style_caption = ParagraphStyle(
    'CaptionCustom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=13,
    alignment=1, # Center
    textColor=COLOR_NAVY,
    spaceBefore=4,
    spaceAfter=10,
    keepWithNext=True
)

story = []

# ===========================================================================
# 1. COVER PAGE
# ===========================================================================
story.append(Spacer(1, 0.4 * inch))
story.append(Paragraph("SMART FACTORY MONITORING SYSTEM<br/>INSPIRED BY KOM-MICS", style_title))
story.append(Spacer(1, 0.1 * inch))
story.append(Paragraph("AN INTERNSHIP REPORT", style_subtitle))
story.append(Spacer(1, 0.2 * inch))

p_by = Paragraph("<font size=11><i>Submitted by</i></font><br/><br/><b><font size=13>" + METADATA["student_name"] + "</font></b><br/><b>(RRN: " + METADATA["register_no"] + ")</b>", ParagraphStyle('CoverBy', alignment=1, leading=18))
story.append(p_by)
story.append(Spacer(1, 0.3 * inch))

p_deg = Paragraph("<font size=10.5><i>in partial fulfillment for the award of the degree of</i></font><br/><br/><b><font size=12>" + METADATA["degree"] + "<br/>in<br/>" + METADATA["branch"] + "</font></b>", ParagraphStyle('CoverDeg', alignment=1, leading=16))
story.append(p_deg)
story.append(Spacer(1, 0.25 * inch))

logo_path = 'report_assets/extracted_p0_0_Image13.jpg'
if os.path.exists(logo_path):
    story.append(RLImage(logo_path, width=3.0 * inch, height=0.81 * inch))

story.append(Spacer(1, 0.25 * inch))
p_inst = Paragraph("<b>" + METADATA["submission_date"] + "</b>", ParagraphStyle('CoverDate', alignment=1, fontName='Helvetica-Bold', fontSize=11))
story.append(p_inst)
story.append(PageBreak())

# ===========================================================================
# 2. BONAFIDE CERTIFICATE (Page i)
# ===========================================================================
if os.path.exists(logo_path):
    story.append(RLImage(logo_path, width=2.4 * inch, height=0.65 * inch))
    story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("BONAFIDE CERTIFICATE", style_h1))
story.append(Spacer(1, 0.15 * inch))
story.append(Paragraph(PRELIMINARIES["bonafide"]["body"], style_body))
story.append(Spacer(1, 0.5 * inch))

# Signatures Table
sig_data = [
    [
        Paragraph("<b>SIGNATURE</b><br/><b>[FACULTY COORDINATOR / ADVISOR]</b><br/>Assistant Professor / Coordinator<br/>Department of CSE<br/>B.S. Abdur Rahman Crescent<br/>Institute of Science and Technology<br/>Vandalur, Chennai – 600 048.", ParagraphStyle('SigL', fontName='Helvetica', fontSize=10, leading=14)),
        Paragraph("<b>SIGNATURE</b><br/><b>[HEAD OF THE DEPARTMENT]</b><br/>Professor and Head<br/>Department of CSE<br/>B.S. Abdur Rahman Crescent<br/>Institute of Science and Technology<br/>Vandalur, Chennai – 600 048.", ParagraphStyle('SigR', fontName='Helvetica', fontSize=10, leading=14))
    ]
]
t_sig = Table(sig_data, colWidths=[3.1 * inch, 3.1 * inch])
t_sig.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
]))
story.append(t_sig)
story.append(PageBreak())

# ===========================================================================
# 3. INTERNSHIP CERTIFICATE (Page ii) - ORIGINAL SCAN EMBEDDED
# ===========================================================================
story.append(Paragraph("INTERNSHIP CERTIFICATE", style_h1))
cert_scan_path = r'C:/Users/Ayaan/.gemini/antigravity/brain/1c37d6d5-00e3-4cf6-86a2-a2af67a7d12c/.user_uploaded/media_1795463364605_b089eca9.jpg'
if os.path.exists(cert_scan_path):
    # 5.5 in wide, height 7.5 in
    story.append(RLImage(cert_scan_path, width=5.5 * inch, height=7.5 * inch))
story.append(PageBreak())

# ===========================================================================
# 4. VIVA VOCE EXAMINATION (Page iii)
# ===========================================================================
if os.path.exists(logo_path):
    story.append(RLImage(logo_path, width=2.4 * inch, height=0.65 * inch))
    story.append(Spacer(1, 0.1 * inch))

story.append(Paragraph("VIVA VOCE EXAMINATION", style_h1))
story.append(Spacer(1, 0.25 * inch))
story.append(Paragraph(PRELIMINARIES["viva_voce"]["body"], style_body))
story.append(Spacer(1, 1.2 * inch))

viva_data = [
    [
        Paragraph("<b>_____________________</b><br/><b>INTERNAL EXAMINER</b>", ParagraphStyle('V1', fontName='Helvetica', fontSize=10, leading=14)),
        Paragraph("<b>_____________________</b><br/><b>EXTERNAL EXAMINER</b>", ParagraphStyle('V2', alignment=2, fontName='Helvetica', fontSize=10, leading=14))
    ]
]
t_viva = Table(viva_data, colWidths=[3.1 * inch, 3.1 * inch])
t_viva.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
story.append(t_viva)
story.append(PageBreak())

# ===========================================================================
# 5. ACKNOWLEDGEMENT (Page iv)
# ===========================================================================
story.append(Paragraph("ACKNOWLEDGEMENT", style_h1))
story.append(Spacer(1, 0.1 * inch))
for p_txt in PRELIMINARIES["acknowledgement"]:
    story.append(Paragraph(p_txt, style_body))

story.append(Spacer(1, 0.2 * inch))
story.append(Paragraph("<b>" + METADATA["student_name"] + "</b>", ParagraphStyle('AckName', alignment=2, fontName='Helvetica-Bold', fontSize=11)))
story.append(PageBreak())

# ===========================================================================
# 6. TABLE OF CONTENTS (Pages v - vi)
# ===========================================================================
story.append(Paragraph("TABLE OF CONTENTS", style_h1))
story.append(Spacer(1, 0.1 * inch))

toc_rows = [
    [Paragraph("<b>CHAPTER / SECTION TITLE</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=10, textColor=COLOR_NAVY)),
     Paragraph("<b>PAGE NO.</b>", ParagraphStyle('TH2', alignment=2, fontName='Helvetica-Bold', fontSize=10, textColor=COLOR_NAVY))]
]

toc_items = [
    ("LIST OF ABBREVIATIONS", ""),
    ("LIST OF FIGURES", ""),
    ("LIST OF TABLES", ""),
    ("ABSTRACT", ""),
    ("1. COMPANY OVERVIEW", "1"),
    ("    1.1 Company Overview", "1"),
    ("    1.2 Company Website and Digital Infrastructure", "2"),
    ("    1.3 Chennai Manufacturing Plant (Oragadam Facility)", "2"),
    ("    1.4 Manufacturing Operations and Business Context", "2"),
    ("2. ROLE AND RESPONSIBILITIES", "4"),
    ("    2.1 Internship Role", "4"),
    ("    2.2 Manufacturing Departments Observed", "4"),
    ("        2.2.1 Welding and Fabrication Division", "5"),
    ("        2.2.2 Assembly and Integration Division", "6"),
    ("        2.2.3 Testing and Inspection Division", "6"),
    ("        2.2.4 Industrial Safety, Material Handling, and IT", "6"),
    ("    2.3 Engineering Responsibilities and Academic Learning", "7"),
    ("3. PROJECT OVERVIEW", "8"),
    ("    3.1 Project Introduction", "8"),
    ("    3.2 Background and Inspiration from KOM-MICS", "8"),
    ("    3.3 Project Objectives", "8"),
    ("    3.4 Scope and Boundaries of the Prototype", "9"),
    ("    3.5 Existing Factory Tracking vs. Proposed System", "9"),
    ("    3.6 Summary of Core System Features", "10"),
    ("4. THEORETICAL ANALYSIS", "12"),
    ("    4.1 Introduction to Smart Manufacturing and Industry 4.0", "12"),
    ("    4.2 Industrial IoT and Machine Health Monitoring", "12"),
    ("    4.3 Core Telemetry Variables in Industrial Equipment", "12"),
    ("    4.4 Web Application Framework: Python 3.12 and Flask", "13"),
    ("    4.5 Relational Database Management: SQLite & WAL Mode", "13"),
    ("    4.6 RESTful API Design & Asynchronous Client Polling", "14"),
    ("    4.7 Dynamic Engineering Data Visualization: Chart.js", "15"),
    ("    4.8 Human-Machine Interface (HMI) & UI/UX Principles", "15"),
    ("    4.9 Chapter Summary", "15"),
    ("5. DESIGN AND IMPLEMENTATION", "16"),
    ("    5.1 System Architecture & Multi-Tier Topology", "16"),
    ("    5.2 Relational Database Schema Design (factory.db)", "17"),
    ("    5.3 Python Flask Backend & RESTful API Implementation", "18"),
    ("    5.4 Stochastic Asset Telemetry Simulator Engine", "20"),
    ("    5.5 Plant Availability Calculation Logic & Formula", "21"),
    ("    5.6 Machine Matrix & Slide-Out Inspector Drawer", "21"),
    ("    5.7 Alarm Lifecycle Management & Finite State Machine", "22"),
    ("    5.8 Equipment Maintenance & Downtime Tracking Module", "23"),
    ("    5.9 Simulated Shift Production & Scrap Rate Tracking", "23"),
    ("    5.10 Testing, Verification & Regression Test Suites", "24"),
    ("    5.11 Technical and Engineering Skills Acquired", "24"),
    ("6. RESULT AND ANALYSIS", "25"),
    ("    6.1 Comprehensive Operational Results Summary", "25"),
    ("    6.2 Machine Availability & Fleet Operational Analysis", "26"),
    ("    6.3 Asset Telemetry & Sensor Consistency Analysis", "26"),
    ("    6.4 Machine Operating State Distribution (Andon Timeline)", "27"),
    ("    6.5 Departmental Production Output & Scrap Rate Analysis", "27"),
    ("    6.6 Maintenance History & Equipment Downtime Evaluation", "28"),
    ("    6.7 Alarm Response & Exception Handling Analysis", "29"),
    ("    6.8 Detailed Dashboard Walkthrough & Visual Analysis", "30"),
    ("        6.8.1 Plant Overview Console (Fig 6.1)", "30"),
    ("        6.8.2 Oscilloscope Charts & Spindle Profile (Fig 6.2)", "30"),
    ("        6.8.3 Equipment Telemetry Matrix (Fig 6.3)", "31"),
    ("        6.8.4 Equipment Side Inspector Drawer (Fig 6.4)", "32"),
    ("        6.8.5 Alarms & Fault Event Management Console (Fig 6.5)", "33"),
    ("        6.8.6 Chronological Telemetry Stream Audit Log (Fig 6.6)", "34"),
    ("        6.8.7 Equipment Maintenance & Downtime Tracker (Fig 6.7)", "35"),
    ("        6.8.8 Record Maintenance Modal Dialog (Fig 6.8)", "36"),
    ("    6.9 Technical Limitations and Academic Observations", "37"),
    ("7. CONCLUSION AND FUTURE SCOPE", "39"),
    ("    7.1 Conclusion", "39"),
    ("    7.2 Synthesis of Observation and Software Engineering", "39"),
    ("    7.3 Future Technical Scope and Scalability", "39"),
    ("8. REFERENCES", "41"),
    ("9. APPENDIX", "42"),
    ("    9.1 Core Application Source Code", "42"),
    ("    9.2 Technical Bibliography & Standards Reference", "44")
]

for t, p in toc_items:
    is_bold = t.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', 'LIST', 'ABSTRACT'))
    f_weight = "<b>" if is_bold else ""
    f_end = "</b>" if is_bold else ""
    toc_rows.append([
        Paragraph(f"{f_weight}{t}{f_end}", ParagraphStyle('TOCItem', fontName='Helvetica', fontSize=9.5, leading=12)),
        Paragraph(f"<b>{p}</b>", ParagraphStyle('TOCPg', alignment=2, fontName='Helvetica-Bold', fontSize=9.5, leading=12))
    ])

t_toc = Table(toc_rows, colWidths=[5.1 * inch, 1.1 * inch])
t_toc.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ('TOPPADDING', (0,0), (-1,-1), 1.5),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
]))
story.append(t_toc)
story.append(PageBreak())

# ===========================================================================
# 7. LIST OF ABBREVIATIONS
# ===========================================================================
story.append(Paragraph("LIST OF ABBREVIATIONS", style_h1))
story.append(Spacer(1, 0.1 * inch))

abbr_rows = [
    [Paragraph("<b>ABBREVIATION</b>", ParagraphStyle('AbH1', fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.white)),
     Paragraph("<b>EXPANDED TECHNICAL DESIGNATION</b>", ParagraphStyle('AbH2', fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.white))]
]

for ab, full in PRELIMINARIES["abbreviations"]:
    abbr_rows.append([
        Paragraph(f"<b>{ab}</b>", ParagraphStyle('AbC1', fontName='Helvetica-Bold', fontSize=9, leading=11)),
        Paragraph(full, ParagraphStyle('AbC2', fontName='Helvetica', fontSize=9, leading=11))
    ])

t_abbr = Table(abbr_rows, colWidths=[1.8 * inch, 4.4 * inch])
t_abbr.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), COLOR_NAVY),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LINEBELOW', (0,0), (-1,-1), 0.5, COLOR_BORDER),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG])
]))
story.append(t_abbr)
story.append(PageBreak())

# ===========================================================================
# 8. LIST OF FIGURES & LIST OF TABLES
# ===========================================================================
story.append(Paragraph("LIST OF FIGURES", style_h1))
story.append(Spacer(1, 0.08 * inch))

fig_rows = [
    [Paragraph("<b>FIGURE NO.</b>", ParagraphStyle('FH1', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY)),
     Paragraph("<b>TITLE</b>", ParagraphStyle('FH2', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY)),
     Paragraph("<b>PAGE NO.</b>", ParagraphStyle('FH3', alignment=2, fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY))]
]

figures_list = [
    ("1.1", "Komatsu Corporate Logo & Industrial Brand Identity", "1"),
    ("4.1", "Four-Tier System Architecture of the Smart Factory Monitoring System", "14"),
    ("5.1", "Relational Database Schema & Entity-Relationship Diagram (factory.db)", "22"),
    ("5.2", "Finite State Machine: Equipment Operating State & Alarm Exception Lifecycle", "27"),
    ("6.1", "Plant Overview Console: Real-Time Operational SCADA Interface", "39"),
    ("6.2", "Dual-Axis Oscilloscope Telemetry Line Chart & Spindle Velocity Bar Chart", "40"),
    ("6.3", "Equipment Telemetry Matrix with Real-Time Query Filtering", "41"),
    ("6.4", "Equipment Side Inspector Drawer: Real-Time Readings, Log & Maintenance", "42"),
    ("6.5", "Alarms & Fault Event Management Console: Severity Filtering & Actions", "43"),
    ("6.6", "Chronological Telemetry Stream Audit Log", "44"),
    ("6.7", "Equipment Maintenance & Downtime Tracker Console", "45"),
    ("6.8", "Record Equipment Maintenance & Downtime Modal Dialog Interface", "46")
]

for fn, ft, fp in figures_list:
    fig_rows.append([
        Paragraph(f"<b>Fig {fn}</b>", ParagraphStyle('FC1', fontName='Helvetica-Bold', fontSize=9)),
        Paragraph(ft, ParagraphStyle('FC2', fontName='Helvetica', fontSize=9)),
        Paragraph(f"<b>{fp}</b>", ParagraphStyle('FC3', alignment=2, fontName='Helvetica-Bold', fontSize=9))
    ])

t_fig = Table(fig_rows, colWidths=[1.1 * inch, 4.1 * inch, 1.0 * inch])
t_fig.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
]))
story.append(t_fig)

story.append(Spacer(1, 0.2 * inch))
story.append(Paragraph("LIST OF TABLES", style_h1))
story.append(Spacer(1, 0.08 * inch))

tbl_rows = [
    [Paragraph("<b>TABLE NO.</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY)),
     Paragraph("<b>TITLE</b>", ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY)),
     Paragraph("<b>PAGE NO.</b>", ParagraphStyle('TH3', alignment=2, fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY))]
]

tables_list = [
    ("2.1", "Overview of Manufacturing & Operational Divisions Observed at Komatsu India", "5"),
    ("3.1", "Monitored Industrial Equipment Specifications in the Academic Cell Prototype", "10"),
    ("3.2", "Comparison Between Traditional Factory Tracking and Proposed Web-Based HMI", "11"),
    ("4.1", "Industrial Telemetry Variables, Sampling Dynamics, and Engineering Units", "15"),
    ("4.2", "Comparison of Relational Database Modes (Rollback Journal vs. Write-Ahead Logging)", "16"),
    ("5.1", "Normalized Database Schema Structure of factory.db", "22"),
    ("5.2", "RESTful Application Programming Interface (API) Route Specification", "23"),
    ("5.3", "Stochastic Parameter Profiles for Simulated Asset Telemetry Generation", "24"),
    ("6.1", "Headline Plant Performance Metrics (Baseline 6-Asset Monitoring Cell)", "32"),
    ("6.2", "Department-Level Operational Metrics & Thermal/Vibration Load Breakdown", "34"),
    ("6.3", "Simulated Shift Production Output, Scrap Counts, and Yield Performance", "36"),
    ("6.4", "Summary of Equipment Maintenance Records and Recorded Downtime Impact", "37"),
    ("6.5", "Active Alarm Records and Threshold Violation Event Audit Log", "38")
]

for tn, tt, tp in tables_list:
    tbl_rows.append([
        Paragraph(f"<b>Table {tn}</b>", ParagraphStyle('TC1', fontName='Helvetica-Bold', fontSize=9)),
        Paragraph(tt, ParagraphStyle('TC2', fontName='Helvetica', fontSize=9)),
        Paragraph(f"<b>{tp}</b>", ParagraphStyle('TC3', alignment=2, fontName='Helvetica-Bold', fontSize=9))
    ])

t_tbl_list = Table(tbl_rows, colWidths=[1.1 * inch, 4.1 * inch, 1.0 * inch])
t_tbl_list.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
]))
story.append(t_tbl_list)
story.append(PageBreak())

# ===========================================================================
# 9. ABSTRACT
# ===========================================================================
story.append(Paragraph("ABSTRACT", style_h1))
story.append(Spacer(1, 0.1 * inch))
for p_txt in PRELIMINARIES["abstract"]:
    story.append(Paragraph(p_txt, style_body))

story.append(PageBreak())

# ===========================================================================
# HELPER FUNCTIONS FOR CHAPTER CONTENT
# ===========================================================================
def add_pdf_table(table_def):
    headers = table_def['headers']
    rows = table_def['rows']
    
    t_data = []
    h_row = [Paragraph(f"<b>{h}</b>", ParagraphStyle('THd', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white)) for h in headers]
    t_data.append(h_row)
    
    for r in rows:
        r_row = [Paragraph(str(c), ParagraphStyle('TRow', fontName='Helvetica', fontSize=8.5, leading=11)) for c in r]
        t_data.append(r_row)
        
    num_cols = len(headers)
    avail_w = 6.2 * inch
    col_w = avail_w / num_cols
    col_widths = [col_w] * num_cols
    
    # Custom widths for specific tables
    if num_cols == 3:
        col_widths = [1.8 * inch, 2.2 * inch, 2.2 * inch]
    elif num_cols == 5:
        col_widths = [1.3 * inch, 1.0 * inch, 1.4 * inch, 1.3 * inch, 1.2 * inch]
    elif num_cols == 7:
        col_widths = [0.8 * inch, 1.2 * inch, 1.0 * inch, 0.8 * inch, 0.7 * inch, 0.8 * inch, 0.9 * inch]
        
    t = Table(t_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_NAVY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG])
    ]))
    
    t_elem = [
        Paragraph(f"<b>Table {table_def['number']} – {table_def['title']}</b>", style_caption),
        t,
        Spacer(1, 0.12 * inch)
    ]
    return t_elem

def add_pdf_figure(img_path, caption_text, width_inches=5.8):
    if os.path.exists(img_path):
        # Scale height proportionally
        from PIL import Image
        im = Image.open(img_path)
        w, h = im.size
        aspect = h / float(w)
        h_inches = width_inches * aspect
        
        # Guard max height to prevent page overflows
        if h_inches > 4.5:
            h_inches = 4.5
            width_inches = h_inches / aspect
            
        fig_elem = [
            Spacer(1, 0.08 * inch),
            RLImage(img_path, width=width_inches * inch, height=h_inches * inch),
            Paragraph(caption_text, style_caption),
            Spacer(1, 0.08 * inch)
        ]
        return fig_elem
    return []

# ===========================================================================
# CHAPTER 1: COMPANY OVERVIEW
# ===========================================================================
story.append(Paragraph("CHAPTER 1<br/>COMPANY OVERVIEW", style_h1))
story.extend(add_pdf_figure('report_assets/komatsu_logo.png', "Fig 1.1 – Komatsu Corporate Logo & Industrial Brand Identity", 4.0))

for sec in CHAPTER_1["sections"]:
    story.append(Paragraph(f"{sec['num']} {sec['title']}", style_h2))
    for p_txt in sec["paragraphs"]:
        story.append(Paragraph(p_txt, style_body))

story.append(PageBreak())

# ===========================================================================
# CHAPTER 2: ROLE AND RESPONSIBILITIES
# ===========================================================================
story.append(Paragraph("CHAPTER 2<br/>ROLE AND RESPONSIBILITIES", style_h1))

for sec in CHAPTER_2["sections"]:
    story.append(Paragraph(f"{sec['num']} {sec['title']}", style_h2))
    for p_txt in sec["paragraphs"]:
        story.append(Paragraph(p_txt, style_body))
    
    if "table" in sec:
        story.extend(add_pdf_table(sec["table"]))
        
    if "subsections" in sec:
        for sub in sec["subsections"]:
            story.append(Paragraph(f"{sub['num']} {sub['title']}", style_h3))
            for sub_p in sub["paragraphs"]:
                story.append(Paragraph(sub_p, style_body))

story.append(PageBreak())

# ===========================================================================
# CHAPTER 3: PROJECT OVERVIEW
# ===========================================================================
story.append(Paragraph("CHAPTER 3<br/>PROJECT OVERVIEW", style_h1))

for sec in CHAPTER_3["sections"]:
    story.append(Paragraph(f"{sec['num']} {sec['title']}", style_h2))
    for p_txt in sec["paragraphs"]:
        story.append(Paragraph(p_txt, style_body))
        
    if "bullets" in sec:
        for prefix, txt in sec["bullets"]:
            story.append(Paragraph(f"• <b>{prefix}</b> {txt}", style_bullet))
            
    if "table" in sec:
        story.extend(add_pdf_table(sec["table"]))

story.append(PageBreak())

# ===========================================================================
# CHAPTER 4: THEORETICAL ANALYSIS
# ===========================================================================
story.append(Paragraph("CHAPTER 4<br/>THEORETICAL ANALYSIS", style_h1))

for sec in CHAPTER_4["sections"]:
    story.append(Paragraph(f"{sec['num']} {sec['title']}", style_h2))
    for p_txt in sec["paragraphs"]:
        story.append(Paragraph(p_txt, style_body))
        
    if "table" in sec:
        story.extend(add_pdf_table(sec["table"]))

story.append(PageBreak())

# ===========================================================================
# CHAPTER 5: DESIGN AND IMPLEMENTATION
# ===========================================================================
story.append(Paragraph("CHAPTER 5<br/>DESIGN AND IMPLEMENTATION", style_h1))

for sec in CHAPTER_5["sections"]:
    story.append(Paragraph(f"{sec['num']} {sec['title']}", style_h2))
    for p_txt in sec["paragraphs"]:
        story.append(Paragraph(p_txt, style_body))
        
    if "figure" in sec:
        story.extend(add_pdf_figure(sec["figure"]["path"], sec["figure"]["caption"], sec["figure"]["width"]))
        
    if "table" in sec:
        story.extend(add_pdf_table(sec["table"]))
        
    if "subsections" in sec:
        for sub in sec["subsections"]:
            story.append(Paragraph(f"{sub['num']} {sub['title']}", style_h3))
            for sub_p in sub["paragraphs"]:
                story.append(Paragraph(sub_p, style_body))
                
    if "bullets" in sec:
        for prefix, txt in sec["bullets"]:
            story.append(Paragraph(f"• <b>{prefix}</b> {txt}", style_bullet))

story.append(PageBreak())

# ===========================================================================
# CHAPTER 6: RESULT AND ANALYSIS
# ===========================================================================
story.append(Paragraph("CHAPTER 6<br/>RESULT AND ANALYSIS", style_h1))

for sec in CHAPTER_6["sections"]:
    story.append(Paragraph(f"{sec['num']} {sec['title']}", style_h2))
    for p_txt in sec["paragraphs"]:
        story.append(Paragraph(p_txt, style_body))
        
    if "table" in sec:
        story.extend(add_pdf_table(sec["table"]))
        
    if "subsections" in sec:
        for sub in sec["subsections"]:
            story.append(Paragraph(f"{sub['num']} {sub['title']}", style_h3))
            for sub_p in sub["paragraphs"]:
                story.append(Paragraph(sub_p, style_body))
                
    if "walkthrough" in sec:
        for item in sec["walkthrough"]:
            story.append(Paragraph(f"{item['num']} {item['title']}", style_h3))
            story.extend(add_pdf_figure(item["figure"]["path"], item["figure"]["caption"], item["figure"]["width"]))
            story.append(Paragraph(item["text"], style_body))
            
    if "bullets" in sec:
        for prefix, txt in sec["bullets"]:
            story.append(Paragraph(f"• <b>{prefix}</b> {txt}", style_bullet))

story.append(PageBreak())

# ===========================================================================
# CHAPTER 7: CONCLUSION AND FUTURE SCOPE
# ===========================================================================
story.append(Paragraph("CHAPTER 7<br/>CONCLUSION AND FUTURE SCOPE", style_h1))

for sec in CHAPTER_7["sections"]:
    story.append(Paragraph(f"{sec['num']} {sec['title']}", style_h2))
    for p_txt in sec["paragraphs"]:
        story.append(Paragraph(p_txt, style_body))
        
    if "bullets" in sec:
        for prefix, txt in sec["bullets"]:
            story.append(Paragraph(f"• <b>{prefix}</b> {txt}", style_bullet))

story.append(PageBreak())

# ===========================================================================
# CHAPTER 8: REFERENCES
# ===========================================================================
story.append(Paragraph("CHAPTER 8<br/>REFERENCES", style_h1))
story.append(Spacer(1, 0.1 * inch))

for i, ref_item in enumerate(CHAPTER_8["references"]):
    story.append(Paragraph(f"<b>[{i+1}]</b> {ref_item}", ParagraphStyle('RefCustom', fontName='Helvetica', fontSize=10, leading=14, leftIndent=20, firstLineIndent=-20, spaceAfter=6)))

story.append(PageBreak())

# ===========================================================================
# CHAPTER 9: APPENDIX
# ===========================================================================
story.append(Paragraph("CHAPTER 9<br/>APPENDIX", style_h1))

for sec in CHAPTER_9["sections"]:
    story.append(Paragraph(f"{sec['num']} {sec['title']}", style_h2))
    if "paragraphs" in sec:
        for p_txt in sec["paragraphs"]:
            story.append(Paragraph(p_txt, style_body))
            
    if "snippets" in sec:
        for snip in sec["snippets"]:
            story.append(Paragraph(f"<b>{snip['title']}</b>", style_h3))
            c_lines = snip["code"]
            p_code = Preformatted(c_lines, ParagraphStyle('CodeSnip', fontName='Courier', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#1E293B')))
            t_code = Table([[p_code]], colWidths=[6.2 * inch])
            t_code.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
                ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t_code)
            story.append(Spacer(1, 0.1 * inch))
            
    if "bullets" in sec:
        for prefix, txt in sec["bullets"]:
            story.append(Paragraph(f"• <b>{prefix}</b> {txt}", style_bullet))

# Build Document with NumberedCanvas
doc.build(story, canvasmaker=NumberedCanvas)
print(f"PDF successfully compiled: {OUTPUT_PDF}")
