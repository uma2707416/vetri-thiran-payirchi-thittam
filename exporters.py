from io import BytesIO
from pathlib import Path
from html import escape
from utils.sanitize import sanitize_text

def format_html_preview(text: str) -> str:
    safe = escape(sanitize_text(text))
    return safe.replace("\n", "<br>")

def format_docx(text: str, doc_type: str) -> bytes:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Inches

    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("LEGALEASE")
    run.bold = True
    run.font.size = Pt(20)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = subtitle.add_run(doc_type)
    r.bold = True
    r.font.size = Pt(14)

    for block in sanitize_text(text).split("\n"):
        line = block.strip()
        if not line:
            continue
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(line)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("LegalEase - AI-generated draft | Review before legal use").font.size = Pt(8)

    output = BytesIO()
    doc.save(output)
    return output.getvalue()

def format_pdf(text: str, doc_type: str) -> bytes:
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=18)

    def header():
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "LEGALEASE", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, doc_type, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

    def footer():
        pdf.set_y(-12)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(0, 8, "LegalEase - AI-generated draft | Review before legal use", align="C")

    pdf.add_page()
    header()
    pdf.set_font("Helvetica", "", 10)

    for line in sanitize_text(text).split("\n"):
        line = line.strip()
        if not line:
            pdf.ln(3)
        else:
            pdf.multi_cell(0, 5.5, line)
            pdf.ln(1)
    footer()
    return bytes(pdf.output())
