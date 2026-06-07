import streamlit as st
import io
import pdfplumber
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Job Application Assistant", layout="wide")
st.title("Job Application Assistant")
st.caption(
    "Upload your CV and a job description — get a tailored rewrite in seconds.")

# Concept: Layout primitives — st.columns, file uploader, text area.

col1, col2 = st.columns(2)

with col1:
    cv_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("Paste the job description", height=300)

# ACTION BUTTON WITH INPUT VALIDATION
run = st.button(
    "Analyse",
    type="primary",
    disabled=(cv_file is None or not job_description.strip()),
)

# WIRE EXTRACTION INTO THE FLOW WITH FEEDBACK AND GUARDS
if run:
    with st.spinner("Extracting CV text..."):
        cv_text = extract_text_from_pdf(cv_file.getvalue())

    if not cv_text.strip():
        st.error("Could not extract text from the PDF. Make sure it is not a scanned image.")
        st.stop()
        




# PDF EXTRACTION
def extract_text_from_pdf(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)
    
    
        
        
