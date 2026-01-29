# 🎭 Service Personas & Roles (페르소나 상세)

ZIPSA 서비스는 LangGraph 기반의 **Hierarchical Logic**을 따르며, 각 페르소나는 특정 소스 코드 파일에 정의된 **Node** 및 **RAG Strategy**와 매핑됩니다.

> [!NOTE]
> 모든 에이전트의 구체적인 지시 사항(System Prompt)과 페르소나는 `src/core/prompts.yaml`에서 동적으로 관리됩니다. 서비스 재시작 없이 `Prompt Editor`를 통해 수정할 수 있습니다.

---

## 🎩 1. The Head Butler (총괄 수석 집사)
> **"집사님, 무엇을 도와드릴까요? 전문가 팀을 호출하겠습니다."**

- **Role**: 사용자 의도(Intent)를 파악하고 적절한 전문가 팀(Adoption/Care)으로 라우팅하는 Supervisor.
- **Responsibility**:
    - 대화의 맥락 파악 및 초기 응대 (General Chat).
    - 사용자 프로필(Housing, Experience) 정보 관리.
    - 하위 팀(Adoption/Care) 호출 및 결과 종합.
- **Source Code**: 
    - 📄 [src/agents/head_butler.py](../../src/agents/head_butler.py)
    - **Node**: `head_butler_node`

---

## 🏢 2. Adoption Team (입양 및 인사 팀)
예비 집사와 새로운 고양이의 만남을 주선합니다.

### 🧩 Matchmaker (인사 담당/품종 추천)
> **"집사님의 라이프스타일에 딱 맞는 묘종을 추천해 드립니다."**
- **Specialist Key**: `"Matchmaker"` (RAG Metadata)
- **Role**: 주거 환경, 활동량, 성향 데이터를 기반으로 최적의 품종을 추천.
- **Logic**: Hybrid Search (Vector + Profile Metadata Filtering).
- **Source Code**:
    - 📄 [src/agents/adoption_team.py](../../src/agents/adoption_team.py)
    - **Node**: `matchmaker_node`

### 🔭 Liaison (대외 협력/구조 연계)
> **"이 아이와 인연을 맺을 수 있는 보호소를 찾아보겠습니다."**
- **Type**: **Tool Agent** (External API Based)
- **Role**: **National Animal Protection Information System API**를 사용하여 유기묘 정보를 검색하고 입양 절차를 안내. (`docs/03_api/openapi_spec.md` 참조)
- **Source Code**:
    - 📄 [src/agents/adoption_team.py](../../src/agents/adoption_team.py)
    - **Node**: `liaison_node` (Tool Execution Node)

---

## 🏥 3. Care Team (케어 및 의료 팀)
반려묘와의 행복하고 건강한 동거를 지원합니다.

### 🩺 Physician (주치의/건강 관리)
> **"건강은 조기 예방이 최우선입니다. 증상을 말씀해 주세요."**
- **Specialist Key**: `"Physician"`
- **Role**: 구토, 설사, 식욕 부진 등 질병 증상을 분석하고 대처법 및 영양 가이드 제공.
- **Logic**: Symptom-based RAG Retrieval.
- **Source Code**:
    - 📄 [src/agents/care_team.py](../../src/agents/care_team.py)
    - **Node**: `physician_node`

### ⚖️ Peacekeeper (평화 유지군/행동 교정)
> **"고양이들 간의 다툼이나 문제 행동에는 이유가 있습니다."**
- **Specialist Key**: `"Peacekeeper"`
- **Role**: 합사 갈등, 배변 실수, 공격성 등 행동학적 문제 원인 분석 및 해결책 제시.
- **Source Code**:
    - 📄 [src/agents/care_team.py](../../src/agents/care_team.py)
    - **Node**: `peacekeeper_node`
