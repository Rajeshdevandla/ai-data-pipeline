# AI Data Pipeline

A Python backend pipeline that ingests raw text, extracts and classifies structured data using the OpenAI API, and stores results for downstream use. Built with FastAPI, Celery, Redis, and PostgreSQL.

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat-square&logo=openai)](https://openai.com)
[![Celery](https://img.shields.io/badge/Celery-Redis-37814A?style=flat-square)](https://docs.celeryq.dev)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker)](https://docker.com)

## What Problem This Solves

Manual classification and data extraction from unstructured text does not scale. This pipeline automates the full flow: raw text in via REST API, LLM extracts structured fields into JSON, results land in a queryable database without any manual intervention.

This is the extraction core used in the [AI Document Intelligence Platform](https://github.com/Rajeshdevandla/ai-document-intelligence-platform). The pipeline also runs standalone for any generic text extraction task.

## Demo

```
POST /process
{"text": "Invoice from Acme Corp dated March 15, 2024 for $4,590 - Cloud Services"}

Response (async, returns immediately):
{"task_id": "abc-123", "status": "processing"}

GET /results/abc-123
{
  "document_type": "Invoice",
  "vendor": "Acme Corp",
  "date": "2024-03-15",
  "amount": 4590.00,
  "line_items": [{"description": "Cloud Services", "amount": 4590.00}],
  "confidence": 0.96
}
```

## Architecture

```
POST /process (text input)
        |
        v
  FastAPI endpoint
  |-- validate input
  |-- enqueue Celery task -> Redis
  |-- return {task_id, status: "processing"}
        |
        v  (async, non-blocking)
  Celery worker
  |-- text preprocessing (normalization, whitespace cleaning)
  |-- build structured extraction prompt
  |-- call OpenAI API (GPT-4o)
  |-- parse and validate JSON response
  |-- store result -> PostgreSQL
        |
        v
GET /results/{task_id}
  |-- fetch from PostgreSQL
  |-- return structured result
```

**Key design decisions:**
- **Async via Celery + Redis** - API returns immediately; heavy LLM work runs in the background. Keeps the API responsive under load.
- **Structured output prompt** - GPT-4o instructed to return JSON matching a fixed schema. Response validation catches malformed extractions.
- **Retries with exponential backoff** - Celery retries failed tasks up to 3 times. OpenAI API errors do not lose work.
- **Preprocessing before LLM** - text normalization before the API call reduces token count and improves extraction accuracy.

## Tech Stack

| Component | Technology |
|---|---|
| API | Python 3.11, FastAPI |
| LLM | OpenAI API (GPT-4o) |
| Async processing | Celery + Redis |
| Data processing | Pandas |
| Storage | PostgreSQL |
| Infrastructure | Docker, Docker Compose |

## Quick Start

```bash
git clone https://github.com/Rajeshdevandla/ai-data-pipeline.git
cd ai-data-pipeline
cp .env.example .env
# Add OpenAI API key and DB config to .env
docker-compose up -d
```

Services started: FastAPI (port 8000), Celery worker, Redis, PostgreSQL

API docs: http://localhost:8000/docs

**Required environment variables:**

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key |
| `POSTGRES_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis URL (default: `redis://localhost:6379`) |

## API Reference

| Method | Path | Description |
|---|---|---|
| GET | /health | Health check |
| POST | /process | Submit text for extraction |
| GET | /results/{task_id} | Retrieve extraction result |
| GET | /tasks | List recent tasks with status |

## Project Structure

```
ai-data-pipeline/
|-- main.py               # FastAPI app + routes
|-- tasks/
|   |-- extraction.py     # Celery task: preprocess -> LLM -> store
|-- core/
|   |-- preprocessor.py   # Text cleaning and normalization
|   |-- extractor.py      # OpenAI API integration + prompt builder
|   |-- validator.py      # Schema validation for LLM output
|-- models/
|   |-- schema.py         # Pydantic models and DB schema
|-- requirements.txt
|-- docker-compose.yml
|-- .env.example
|-- Dockerfile
```

## What I'd Build Next

- **Document type routing** - detect type first (invoice/contract/receipt) and use type-specific extraction prompts
- **Confidence thresholds** - route low-confidence extractions to a human review queue
- **Streaming status** - WebSocket endpoint for real-time task progress instead of polling
- **Batch processing** - accept lists of documents and process in parallel across Celery workers
- **Eval framework** - track extraction accuracy over time with labeled test cases

## Related Projects

- [AI Document Intelligence Platform](https://github.com/Rajeshdevandla/ai-document-intelligence-platform) - Enterprise version with Java microservices, OCR, React dashboard
- [AskDocs AI](https://github.com/Rajeshdevandla/askdocs-ai) - PDF RAG chatbot using Amazon Bedrock and FAISS
- [SQLGenie](https://github.com/Rajeshdevandla/sql-genie) - Natural language to SQL with safety validation

---

Built by [Rajesh Kumar](https://rajeshdevandla.github.io) - Full Stack Java & AI Developer | Chicago, IL
