import asyncio
import uuid
from pipeline.extractor import LLMExtractor
from pipeline.classifier import DocumentClassifier
from pipeline.embedder import VectorEmbedder
from pipeline.preprocessor import DataPreprocessor
from pipeline.models import PipelineResult

class PipelineOrchestrator:

    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.extractor = LLMExtractor()
        self.classifier = DocumentClassifier()
        self.embedder = VectorEmbedder()
        self._jobs = {}

    async def run(self, content: bytes, filename: str) -> PipelineResult:
        job_id = str(uuid.uuid4())
        self._jobs[job_id] = "processing"

        try:
            # Step 1: Preprocess
            text = self.preprocessor.extract_text(content, filename)
            cleaned = self.preprocessor.clean(text)

            # Step 2: LLM Extraction
            extracted = await self.extractor.extract(cleaned)

            # Step 3: Classification
            label, confidence = self.classifier.classify(cleaned)

            # Step 4: Embed & Store
            vector_id = await self.embedder.embed_and_store(cleaned, extracted, job_id)

            self._jobs[job_id] = "complete"
            return PipelineResult(
                job_id=job_id,
                extracted_data=extracted,
                classification=label,
                confidence=confidence,
                vector_id=vector_id,
                status="complete"
            )
        except Exception as e:
            self._jobs[job_id] = "failed"
            raise e

    def get_job_status(self, job_id: str):
        return {"job_id": job_id, "status": self._jobs.get(job_id, "not_found")}

    async def vector_search(self, query: str, top_k: int):
        return await self.embedder.search(query, top_k)
