import os
import json
import pdfplumber
from openai import OpenAI
from openai import RateLimitError, APITimeoutError, APIConnectionError
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#module level is better, so i dont have to call everytime


def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from a PDF file and return as a single string."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def analyse_application(cv_text: str, job_description: str) -> dict:
    """
    Analyse a CV against a job description using OpenAI.
    Returns a dict with: match_score, missing_skills, rewritten_cv, cover_letter.
    """

    prompt = f"""
You are an expert career coach and CV writer.

Analyse the following CV against the job description provided.

Return your response as a valid JSON object with EXACTLY these four keys:
- "match_score": a string like "72/100" rating how well the CV matches the job
- "missing_skills": a list of skills or experience the candidate lacks
- "rewritten_cv": a full rewritten version of the CV tailored to the job
- "cover_letter": a professional cover letter tailored to the job

Do not include any explanation or text outside the JSON object.

CV:
{cv_text}

Job Description:
{job_description}
"""
    #two failure guards, one wrapping the API call itself (network/auth failures) nd one wrapping the JSON parsing (model output failures)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert career coach. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
                temperature=0.3,
                timeout=30,
                response_format={"type": "json_object"}
        )
    except RateLimitError:
        raise ValueError("OpenAI rate limit hit — try again shortly")
    except APITimeoutError:
        raise ValueError("Request timed out after 30 seconds")
    except APIConnectionError:
        raise ValueError("Could not reach OpenAI — check your connection") 

    raw = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model returned invalid JSON: {e}\nRaw output:\n{raw}")

    return {
        "match_score": result.get("match_score", ""),
        "missing_skills": result.get("missing_skills", []),
        "rewritten_cv": result.get("rewritten_cv", ""),
        "cover_letter": result.get("cover_letter", "")
    }


# ── TEST BLOCK ────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    sample_cv = """
    Alfred Esan — Software Engineer
    Skills: Python, FastAPI, PostgreSQL, Docker, Azure, Machine Learning, PyTorch
    Experience: 2 years in data engineering and ML pipelines at Mitsubishi Electric.
    Education: M.Sc. Next Level Engineering, Utrecht University of Applied Sciences.
    """

    sample_job = """
    Senior Data Engineer — FinTech Startup
    We are looking for a data engineer with strong Python skills, experience with
    cloud platforms (AWS or Azure), Kafka, Spark, and real-time data pipelines.
    Knowledge of dbt and Airflow is a plus. Must have 3+ years experience.
    """

    print("Running analyse_application...\n")
    result = analyse_application(sample_cv, sample_job)

    print(f"Match Score:     {result['match_score']}")
    print(f"\nMissing Skills:  {result['missing_skills']}")
    print(f"\nRewritten CV:\n{result['rewritten_cv']}")
    print(f"\nCover Letter:\n{result['cover_letter']}")