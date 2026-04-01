# Job Application Assistant

An AI-powered tool that reads your CV and a job description, rewrites your CV to match the role, and generates a tailored cover letter — all in one workflow.

---

## Description

Job Application Assistant takes the friction out of job applications. Upload your CV and paste a job description, and the tool uses OpenAI to:

- Analyse the job requirements against your experience
- Rewrite your CV to highlight the most relevant skills and achievements
- Generate a professional, personalised cover letter ready to send

---

## Tech Stack

| Layer     | Technology                |
|-----------|---------------------------|
| Backend   | FastAPI, Python           |
| Frontend  | Streamlit                 |
| AI        | OpenAI API (GPT-4)        |
| Database  | PostgreSQL, SQLAlchemy    |
| Container | Docker, Docker Compose    |

---

## Folder Structure

```
jon-assistant/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
├── ai/
│   ├── prompts/
│   │   └── analyse_prompt.txt  # Prompt templates
│   └── engine.py               # OpenAI interaction logic
├── backend/
│   ├── models/
│   │   └── __init__.py         # Database models
│   ├── routes/
│   │   └── __init__.py         # API route definitions
│   ├── services/
│   │   └── __init__.py         # Business logic
│   └── main.py                 # FastAPI app entry point
├── database/
│   ├── db.py                   # Database connection
│   └── schema.sql              # Table definitions
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── frontend/
│   └── app.py                  # Streamlit UI
├── .env.example                # Environment variable template
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-org/jon-assistant.git
cd jon-assistant
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://postgres:password@localhost:5432/jon_assistant
ENVIRONMENT=development
```

### 3. Run with Docker

```bash
docker-compose up --build
```

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 4. Run locally (without Docker)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn backend.main:app --reload

# Start frontend (new terminal)
streamlit run frontend/app.py
```

---

## Team

| Name    | Role                  | Responsibilities                              |
|---------|-----------------------|-----------------------------------------------|
| Alfred  | Team Lead             | Architecture, project oversight, code reviews |

---

## License

MIT
