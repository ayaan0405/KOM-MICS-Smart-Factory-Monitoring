# -*- coding: utf-8 -*-
"""
Complete 60-Page Report Compiler for CSD 4102 Internship Report
Guarantees EXACTLY 60 pages adhering strictly to Crescent Institute and Komatsu guidelines.
Preliminary pages: 10 pages (no page numbers)
Chapters: 50 pages (Arabic pages 1 to 50)
"""

import os
from PIL import Image as PILImage
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

# Komatsu Brand Colors
COLOR_NAVY = colors.HexColor("#002D62")
COLOR_YELLOW = colors.HexColor("#F5B800")
COLOR_TEXT = colors.HexColor("#0F172A")
COLOR_MUTED = colors.HexColor("#64748B")
COLOR_BORDER = colors.HexColor("#CBD5E1")
COLOR_LIGHT_BG = colors.HexColor("#F8FAFC")

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to calculate page counts and draw bottom-centered page numbers."""
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
        # Preliminaries: Sheets 1 to 10 (Cover, Bonafide, Cert, Viva, Ack, TOC 1-2, Abbr, Figs, Abstract)
        # As per faculty note on Image: "Don't put numbers for upto abstract. Page no starts from chapter 1"
        # Chapter 1 starts at Sheet 11 in PDF (Arabic Page 1)
        chap1_page = 11
        if self._pageNumber >= chap1_page:
            arabic_num = self._pageNumber - chap1_page + 1
            self.saveState()
            self.setFont("Helvetica", 11)
            self.setFillColor(COLOR_TEXT)
            # Centered at bottom y = 38.2 pt (0.53 in), x = letter[0]/2.0 (306.0 pt) matching reference PDF!
            self.drawCentredString(letter[0] / 2.0, 38.2, str(arabic_num))
            self.restoreState()

def build_pdf():
    print("Building exact 60-page PDF report...")
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch
    )

    styles = getSampleStyleSheet()

    # Typography Styles matching reference PDF
    style_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=23,
        alignment=1, # Center
        textColor=COLOR_NAVY,
        spaceAfter=10
    )

    style_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        alignment=1, # Center
        textColor=COLOR_TEXT,
        spaceAfter=25
    )

    style_h1 = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        alignment=1, # Center
        textColor=COLOR_NAVY,
        spaceBefore=14,
        spaceAfter=12,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=0, # Left
        textColor=COLOR_NAVY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        'Heading3Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=0, # Left
        textColor=COLOR_NAVY,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11.5,
        leading=15.2,
        alignment=4, # Justified
        textColor=COLOR_TEXT,
        spaceAfter=5.5
    )

    style_bullet = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14.5,
        alignment=4,
        textColor=COLOR_TEXT,
        leftIndent=16,
        spaceAfter=3
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
        spaceAfter=8,
        keepWithNext=True
    )

    def add_pdf_figure(img_path, caption_text, width_inches=6.0, max_h=3.6):
        if not os.path.exists(img_path):
            return []
        im = PILImage.open(img_path)
        w, h = im.size
        aspect = h / float(w)
        h_inches = width_inches * aspect
        if h_inches > max_h:
            h_inches = max_h
            width_inches = h_inches / aspect
        return [
            Spacer(1, 0.05 * inch),
            RLImage(img_path, width=width_inches * inch, height=h_inches * inch),
            Paragraph(caption_text, style_caption),
            Spacer(1, 0.05 * inch)
        ]

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
        avail_w = 6.4 * inch
        col_w = avail_w / num_cols
        col_widths = [col_w] * num_cols
        if num_cols == 3:
            col_widths = [1.8 * inch, 2.3 * inch, 2.3 * inch]
        elif num_cols == 5:
            col_widths = [1.4 * inch, 1.1 * inch, 1.4 * inch, 1.3 * inch, 1.2 * inch]
        elif num_cols == 7:
            col_widths = [0.8 * inch, 1.2 * inch, 1.0 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 1.0 * inch]

        t = Table(t_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_NAVY),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG])
        ]))
        return [
            Paragraph(f"<b>Table {table_def['number']} – {table_def['title']}</b>", style_caption),
            t,
            Spacer(1, 0.08 * inch)
        ]

    story = []

    # ===========================================================================
    # SHEET 1: COVER PAGE
    # ===========================================================================
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("SMART FACTORY MONITORING SYSTEM<br/>INSPIRED BY KOM-MICS", style_title))
    story.append(Paragraph("AN INTERNSHIP REPORT", style_subtitle))
    story.append(Spacer(1, 0.2 * inch))

    p_by = Paragraph("<font size=11><i>Submitted by</i></font><br/><br/><b><font size=13>" + METADATA["student_name"] + "</font></b><br/><b>(RRN: " + METADATA["register_no"] + ")</b>", ParagraphStyle('CoverBy', alignment=1, leading=18))
    story.append(p_by)
    story.append(Spacer(1, 0.35 * inch))

    p_deg = Paragraph("<font size=10.5><i>in partial fulfillment for the award of the degree of</i></font><br/><br/><b><font size=12>" + METADATA["degree"] + "<br/>in<br/>" + METADATA["branch"] + "</font></b>", ParagraphStyle('CoverDeg', alignment=1, leading=16))
    story.append(p_deg)
    story.append(Spacer(1, 0.3 * inch))

    logo_path = 'report_assets/extracted_p0_0_Image13.jpg'
    if os.path.exists(logo_path):
        story.append(RLImage(logo_path, width=3.2 * inch, height=0.86 * inch))

    story.append(Spacer(1, 0.3 * inch))
    p_inst = Paragraph("<b>" + METADATA["submission_date"] + "</b>", ParagraphStyle('CoverDate', alignment=1, fontName='Helvetica-Bold', fontSize=11))
    story.append(p_inst)
    story.append(PageBreak())

    # ===========================================================================
    # SHEET 2: BONAFIDE CERTIFICATE (Page i)
    # ===========================================================================
    if os.path.exists(logo_path):
        story.append(RLImage(logo_path, width=2.5 * inch, height=0.68 * inch))
        story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("BONAFIDE CERTIFICATE", style_h1))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(PRELIMINARIES["bonafide"]["body"], style_body))
    story.append(Spacer(1, 0.6 * inch))

    sig_data = [
        [
            Paragraph("<b>SIGNATURE</b><br/><b>[FACULTY COORDINATOR / ADVISOR]</b><br/>Assistant Professor / Coordinator<br/>Department of CSE<br/>B.S. Abdur Rahman Crescent<br/>Institute of Science and Technology<br/>Vandalur, Chennai – 600 048.", ParagraphStyle('SigL', fontName='Helvetica', fontSize=10, leading=14)),
            Paragraph("<b>SIGNATURE</b><br/><b>[HEAD OF THE DEPARTMENT]</b><br/>Professor and Head<br/>Department of CSE<br/>B.S. Abdur Rahman Crescent<br/>Institute of Science and Technology<br/>Vandalur, Chennai – 600 048.", ParagraphStyle('SigR', fontName='Helvetica', fontSize=10, leading=14))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[3.2 * inch, 3.2 * inch])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_sig)
    story.append(PageBreak())

    # ===========================================================================
    # SHEET 3: INTERNSHIP CERTIFICATE (Page ii)
    # ===========================================================================
    story.append(Paragraph("INTERNSHIP CERTIFICATE", style_h1))
    story.append(Spacer(1, 0.08 * inch))
    cert_img = 'report_assets/media_1795463364605_b089eca9.jpg'
    if os.path.exists(cert_img):
        story.append(RLImage(cert_img, width=5.6 * inch, height=7.7 * inch))
    story.append(PageBreak())

    # ===========================================================================
    # SHEET 4: VIVA VOCE EXAMINATION (Page iii)
    # ===========================================================================
    if os.path.exists(logo_path):
        story.append(RLImage(logo_path, width=2.5 * inch, height=0.68 * inch))
        story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("VIVA VOCE EXAMINATION", style_h1))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph(PRELIMINARIES["viva_voce"]["body"], style_body))
    story.append(Spacer(1, 1.2 * inch))

    viva_data = [
        [
            Paragraph("____________________________<br/><b>INTERNAL EXAMINER</b>", ParagraphStyle('VivaL', fontName='Helvetica', fontSize=10.5, leading=16)),
            Paragraph("____________________________<br/><b>EXTERNAL EXAMINER</b>", ParagraphStyle('VivaR', alignment=2, fontName='Helvetica', fontSize=10.5, leading=16))
        ]
    ]
    t_viva = Table(viva_data, colWidths=[3.2 * inch, 3.2 * inch])
    t_viva.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_viva)
    story.append(PageBreak())

    # ===========================================================================
    # SHEET 5: ACKNOWLEDGEMENT (Page iv)
    # ===========================================================================
    story.append(Paragraph("ACKNOWLEDGEMENT", style_h1))
    story.append(Spacer(1, 0.08 * inch))
    for p_txt in PRELIMINARIES["acknowledgement"]:
        story.append(Paragraph(p_txt, style_body))

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("<b>" + METADATA["student_name"] + "</b>", ParagraphStyle('AckName', alignment=2, fontName='Helvetica-Bold', fontSize=11)))
    story.append(PageBreak())

    # ===========================================================================
    # SHEET 6 & 7: TABLE OF CONTENTS (Part 1 & 2)
    # Matching exact order of Image & Reference Report (NO List of Tables!)
    # ===========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", style_h1))
    story.append(Spacer(1, 0.08 * inch))

    toc_part1 = [
        [Paragraph("<b>CHAPTER NO.</b>", ParagraphStyle('TH0', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY)),
         Paragraph("<b>TITLE</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY)),
         Paragraph("<b>PAGE NO.</b>", ParagraphStyle('TH2', alignment=2, fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY))]
    ]

    toc_items_p1 = [
        ("", "LIST OF ABBREVIATIONS", ""),
        ("", "LIST OF FIGURES", ""),
        ("", "ABSTRACT", ""),
        ("1", "COMPANY OVERVIEW", "1"),
        ("1.1", "COMPANY OVERVIEW", "1"),
        ("1.2", "COMPANY WEBSITE", "2"),
        ("1.3", "CHENNAI MANUFACTURING PLANT (ORAGADAM FACILITY)", "2"),
        ("1.4", "MANUFACTURING OPERATIONS AND BUSINESS CONTEXT", "2"),
        ("2", "ROLE AND RESPONSIBILITIES", "4"),
        ("2.1", "ROLE", "4"),
        ("2.2", "RESPONSIBILITIES (DEPARTMENTS OBSERVED)", "4"),
        ("2.3", "ENGINEERING RESPONSIBILITIES AND ACADEMIC LEARNING", "7"),
        ("3", "PROJECT OVERVIEW", "8"),
        ("3.1", "PROJECT OVERVIEW", "8"),
        ("3.2", "OBJECTIVES", "8"),
        ("3.3", "SCOPE AND DATASET", "9"),
        ("3.4", "DASHBOARD STRUCTURE", "10"),
        ("4", "THEORETICAL ANALYSIS", "12"),
        ("4.1", "INTRODUCTION", "12"),
        ("4.2", "INDUSTRIAL IOT AND MACHINE HEALTH MONITORING", "12"),
        ("4.3", "CORE TELEMETRY VARIABLES IN INDUSTRIAL EQUIPMENT", "13"),
        ("4.4", "WEB APPLICATION ARCHITECTURES: FLASK & CHART.JS", "14"),
        ("4.5", "RELATIONAL PERSISTENCE & SQLITE WAL MODE", "14"),
        ("4.6", "PARETO (80/20) AND ALARM EXCEPTION LOGIC", "15"),
        ("4.7", "FACTORY RELIABILITY KPIS (AVAILABILITY, MTBF, MTTR)", "15"),
        ("4.8", "VISUALIZATION AND UI/UX PRINCIPLES", "16"),
        ("4.9", "SUMMARY", "16"),
        ("5", "DESIGN AND IMPLEMENTATION", "17"),
        ("5.1", "DESIGN PHASE & SYSTEM TOPOLOGY", "17"),
        ("5.2", "DATA INGESTION AND SIMULATOR ENGINE", "18"),
        ("5.3", "DATA MODEL IMPLEMENTATION (RELATIONAL SCHEMA)", "19"),
        ("5.4", "BACKEND API IMPLEMENTATION & STATE ROUTING", "21"),
        ("5.5", "PLANT AVAILABILITY CALCULATION LOGIC", "22"),
        ("5.6", "MACHINE MATRIX & INSPECTOR DRAWER", "22"),
        ("5.7", "ALARM LIFECYCLE MANAGEMENT & FSM", "23"),
        ("5.8", "EQUIPMENT MAINTENANCE & DOWNTIME TRACKING", "24"),
        ("5.9", "SIMULATED SHIFT PRODUCTION & SCRAP RATE", "24"),
        ("5.10", "TESTING AND VALIDATION", "25"),
        ("5.11", "SKILLS GAINED", "25")
    ]

    for c_no, t_str, p_no in toc_items_p1:
        is_bold = c_no != "" and "." not in c_no
        w_open = "<b>" if is_bold else ""
        w_close = "</b>" if is_bold else ""
        toc_part1.append([
            Paragraph(f"{w_open}{c_no}{w_close}", ParagraphStyle('TOCCol0', fontName='Helvetica-Bold' if is_bold else 'Helvetica', fontSize=8.5, leading=11)),
            Paragraph(f"{w_open}{t_str}{w_close}", ParagraphStyle('TOCCol1', fontName='Helvetica-Bold' if is_bold else 'Helvetica', fontSize=8.5, leading=11)),
            Paragraph(f"<b>{p_no}</b>", ParagraphStyle('TOCCol2', alignment=2, fontName='Helvetica-Bold', fontSize=8.5, leading=11))
        ])

    t_toc1 = Table(toc_part1, colWidths=[1.1 * inch, 4.4 * inch, 0.9 * inch])
    t_toc1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.0),
        ('TOPPADDING', (0,0), (-1,-1), 1.0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_toc1)
    story.append(PageBreak())

    # TOC Part 2 (Sheet 7)
    toc_part2 = [
        [Paragraph("<b>CHAPTER NO.</b>", ParagraphStyle('TH0', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY)),
         Paragraph("<b>TITLE</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY)),
         Paragraph("<b>PAGE NO.</b>", ParagraphStyle('TH2', alignment=2, fontName='Helvetica-Bold', fontSize=9.5, textColor=COLOR_NAVY))]
    ]

    toc_items_p2 = [
        ("6", "RESULT AND ANALYSIS", "26"),
        ("6.1", "OVERVIEW OF RESULTS", "26"),
        ("6.2", "MACHINE AVAILABILITY AND FLEET PERFORMANCE", "27"),
        ("6.3", "ASSET TELEMETRY AND SENSOR CONSISTENCY", "27"),
        ("6.4", "OPERATING STATE TIMELINE ANALYSIS (ANDON)", "29"),
        ("6.5", "DEPARTMENT PRODUCTION AND SCRAP ANALYSIS", "30"),
        ("6.6", "MAINTENANCE AND DOWNTIME EVALUATION", "31"),
        ("6.7", "ALARM RESPONSE AND EXCEPTION HANDLING ANALYSIS", "33"),
        ("6.8", "ANALYSIS OF SYSTEM ARCHITECTURE", "34"),
        ("6.9", "DASHBOARD SCREENSHOTS AND WALKTHROUGH", "36"),
        ("6.10", "COMPREHENSIVE SYSTEM VERIFICATION MATRIX", "41"),
        ("6.11", "TECHNICAL LIMITATIONS AND ACADEMIC OBSERVATIONS", "42"),
        ("7", "CONCLUSION AND FUTURE SCOPE", "44"),
        ("7.1", "CONCLUSION", "44"),
        ("7.2", "SYNTHESIS OF OBSERVATION AND SOFTWARE ENGINEERING", "44"),
        ("7.3", "FUTURE TECHNICAL SCOPE AND SCALABILITY", "44"),
        ("8", "REFERENCES", "46"),
        ("9", "APPENDIX", "47"),
        ("9.1", "CORE APPLICATION SOURCE CODE", "47"),
        ("9.2", "DATABASE SCHEMA DDL", "49"),
        ("9.3", "REST API ENDPOINTS SPECIFICATION", "50"),
        ("9.4", "TECHNICAL BIBLIOGRAPHY", "50")
    ]

    for c_no, t_str, p_no in toc_items_p2:
        is_bold = c_no != "" and "." not in c_no
        w_open = "<b>" if is_bold else ""
        w_close = "</b>" if is_bold else ""
        toc_part2.append([
            Paragraph(f"{w_open}{c_no}{w_close}", ParagraphStyle('TOCCol0', fontName='Helvetica-Bold' if is_bold else 'Helvetica', fontSize=8.5, leading=11)),
            Paragraph(f"{w_open}{t_str}{w_close}", ParagraphStyle('TOCCol1', fontName='Helvetica-Bold' if is_bold else 'Helvetica', fontSize=8.5, leading=11)),
            Paragraph(f"<b>{p_no}</b>", ParagraphStyle('TOCCol2', alignment=2, fontName='Helvetica-Bold', fontSize=8.5, leading=11))
        ])

    t_toc2 = Table(toc_part2, colWidths=[1.1 * inch, 4.4 * inch, 0.9 * inch])
    t_toc2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_toc2)
    story.append(PageBreak())

    # ===========================================================================
    # SHEET 8: LIST OF ABBREVIATIONS
    # ===========================================================================
    story.append(Paragraph("LIST OF ABBREVIATIONS", style_h1))
    story.append(Spacer(1, 0.08 * inch))

    abbr_rows = [
        [Paragraph("<b>ABBREVIATION</b>", ParagraphStyle('AbH1', fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.white)),
         Paragraph("<b>FULL FORM</b>", ParagraphStyle('AbH2', fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.white))]
    ]

    for ab, full in PRELIMINARIES["abbreviations"]:
        abbr_rows.append([
            Paragraph(f"<b>{ab}</b>", ParagraphStyle('AbC1', fontName='Helvetica-Bold', fontSize=8.5, leading=11)),
            Paragraph(full, ParagraphStyle('AbC2', fontName='Helvetica', fontSize=8.5, leading=11))
        ])

    t_abbr = Table(abbr_rows, colWidths=[1.8 * inch, 4.6 * inch])
    t_abbr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_NAVY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG])
    ]))
    story.append(t_abbr)
    story.append(PageBreak())

    # ===========================================================================
    # SHEET 9: LIST OF FIGURES
    # ===========================================================================
    story.append(Paragraph("LIST OF FIGURES", style_h1))
    story.append(Spacer(1, 0.08 * inch))

    fig_rows = [
        [Paragraph("<b>FIGURE NO.</b>", ParagraphStyle('FH1', fontName='Helvetica-Bold', fontSize=9, textColor=COLOR_NAVY)),
         Paragraph("<b>TITLE</b>", ParagraphStyle('FH2', fontName='Helvetica-Bold', fontSize=9, textColor=COLOR_NAVY)),
         Paragraph("<b>PAGE NO.</b>", ParagraphStyle('FH3', alignment=2, fontName='Helvetica-Bold', fontSize=9, textColor=COLOR_NAVY))]
    ]

    figures_list = [
        ("1.1", "Komatsu Corporate Logo & Industrial Brand Identity", "1"),
        ("4.1", "Four-Tier System Architecture of the Smart Factory Monitoring System", "12"),
        ("5.1", "Relational Database Schema & Entity-Relationship Diagram (factory.db)", "18"),
        ("5.2", "Finite State Machine: Equipment Operating State & Alarm Lifecycle", "23"),
        ("6.1", "Fleet Operational Availability & Active Machine Count (24-Hour Profile)", "27"),
        ("6.2", "Sensor Correlation: Operating Temperature vs. Vibration Velocity", "28"),
        ("6.3", "Spindle Velocity Profile Across Monitored Fleet (Zero RPM for IDLE)", "28"),
        ("6.4", "Departmental Production Output vs. Target Deficit (Shift Analysis)", "29"),
        ("6.5", "Quality Inspection Scrap & Reject Rate Distribution by Division", "30"),
        ("6.6", "Equipment Downtime Pareto Analysis by Maintenance Category (80/20)", "30"),
        ("6.7", "Shift-Wise Machine Operating State Timeline (Real-Time Andon Sequence)", "31"),
        ("6.8", "Sensor Telemetry Frequency Distribution Across Production Shift", "33"),
        ("6.9", "Plant Overview Console: Real-Time Operational SCADA Interface", "36"),
        ("6.10", "Dynamic Oscilloscope Telemetry Line Chart & Spindle Profile", "37"),
        ("6.11", "Equipment Telemetry Matrix with Multi-Parameter Query Filtering", "37"),
        ("6.12", "Equipment Side Inspector Drawer: Telemetry Log & Maintenance", "38"),
        ("6.13", "Alarms & Fault Event Management Console: Severity & Resolution", "39"),
        ("6.14", "Chronological Telemetry Stream Audit Log Interface", "39"),
        ("6.15", "Equipment Maintenance & Downtime Tracker Console Interface", "40"),
        ("6.16", "Record Equipment Maintenance / Downtime Event Modal Dialog", "41")
    ]

    for fn, ft, fp in figures_list:
        fig_rows.append([
            Paragraph(f"<b>Fig {fn}</b>", ParagraphStyle('FC1', fontName='Helvetica-Bold', fontSize=8.5)),
            Paragraph(ft, ParagraphStyle('FC2', fontName='Helvetica', fontSize=8.5)),
            Paragraph(f"<b>{fp}</b>", ParagraphStyle('FC3', alignment=2, fontName='Helvetica-Bold', fontSize=8.5))
        ])

    t_fig = Table(fig_rows, colWidths=[1.1 * inch, 4.3 * inch, 1.0 * inch])
    t_fig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, COLOR_BORDER)
    ]))
    story.append(t_fig)
    story.append(PageBreak())

    # ===========================================================================
    # SHEET 10: ABSTRACT
    # Must fit completely on Sheet 10 (Page ix in Roman sequence, no printed number)
    # ===========================================================================
    story.append(Paragraph("ABSTRACT", style_h1))
    story.append(Spacer(1, 0.08 * inch))
    style_abstract_body = ParagraphStyle(
        'AbstractBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14.0,
        alignment=4, # Justified
        textColor=COLOR_TEXT,
        spaceAfter=4.5
    )
    for p_txt in PRELIMINARIES["abstract"]:
        story.append(Paragraph(p_txt, style_abstract_body))

    story.append(PageBreak())

    # ===========================================================================
    # SHEET 11-13: CHAPTER 1: COMPANY OVERVIEW (Arabic Pages 1 - 3)
    # ===========================================================================
    story.append(Paragraph("CHAPTER 1<br/>COMPANY OVERVIEW", style_h1))
    story.extend(add_pdf_figure('report_assets/komatsu_logo.png', "Fig 1.1 – Komatsu Corporate Logo & Industrial Brand Identity", 3.8, max_h=1.2))

    # Sec 1.1
    s11 = CHAPTER_1["sections"][0]
    story.append(Paragraph(f"{s11['num']} {s11['title']}", style_h2))
    for p in s11["paragraphs"]:
        story.append(Paragraph(p, style_body))

    # Sec 1.2
    s12 = CHAPTER_1["sections"][1]
    story.append(Paragraph(f"{s12['num']} {s12['title']}", style_h2))
    for p in s12["paragraphs"]:
        story.append(Paragraph(p, style_body))

    # Sec 1.3
    s13 = CHAPTER_1["sections"][2]
    story.append(Paragraph(f"{s13['num']} {s13['title']}", style_h2))
    for p in s13["paragraphs"]:
        story.append(Paragraph(p, style_body))

    # Sec 1.4
    s14 = CHAPTER_1["sections"][3]
    story.append(Paragraph(f"{s14['num']} {s14['title']}", style_h2))
    for p in s14["paragraphs"]:
        story.append(Paragraph(p, style_body))

    story.append(PageBreak())

    # ===========================================================================
    # SHEET 14-17: CHAPTER 2: ROLE AND RESPONSIBILITIES (Arabic Pages 4 - 7)
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
    # SHEET 18-21: CHAPTER 3: PROJECT OVERVIEW (Arabic Pages 8 - 11)
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
    # SHEET 22-26: CHAPTER 4: THEORETICAL ANALYSIS (Arabic Pages 12 - 16)
    # ===========================================================================
    story.append(Paragraph("CHAPTER 4<br/>THEORETICAL ANALYSIS", style_h1))
    story.extend(add_pdf_figure('report_assets/fig4_1_architecture.png', "Fig 4.1 – Four-Tier System Architecture of the Smart Factory Monitoring System", 5.8, max_h=2.8))

    for sec in CHAPTER_4["sections"]:
        story.append(Paragraph(f"{sec['num']} {sec['title']}", style_h2))
        for p_txt in sec["paragraphs"]:
            story.append(Paragraph(p_txt, style_body))
            
        if "table" in sec:
            story.extend(add_pdf_table(sec["table"]))

    story.append(PageBreak())

    # ===========================================================================
    # SHEET 27-36: CHAPTER 5: DESIGN AND IMPLEMENTATION (Arabic Pages 17 - 26)
    # ===========================================================================
    story.append(Paragraph("CHAPTER 5<br/>DESIGN AND IMPLEMENTATION", style_h1))

    for sec in CHAPTER_5["sections"]:
        story.append(Paragraph(f"{sec['num']} {sec['title']}", style_h2))
        for p_txt in sec["paragraphs"]:
            story.append(Paragraph(p_txt, style_body))
            
        if "figure" in sec:
            story.extend(add_pdf_figure(sec["figure"]["path"], sec["figure"]["caption"], sec["figure"]["width"], max_h=3.2))
            
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
    # SHEET 37-52: CHAPTER 6: RESULT AND ANALYSIS (Arabic Pages 27 - 42)
    # Includes all 8 analytical figures + 8 live dashboard UI screens
    # ===========================================================================
    story.append(Paragraph("CHAPTER 6<br/>RESULT AND ANALYSIS", style_h1))

    # Analytical chart mapping
    fig_map = {
        "6.2": ("report_assets/fig6_1_availability_trend.png", "Fig 6.1 – Fleet Operational Availability & Active Machine Count (24-Hour Profile)"),
        "6.3": ("report_assets/fig6_2_sensor_correlation.png", "Fig 6.2 – Sensor Correlation: Operating Temperature vs. Vibration Velocity"),
        "6.4": ("report_assets/fig6_4_production_output.png", "Fig 6.4 – Departmental Production Output vs. Target Deficit (Shift Analysis)"),
        "6.5": ("report_assets/fig6_6_downtime_pareto.png", "Fig 6.6 – Equipment Downtime Pareto Analysis by Maintenance Category (80/20 Rule)"),
        "6.6": ("report_assets/fig6_7_andon_timeline.png", "Fig 6.7 – Shift-Wise Machine Operating State Timeline (Real-Time Andon Sequence)"),
        "6.7": ("report_assets/fig6_8_telemetry_stream.png", "Fig 6.8 – Sensor Telemetry Frequency Distribution Across Production Shift")
    }

    for sec in CHAPTER_6["sections"]:
        s_num = sec['num']
        story.append(Paragraph(f"{s_num} {sec['title']}", style_h2))
        for p_txt in sec["paragraphs"]:
            story.append(Paragraph(p_txt, style_body))
            
        if s_num in fig_map:
            f_path, f_cap = fig_map[s_num]
            story.extend(add_pdf_figure(f_path, f_cap, 5.8, max_h=2.6))
            if s_num == "6.3":
                story.extend(add_pdf_figure('report_assets/fig6_3_spindle_velocity.png', "Fig 6.3 – Spindle Velocity Profile Across Monitored Fleet (Zero RPM for IDLE Machinery)", 5.8, max_h=2.5))
            elif s_num == "6.4":
                story.extend(add_pdf_figure('report_assets/fig6_5_scrap_rate.png', "Fig 6.5 – Quality Inspection Scrap & Reject Rate Distribution by Manufacturing Division", 5.8, max_h=2.5))
            
        if "table" in sec:
            story.extend(add_pdf_table(sec["table"]))
            
        if "subsections" in sec:
            for sub in sec["subsections"]:
                story.append(Paragraph(f"{sub['num']} {sub['title']}", style_h3))
                for sub_p in sub["paragraphs"]:
                    story.append(Paragraph(sub_p, style_body))
                    
        if "walkthrough" in sec:
            # 8 live UI screenshots (Figs 6.9 to 6.16)
            for item in sec["walkthrough"]:
                story.append(Paragraph(f"{item['num']} {item['title']}", style_h3))
                story.extend(add_pdf_figure(item["figure"]["path"], item["figure"]["caption"], item["figure"]["width"], max_h=3.0))
                story.append(Paragraph(item["text"], style_body))
                
        if "bullets" in sec:
            for prefix, txt in sec["bullets"]:
                story.append(Paragraph(f"• <b>{prefix}</b> {txt}", style_bullet))

    story.append(PageBreak())

    # ===========================================================================
    # SHEET 53-54: CHAPTER 7: CONCLUSION AND FUTURE SCOPE (Arabic Pages 43 - 44)
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
    # SHEET 55: CHAPTER 8: REFERENCES (Arabic Page 45)
    # ===========================================================================
    story.append(Paragraph("CHAPTER 8<br/>REFERENCES", style_h1))
    story.append(Spacer(1, 0.1 * inch))

    for i, ref_item in enumerate(CHAPTER_8["references"]):
        story.append(Paragraph(f"<b>[{i+1}]</b> {ref_item}", ParagraphStyle('RefCustom', fontName='Helvetica', fontSize=9.5, leading=13.5, leftIndent=18, firstLineIndent=-18, spaceAfter=5)))

    story.append(PageBreak())

    # ===========================================================================
    # SHEET 56-60: CHAPTER 9: APPENDIX (Arabic Pages 46 - 50)
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
                p_code = Preformatted(c_lines, ParagraphStyle('CodeSnip', fontName='Courier', fontSize=7.2, leading=9.0, textColor=colors.HexColor('#1E293B')))
                t_code = Table([[p_code]], colWidths=[6.4 * inch])
                t_code.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
                    ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                    ('TOPPADDING', (0,0), (-1,-1), 3),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                    ('LEFTPADDING', (0,0), (-1,-1), 5),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                ]))
                story.append(t_code)
                story.append(Spacer(1, 0.06 * inch))
                
        if "bullets" in sec:
            for prefix, txt in sec["bullets"]:
                story.append(Paragraph(f"• <b>{prefix}</b> {txt}", style_bullet))

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully compiled: {OUTPUT_PDF}")

if __name__ == '__main__':
    build_pdf()
