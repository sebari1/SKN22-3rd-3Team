# Data Preprocessing Report (V3 Clean - Latest)

**Version**: `v3` (Clean Policy)
**Database**: `cat_library` (MongoDB Atlas)
**Domain Dictionary**: `data/v3/domain_dictionary.txt` (1,085 terms)

---

## 1. Dataset Statistics

| Source | Raw Count | Processed Count | Status |
| :--- | :---: | :---: | :--- |
| **BemyPet Catlab** | 1,153 | 1,153 | ✅ Complete |
| **Cat Breeds** | 67 | 67 | ✅ Complete |

---

## 2. Collections & Schema

### 📚 Articles Collection
- **Namespace**: `cat_library.care_guides`
- **UID Format**: `guide_00000` (Standardized)

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `uid` | `str` | standardized ID (e.g., `guide_00123`) |
| `title` | `str` | Article Title |
| `text` | `str` | Cleaned Text Content |
| `summary` | `str` | Article Summary |
| `keywords` | `List[str]` | **Core Keywords** (From V2) |
| `categories` | `List[str]` | **Taxonomy Topics** (Start with English) |
| `specialists` | `List[str]` | **English Personas** (Matchmaker, etc.) |
| `embedding` | `List[float]` | OpenAI Embedding (Structured) |
| `tokenized_text` | `str` | Full Text + Summary + Title Tokens |

### 🐈 Breeds Collection
- **Namespace**: `cat_library.breeds`
- **Source**: `data/v2/cat_breeds_integrated.json`
- **Validation**: All 67 breeds included in Domain Dictionary.

---

## 3. Taxonomy (V3 Standardized)

### Categories (Topics)
- `Health (건강/질병)`, `Nutrition (영양/식단)`, `Behavior (행동/심리)`
- `Care (양육/관리)`, `Living (생활/환경)`, `Product (제품/용품)`
- `Legal/Social (법률/사회)`, `Farewell (이별/상실)`, `General Info (상식/정보)`

### Specialists (Personas)
> **Note**: V3 uses English keys. `Liaison` is a **Tool Agent** (External API/Action) and usually does not retrieve from this static KB.

- **`Matchmaker`**: 맞춤 추천 / 양육
- **`Liaison`**: **[Tool Agent]** 입양/구조 (Uses **National Animal Protection Information System API** - see `docs/03_api/openapi_spec.md`)
- **`Peacekeeper`**: 행동 / 갈등
- **`Physician`**: 건강 / 영양 / 의료

---

## 4. Domain Dictionary & Tokenization

### Custom Dictionary
- **Path**: `data/v3/domain_dictionary.txt`
- **Total Terms**: 1,085 (Top 1000 Nouns + 67 Breeds)
- **Features**:
  - **Compound Support**: `벤토나이트`, `스크래쳐`, `아비시니안`
  - **Stopword Handling**: Enhanced filtering for cleaner tokens.
  - **1-Char Retention**: Retains essential 1-char verbs (e.g., `먹`, `자`).

### Performance
| Case | Default Tokenizer | V3 Custom Tokenizer |
| :--- | :--- | :--- |
| **Compound** | `벤토` + `나이트` | `벤토나이트` (✅) |
| **Breed** | `메인` + `쿤` | `메인쿤` (✅) |
| **Common** | `맛` + `동산` | `맛동산` (✅) |

---

## 5. Index Configuration

**Vector Index (`vector_index`)**:
```json
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    },
    {
      "path": "categories",
      "type": "filter"
    },
    {
      "path": "specialists",
      "type": "filter"
    }
  ]
}
```

---

## 6. Pipeline Architecture (3-Stage Decoupled)

The V3 pipeline uses a strictly decoupled 3-stage process located in `src/pipelines/v3/`.

### Stage 1: Preprocessor (`preprocessor.py`)
- **Input**: Raw JSON
- **Process**: Text cleaning, UID generation, Tokenization (Kiwi + Domain Dict), Field Mapping.
- **Output**: `data/v3/processed.json` (Text-only, no vector data).
- **Benefit**: Fast iteration on text processing without re-embedding cost.

### Stage 2: Embedder (`embedder.py`)
- **Input**: `processed.json`
- **Process**: Generates embeddings using OpenAI `text-embedding-3-small`.
- **Output**: `data/v3/embedded.pkl` (Python Pickle).
- **Benefit**: Cost optimization. Embeddings are persisted separately, allowing DB reload without API calls.

### Stage 3: Loader (`loader.py`)
- **Input**: `embedded.pkl`
- **Process**: Batch upsert to MongoDB `cat_library`.
- **Benefit**: Pure IO operation. Separation of concerns.
