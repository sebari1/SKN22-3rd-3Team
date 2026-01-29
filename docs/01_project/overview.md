# 🏰 ZIPSA: AI-Powered Cat Head Butler Service
> **"Every Butler Needs a Head Butler."**  
> **Agentic RAG-based Lifestyle Matching & Comprehensive Care System**

---

## 1. Project Vision (비전)
**ZIPSA(집사)**는 초보 및 예비 '집사(고양이 반려인)'를 위한 **AI 수석 집사 서비스**입니다.  
사용자의 라이프스타일을 심층 분석하여 가장 적합한 묘종을 추천하고(Matching), 입양 후에는 다중묘 갈등 조정부터 건강 관리까지(Care) 전방위로 지원하는 **'Agentic RAG' 기반의 코칭 시스템**입니다. 단순한 챗봇을 넘어, 전문성을 가진 **전문가 팀(Specialist Agents)**이 협업하여 사용자의 고민을 해결합니다.

---

## 2. Core Features (핵심 기능)

### 🧩 1. Lifestyle Matching (맞춤형 매칭)
- **사용자 분석**: 주거 환경(아파트/주택), 가족 구성원, 알러지 유무, 활동량 등을 고려한 정밀 분석.
- **RAG 기반 추천**: 67종의 고양이 품종 데이터와 수천 건의 양육 가이드를 기반으로 최적의 묘종 매칭.
- **파양 방지**: 단순 외모가 아닌, '함께 살 수 있는' 반려묘를 추천하여 파양률을 낮춥니다.

### 🔭 2. Ethical Adoption (유기묘 연계)
- **보호소 연계**: 추천된 품종과 유사한 유기묘 정보를 실시간으로 탐색.
- **입양 지원**: 입양 절차, 필수 준비물, 법적 고려사항 가이드 제공.

### ⚖️ 3. Conflict Resolution (다묘 갈등 조정)
- **성향 분석**: 기존 반려묘와 새로운 반려묘의 MBTI(성격 유형) 분석.
- **합사 솔루션**: 단계별 합사 스케줄링 및 긴장 완화(Peacekeeping) 프로토콜 제공.

### 🩺 4. Lifecycle Care (생애주기 케어)
- **건강 모니터링**: 구토, 배변 등 이상 징후 발생 시 초기 대응 가이드(Triage) 제공.
- **영양 관리**: 연령별/묘종별 사료 및 영양학적 조언.

---

## 3. Team Structure (AI 페르소나 조직도)
ZIPSA 시스템은 **수석 집사(Head Butler)**를 중심으로 두 개의 전문 팀으로 구성되어 있습니다.

### 🎩 Head Butler (수석 집사)
- **역할**: 사용자의 의도를 파악하고 적절한 전문가 팀으로 업무를 배분(Routing)하는 총괄 관리자.
- **위치**: `src/agents/head_butler.py`

### 🏢 Team 1: Adoption (입양 팀)
새로운 가족을 맞이하는 과정을 전담합니다.
- **Matchmaker (인사 담당)**: 라이프스타일 기반 품종 추천 및 성향 분석.
- **Liaison (대외 협력)**: **[Tool]** 국가동물보호정보시스템 API 기반 유기묘 검색 및 입양 절차 안내.
- **위치**: `src/agents/adoption_team.py`

### 🏥 Team 2: Care (케어 팀)
반려 생활 중 발생하는 건강 및 행동 문제를 해결합니다.
- **Physician (주치의)**: 질병 증상 분석 및 식이/영양 상담.
- **Peacekeeper (평화유지군)**: 다묘 가정 갈등 해결 및 행동 교정.
- **위치**: `src/agents/care_team.py`

> [!TIP]
> 각 페르소나의 상세 역할과 동작 방식은 **[personas.md](./personas.md)** 문서를 참조하세요.

---

## 4. Technical Architecture (아키텍처)
본 프로젝트는 **Hierarchical LangGraph (Multi-Agent Supervisor)** 패턴을 채택했습니다.

- **Orchestraion**: `LangGraph`를 이용한 상태 관리(Stateful) 및 에이전트 라우팅.
- **Knowledge Base (RAG)**: 
    - **Vector Store**: MongoDB Atlas Vector Search (v1/v2 Clusters).
    - **Retrieval**: Hybrid Search (Vector + Keyword/BM25 + RRF Re-ranking).
    - **Data Source**: TheCatAPI(품종), Wikipedia(상세), BemyPet(케어 가이드).
- **Interface**: Streamlit 기반의 인터랙티브 채팅 UI.
- **Environment**: Python 3.11+ (Conda `skn-third-proj`).
- **Data Pipeline**:
  - **V3 Pipeline**: `src/pipelines/v3/` (Decoupled 3-Stage Process)
    1. **Preprocessor**: Text Cleaning & Tokenization -> `processed.json`
    2. **Embedder**: OpenAI Embedding Generation -> `embedded.pkl`
    3. **Loader**: MongoDB Ingestion (`cat_library`)

> [!IMPORTANT]
> 시스템의 시각적 구조도와 데이터 흐름은 **[architecture_graph.md](./architecture_graph.md)**를 확인하세요.

---

## 5. Directory Structure
```
skn-third-proj/
├── data/               # Raw & Processed Data
├── docs/               # Documentation
├── scripts/            # Execution Scripts
│   └── v3/             # V3 Pipeline Scripts (run_preprocess, run_embed, run_load)
├── src/
│   ├── agents/         # LangGraph Agents
│   ├── core/           # Config & Settings
│   ├── pipelines/      # Data Pipelines (ETL)
│   │   ├── base.py     # Base Interfaces
│   │   └── v3/         # V3 Pipeline Logic (Preprocess -> Embed -> Load)
│   ├── retrieval/      # RAG Logic
│   └── utils/          # Helper Functions
├── tests/              # Unit Tests
└── .env                # Environment Variables
```
