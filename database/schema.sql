CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    cv_text TEXT NOT NULL,
    job_description TEXT NOT NULL,
    match_score VARCHAR(20),
    missing_skills TEXT,
    rewritten_cv TEXT,
    cover_letter TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);