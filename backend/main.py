import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ai.engine import analyse_application, extract_text_from_pdf

app = FastAPI(title="Job Assistant-solo API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint 1 — Health check
@app.get("/")
def health_check():
    return {"status": "running", "message": "Job Assistant-solo API is Live"}

# Endpoint 2 — Main feature
@app.post("/analyse")
async def analyse(
    cv_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        # Validate file is a PDF
        if not cv_file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="File must be a PDF.")

        # Validate job description is not empty
        if not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description cannot be empty.")

        # Save uploaded PDF to a temp file and extract text
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await cv_file.read())
                tmp_path = tmp.name
            cv_text = extract_text_from_pdf(tmp_path)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

        # Call AI engine
        result = analyse_application(cv_text, job_description)

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")