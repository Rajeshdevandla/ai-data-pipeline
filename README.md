# AI-Powered Data Pipeline

Intelligent backend pipeline using LLM APIs to automate data extraction, classification, and vector-based search at enterprise scale.

## Key Achievements
- Integrated **OpenAI GPT-4o & AWS Bedrock** APIs for intelligent extraction
- Reduced manual data processing by **80%**
- **Sub-2-second** pipeline execution for standard documents
- **97.3% classification accuracy** on production data

## Tech Stack
| Component | Technology |
|---|---|
| API | Python 3.11, FastAPI |
| LLM | OpenAI GPT-4o, AWS Bedrock (Claude 3) |
| Vector Store | Pinecone, Elasticsearch |
| Data Processing | Pandas, NumPy |
| Queue | Celery + Redis |
| Infrastructure | Docker, AWS ECS |

## Pipeline Flow
```
Input Data → FastAPI Ingest → Pandas Preprocessing
                                    ↓
                            LLM Extraction (GPT-4o / Claude)
                                    ↓
                    Classification (97.3% accuracy)
                                    ↓
              Vector Embedding → Pinecone Store
                                    ↓
                    Elasticsearch Index → Query API
```

## Quick Start
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
