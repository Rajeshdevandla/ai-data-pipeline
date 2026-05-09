import openai
from pinecone import Pinecone
import hashlib

class VectorEmbedder:

    def __init__(self):
        self.client = openai.AsyncOpenAI()
        self.pc = Pinecone()
        self.index = self.pc.Index("ai-pipeline-index")

    async def embed_and_store(self, text: str, metadata: dict, job_id: str) -> str:
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:8000]
        )
        vector = response.data[0].embedding
        vector_id = hashlib.md5(job_id.encode()).hexdigest()
        self.index.upsert(vectors=[{
            "id": vector_id,
            "values": vector,
            "metadata": {**metadata, "job_id": job_id, "text_preview": text[:200]}
        }])
        return vector_id

    async def search(self, query: str, top_k: int = 10) -> list:
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        query_vector = response.data[0].embedding
        results = self.index.query(vector=query_vector, top_k=top_k, include_metadata=True)
        return [{"id": m.id, "score": m.score, "metadata": m.metadata} for m in results.matches]
