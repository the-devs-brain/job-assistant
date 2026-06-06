import streamlit as st

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
