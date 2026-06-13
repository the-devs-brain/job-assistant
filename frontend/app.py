import streamlit as st
import io
import pdfplumber
import os
import json
# from openai import OpenAI
# For cost sake we use Groq instead
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Job Application Assistant", layout="wide")
st.title("Job Application Assistant")
st.caption(
    "Upload your CV and a job description — get a tailored rewrite in seconds.")


# PDF EXTRACTION
def extract_text_from_pdf(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def analyse(cv_text: str, job_description: str) -> dict:
    prompt = f"""You are an expert CV writer and career coach.

Given the CV and job description below, return a JSON object with exactly these four keys:
- "match_score": integer 0-100 showing how well the CV matches the job
- "missing_skills": list of strings — skills in the job description not present in the CV
- "rewritten_cv": string — the full CV rewritten to match the job description language and requirements
- "cover_letter": string — a tailored cover letter for this specific role

CV:
{cv_text}

Job Description:
{job_description}

Return only valid JSON, no extra text."""

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
    return json.loads(response.choices[0].message.content)


# Sidebar: history placeholder

with st.sidebar:

    st.header("Past Analyses")

    st.info("History will appear here once the database is connected.")

# Main form - Concept: Layout primitives — st.columns, file uploader, text area.

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
        st.error(
            "Could not extract text from the PDF. Make sure it is not a scanned image.")
        st.stop()

    with st.spinner("Analysing — this takes a few seconds..."):
        try:
            result = analyse(cv_text, job_description)
        except Exception as e:
            st.error(f"AI call failed: {e}")
            st.stop()

    st.success("Analysis complete!")

    score = result.get("match_score", 0)
    colour = "green" if score >= 70 else "orange" if score >= 40 else "red"
    st.markdown(f"### Match Score: :{colour}[{score}%]")

    st.subheader("Missing Skills")
    skills = result.get("missing_skills", [])
    if skills:
        for skill in skills:
            st.markdown(f"- {skill}")
    else:
        st.write("No critical gaps found.")

    tab1, tab2 = st.tabs(["Rewritten CV", "Cover Letter"])

    with tab1:

        st.text_area("Copy your rewritten CV", value=result.get(
            "rewritten_cv", ""), height=400)

    with tab2:

        st.text_area("Copy your cover letter", value=result.get(
            "cover_letter", ""), height=400)
