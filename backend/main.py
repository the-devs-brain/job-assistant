import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from ai.engine import analyse_application, extract_text_from_pdf
from database.db import get_db, create_tables, Analysis

app = FastAPI(title="Job Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_tables()


# Endpoint 1 — Health check
@app.get("/")
def health_check():
    return {"status": "running", "message": "Job Assistant API is live"}


# Endpoint 2 — Main feature
@app.post("/analyse")
async def analyse(
    cv_file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if not cv_file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="File must be a PDF.")

        if not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description cannot be empty.")

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await cv_file.read())
                tmp_path = tmp.name
            cv_text = extract_text_from_pdf(tmp_path)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

        result = analyse_application(cv_text, job_description)

        # Save to database
        record = Analysis(
            cv_text=cv_text,
            job_description=job_description,
            match_score=result["match_score"],
            missing_skills=", ".join(result["missing_skills"]),
            rewritten_cv=result["rewritten_cv"],
            cover_letter=result["cover_letter"]
        )
        db.add(record)
        db.commit()

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


# Endpoint 3 — History
@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(Analysis).order_by(Analysis.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "match_score": r.match_score,
            "missing_skills": r.missing_skills,
            "created_at": r.created_at.isoformat()
        }
        for r in records
    ]