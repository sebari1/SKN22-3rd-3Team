import asyncio
import sys
import os

# Ensure project root is in path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

from src.utils.mongodb import MongoDBManager
from dotenv import load_dotenv

load_dotenv()

async def verify():
    db = MongoDBManager.get_v3_db()
    collection = db["care_guides"]
    
    # Get total count
    count = await collection.count_documents({})
    print(f"📊 Total V3 Documents: {count}")

    # Get one document from V3
    doc = await collection.find_one({"uid": {"$regex": "^v3_"}})
    
    if doc:
        print("✅ Sample V3 Document Found:")
        for key, value in doc.items():
            if key == "embedding":
                print(f"- {key}: [{len(value)} dimensions]")
            elif isinstance(value, str):
                print(f"- {key}: ({len(value)} chars) {value[:100]}...")
            elif isinstance(value, list):
                print(f"- {key}: (List of {len(value)}) {value}")
            else:
                print(f"- {key}: {value}")
    else:
        print("❌ No V3 document found.")

if __name__ == "__main__":
    asyncio.run(verify())
