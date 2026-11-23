# -*- coding: utf-8 -*-
"""
Master Document Compiler: Smart Factory Monitoring System Internship Report
Constructs a publication-grade .docx document adhering strictly to Crescent Institute & Komatsu guidelines.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from report_text_part1 import METADATA, PRELIMINARIES, CHAPTER_1, CHAPTER_2, CHAPTER_3
from report_text_part2 import CHAPTER_4, CHAPTER_5
from report_text_part3 import CHAPTER_6, CHAPTER_7, CHAPTER_8, CHAPTER_9

OUTPUT_DOCX = "SMART_FACTORY_MONITORING_SYSTEM_INTERNSHIP_REPORT.docx"

# Color Palette
COLOR_NAVY = RGBColor(0, 45, 98)       # #002D62 (Komatsu Corporate Navy)
COLOR_YELLOW = RGBColor(245, 184, 0)   # #F5B800 (Komatsu Yellow)
COLOR_TEXT = RGBColor(15, 23, 42)      # #0F172A (Dark Charcoal)
COLOR_MUTED = RGBColor(100, 116, 139)  # #64748B (Muted Slate)
HEX_NAVY = "002D62"
HEX_LIGHT_BG = "F8FAFC"
HEX_BORDER = "CBD5E1"
HEX_YELLOW_BG = "FEF3C7"

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Sets inner padding for a table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    """Applies background fill color to a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    """Applies clean, subtle borders to an entire table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_page_number_field(run):
    """Inserts a dynamic Word PAGE number XML field."""
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def add_heading_1(doc, text):
    """Adds a Chapter / Major Section Heading (Centered, Bold, 16pt)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_heading_2(doc, text):
    """Adds a Section Heading (Centered, Bold, 13pt)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_heading_3(doc, text):
    """Adds a Subsection Heading (Centered/Left, Bold, 12pt)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_body_p(doc, text):
    """Adds standard body text (Arial 12pt, Justified, 1.15 line spacing)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    run.font.color.rgb = COLOR_TEXT
    return p

def add_bullet_p(doc, bold_prefix, text):
    """Adds a structured bullet paragraph."""
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    r_bold = p.add_run(bold_prefix)
    r_bold.font.name = 'Arial'
    r_bold.font.size = Pt(12)
    r_bold.font.bold = True
    r_bold.font.color.rgb = COLOR_TEXT
    
    r_text = p.add_run(text)
    r_text.font.name = 'Arial'
    r_text.font.size = Pt(12)
    r_text.font.color.rgb = COLOR_TEXT
    return p

def add_figure(doc, img_path, caption_text, width_inches=6.0):
    """Embeds a centered figure with an official academic caption."""
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        p_cap.paragraph_format.keep_with_next = True
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = 'Arial'
        run_cap.font.size = Pt(10)
        run_cap.font.bold = True
        run_cap.font.color.rgb = COLOR_NAVY
    else:
        p_err = doc.add_paragraph(f"[Image Missing: {img_path}]")
        p_err.alignment = WD_ALIGN_PARAGRAPH.CENTER

def add_table(doc, table_def):
    """Renders a styled academic data table with official caption."""
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(8)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(f"Table {table_def['number']} – {table_def['title']}")
    r_cap.font.name = 'Arial'
    r_cap.font.size = Pt(10)
    r_cap.font.bold = True
    r_cap.font.color.rgb = COLOR_NAVY

    headers = table_def['headers']
    rows = table_def['rows']
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl, color="CBD5E1", sz="4", val="single")

    # Header Row
    hdr_row = tbl.rows[0]
    hdr_row._tr.get_or_add_trPr().append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    for idx, heading in enumerate(headers):
        cell = hdr_row.cells[idx]
        set_cell_shading(cell, HEX_NAVY)
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(heading)
        r.font.name = 'Arial'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for r_idx, row_data in enumerate(rows):
        row = tbl.rows[r_idx + 1]
        bg_color = HEX_LIGHT_BG if (r_idx % 2 == 1) else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            if bg_color != "FFFFFF":
                set_cell_shading(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(str(val))
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_TEXT

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(6)

def add_code_snippet(doc, title, code):
    """Renders a formatted source code block."""
    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(8)
    p_t.paragraph_format.space_after = Pt(2)
    p_t.paragraph_format.keep_with_next = True
    r_t = p_t.add_run(title)
    r_t.font.name = 'Arial'
    r_t.font.size = Pt(10)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_NAVY

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.rows[0].cells[0]
    set_cell_shading(cell, "F1F5F9")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    set_table_borders(tbl, color="CBD5E1", sz="6", val="single")

    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(code)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

print("Starting document compilation...")
doc = docx.Document()

# Configure standard margins for Section 1 (Preliminaries)
sec1 = doc.sections[0]
sec1.top_margin = Inches(1.0)
sec1.bottom_margin = Inches(1.0)
sec1.left_margin = Inches(1.25)
sec1.right_margin = Inches(1.0)

# Configure Default Normal Style
normal_style = doc.styles['Normal']
normal_style.font.name = 'Arial'
normal_style.font.size = Pt(12)
normal_style.font.color.rgb = COLOR_TEXT

# ===========================================================================
# 1. COVER PAGE
# ===========================================================================
p_cov = doc.add_paragraph()
p_cov.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cov.paragraph_format.space_before = Pt(36)
p_cov.paragraph_format.space_after = Pt(10)
r = p_cov.add_run("SMART FACTORY MONITORING SYSTEM\nINSPIRED BY KOM-MICS")
r.font.name = 'Arial'
r.font.size = Pt(18)
r.font.bold = True
r.font.color.rgb = COLOR_NAVY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(8)
p_sub.paragraph_format.space_after = Pt(40)
r = p_sub.add_run("AN INTERNSHIP REPORT")
r.font.name = 'Arial'
r.font.size = Pt(13)
r.font.bold = True
r.font.color.rgb = COLOR_TEXT

p_by = doc.add_paragraph()
p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_by.paragraph_format.space_after = Pt(6)
r = p_by.add_run("Submitted by")
r.font.name = 'Arial'
r.font.size = Pt(12)
r.font.italic = True

p_name = doc.add_paragraph()
p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_name.paragraph_format.space_after = Pt(2)
r = p_name.add_run(METADATA["student_name"])
r.font.name = 'Arial'
r.font.size = Pt(14)
r.font.bold = True

p_rrn = doc.add_paragraph()
p_rrn.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_rrn.paragraph_format.space_after = Pt(36)
r = p_rrn.add_run(f"(RRN: {METADATA['register_no']})")
r.font.name = 'Arial'
r.font.size = Pt(12)
r.font.bold = True

p_deg = doc.add_paragraph()
p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_deg.paragraph_format.space_after = Pt(6)
r = p_deg.add_run("in partial fulfillment for the award of the degree of")
r.font.name = 'Arial'
r.font.size = Pt(11)
r.font.italic = True

p_deg_title = doc.add_paragraph()
p_deg_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_deg_title.paragraph_format.space_after = Pt(4)
r = p_deg_title.add_run(f"{METADATA['degree']}\nin\n{METADATA['branch']}")
r.font.name = 'Arial'
r.font.size = Pt(13)
r.font.bold = True

# Embed Crescent Logo
logo_path = 'report_assets/extracted_p0_0_Image13.jpg'
if os.path.exists(logo_path):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(28)
    p_logo.paragraph_format.space_after = Pt(16)
    r_logo = p_logo.add_run()
    r_logo.add_picture(logo_path, width=Inches(3.2))

p_date = doc.add_paragraph()
p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_date.paragraph_format.space_before = Pt(16)
r = p_date.add_run(METADATA["submission_date"])
r.font.name = 'Arial'
r.font.size = Pt(12)
r.font.bold = True

doc.add_page_break()

# ===========================================================================
# 2. BONAFIDE CERTIFICATE (Page i)
# ===========================================================================
if os.path.exists(logo_path):
    p_l = doc.add_paragraph()
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.space_after = Pt(12)
    p_l.add_run().add_picture(logo_path, width=Inches(2.6))

add_heading_1(doc, "BONAFIDE CERTIFICATE")

p_cert_body = doc.add_paragraph()
p_cert_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_cert_body.paragraph_format.line_spacing = 1.25
p_cert_body.paragraph_format.space_before = Pt(16)
p_cert_body.paragraph_format.space_after = Pt(40)
r_cb = p_cert_body.add_run(PRELIMINARIES["bonafide"]["body"])
r_cb.font.name = 'Arial'
r_cb.font.size = Pt(12)

# Two-column signature table (Faculty Guide Placeholder Left, HOD Placeholder Right)
sig_tbl = doc.add_table(rows=1, cols=2)
sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
sig_tbl.autofit = False
set_table_borders(sig_tbl, val="none")

# Left: Faculty Guide
c_left = sig_tbl.rows[0].cells[0]
c_left.width = Inches(3.2)
p_sl = c_left.paragraphs[0]
p_sl.paragraph_format.line_spacing = 1.15
r_sl = p_sl.add_run(
    "SIGNATURE\n"
    "[FACULTY COORDINATOR / ADVISOR]\n"
    "Assistant Professor / Coordinator\n"
    "Department of CSE\n"
    "B.S. Abdur Rahman Crescent\n"
    "Institute of Science and Technology\n"
    "Vandalur, Chennai – 600 048."
)
r_sl.font.name = 'Arial'
r_sl.font.size = Pt(11)
r_sl.font.bold = True

# Right: HOD
c_right = sig_tbl.rows[0].cells[1]
c_right.width = Inches(3.2)
p_sr = c_right.paragraphs[0]
p_sr.paragraph_format.line_spacing = 1.15
r_sr = p_sr.add_run(
    "SIGNATURE\n"
    "[HEAD OF THE DEPARTMENT]\n"
    "Professor and Head\n"
    "Department of CSE\n"
    "B.S. Abdur Rahman Crescent\n"
    "Institute of Science and Technology\n"
    "Vandalur, Chennai – 600 048."
)
r_sr.font.name = 'Arial'
r_sr.font.size = Pt(11)
r_sr.font.bold = True

doc.add_page_break()

# ===========================================================================
# 3. INTERNSHIP CERTIFICATE (Page ii) - EMBEDDED ORIGINAL SCAN
# ===========================================================================
add_heading_1(doc, "INTERNSHIP CERTIFICATE")

cert_scan_path = r'C:/Users/Ayaan/.gemini/antigravity/brain/1c37d6d5-00e3-4cf6-86a2-a2af67a7d12c/.user_uploaded/media_1795463364605_b089eca9.jpg'
if os.path.exists(cert_scan_path):
    p_cert_img = doc.add_paragraph()
    p_cert_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_img.paragraph_format.space_before = Pt(8)
    p_cert_img.paragraph_format.space_after = Pt(8)
    r_ci = p_cert_img.add_run()
    # 5.8 inches width fits standard 8.5x11 page with 1.25" and 1.0" margins
    r_ci.add_picture(cert_scan_path, width=Inches(5.6))
else:
    doc.add_paragraph("[Internship Certificate Image Not Found]")

doc.add_page_break()

# ===========================================================================
# 4. VIVA VOCE EXAMINATION (Page iii)
# ===========================================================================
if os.path.exists(logo_path):
    p_vl = doc.add_paragraph()
    p_vl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_vl.paragraph_format.space_after = Pt(12)
    p_vl.add_run().add_picture(logo_path, width=Inches(2.6))

add_heading_1(doc, "VIVA VOCE EXAMINATION")

p_viva = doc.add_paragraph()
p_viva.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_viva.paragraph_format.line_spacing = 1.25
p_viva.paragraph_format.space_before = Pt(24)
p_viva.paragraph_format.space_after = Pt(72)
r_v = p_viva.add_run(PRELIMINARIES["viva_voce"]["body"])
r_v.font.name = 'Arial'
r_v.font.size = Pt(12)

# Examiner signatures
viva_tbl = doc.add_table(rows=1, cols=2)
viva_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
viva_tbl.autofit = False
set_table_borders(viva_tbl, val="none")

c_ie = viva_tbl.rows[0].cells[0]
c_ie.width = Inches(3.2)
p_ie = c_ie.paragraphs[0]
r_ie = p_ie.add_run("_____________________\nINTERNAL EXAMINER")
r_ie.font.name = 'Arial'
r_ie.font.size = Pt(11)
r_ie.font.bold = True

c_ee = viva_tbl.rows[0].cells[1]
c_ee.width = Inches(3.2)
p_ee = c_ee.paragraphs[0]
p_ee.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r_ee = p_ee.add_run("_____________________\nEXTERNAL EXAMINER")
r_ee.font.name = 'Arial'
r_ee.font.size = Pt(11)
r_ee.font.bold = True

doc.add_page_break()

# ===========================================================================
# 5. ACKNOWLEDGEMENT (Page iv)
# ===========================================================================
add_heading_1(doc, "ACKNOWLEDGEMENT")

for para in PRELIMINARIES["acknowledgement"]:
    add_body_p(doc, para)

p_ack_sign = doc.add_paragraph()
p_ack_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_ack_sign.paragraph_format.space_before = Pt(20)
r_as = p_ack_sign.add_run(METADATA["student_name"])
r_as.font.name = 'Arial'
r_as.font.size = Pt(12)
r_as.font.bold = True

doc.add_page_break()

# ===========================================================================
# 6. TABLE OF CONTENTS (Pages v - vi)
# Note from Faculty annotation: Don't put numbers for upto abstract. Page no starts from chapter 1!
# ===========================================================================
add_heading_1(doc, "TABLE OF CONTENTS")

toc_items = [
    ("LIST OF ABBREVIATIONS", ""),
    ("LIST OF FIGURES", ""),
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
    ("    3.5 Existing Factory Tracking vs. Proposed System", "10"),
    ("    3.6 Summary of Core System Features", "10"),
    ("4. THEORETICAL ANALYSIS", "12"),
    ("    4.1 Introduction to Smart Manufacturing and Industry 4.0", "12"),
    ("    4.2 Industrial IoT and Machine Health Monitoring", "12"),
    ("    4.3 Core Telemetry Variables in Industrial Equipment", "13"),
    ("    4.4 Web Application Framework: Python 3.12 and Flask", "14"),
    ("    4.5 Relational Database Management: SQLite & WAL Mode", "14"),
    ("    4.6 RESTful API Design & Asynchronous Client Polling", "15"),
    ("    4.7 Dynamic Engineering Data Visualization: Chart.js", "15"),
    ("    4.8 Human-Machine Interface (HMI) & UI/UX Principles", "16"),
    ("    4.9 Chapter Summary", "16"),
    ("5. DESIGN AND IMPLEMENTATION", "17"),
    ("    5.1 System Architecture & Multi-Tier Topology", "17"),
    ("    5.2 Relational Database Schema Design (factory.db)", "18"),
    ("    5.3 Python Flask Backend & RESTful API Implementation", "19"),
    ("    5.4 Stochastic Asset Telemetry Simulator Engine", "21"),
    ("    5.5 Plant Availability Calculation Logic & Formula", "22"),
    ("    5.6 Machine Matrix & Slide-Out Inspector Drawer", "22"),
    ("    5.7 Alarm Lifecycle Management & Finite State Machine", "23"),
    ("    5.8 Equipment Maintenance & Downtime Tracking Module", "24"),
    ("    5.9 Simulated Shift Production & Scrap Rate Tracking", "24"),
    ("    5.10 Testing, Verification & Regression Test Suites", "25"),
    ("    5.11 Technical and Engineering Skills Acquired", "25"),
    ("6. RESULT AND ANALYSIS", "26"),
    ("    6.1 Comprehensive Operational Results Summary", "26"),
    ("    6.2 Machine Availability & Fleet Operational Analysis", "27"),
    ("    6.3 Asset Telemetry & Sensor Consistency Analysis", "27"),
    ("    6.4 Machine Operating State Distribution (Andon Timeline)", "29"),
    ("    6.5 Departmental Production Output & Scrap Rate Analysis", "30"),
    ("    6.6 Maintenance History & Equipment Downtime Evaluation", "31"),
    ("    6.7 Alarm Response & Exception Handling Analysis", "33"),
    ("    6.8 Analysis of System Architecture and Performance", "34"),
    ("    6.9 Dashboard Screenshots and Operational Walkthrough", "36"),
    ("        6.9.1 Plant Overview Console (Fig 6.9)", "36"),
    ("        6.9.2 Oscilloscope Charts & Spindle Profile (Fig 6.10)", "37"),
    ("        6.9.3 Equipment Telemetry Matrix (Fig 6.11)", "37"),
    ("        6.9.4 Equipment Side Inspector Drawer (Fig 6.12)", "38"),
    ("        6.9.5 Alarms & Fault Event Management Console (Fig 6.13)", "39"),
    ("        6.9.6 Chronological Telemetry Stream Audit Log (Fig 6.14)", "39"),
    ("        6.9.7 Equipment Maintenance & Downtime Tracker (Fig 6.15)", "40"),
    ("        6.9.8 Record Maintenance Modal Dialog (Fig 6.16)", "41"),
    ("    6.10 Comprehensive System Verification Matrix", "41"),
    ("    6.11 Technical Limitations and Academic Observations", "42"),
    ("7. CONCLUSION AND FUTURE SCOPE", "44"),
    ("    7.1 Conclusion", "44"),
    ("    7.2 Synthesis of Observation and Software Engineering", "44"),
    ("    7.3 Future Technical Scope and Scalability", "44"),
    ("8. REFERENCES", "46"),
    ("9. APPENDIX", "47"),
    ("    9.1 Core Application Source Code", "47"),
    ("    9.2 Database Schema DDL", "49"),
    ("    9.3 REST API Endpoints Specification", "50"),
    ("    9.4 Technical Bibliography & Standards Reference", "50")
]

toc_tbl = doc.add_table(rows=len(toc_items) + 1, cols=2)
toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
toc_tbl.autofit = False
set_table_borders(toc_tbl, val="none")

# Header
th = toc_tbl.rows[0]
th.cells[0].width = Inches(5.2)
th.cells[1].width = Inches(1.2)
p_th0 = th.cells[0].paragraphs[0]
r_th0 = p_th0.add_run("CHAPTER / SECTION TITLE")
r_th0.font.bold = True
r_th0.font.size = Pt(11)
r_th0.font.color.rgb = COLOR_NAVY

p_th1 = th.cells[1].paragraphs[0]
p_th1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r_th1 = p_th1.add_run("PAGE NO.")
r_th1.font.bold = True
r_th1.font.size = Pt(11)
r_th1.font.color.rgb = COLOR_NAVY

for i, (title, pg) in enumerate(toc_items):
    row = toc_tbl.rows[i + 1]
    c0 = row.cells[0]
    c1 = row.cells[1]
    c0.width = Inches(5.2)
    c1.width = Inches(1.2)
    
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    p0.paragraph_format.line_spacing = 1.05
    r0 = p0.add_run(title)
    r0.font.name = 'Arial'
    r0.font.size = Pt(10.5)
    if title.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', 'LIST', 'ABSTRACT')):
        r0.font.bold = True
    
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_after = Pt(2)
    p1.paragraph_format.line_spacing = 1.05
    r1 = p1.add_run(str(pg))
    r1.font.name = 'Arial'
    r1.font.size = Pt(10.5)
    if pg:
        r1.font.bold = True

doc.add_page_break()

# ===========================================================================
# 7. LIST OF ABBREVIATIONS (Page vii)
# ===========================================================================
add_heading_1(doc, "LIST OF ABBREVIATIONS")

abbr_tbl = doc.add_table(rows=len(PRELIMINARIES["abbreviations"]) + 1, cols=2)
abbr_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
abbr_tbl.autofit = False
set_table_borders(abbr_tbl, color="CBD5E1", sz="4", val="single")

hdr = abbr_tbl.rows[0]
hdr.cells[0].width = Inches(1.8)
hdr.cells[1].width = Inches(4.6)
set_cell_shading(hdr.cells[0], HEX_NAVY)
set_cell_shading(hdr.cells[1], HEX_NAVY)

r_h0 = hdr.cells[0].paragraphs[0].add_run("ABBREVIATION")
r_h0.font.bold = True
r_h0.font.size = Pt(10)
r_h0.font.color.rgb = RGBColor(255, 255, 255)

r_h1 = hdr.cells[1].paragraphs[0].add_run("EXPANDED TECHNICAL DESIGNATION")
r_h1.font.bold = True
r_h1.font.size = Pt(10)
r_h1.font.color.rgb = RGBColor(255, 255, 255)

for i, (ab, full) in enumerate(PRELIMINARIES["abbreviations"]):
    row = abbr_tbl.rows[i + 1]
    row.cells[0].width = Inches(1.8)
    row.cells[1].width = Inches(4.6)
    if i % 2 == 1:
        set_cell_shading(row.cells[0], HEX_LIGHT_BG)
        set_cell_shading(row.cells[1], HEX_LIGHT_BG)
    set_cell_margins(row.cells[0], top=80, bottom=80, left=120, right=120)
    set_cell_margins(row.cells[1], top=80, bottom=80, left=120, right=120)
    
    p0 = row.cells[0].paragraphs[0]
    p0.paragraph_format.space_after = Pt(0)
    r0 = p0.add_run(ab)
    r0.font.name = 'Consolas'
    r0.font.bold = True
    r0.font.size = Pt(10)
    
    p1 = row.cells[1].paragraphs[0]
    p1.paragraph_format.space_after = Pt(0)
    r1 = p1.add_run(full)
    r1.font.name = 'Arial'
    r1.font.size = Pt(10)

doc.add_page_break()

# ===========================================================================
# 8. LIST OF FIGURES & LIST OF TABLES (Pages viii - ix)
# ===========================================================================
add_heading_1(doc, "LIST OF FIGURES")

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

fig_tbl = doc.add_table(rows=len(figures_list) + 1, cols=3)
fig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
fig_tbl.autofit = False
set_table_borders(fig_tbl, val="none")

fh = fig_tbl.rows[0]
fh.cells[0].width = Inches(1.2)
fh.cells[1].width = Inches(4.2)
fh.cells[2].width = Inches(1.0)
fh.cells[0].paragraphs[0].add_run("FIGURE NO.").font.bold = True
fh.cells[1].paragraphs[0].add_run("TITLE").font.bold = True
p_fhp = fh.cells[2].paragraphs[0]
p_fhp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_fhp.add_run("PAGE NO.").font.bold = True

for i, (fnum, ftitle, fpage) in enumerate(figures_list):
    r = fig_tbl.rows[i + 1]
    r.cells[0].width = Inches(1.2)
    r.cells[1].width = Inches(4.2)
    r.cells[2].width = Inches(1.0)
    
    p0 = r.cells[0].paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    p0.add_run(f"Fig {fnum}").font.bold = True
    
    p1 = r.cells[1].paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    p1.add_run(ftitle)
    
    p2 = r.cells[2].paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.paragraph_format.space_after = Pt(2)
    p2.add_run(fpage).font.bold = True

doc.add_paragraph().paragraph_format.space_before = Pt(16)
add_heading_1(doc, "LIST OF TABLES")

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

tbl_list_tbl = doc.add_table(rows=len(tables_list) + 1, cols=3)
tbl_list_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_list_tbl.autofit = False
set_table_borders(tbl_list_tbl, val="none")

th = tbl_list_tbl.rows[0]
th.cells[0].width = Inches(1.2)
th.cells[1].width = Inches(4.2)
th.cells[2].width = Inches(1.0)
th.cells[0].paragraphs[0].add_run("TABLE NO.").font.bold = True
th.cells[1].paragraphs[0].add_run("TITLE").font.bold = True
p_thp = th.cells[2].paragraphs[0]
p_thp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_thp.add_run("PAGE NO.").font.bold = True

for i, (tnum, ttitle, tpage) in enumerate(tables_list):
    r = tbl_list_tbl.rows[i + 1]
    r.cells[0].width = Inches(1.2)
    r.cells[1].width = Inches(4.2)
    r.cells[2].width = Inches(1.0)
    
    p0 = r.cells[0].paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    p0.add_run(f"Table {tnum}").font.bold = True
    
    p1 = r.cells[1].paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    p1.add_run(ttitle)
    
    p2 = r.cells[2].paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.paragraph_format.space_after = Pt(2)
    p2.add_run(tpage).font.bold = True

doc.add_page_break()

# ===========================================================================
# 9. ABSTRACT (Page x)
# ===========================================================================
add_heading_1(doc, "ABSTRACT")

for para in PRELIMINARIES["abstract"]:
    add_body_p(doc, para)

# ===========================================================================
# SECTION BREAK -> START OF CHAPTER 1 (PAGE 1)
# ===========================================================================
# Add Section Break
new_sec = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
new_sec.top_margin = Inches(1.0)
new_sec.bottom_margin = Inches(1.0)
new_sec.left_margin = Inches(1.25)
new_sec.right_margin = Inches(1.0)

# Unlink Header and Footer
new_sec.header.is_linked_to_previous = False
new_sec.footer.is_linked_to_previous = False

# Restart Page Numbering at 1
sectPr = new_sec._sectPr
pgNumType = OxmlElement('w:pgNumType')
pgNumType.set(qn('w:start'), '1')
sectPr.append(pgNumType)

# Add Center-Aligned Page Number in Footer of Section 2
f_p = new_sec.footer.paragraphs[0]
f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
f_run = f_p.add_run()
f_run.font.name = 'Arial'
f_run.font.size = Pt(10)
f_run.font.color.rgb = COLOR_TEXT
add_page_number_field(f_run)

# ===========================================================================
# CHAPTER 1: COMPANY OVERVIEW
# ===========================================================================
add_heading_1(doc, "CHAPTER 1\nCOMPANY OVERVIEW")

# Add Komatsu Logo
add_figure(doc, 'report_assets/komatsu_logo.png', "Fig 1.1 – Komatsu Corporate Logo & Industrial Brand Identity", width_inches=4.2)

for sec in CHAPTER_1["sections"]:
    add_heading_2(doc, f"{sec['num']} {sec['title']}")
    for p_txt in sec["paragraphs"]:
        add_body_p(doc, p_txt)

doc.add_page_break()

# ===========================================================================
# CHAPTER 2: ROLE AND RESPONSIBILITIES
# ===========================================================================
add_heading_1(doc, "CHAPTER 2\nROLE AND RESPONSIBILITIES")

for sec in CHAPTER_2["sections"]:
    add_heading_2(doc, f"{sec['num']} {sec['title']}")
    for p_txt in sec["paragraphs"]:
        add_body_p(doc, p_txt)
    
    if "table" in sec:
        add_table(doc, sec["table"])
    
    if "subsections" in sec:
        for sub in sec["subsections"]:
            add_heading_3(doc, f"{sub['num']} {sub['title']}")
            for sub_p in sub["paragraphs"]:
                add_body_p(doc, sub_p)

doc.add_page_break()

# ===========================================================================
# CHAPTER 3: PROJECT OVERVIEW
# ===========================================================================
add_heading_1(doc, "CHAPTER 3\nPROJECT OVERVIEW")

for sec in CHAPTER_3["sections"]:
    add_heading_2(doc, f"{sec['num']} {sec['title']}")
    for p_txt in sec["paragraphs"]:
        add_body_p(doc, p_txt)
    
    if "bullets" in sec:
        for prefix, txt in sec["bullets"]:
            add_bullet_p(doc, prefix, txt)
    
    if "table" in sec:
        add_table(doc, sec["table"])

doc.add_page_break()

# ===========================================================================
# CHAPTER 4: THEORETICAL ANALYSIS
# ===========================================================================
add_heading_1(doc, "CHAPTER 4\nTHEORETICAL ANALYSIS")

for sec in CHAPTER_4["sections"]:
    add_heading_2(doc, f"{sec['num']} {sec['title']}")
    for p_txt in sec["paragraphs"]:
        add_body_p(doc, p_txt)
    
    if "table" in sec:
        add_table(doc, sec["table"])

doc.add_page_break()

# ===========================================================================
# CHAPTER 5: DESIGN AND IMPLEMENTATION
# ===========================================================================
add_heading_1(doc, "CHAPTER 5\nDESIGN AND IMPLEMENTATION")

for sec in CHAPTER_5["sections"]:
    add_heading_2(doc, f"{sec['num']} {sec['title']}")
    for p_txt in sec["paragraphs"]:
        add_body_p(doc, p_txt)
    
    if "figure" in sec:
        add_figure(doc, sec["figure"]["path"], sec["figure"]["caption"], sec["figure"]["width"])
    
    if "table" in sec:
        add_table(doc, sec["table"])
    
    if "subsections" in sec:
        for sub in sec["subsections"]:
            add_heading_3(doc, f"{sub['num']} {sub['title']}")
            for sub_p in sub["paragraphs"]:
                add_body_p(doc, sub_p)
                
    if "bullets" in sec:
        for prefix, txt in sec["bullets"]:
            add_bullet_p(doc, prefix, txt)

doc.add_page_break()

# ===========================================================================
# CHAPTER 6: RESULT AND ANALYSIS
# ===========================================================================
add_heading_1(doc, "CHAPTER 6\nRESULT AND ANALYSIS")

fig_map_docx = {
    "6.2": ("report_assets/fig6_1_availability_trend.png", "Fig 6.1 – Fleet Operational Availability & Active Machine Count (24-Hour Profile)"),
    "6.3": ("report_assets/fig6_2_sensor_correlation.png", "Fig 6.2 – Sensor Correlation: Operating Temperature vs. Vibration Velocity"),
    "6.4": ("report_assets/fig6_4_production_output.png", "Fig 6.4 – Departmental Production Output vs. Target Deficit (Shift Analysis)"),
    "6.5": ("report_assets/fig6_6_downtime_pareto.png", "Fig 6.6 – Equipment Downtime Pareto Analysis by Maintenance Category (80/20 Rule)"),
    "6.6": ("report_assets/fig6_7_andon_timeline.png", "Fig 6.7 – Shift-Wise Machine Operating State Timeline (Real-Time Andon Sequence)"),
    "6.7": ("report_assets/fig6_8_telemetry_stream.png", "Fig 6.8 – Sensor Telemetry Frequency Distribution Across Production Shift")
}

for sec in CHAPTER_6["sections"]:
    s_num = sec['num']
    add_heading_2(doc, f"{s_num} {sec['title']}")
    for p_txt in sec["paragraphs"]:
        add_body_p(doc, p_txt)
        
    if s_num in fig_map_docx:
        f_p, f_c = fig_map_docx[s_num]
        add_figure(doc, f_p, f_c, width_inches=5.8)
        if s_num == "6.3":
            add_figure(doc, 'report_assets/fig6_3_spindle_velocity.png', "Fig 6.3 – Spindle Velocity Profile Across Monitored Fleet (Zero RPM for IDLE Machinery)", width_inches=5.8)
        elif s_num == "6.4":
            add_figure(doc, 'report_assets/fig6_5_scrap_rate.png', "Fig 6.5 – Quality Inspection Scrap & Reject Rate Distribution by Manufacturing Division", width_inches=5.8)
    
    if "table" in sec:
        add_table(doc, sec["table"])
    
    if "subsections" in sec:
        for sub in sec["subsections"]:
            add_heading_3(doc, f"{sub['num']} {sub['title']}")
            for sub_p in sub["paragraphs"]:
                add_body_p(doc, sub_p)
                
    if "walkthrough" in sec:
        for item in sec["walkthrough"]:
            add_heading_3(doc, f"{item['num']} {item['title']}")
            add_figure(doc, item["figure"]["path"], item["figure"]["caption"], item["figure"]["width"])
            add_body_p(doc, item["text"])
            
    if "bullets" in sec:
        for prefix, txt in sec["bullets"]:
            add_bullet_p(doc, prefix, txt)

doc.add_page_break()

# ===========================================================================
# CHAPTER 7: CONCLUSION AND FUTURE SCOPE
# ===========================================================================
add_heading_1(doc, "CHAPTER 7\nCONCLUSION AND FUTURE SCOPE")

for sec in CHAPTER_7["sections"]:
    add_heading_2(doc, f"{sec['num']} {sec['title']}")
    for p_txt in sec["paragraphs"]:
        add_body_p(doc, p_txt)
    
    if "bullets" in sec:
        for prefix, txt in sec["bullets"]:
            add_bullet_p(doc, prefix, txt)

doc.add_page_break()

# ===========================================================================
# CHAPTER 8: REFERENCES
# ===========================================================================
add_heading_1(doc, "CHAPTER 8\nREFERENCES")

for i, ref_item in enumerate(CHAPTER_8["references"]):
    p_ref = doc.add_paragraph()
    p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ref.paragraph_format.line_spacing = 1.15
    p_ref.paragraph_format.space_after = Pt(6)
    p_ref.paragraph_format.left_indent = Inches(0.4)
    p_ref.paragraph_format.first_line_indent = Inches(-0.4)
    
    r_num = p_ref.add_run(f"[{i+1}] ")
    r_num.font.name = 'Arial'
    r_num.font.size = Pt(11)
    r_num.font.bold = True
    r_num.font.color.rgb = COLOR_NAVY
    
    r_txt = p_ref.add_run(ref_item)
    r_txt.font.name = 'Arial'
    r_txt.font.size = Pt(11)

doc.add_page_break()

# ===========================================================================
# CHAPTER 9: APPENDIX
# ===========================================================================
add_heading_1(doc, "CHAPTER 9\nAPPENDIX")

for sec in CHAPTER_9["sections"]:
    add_heading_2(doc, f"{sec['num']} {sec['title']}")
    if "paragraphs" in sec:
        for p_txt in sec["paragraphs"]:
            add_body_p(doc, p_txt)
    
    if "snippets" in sec:
        for snip in sec["snippets"]:
            add_code_snippet(doc, snip["title"], snip["code"])
            
    if "bullets" in sec:
        for prefix, txt in sec["bullets"]:
            add_bullet_p(doc, prefix, txt)

# Save the complete Word document
doc.save(OUTPUT_DOCX)
print(f"Document saved successfully as: {OUTPUT_DOCX}")
