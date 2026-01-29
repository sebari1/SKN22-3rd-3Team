import os
import json
import pickle
import asyncio
from typing import List, Dict, Any
from tqdm import tqdm
from src.embeddings.factory import EmbeddingFactory
from src.pipelines.base import BaseEmbedder

class V3Embedder(BaseEmbedder):
    def __init__(self):
        self.embedder = EmbeddingFactory.get_embedder("openai")
        self.output_path = "data/v3/embedded.pkl"

    async def _embed_batch(self, batch: List[Dict[str, Any]], semaphore: asyncio.Semaphore):
        async with semaphore:
            texts = []
            for item in batch:
                cats = ", ".join(item.get("categories", []))
                specs = ", ".join(item.get("specialists", []))
                keywords = ", ".join(item.get("keywords", []))
                summary = item.get('summary', '')
                title = item.get('title_refined', '')
                content = f"[{cats}] [{specs}] 제목: {title} | 키워드: {keywords} | 요약: {summary}"
                texts.append(content[:8000])

            vectors = await self.embedder.embed_documents(texts)
            for item, vector in zip(batch, vectors):
                item["embedding"] = vector

    async def run(self, input_path: str) -> str:
        print(f"🚀 Starting Parallel V3 Embedding Generation reading from {input_path}...")
        
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
            
        with open(input_path, "r", encoding="utf-8") as f:
            items = json.load(f)
            
        print(f"📊 Generating embeddings for {len(items)} documents (Parallel)...")
        
        batch_size = 100
        semaphore = asyncio.Semaphore(5)
        batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
        
        tasks = [self._embed_batch(batch, semaphore) for batch in batches]
        
        # Using a simple gather, tqdm can be added if needed but keeping it clean
        await asyncio.gather(*tasks)
            
        # Save as Pickle
        with open(self.output_path, "wb") as f:
            pickle.dump(items, f)
            
        print(f"✨ Saved {len(items)} embedded items to {self.output_path} (Pickle format)")
        return self.output_path
