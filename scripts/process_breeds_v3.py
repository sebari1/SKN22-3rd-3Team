import os
import json
import asyncio
from tqdm import tqdm
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Local Modules
import sys
sys.path.append(os.getcwd())
from src.pipelines.v3.schemas import StoredBreedV3, BreedStats
from src.utils.text import tokenize_korean
from src.embeddings.factory import EmbeddingFactory
from src.core.config import ZipsaConfig

load_dotenv()

class BreedPipeline:
    def __init__(self):
        # Initialize Embedder (Using Factory)
        self.embedder = EmbeddingFactory.get_embedder("openai")
        
        # Initialize DB (Using V3 Policy Config)
        self.db_client = AsyncIOMotorClient(os.getenv("MONGO_V3_URI"))
        v3_policy = ZipsaConfig.get_policy("v3")
        self.db = self.db_client[v3_policy.db_name] # cat_library
        self.collection = self.db[v3_policy.collection_name] # care_guides (Unified Collection Strategy)
        
    async def process(self):
        print(f"🚀 Starting V3 Breed Pipeline (Target: {self.collection.name})...")
        
        # 1. Load Data
        v2_path = "data/v2/cat_breeds_integrated.json"
        
        if not os.path.exists(v2_path):
             print(f"❌ Input file not found: {v2_path}")
             return

        with open(v2_path, "r", encoding="utf-8") as f:
            raw_breeds = json.load(f)
            
        print(f"📦 Loaded {len(raw_breeds)} breeds from {v2_path}")
        
        documents = []
        
        for breed in tqdm(raw_breeds, desc="Processing"):
            try:
                # A. Transform
                stats = BreedStats(**breed["stats"])
                
                # Construct Rich Text for RAG Context
                rich_text = f"""
                품종: {breed['name_ko']} ({breed['name_en']})
                
                [개요]
                {breed['summary_ko']}
                
                [성격]
                {', '.join(breed['personality_traits'])}
                
                [외형]
                {', '.join(breed['physical_traits'])}
                
                [주요 특징]
                - 털 빠짐: {breed['stats']['shedding_level']}/5
                - 활동량: {breed['stats']['energy_level']}/5
                - 지능: {breed['stats']['intelligence']}/5
                """
                
                # Clean Indentation
                clean_text = "\n".join([line.strip() for line in rich_text.split("\n") if line.strip()])
                
                # B. Tokenize (for Keyword Search)
                tokenized = tokenize_korean(clean_text)
                
                # C. Embedding Content
                embed_content = f"[Breeds] [Matchmaker] {breed['name_ko']} ({breed['name_en']}) | {', '.join(breed['personality_traits'])} | {breed['summary_ko']}"
                
                doc = StoredBreedV3(
                    uid=f"v3_breed_{breed['breed_id']}",
                    title_refined=f"{breed['name_ko']} (고양이 품종)",
                    name_ko=breed['name_ko'],
                    name_en=breed['name_en'],
                    summary=breed['summary_ko'],
                    personality_traits=breed['personality_traits'],
                    physical_traits=breed['physical_traits'],
                    stats=stats,
                    text=clean_text,
                    tokenized_text=tokenized,
                    categories=["Breeds"],
                    specialists=["Matchmaker"]
                )
                
                # D. Get Embedding
                vector = await self.embedder.embed_query(embed_content)
                doc.embedding = vector
                
                documents.append(doc)
            except Exception as e:
                print(f"⚠️ Error processing breed {breed.get('name_ko', '?')}: {e}")
            
        # 3. Load to DB
        print(f"💾 Upserting {len(documents)} breeds to MongoDB ({self.collection.name})...")
        
        if not documents:
            print("⚠️ No documents to save.")
            return

        operations = []
        from pymongo import UpdateOne
        
        for doc in documents:
            op = UpdateOne(
                {"uid": doc.uid},
                {"$set": doc.model_dump()},
                upsert=True
            )
            operations.append(op)
            
        if operations:
            result = await self.collection.bulk_write(operations)
            print(f"✅ Upserted: {result.upserted_count}, Modified: {result.modified_count}")
        
        print("🎉 Breed Pipeline Completed!")

if __name__ == "__main__":
    pipeline = BreedPipeline()
    asyncio.run(pipeline.process())
