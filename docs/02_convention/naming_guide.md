# 🏷️ Naming Conventions (네이밍 규칙)

프로젝트의 일관성과 가독성을 위해 아래의 네이밍 규칙을 반드시 준수합니다.

---

## 1. File & Directory Naming (파일 및 폴더)
모든 파일명과 폴더명은 **`snake_case` (소문자 + 언더바)**를 사용합니다.

- ✅ **Good**: `user_profile.py`, `data_loader.py`, `01_project/`
- ❌ **Bad**: `UserProfile.py`, `data-loader.py`, `01Project/`

### 1-1. Python Modules
- 모듈명은 짧고 간결해야 하며, 해당 파일의 역할을 명확히 드러내야 합니다.
- **예시**: `classifier.py`, `ingestor.py`

### 1-2. Documentation
- 문서는 번호를 붙여 정렬 순서를 제어할 수 있습니다.
- **예시**: `01_project`, `02_convention`, `03_api`

---

## 2. Code Naming (코드)

### 2-1. Python
- **Global Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_COUNT = 3`)
- **Classes**: `PascalCase` (e.g., `HybridRetriever`)
- **Functions/Methods**: `snake_case` (e.g., `get_user_profile()`)
- **Variables**: `snake_case` (e.g., `user_id`)
- **Private Members**: `_snake_case` (e.g., `_connect_db()`)

### 2-2. MongoDB Collections
- **Collections**: `snake_case` (e.g., `cat_breeds`, `user_logs`)

---

## 3. API & Data
- **JSON Fields**: `snake_case`를 원칙으로 합니다.
    ```json
    {
        "user_id": "12345",
        "created_at": "2024-01-01"
    }
    ```
