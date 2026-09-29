# LegalEase

LegalEase is an AI-assisted legal document drafting application built from the supplied project specification.

## Architecture

Streamlit frontend -> FastAPI backend -> Google Gemini API

The frontend also creates TXT, DOCX and PDF exports locally after generation.

## Project structure

```text
LegalEase/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── routes.py
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── frontend/
│   └── app.py
├── utils/
│   ├── __init__.py
│   ├── sanitize.py
│   └── exporters.py
├── tests/
│   └── test_utils.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows VS Code setup

Open the LegalEase folder in VS Code.

Create a virtual environment:

```powershell
py -3 -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate
```

Install packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create `.env` from `.env.example` and put your Gemini API key in:

```env
GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL=gemini-3.8-flash
BACKEND_URL=http://127.0.0.1:8000
```

Do not commit `.env` to Git.

## Run

Terminal 1:

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2:

```powershell
streamlit run frontend/app.py
```

Open the Streamlit URL shown in the terminal, normally:

```text
http://localhost:8501
```

FastAPI Swagger docs:

```text
http://127.0.0.1:8000/docs
```

## Test

With the virtual environment active:

```powershell
pytest -q
```

Health check:

```powershell
curl http://127.0.0.1:8000/health
```

Expected:

```json
{"status":"healthy"}
```

## API example

POST `/generate`:

```json
{
  "document_type": "Freelance Work Contract",
  "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
  "terms": "Payment within 30 days; Confidentiality; 15-day termination notice",
  "dates": "April 15, 2026"
}
```

## Important

This application creates AI-assisted drafts, not legal advice. Review generated documents with a qualified legal professional before signing or relying on them.
