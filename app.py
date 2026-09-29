import os
import requests
import streamlit as st
from dotenv import load_dotenv
from utils.exporters import format_docx, format_pdf, format_html_preview
from utils.sanitize import sanitize_text

load_dotenv()

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.markdown("""
<style>
.block-container {max-width: 1100px; padding-top: 2rem;}
.legal-card {
    background: #111827; color: #f9fafb; padding: 24px;
    border-radius: 12px; line-height: 1.65;
    max-height: 520px; overflow-y: auto;
}
.small-note {font-size: 0.85rem; color: #6b7280;}
</style>
""", unsafe_allow_html=True)

st.title("⚖️ LegalEase")
st.caption("AI-powered legal document drafting and export")

with st.sidebar:
    st.header("Document Details")
    document_type = st.selectbox(
        "Document type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement (NDA)",
            "Lease Agreement",
            "Service Agreement",
            "Freelance Work Contract",
            "Employment Offer Letter",
            "General Agreement",
        ],
    )
    dates = st.text_input("Effective date / dates", placeholder="April 15, 2026")
    parties = st.text_area(
        "Parties involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=110,
    )
    terms = st.text_area(
        "Terms & conditions",
        placeholder="Payment within 30 days; Confidentiality; 15-day termination notice",
        height=180,
    )
    generate = st.button("Generate Document", type="primary", use_container_width=True)

st.info("LegalEase produces an AI-assisted draft. It is not a substitute for advice from a qualified lawyer.")

if generate:
    if not all([document_type.strip(), dates.strip(), parties.strip(), terms.strip()]):
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Generating your document..."):
            try:
                response = requests.post(
                    f"{API_URL}/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": dates,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                st.session_state["document"] = response.json()["document"]
                st.session_state["document_type"] = document_type
            except requests.RequestException as exc:
                st.error(f"Backend connection failed: {exc}")

if "document" in st.session_state:
    st.subheader("Generated Document")
    edited = st.text_area(
        "Edit the document",
        value=st.session_state["document"],
        height=500,
        key="document_editor",
    )
    st.session_state["document"] = edited

    st.subheader("Preview")
    st.markdown(
        f'<div class="legal-card">{format_html_preview(edited)}</div>',
        unsafe_allow_html=True,
    )

    txt = sanitize_text(edited).encode("utf-8")
    docx = format_docx(edited, st.session_state.get("document_type", "Legal Document"))
    pdf = format_pdf(edited, st.session_state.get("document_type", "Legal Document"))

    c1, c2, c3 = st.columns(3)
    c1.download_button("Download TXT", txt, "legalease_document.txt", "text/plain", use_container_width=True)
    c2.download_button(
        "Download DOCX", docx, "legalease_document.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
    )
    c3.download_button("Download PDF", pdf, "legalease_document.pdf", "application/pdf", use_container_width=True)
