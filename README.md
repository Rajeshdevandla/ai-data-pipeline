# AI Data Pipeline

A Python-based backend pipeline that takes raw text input, calls the OpenAI API for classification and extraction, and stores structured results for downstream use.

Built as a learning project to understand how to integrate LLM APIs into a backend service, and how to structure Python data pipelines with FastAPI.

## What It Does

- Accepts raw text or document content via a REST API endpoint
- Preprocesses and cleans the text (normalization, whitespace handling)
- Sends cleaned text to OpenAI API with a structured prompt for classification/extraction
- Parses the JSON response and stores results in a database
- Exposes a query endpoint to retrieve processed results

## Tech Stack

| Component | Technology |
|---|---|
| API | Python 3.11, FastAPI |
| LLM | OpenAI API (GPT-4o) |
| Data Processing | Pandas |
| Queue | Celery + Redis |
| Storage | PostgreSQL |
| Infrastructure | Docker, Docker Compose |

## How It Works

```
POST /process (text input)
     ↓
Text preprocessing (cleaning, normalization)
     ↓
OpenAI API call (extraction/classification prompt)
     ↓
Parse structured JSON response
     ↓
Store to PostgreSQL
     ↓
GET /results/{id} (retrieve processed output)
```

## Running Locally

Prerequisites: Python 3.11+, Docker, OpenAI API key

```bash
git clone https://github.com/Rajeshdevandla/ai-data-pipeline.git
cd ai-data-pipeline
pip install -r requirements.txt
# Add your OpenAI API key to .env
uvicorn main:app --reload
```

API docs: `http://localhost:8000/docs`

## Sample Request / Response

```bash
POST /process
{ "text": "Invoice from Acme Corp dated March 15, 2024 for $4,590" }
```

```json
{
  "document_type": "Invoice",
  "vendor": "Acme Corp",
  "date": "2024-03-15",
  "amount": 4590.00
}
```

## What I Applied Here

- Structuring a Python FastAPI project with clean routing and service layers
- Calling OpenAI API with system/user prompts and parsing structured responses
- Using Celery and Redis for async task processing
- Handling failures gracefully with retries and error logging
- Docker Compose for running the full stack locally

---

**Rajesh Kumar** — Full Stack Java Developer | Chicago, IL
[Portfolio](https://rajeshdevandla.github.io) · [GitHub](https://github.com/Rajeshdevandla)
