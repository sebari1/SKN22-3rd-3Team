# V3 Pipeline Strategy: Pure Clean Flow (Fact-Based)

## 1. Overview
The V3 pipeline represents a fundamental shift from the incremental improvements of V2 to a high-precision, production-grade data architecture. The primary goal is to maximize RAG (Retrieval-Augmented Generation) performance by eliminating semantic noise and standardizing metadata.

## 2. Core Principles
- **Total Independence**: V3 processes raw source data (`data/bemypet_catlab.json`) from scratch, removing legacy dependencies on V2's intermediate processing.
- **LLM-Driven Refinement**: Uses LLMs (`gpt-4o-mini`) not just for classification, but for rewriting search-friendly titles and generating structured summaries.
- **Noise Reduction**: Explicitly excludes raw article text from the vector embedding to prevent "semantic drift" caused by non-essential content (headers, intros, ads).

## 3. Data Schema (Standardized)
The V3 schema is designed for highly filtered and precise retrieval.

| Component | Field | Purpose |
| :--- | :--- | :--- |
| **Identity** | `uid` | Standardized `v3_XXXXX` format. |
| **Display** | `title_refined` | LLM-generated, search-optimized title. |
| **RAG Input** | `text` | Cleaned full content for LLM context. |
| **Semantic** | `summary` | Professional 1-sentence summary. |
| **Search** | `keywords` | 3-5 high-signal domain keywords. |
| **Intent** | `intent_tags` | Emotional/Functional tags (e.g., 'Emergency'). |
| **Filter** | `categories` | Standardized English category keys. |
| **Filter** | `specialists` | Persona-based classification (e.g., 'Physician'). |

## 4. Pipeline Workflow
1.  **Preprocessing**: 
    - Extracts raw text from `data/bemypet_catlab.json`.
    - Batches data for the `V3Classifier`.
    - Performs LLM extraction of metadata.
    - Generates `tokenized_text` using Kiwi with a custom domain dictionary.
2.  **Embedding**:
    - Constructs an **Embedding Content String**: 
      `[Categories] [Specialists] Title: {title_refined} | Keywords: {keywords} | Summary: {summary}`
    - Generates 1536-dim vectors via `text-embedding-3-small`.
3.  **Loading**:
    - Upserts to `cat_library.care_guides` collection.
    - Synchronizes with MongoDB Atlas Search Index.

## 5. Embedding Policy: Structured Semantic Signal
Contrary to V2, V3 does **not** embed the raw `text` field. 
- **Reasoning**: Raw text often contains irrelevant conversational filler. By embedding only the "Refined Title + Keywords + Summary", the vector space is populated only with the "essence" of the article.
- **Result**: Drastically higher Top-K precision for specific user queries.

## 6. Verification Status
- **Schema Validation**: Verified with Pydantic models.
- **Pipeline Test**: Successfully verified with 3-item batch processing.
- **Search Readiness**: Atlas Search Index definitions for `vector_index` and `keyword_index` (BM25) are prepared.
