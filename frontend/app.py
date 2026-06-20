import streamlit as st
import requests
from datetime import datetime

BACKEND_URL = "http://localhost:8000"

# ── PAGE SETUP ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Job Application Assistant")
st.title("Job Application Assistant")
st.write("Upload your CV and paste a job description to get a match score, missing skills, a tailored CV, and a cover letter.")

# ── INPUT SECTION ─────────────────────────────────────────────────────────────
st.subheader("Your CV")
cv_file = st.file_uploader("Upload your CV (PDF only)", type=["pdf"])

st.subheader("Job Description")
job_description = st.text_area("Job Description", placeholder="Paste the job description here")

# ── ANALYSE BUTTON ────────────────────────────────────────────────────────────
if st.button("Analyse My Application"):

    # ── VALIDATION ────────────────────────────────────────────────────────────
    if not cv_file:
        st.warning("Please upload your CV as a PDF.")
    elif not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        # ── SEND TO BACKEND ───────────────────────────────────────────────────
        with st.spinner("Analysing your application..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/analyse",
                    files={"cv_file": (cv_file.name, cv_file.getvalue(), "application/pdf")},
                    data={"job_description": job_description}
                )

                if response.status_code == 200:
                    result = response.json()

                    # ── DISPLAY RESULTS ───────────────────────────────────────
                    st.success("Analysis complete!")

                    st.metric(label="Match Score", value=result["match_score"])

                    st.subheader("Missing Skills")
                    for skill in result["missing_skills"]:
                        st.write(f"• {skill}")

                    with st.expander("Rewritten CV"):
                       st.text_area("Rewritten CV", value=result["rewritten_cv"], height=400, label_visibility="collapsed")

                    with st.expander("Cover Letter"):
                        st.text_area("Cover Letter", value=result["cover_letter"], height=300, label_visibility="collapsed")

                else:
                    st.error(f"Error from backend: {response.json().get('detail', 'Unknown error')}")

            except Exception as e:
                st.error(f"Could not connect to backend: {str(e)}")
                # ── HISTORY SECTION ───────────────────────────────────────────────────────────
st.divider()
if st.button("View History"):
    try:
        response = requests.get(f"{BACKEND_URL}/history")
        if response.status_code == 200:
            history = response.json()
            if not history:
                st.info("No analyses saved yet.")
            else:
                st.subheader("Past Analyses")
                for item in history:
                    with st.expander(f"#{item['id']} — {item['match_score']} — {item['created_at'][:10]}"):
                        st.write(f"**Match Score:** {item['match_score']}")
                        st.write(f"**Missing Skills:** {item['missing_skills']}")
                        date = datetime.fromisoformat(item["created_at"]).strftime("%d %b %Y, %H:%M")
                        st.write(f"**Date:** {date}")
        else:
            st.error("Could not load history.")
    except Exception as e:
        st.error(f"Could not connect to backend: {str(e)}")