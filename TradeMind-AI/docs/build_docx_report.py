import os
import re
import shutil
import docx
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(DOCS_DIR)
FRONTEND_PUBLIC = os.path.join(PROJECT_ROOT, "frontend", "public")
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

MD_PATH = os.path.join(DOCS_DIR, "FINAL_PROJECT_REPORT_BIS786.md")
DOCX_PATH = os.path.join(DOCS_DIR, "FINAL_PROJECT_REPORT_BIS786.docx")

def set_cell_background(cell, hex_color):
    """Set background shading for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set padding for a table cell in dxa (1 pt = 20 dxa)."""
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

def set_cell_borders(cell, color="475569", sz="4", val="single"):
    """Set borders for a cell."""
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
    """Insert a dynamic page number field into a run."""
    fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    run._r.append(fldSimple)

def generate_docx():
    print(f"Reading {MD_PATH}...")
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = docx.Document()

    # Configure A4 page size and SVIT margins:
    # Left = 31 mm (1.22 in), Right = 25 mm (0.98 in), Top = 20 mm (0.78 in), Bottom = 20 mm (0.78 in)
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.left_margin = Mm(31)
    section.right_margin = Mm(25)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)

    # Set up Header
    header = section.header
    header_p = header.paragraphs[0]
    header_p.text = ""
    run_h_left = header_p.add_run("BIS786")
    run_h_left.font.name = "Times New Roman"
    run_h_left.font.size = Pt(8.5)
    run_h_left.font.bold = True
    run_h_left.font.color.rgb = RGBColor(0x4b, 0x55, 0x63)
    
    # Tab to right
    run_h_right = header_p.add_run("\t\tMAJOR PROJECT PHASE-II")
    run_h_right.font.name = "Times New Roman"
    run_h_right.font.size = Pt(8.5)
    run_h_right.font.italic = True
    run_h_right.font.color.rgb = RGBColor(0x4b, 0x55, 0x63)

    # Set up Footer
    footer = section.footer
    footer_p = footer.paragraphs[0]
    footer_p.text = ""
    run_f_left = footer_p.add_run("Dept. of IS&E, SVIT")
    run_f_left.font.name = "Times New Roman"
    run_f_left.font.size = Pt(8.5)
    run_f_left.font.bold = True
    run_f_left.font.color.rgb = RGBColor(0x4b, 0x55, 0x63)

    run_f_tab = footer_p.add_run("\t\tPage ")
    run_f_tab.font.name = "Times New Roman"
    run_f_tab.font.size = Pt(8.5)
    run_f_tab.font.color.rgb = RGBColor(0x4b, 0x55, 0x63)
    add_page_number(run_f_tab)

    # Base Normal Style setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.space_before = Pt(0)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    lines = md_text.splitlines()
    i = 0
    in_code_block = False
    code_lines = []
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Handle page breaks
        if '<div style="page-break-after: always;"></div>' in line or '<div class="page-break"></div>' in line:
            doc.add_page_break()
            i += 1
            continue

        # Handle Code Blocks
        if stripped.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False
                code_content = "\n".join(code_lines)
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(8)
                p.paragraph_format.line_spacing = 1.15
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = p.add_run(code_content)
                run.font.name = 'Courier New'
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Handle Images & Flowchart Figures: ![Caption](path)
        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)', stripped)
        if img_match:
            caption = img_match.group(1).strip()
            img_rel_path = img_match.group(2).strip()
            img_full_path = os.path.normpath(os.path.join(DOCS_DIR, img_rel_path))

            if os.path.exists(img_full_path):
                # Add picture centered
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(10)
                p_img.paragraph_format.space_after = Pt(4)
                p_img.paragraph_format.keep_with_next = True
                
                run_img = p_img.add_run()
                run_img.add_picture(img_full_path, width=Inches(5.7))

                # Add figure caption centered below
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
            else:
                print(f"WARNING: Image not found at {img_full_path}")

            i += 1
            # If next line is a redundant <div align="center">...</div> caption, skip it
            if i < len(lines) and ("Figure " in lines[i] or "<b>Figure" in lines[i] or "<i>Figure" in lines[i]):
                i += 1
            continue

        # Skip redundant html caption divs if they appear standalone
        if re.match(r'^<div align="center"><b>Figure\s+.*?</div>$', stripped) or re.match(r'^<div align="center"><i>Figure\s+.*?</div>$', stripped):
            i += 1
            continue

        # Handle Markdown Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            
            # Parse table rows
            rows_data = []
            for tl in table_lines:
                # check if it's separator row | :--- | :--- |
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
                    is_header = (r_idx == 0)
                    for c_idx in range(num_cols):
                        cell = table.cell(r_idx, c_idx)
                        text_val = r_data[c_idx] if c_idx < len(r_data) else ""
                        
                        # Strip basic markdown bold tags for clean table text
                        clean_text = text_val.replace("**", "").replace("*", "")
                        cell.text = clean_text
                        
                        set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
                        set_cell_borders(cell, color="64748b", sz="4")
                        
                        p = cell.paragraphs[0]
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.space_after = Pt(2)
                        p.paragraph_format.line_spacing = 1.2
                        
                        if is_header:
                            set_cell_background(cell, "F1F5F9")
                            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            for r in p.runs:
                                r.font.name = 'Times New Roman'
                                r.font.size = Pt(10)
                                r.font.bold = True
                                r.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
                        else:
                            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                            for r in p.runs:
                                r.font.name = 'Times New Roman'
                                r.font.size = Pt(10)
                                r.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
                
                # Add spacing after table
                p_spacer = doc.add_paragraph()
                p_spacer.paragraph_format.space_before = Pt(0)
                p_spacer.paragraph_format.space_after = Pt(6)
            continue

        # Handle Headings
        if stripped.startswith("#"):
            match = re.match(r'^(#{1,6})\s+(.*)', stripped)
            if match:
                level = len(match.group(1))
                h_text = match.group(2).strip()
                
                # Clean markdown formatting from heading
                clean_h_text = h_text.replace("**", "").replace("*", "").replace("“", '"').replace("”", '"')
                
                # Automatic page breaks before chapters
                if clean_h_text.startswith("CHAPTER ") or clean_h_text in ["REFERENCES", "APPENDIX A: USER INTERFACE SNAPSHOTS", "APPENDIX B: PUBLISHED PAPER DETAILS", "PLAGIARISM VERIFICATION COMPLIANCE NOTE"]:
                    doc.add_page_break()

                p = doc.add_paragraph()
                p.paragraph_format.keep_with_next = True
                run = p.add_run(clean_h_text)
                run.font.name = 'Times New Roman'
                run.font.bold = True

                if level == 1:
                    run.font.size = Pt(15)
                    run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ("CHAPTER" in clean_h_text or "VISVESVARAYA" in clean_h_text or "SAI VIDYA" in clean_h_text or clean_h_text in ["REFERENCES", "ABSTRACT", "ACKNOWLEDGEMENT", "TABLE OF CONTENTS", "LIST OF FIGURES", "LIST OF TABLES", "LIST OF SYMBOLS AND ABBREVIATIONS"]) else WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_before = Pt(16)
                    p.paragraph_format.space_after = Pt(10)
                elif level == 2:
                    run.font.size = Pt(13.5)
                    run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_before = Pt(14)
                    p.paragraph_format.space_after = Pt(6)
                elif level == 3:
                    run.font.size = Pt(12.5)
                    run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_before = Pt(10)
                    p.paragraph_format.space_after = Pt(4)
                else:
                    run.font.size = Pt(12)
                    run.font.italic = True
                    run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_before = Pt(8)
                    p.paragraph_format.space_after = Pt(2)

                i += 1
                continue

        # Handle Horizontal Rules
        if stripped in ["---", "***", "___"]:
            i += 1
            continue

        # Handle empty lines & html tags
        if not stripped or stripped in ["<br>", "<br/>", "<br><br>", "<br><br><br>"]:
            i += 1
            continue

        if stripped.startswith("<div align=\"center\">") or stripped == "<div align=\"center\">" or stripped == "</div>":
            i += 1
            continue

        # Handle Regular Paragraphs & Lists
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.space_before = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        # Check if list item
        if stripped.startswith("- ") or stripped.startswith("* ") or stripped.startswith("• "):
            p.paragraph_format.left_indent = Inches(0.25)
            content = stripped[2:].strip()
            run_bullet = p.add_run("• ")
            run_bullet.font.bold = True
            parse_inline_formatting(p, content)
        elif re.match(r'^\d+\.\s+', stripped):
            match_num = re.match(r'^(\d+\.)\s+(.*)', stripped)
            p.paragraph_format.left_indent = Inches(0.25)
            num_str = match_num.group(1)
            content = match_num.group(2)
            run_num = p.add_run(f"{num_str} ")
            run_num.font.bold = True
            parse_inline_formatting(p, content)
        else:
            parse_inline_formatting(p, stripped)

        i += 1

    print(f"Saving formatted docx to {DOCX_PATH}...")
    doc.save(DOCX_PATH)
    print(f"SUCCESS: Saved {DOCX_PATH} ({os.path.getsize(DOCX_PATH):,} bytes)")

    # Copy to user's Windows Downloads folder
    dl_docx = os.path.join(DOWNLOADS_DIR, "FINAL_PROJECT_REPORT_BIS786.docx")
    try:
        shutil.copyfile(DOCX_PATH, dl_docx)
        print(f"Copied docx to: {dl_docx}")
    except Exception as e:
        print(f"Notice copying to downloads: {e}")

    # Copy to frontend public folder
    fe_docx = os.path.join(FRONTEND_PUBLIC, "FINAL_PROJECT_REPORT_BIS786.docx")
    try:
        shutil.copyfile(DOCX_PATH, fe_docx)
        print(f"Copied docx to: {fe_docx}")
    except Exception as e:
        print(f"Notice copying to frontend public: {e}")

def parse_inline_formatting(paragraph, text):
    """Parse basic markdown bold (**), italic (*), and code (`) runs."""
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

if __name__ == "__main__":
    generate_docx()
