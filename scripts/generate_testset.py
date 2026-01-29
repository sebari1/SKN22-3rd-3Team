import json
import os
import random

def generate_testset():
    print("🚀 Generating Golden Dataset from V2 Potential Questions...")
    
    # Paths
    v2_path = "data/v2/bemypet_catlab_v2_preprocessed.json"
    output_path = "data/v3/golden_dataset.json"
    
    # Load V2 Data
    with open(v2_path, "r", encoding="utf-8") as f:
        v2_docs = json.load(f)

    # Load V3 Data (Source of Truth for IDs and Titles)
    v3_path = "data/v3/processed.json"
    if not os.path.exists(v3_path):
        print(f"❌ V3 Data not found at {v3_path}")
        return

    with open(v3_path, "r", encoding="utf-8") as f:
        v3_docs = json.load(f)

    # Ensure V2 and V3 are aligned by index (Assuming 1:1 mapping from pipeline)
    if len(v2_docs) != len(v3_docs):
        print(f"⚠️ Warning: V2 count ({len(v2_docs)}) != V3 count ({len(v3_docs)}). Mapping by index might be risky.")
    
    # Iterate and Map
    # We assume v2_docs[i] corresponds to v3_docs[i] because the pipeline processed them in order.
    # If not, we would need a key to match them (e.g. original title), but titles changed.
    # If not, we would need a key to match them (e.g. original title), but titles changed.
    # Let's rely on index for now as V3 was built from V2 batch.
    
    evaluation_set = []
    count = 0
    loop_count = min(len(v2_docs), len(v3_docs))
    
    for i in range(loop_count):
        v2_doc = v2_docs[i]
        v3_doc = v3_docs[i]
        
        # Questions from V2
        questions = v2_doc.get("potential_questions", [])
        if not questions:
            continue
            
        # Metadata from V3 (Target)
        target_uid = v3_doc.get("uid")
        target_title = v3_doc.get("title_refined") # V3 Title
        
        # Specialist mapping (From V3 or V2? V3 specs are just strings, V2 has full text)
        # Let's use V3's cleaner specialist field if available, else V2
        specialist_list = v3_doc.get("specialists", [])
        specialist = specialist_list[0] if specialist_list else "General"
        
        # Iterate through ALL potential questions
        for q in questions:
            evaluation_set.append({
                "query": q,
                "expected_keyword": target_title, # Ground Truth is the Refined Title
                "specialist": specialist,
                "source_doc_id": target_uid # Correct V3 ID (v3_XXXXX)
            })
            count += 1
        
    # Shuffle (Optional, but good for randomness if we inspect manually)
    random.shuffle(evaluation_set)
    final_set = evaluation_set # No limit
    
    # Save
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_set, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Generated {len(final_set)} test cases (Source: {count} docs).")
    print(f"📂 Saved to: {output_path}")

if __name__ == "__main__":
    generate_testset()
