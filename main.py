from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pipeline.orchestrator import PipelineOrchestrator
from pipeline.models import PipelineRequest, PipelineResult
import uvicorn

app = FastAPI(
    title="AI Data Pipeline API",
    description="Enterprise LLM-powered data extraction and classification pipeline",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

orchestrator = PipelineOrchestrator()

@app.post("/api/pipeline/process", response_model=PipelineResult)
async def process_document(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    content = await file.read()
    result = await orchestrator.run(content, file.filename)
    return result

@app.get("/api/pipeline/status/{job_id}")
async def get_status(job_id: str):
    return orchestrator.get_job_status(job_id)

@app.get("/api/search")
async def semantic_search(query: str, top_k: int = 10):
    return await orchestrator.vector_search(query, top_k)

@app.get("/health")
async def health():
    return {"status": "ok", "pipeline": "ready"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
