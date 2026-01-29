import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def check_db():
    uri = os.getenv("MONGO_V3_URI")
    client = AsyncIOMotorClient(uri)
    db = client["cat_library"]
    collection = db["care_guides"]
    
    total_count = await collection.count_documents({})
    breed_count = await collection.count_documents({"uid": {"$regex": "^v3_breed_"}})
    
    print(f"📊 Total Documents in 'cat_library.care_guides': {total_count}")
    print(f"🐈 Breed Documents (UID: v3_breed_...): {breed_count}")
    
    if breed_count > 0:
        sample = await collection.find_one({"uid": {"$regex": "^v3_breed_"}})
        print("\n🔍 Sample Breed Document:")
        print(f"Title: {sample.get('title_refined')}")
        print(f"UID: {sample.get('uid')}")
        print(f"Embedding Length: {len(sample.get('embedding', []))}")
        print(f"Tokenized Text: {sample.get('tokenized_text')[:50]}...")
    else:
        print("⚠️ No breed documents found!")

if __name__ == "__main__":
    asyncio.run(check_db())
