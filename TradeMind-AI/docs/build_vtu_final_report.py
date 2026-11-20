import os
import re
import shutil
import subprocess
import markdown
import docx
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(DOCS_DIR)
FRONTEND_PUBLIC = os.path.join(PROJECT_ROOT, "frontend", "public")
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
FIGURES_DIR = os.path.join(DOCS_DIR, "figures")

MD_PATH = os.path.join(DOCS_DIR, "PROJECT_REPORT_VTU_7_CHAPTERS.md")
DOCX_OUT = os.path.join(DOCS_DIR, "PROJECT_REPORT_VTU_FINAL.docx")
HTML_FULL_OUT = os.path.join(DOCS_DIR, "report_vtu_full.html")
PDF_FULL_OUT = os.path.join(DOCS_DIR, "PROJECT_REPORT_VTU_FINAL.pdf")
HTML_PLAG_OUT = os.path.join(DOCS_DIR, "report_vtu_plagiarism.html")
PDF_PLAG_OUT = os.path.join(DOCS_DIR, "PLAGIARISM_CHECK_CHAPTERS_1_TO_7.pdf")

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_borders(cell, color="000000", sz="4", val="single"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

def add_page_number(run):
    fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    run._r.append(fldSimple)

def parse_inline_formatting(paragraph, text):
    token_pattern = re.compile(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)')
    parts = token_pattern.split(text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) >= 4:
            run = paragraph.add_run(part[2:-2])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.font.bold = True
        elif part.startswith("*") and part.endswith("*") and len(part) >= 2:
            run = paragraph.add_run(part[1:-1])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.font.italic = True
        elif part.startswith("`") and part.endswith("`") and len(part) >= 2:
            run = paragraph.add_run(part[1:-1])
            run.font.name = 'Courier New'
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        else:
            run = paragraph.add_run(part)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)

# ==========================================
# 1. BUILD MICROSOFT WORD (.DOCX) REPORT
# ==========================================
def build_docx_report():
    print("Building VTU 7-Chapter Word Document (.docx)...")
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = docx.Document()
    sec = doc.sections[0]
    sec.page_width = Mm(210)
    sec.page_height = Mm(297)
    sec.left_margin = Mm(31)
    sec.right_margin = Mm(25)
    sec.top_margin = Mm(20)
    sec.bottom_margin = Mm(20)

    # Double Border on Pages (matching reference report)
    sectPr = sec._sectPr
    pgBorders = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
        f'<w:top w:val="double" w:sz="12" w:space="24" w:color="000000"/>'
        f'<w:left w:val="double" w:sz="12" w:space="24" w:color="000000"/>'
        f'<w:bottom w:val="double" w:sz="12" w:space="24" w:color="000000"/>'
        f'<w:right w:val="double" w:sz="12" w:space="24" w:color="000000"/>'
        f'</w:pgBorders>'
    )
    sectPr.append(pgBorders)

    # Header: Project Title (with horizontal rule)
    hdr = sec.header
    hdr_p = hdr.paragraphs[0]
    hdr_p.text = ""
    r_hdr = hdr_p.add_run("Intelligent Trading Bot with Real-Time Market Data Analysis")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.size = Pt(9)
    r_hdr.font.italic = True
    r_hdr.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
    # Add bottom border to header paragraph
    pPr = hdr_p._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="1" w:color="000000"/></w:pBdr>')
    pPr.append(pBdr)

    # Footer: Dept. of ISE, SVIT | 2026-27 | Page N
    ftr = sec.footer
    ftr_p = ftr.paragraphs[0]
    ftr_p.text = ""
    r_ftr_l = ftr_p.add_run("Dept. of ISE, SVIT")
    r_ftr_l.font.name = "Times New Roman"
    r_ftr_l.font.size = Pt(9)
    r_ftr_l.font.bold = True
    r_ftr_l.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    r_ftr_c = ftr_p.add_run("\t2026-27\tPage ")
    r_ftr_c.font.name = "Times New Roman"
    r_ftr_c.font.size = Pt(9)
    r_ftr_c.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    add_page_number(r_ftr_c)

    pPr_f = ftr_p._p.get_or_add_pPr()
    pBdr_f = parse_xml(f'<w:pBdr {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="1" w:color="000000"/></w:pBdr>')
    pPr_f.append(pBdr_f)

    # Base Normal Style
    norm = doc.styles['Normal']
    norm.font.name = 'Times New Roman'
    norm.font.size = Pt(12)
    norm.paragraph_format.line_spacing = 1.5
    norm.paragraph_format.space_after = Pt(6)
    norm.paragraph_format.space_before = Pt(0)
    norm.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    lines = md_text.splitlines()
    i = 0
    in_code = False
    code_lines = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Page Breaks
        if '<div style="page-break-after: always;"></div>' in line or '<div class="page-break"></div>' in line:
            doc.add_page_break()
            i += 1
            continue

        # Code Blocks
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(8)
                p.paragraph_format.line_spacing = 1.15
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = p.add_run("\n".join(code_lines))
                run.font.name = 'Courier New'
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Image Embeds: ![Caption](path) or <img src="..." />
        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)', stripped)
        html_img_match = re.match(r'^<img src=\"(.*?)\".*?width=\"(\d+)\"', stripped)

        if img_match:
            caption = img_match.group(1).strip()
            rel_p = img_match.group(2).strip()
            full_p = os.path.normpath(os.path.join(DOCS_DIR, rel_p))

            if os.path.exists(full_p):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(10)
                p_img.paragraph_format.space_after = Pt(4)
                p_img.paragraph_format.keep_with_next = True
                run_img = p_img.add_run()
                run_img.add_picture(full_p, width=Inches(5.7))

                p_cap = doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cap.paragraph_format.space_before = Pt(2)
                p_cap.paragraph_format.space_after = Pt(12)
                run_cap = p_cap.add_run(caption)
                run_cap.font.name = 'Times New Roman'
                run_cap.font.size = Pt(10)
                run_cap.font.italic = True
                run_cap.font.bold = True
                run_cap.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

            i += 1
            if i < len(lines) and ("Figure " in lines[i] or "<b>Figure" in lines[i]):
                i += 1
            continue

        if html_img_match:
            src = html_img_match.group(1).strip()
            w_px = int(html_img_match.group(2).strip())
            full_p = os.path.normpath(os.path.join(DOCS_DIR, src))
            if os.path.exists(full_p):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(6)
                p_img.paragraph_format.space_after = Pt(6)
                run_img = p_img.add_run()
                width_in = Inches(w_px / 100.0 * 1.5)
                run_img.add_picture(full_p, width=width_in)
            i += 1
            continue

        if re.match(r'^<div align="center"><b>Figure\s+.*?</div>$', stripped):
            i += 1
            continue

        # Markdown Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i].strip())
                i += 1

            rows_data = []
            for tl in table_lines:
                if re.match(r'^\|[\s\:\-\|]+$', tl):
                    continue
                cells = [c.strip() for c in tl.strip('|').split('|')]
                rows_data.append(cells)

            if rows_data:
                num_cols = max(len(r) for r in rows_data)
                table = doc.add_table(rows=len(rows_data), cols=num_cols)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                table.autofit = True

                for r_idx, r_data in enumerate(rows_data):
                    is_hdr = (r_idx == 0)
                    for c_idx in range(num_cols):
                        cell = table.cell(r_idx, c_idx)
                        text_val = r_data[c_idx] if c_idx < len(r_data) else ""
                        clean_text = text_val.replace("**", "").replace("*", "").replace("🟢", "").replace("🔴", "").replace("🟡", "")
                        cell.text = clean_text
                        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
                        set_cell_borders(cell, color="000000", sz="4")

                        p = cell.paragraphs[0]
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.space_after = Pt(2)
                        p.paragraph_format.line_spacing = 1.15

                        if is_hdr:
                            set_cell_background(cell, "F1F5F9")
                            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            for r in p.runs:
                                r.font.name = 'Times New Roman'
                                r.font.size = Pt(10)
                                r.font.bold = True
                        else:
                            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                            for r in p.runs:
                                r.font.name = 'Times New Roman'
                                r.font.size = Pt(9.5)
                p_spacer = doc.add_paragraph()
                p_spacer.paragraph_format.space_before = Pt(0)
                p_spacer.paragraph_format.space_after = Pt(4)
            continue

        # Headings
        if stripped.startswith("#"):
            match = re.match(r'^(#{1,6})\s+(.*)', stripped)
            if match:
                level = len(match.group(1))
                h_text = match.group(2).strip()
                clean_h = h_text.replace("**", "").replace("*", "").replace("“", '"').replace("”", '"')

                # Auto page breaks before chapters
                if clean_h.startswith("CHAPTER ") or clean_h in ["REFERENCES", "ABSTRACT", "ACKNOWLEDGEMENT", "Table of Contents", "List of Figures", "List of Tables"]:
                    doc.add_page_break()

                p = doc.add_paragraph()
                p.paragraph_format.keep_with_next = True
                run = p.add_run(clean_h)
                run.font.name = 'Times New Roman'
                run.font.bold = True

                if level == 1:
                    run.font.size = Pt(15)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ("CHAPTER" in clean_h or "VISVESVARAYA" in clean_h or "SAI VIDYA" in clean_h or clean_h in ["REFERENCES", "ABSTRACT", "ACKNOWLEDGEMENT", "Table of Contents", "List of Figures", "List of Tables"]) else WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_before = Pt(14)
                    p.paragraph_format.space_after = Pt(8)
                elif level == 2:
                    run.font.size = Pt(13)
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_before = Pt(12)
                    p.paragraph_format.space_after = Pt(5)
                elif level == 3:
                    run.font.size = Pt(12)
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_before = Pt(10)
                    p.paragraph_format.space_after = Pt(3)
                else:
                    run.font.size = Pt(11.5)
                    run.font.italic = True
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_before = Pt(8)
                    p.paragraph_format.space_after = Pt(2)

                i += 1
                continue

        if stripped in ["---", "***", "___"]:
            i += 1
            continue

        if not stripped or stripped in ["<br>", "<br/>", "<br><br>", "<br><br><br>"]:
            i += 1
            continue

        if stripped.startswith("<div") or stripped == "</div>":
            i += 1
            continue

        # Regular Paragraph
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.space_before = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        if stripped.startswith("- ") or stripped.startswith("* ") or stripped.startswith("• "):
            p.paragraph_format.left_indent = Inches(0.25)
            content = stripped[2:].strip()
            run_bullet = p.add_run("• ")
            run_bullet.font.bold = True
            parse_inline_formatting(p, content)
        elif re.match(r'^\d+\.\s+', stripped):
            match_num = re.match(r'^(\d+\.)\s+(.*)', stripped)
            p.paragraph_format.left_indent = Inches(0.25)
            run_num = p.add_run(f"{match_num.group(1)} ")
            run_num.font.bold = True
            parse_inline_formatting(p, match_num.group(2))
        else:
            parse_inline_formatting(p, stripped)

        i += 1

    doc.save(DOCX_OUT)
    print(f"SUCCESS: Saved {DOCX_OUT} ({os.path.getsize(DOCX_OUT):,} bytes)")

    # Copy to Downloads and Public folder
    shutil.copyfile(DOCX_OUT, os.path.join(DOWNLOADS_DIR, "PROJECT_REPORT_VTU_FINAL.docx"))
    shutil.copyfile(DOCX_OUT, os.path.join(FRONTEND_PUBLIC, "PROJECT_REPORT_VTU_FINAL.docx"))
    print("Copied DOCX to Downloads and Frontend Public directory.")

# ==========================================
# 2. BUILD PRINT-READY PDF REPORT VIA CHROME
# ==========================================
REPORT_CSS = """
@page {
    size: A4 portrait;
    margin-left: 20mm;
    margin-right: 20mm;
    margin-top: 20mm;
    margin-bottom: 20mm;
    
    @top-left {
        content: "Intelligent Trading Bot with Real-Time Market Data Analysis";
        font-family: 'Times New Roman', Times, serif;
        font-size: 8.5pt;
        color: #0f172a;
        font-style: italic;
        border-bottom: 1pt solid #000000;
        padding-bottom: 3pt;
    }
    @bottom-left {
        content: "Dept. of ISE, SVIT";
        font-family: 'Times New Roman', Times, serif;
        font-size: 8.5pt;
        color: #0f172a;
        font-weight: bold;
        border-top: 1pt solid #000000;
        padding-top: 3pt;
    }
    @bottom-center {
        content: "2026-27";
        font-family: 'Times New Roman', Times, serif;
        font-size: 8.5pt;
        color: #0f172a;
        border-top: 1pt solid #000000;
        padding-top: 3pt;
    }
    @bottom-right {
        content: "Page " counter(page);
        font-family: 'Times New Roman', Times, serif;
        font-size: 8.5pt;
        color: #0f172a;
        border-top: 1pt solid #000000;
        padding-top: 3pt;
    }
}

*, *:before, *:after {
    box-sizing: border-box;
}

body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000000;
    text-align: justify;
    text-justify: inter-word;
    margin: 0;
    padding: 0;
    background: #ffffff;
}

p {
    margin-top: 0;
    margin-bottom: 10pt;
    text-align: justify;
}

h1 {
    font-size: 15pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    margin-top: 16pt;
    margin-bottom: 10pt;
    page-break-after: avoid;
}

h2 {
    font-size: 13pt;
    font-weight: bold;
    margin-top: 14pt;
    margin-bottom: 6pt;
    page-break-after: avoid;
}

h3 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 10pt;
    margin-bottom: 4pt;
    page-break-after: avoid;
}

h4 {
    font-size: 11.5pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 8pt;
    margin-bottom: 3pt;
    page-break-after: avoid;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10pt;
    margin-bottom: 14pt;
    font-size: 10pt;
    line-height: 1.25;
    page-break-inside: avoid;
}

th, td {
    border: 1px solid #000000;
    padding: 5pt 7pt;
    vertical-align: top;
    text-align: left;
}

th {
    background-color: #f1f5f9;
    font-weight: bold;
    text-align: center;
}

img {
    display: block;
    max-width: 90%;
    max-height: 5.2in;
    height: auto;
    margin: 10pt auto 4pt auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    page-break-inside: avoid;
}

.page-break {
    page-break-after: always;
    break-after: page;
}
"""

def build_pdf_reports():
    print("Building VTU 7-Chapter PDF Reports via Headless Chrome...")
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Pre-process image paths to absolute URIs for headless Chrome
    def fix_img_src(match):
        alt = match.group(1)
        rel_path = match.group(2)
        full_p = os.path.normpath(os.path.join(DOCS_DIR, rel_path))
        uri = "file:///" + full_p.replace(os.sep, "/")
        return f'![{alt}]({uri})'

    md_formatted = re.sub(r'!\[(.*?)\]\((figures/.*?)\)', fix_img_src, md_text)
    md_formatted = re.sub(r'<img src=\"figures/(.*?)\"', lambda m: f'<img src="file:///{os.path.normpath(os.path.join(DOCS_DIR, "figures", m.group(1))).replace(os.sep, "/")}"', md_formatted)
    md_formatted = md_formatted.replace('<div style="page-break-after: always;"></div>', '<div class="page-break"></div>')

    # Convert to HTML
    md_extensions = ['tables', 'fenced_code', 'codehilite', 'sane_lists']
    html_body = markdown.markdown(md_formatted, extensions=md_extensions)

    # Insert page breaks before chapters
    for ch_num in range(1, 8):
        h1_tag = f"<h1>CHAPTER {ch_num}"
        html_body = html_body.replace(h1_tag, f'<div class="page-break"></div>\n{h1_tag}')
    html_body = html_body.replace("<h1>REFERENCES", '<div class="page-break"></div>\n<h1>REFERENCES')

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Intelligent Trading Bot with Real-Time Market Data Analysis - Project Report</title>
    <style>{REPORT_CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    with open(HTML_FULL_OUT, "w", encoding="utf-8") as f:
        f.write(full_html)

    # Plagiarism check HTML: Chapters 1 to 7 only
    ch1_idx = md_text.find("# CHAPTER 1")
    ref_idx = md_text.find("# REFERENCES")
    if ch1_idx != -1 and ref_idx != -1:
        plag_body_md = md_text[ch1_idx:ref_idx].strip()
        plag_header = """# Intelligent Trading Bot with Real-Time Market Data Analysis
### Major Project Phase II (BIS786) Report – Chapters 1 to 7 (Plagiarism Verification Scope)
**Candidates:** Athish Advi K.N (1VA23IS013), Suhas K.L (1VA23IS106), Yashwanth Gowda H (1VA23IS122), Yashwanth M (1VA23IS122)  
**Guide:** Prof. Divyamani M.K, Assistant Professor, Dept. of ISE, SVIT  
**Institution:** Sai Vidya Institute of Technology, Rajanukunte, Bengaluru - 560 064 (VTU Belagavi)  
**Academic Year:** 2026-27

---

"""
        plag_md_full = plag_header + plag_body_md
        plag_md_formatted = re.sub(r'!\[(.*?)\]\((figures/.*?)\)', fix_img_src, plag_md_full)
        plag_html_body = markdown.markdown(plag_md_formatted, extensions=md_extensions)
        for ch_num in range(1, 8):
            h1_tag = f"<h1>CHAPTER {ch_num}"
            plag_html_body = plag_html_body.replace(h1_tag, f'<div class="page-break"></div>\n{h1_tag}')

        plag_full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Plagiarism Verification File (Chapters 1-7)</title>
    <style>{REPORT_CSS}</style>
</head>
<body>
{plag_html_body}
</body>
</html>"""
        with open(HTML_PLAG_OUT, "w", encoding="utf-8") as f:
            f.write(plag_full_html)

    # Compile using Headless Chrome
    def compile_pdf(html_file, pdf_file):
        html_uri = f"file:///{os.path.abspath(html_file).replace(os.sep, '/')}"
        pdf_abs = os.path.abspath(pdf_file)
        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            f"--print-to-pdf={pdf_abs}",
            html_uri
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(pdf_abs) and os.path.getsize(pdf_abs) > 1000:
            print(f"SUCCESS: Generated {pdf_abs} ({os.path.getsize(pdf_abs):,} bytes)")
            return True
        else:
            print(f"ERROR: {res.stderr}")
            return False

    success_full = compile_pdf(HTML_FULL_OUT, PDF_FULL_OUT)
    success_plag = compile_pdf(HTML_PLAG_OUT, PDF_PLAG_OUT)

    if success_full:
        shutil.copyfile(PDF_FULL_OUT, os.path.join(DOWNLOADS_DIR, "PROJECT_REPORT_VTU_FINAL.pdf"))
        shutil.copyfile(PDF_FULL_OUT, os.path.join(FRONTEND_PUBLIC, "PROJECT_REPORT_VTU_FINAL.pdf"))
        print("Copied Full PDF to Downloads and Frontend Public.")

    if success_plag:
        shutil.copyfile(PDF_PLAG_OUT, os.path.join(DOWNLOADS_DIR, "PLAGIARISM_CHECK_CHAPTERS_1_TO_7.pdf"))
        shutil.copyfile(PDF_PLAG_OUT, os.path.join(FRONTEND_PUBLIC, "PLAGIARISM_CHECK_CHAPTERS_1_TO_7.pdf"))
        print("Copied Plagiarism PDF to Downloads and Frontend Public.")

if __name__ == "__main__":
    build_docx_report()
    build_pdf_reports()
    print("VTU Final Project Report generation complete!")
