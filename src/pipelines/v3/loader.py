import os
import pickle
import asyncio
from tqdm import tqdm
from src.utils.mongodb import MongoDBManager
from src.core.config import ZipsaConfig
from src.pipelines.base import BaseLoader

class V3Loader(BaseLoader):
    def __init__(self):
        self.policy = ZipsaConfig.get_policy("v3")
        # Ensure we use the correct DB
        self.db = MongoDBManager.get_v3_db() # Uses policy.db_name which we updated to 'cat_library'
        self.collection = self.db[self.policy.collection_name]

    async def run(self, input_path: str):
        print(f"🚀 Starting V3 Loading from {input_path}...")
        
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
            
        with open(input_path, "rb") as f:
            items = pickle.load(f)
            
        print(f"📊 Loading {len(items)} documents into {self.policy.db_name}.{self.policy.collection_name}...")
        
        # Create Index if needed (usually done by Manager or check existence)
        # For now, just upsert
        
        for item in tqdm(items, desc="Loading to MongoDB"):
            # Upsert based on UID
            await self.collection.update_one(
                {"uid": item["uid"]},
                {"$set": item},
                upsert=True
            )
            
        print("✨ V3 Loading Complete!")
