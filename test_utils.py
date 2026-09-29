from utils.sanitize import sanitize_text
from utils.exporters import format_docx, format_pdf, format_html_preview

def test_sanitize_text():
    assert sanitize_text("Hello\u2019s  \n world") == "Hello's\n world"

def test_html_preview():
    assert "&lt;script&gt;" in format_html_preview("<script>")

def test_docx_export():
    data = format_docx("TEST DOCUMENT", "Agreement")
    assert data.startswith(b"PK")

def test_pdf_export():
    data = format_pdf("TEST DOCUMENT", "Agreement")
    assert data.startswith(b"%PDF")
