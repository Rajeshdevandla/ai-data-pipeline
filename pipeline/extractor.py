import openai
import boto3
import json
from functools import lru_cache

class LLMExtractor:

    def __init__(self):
        self.openai_client = openai.AsyncOpenAI()
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

    async def extract(self, text: str, provider: str = "openai") -> dict:
        if provider == "openai":
            return await self._extract_openai(text)
        return self._extract_bedrock(text)

    async def _extract_openai(self, text: str) -> dict:
        response = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extract structured data as JSON from the given text. Return only valid JSON."},
                {"role": "user", "content": f"Extract key entities, dates, amounts, and categories from:\n\n{text[:4000]}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(response.choices[0].message.content)

    def _extract_bedrock(self, text: str) -> dict:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": f"Extract structured JSON from:\n\n{text[:4000]}"}]
        })
        response = self.bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=body
        )
        return json.loads(json.loads(response['body'].read())['content'][0]['text'])
