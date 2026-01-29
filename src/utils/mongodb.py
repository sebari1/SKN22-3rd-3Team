import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class MongoDBManager:
    """
    Centralized manager for MongoDB connections.
    Supports both V1 (Legacy) and V2 (Pro) clusters.
    """
    
    @staticmethod
    def get_v1_client():
        uri = os.getenv("MONGO_V1_URI") or os.getenv("MONGO_URI")
        if not uri:
            raise ValueError("MONGO_V1_URI or MONGO_URI not found in .env")
        return AsyncIOMotorClient(uri)

    @staticmethod
    def get_v2_client():
        uri = os.getenv("MONGO_V2_URI")
        if not uri:
            raise ValueError("MONGO_V2_URI not found in .env")
        return AsyncIOMotorClient(uri)

    @staticmethod
    def get_v1_db():
        from src.core.config import ZipsaConfig
        client = MongoDBManager.get_v1_client()
        return client[ZipsaConfig.get_policy("v1").db_name]

    @staticmethod
    def get_v2_db():
        from src.core.config import ZipsaConfig
        client = MongoDBManager.get_v2_client()
        return client[ZipsaConfig.get_policy("v2").db_name]

    @staticmethod
    def get_v1_index_config():
        return {
            "name": "vector_index",
            "definition": {
                "fields": [
                    {"numDimensions": 1536, "path": "embedding", "similarity": "cosine", "type": "vector"},
                    {"path": "category", "type": "filter"}
                ]
            }
        }

    @staticmethod
    def get_v2_index_config():
        return {
            "name": "vector_index",
            "definition": {
                "fields": [
                    {"numDimensions": 1536, "path": "embedding", "similarity": "cosine", "type": "vector"},
                    {"path": "categories", "type": "filter"},
                    {"path": "specialists", "type": "filter"}
                ]
            }
        }

    @staticmethod
    def get_v3_client():
        uri = os.getenv("MONGO_V3_URI")
        if not uri:
            # Fallback to V2 URI if V3 is not explicitly set (assuming same cluster)
            uri = os.getenv("MONGO_V2_URI")
            if not uri:
                 raise ValueError("MONGO_V3_URI or MONGO_V2_URI not found in .env")
        return AsyncIOMotorClient(uri)

    @staticmethod
    def get_v3_db():
        from src.core.config import ZipsaConfig
        client = MongoDBManager.get_v3_client()
        return client[ZipsaConfig.get_policy("v3").db_name]

    @staticmethod
    def get_v3_index_config():
        # Same as V2 for now
        return MongoDBManager.get_v2_index_config()
