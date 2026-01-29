import os
import logging
from typing import List, Dict, Any
from openai import AsyncOpenAI
from src.core.config import ZipsaConfig
from src.pipelines.v3.schemas import BatchResultV3

class V3Classifier:
    """
    New Classifier for V3 Pure Clean Pipeline.
    Strictly maps to V3 taxonomy and extracts high-signal metadata.
    """
    def __init__(self, model: str = "gpt-4o-mini"):
        self.policy = ZipsaConfig.get_policy("v3")
        self.model = model
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _get_system_prompt(self) -> str:
        categories = ", ".join(self.policy.categories)
        specialists = ", ".join(self.policy.specialists)
        return f"""
        You are a cat care domain expert. Analyze the provided articles and extract metadata.
        
        CATALOG OF CATEGORIES:
        {categories}
        
        CATALOG OF SPECIALISTS:
        {specialists}
        
        GUIDELINES:
        1. title_refined: Make the title concise and helpful for search queries.
        2. categories: Select 1-3 most relevant categories from the catalog.
        3. specialists: Select the most appropriate persona(s).
        4. intent_tags: Emotional/Functional intent (e.g., 'Health Alert', 'New Owner Guide', 'Pro Tip').
        5. summary: Exactly one sentence in professional Korean.
        """

    async def classify_batch(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not items:
            return []

        user_content = "Analyze these articles for V3 database ingestion:\n\n"
        for item in items:
            user_content += f"Original Title: {item['title']}\nContent: {item.get('content', '')[:1500]}\n\n"

        try:
            response = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": user_content}
                ],
                response_format=BatchResultV3,
                temperature=0
            )
            # Merge with original data (like URL) if needed
            results = response.choices[0].message.parsed.results
            return [res.model_dump() for res in results]
        except Exception as e:
            logging.error(f"[V3] Classification Error: {e}")
            return []
