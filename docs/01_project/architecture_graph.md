# 🏗️ System Architecture (LangGraph)

ZIPSA 서비스는 **계층형 멀티 에이전트 시스템 (Hierarchical Multi-Agent System)**으로 설계되었습니다.  
사용자의 요청은 최상위 Supervisor인 **Head Butler**를 통해 분류되며, 각 전문 팀(Team)으로 이관되어 처리됩니다.

---

## 📊 Graph Visualization (Live Structure)

아래 다이어그램은 실제 소스 코드(`src/agents/graph.py`)에서 생성된 LangGraph 구조입니다.

![LangGraph Architecture](../assets/zipsa_graph_structure.png)

---

## 🔄 Workflow Logic

### 1. Root Level: Head Butler
- **Start Node**: `head_butler`
- **Logic**: 사용자의 입력(Message)을 분석하여 라우팅(`adoption`, `care`, `general`) 결정.
- **Conditional Edge**: 
    - `router_decision == "adoption"` → **Adoption Team**으로 이동.
    - `router_decision == "care"` → **Care Team**으로 이동.
    - `router_decision == "general"` → 즉시 응답 후 종료(`__end__`).

### 2. Team Level: Sub-Supervisors
각 팀은 자체적인 Supervisor 로직을 통해 더 세부적인 전문가(Specialist)를 호출합니다.

#### Adoption Team
- **Supervisor**: `adoption_team_node`
- **Specialists**:
    - `matchmaker`: 품종 추천 및 성향 분석 RAG 수행.
    - `liaison`: (Optional) 보호소 정보 검색. (현재 `matchmaker` 응답에 통합됨)

#### Care Team
- **Supervisor**: `care_team_node`
- **Specialists**:
    - `physician`: 의료/건강 지식 검색 RAG 수행.
    - `peacekeeper`: 행동/심리 문제 해결 RAG 수행.

### 3. State Management
- **Persistence**: `MemorySaver`를 사용하여 대화 맥락(Context)을 유지합니다.
- **Shared State**: `AgentState` 객체를 통해 대화 기록(`messages`)과 사용자 프로필(`user_profile`)을 모든 노드가 공유합니다.

---

## 🎭 Prompt Management System
ZIPSA는 하드코딩된 프롬프트 대신, 유연한 관리를 위해 **Prompt Manager**를 도입했습니다.
- **Config-driven**: 모든 페르소나와 지침은 `src/core/prompts.yaml`에 관리됩니다.
- **Dynamic Loading**: `src/core/prompt_manager.py` (Singleton)가 프롬프트를 메모리에 로드하며, 실시간 업데이트를 지원합니다.
- **Developer Tool**: Streamlit의 `Prompt Editor` 페이지를 통해 운영 중에도 에이전트의 성격을 즉시 수정할 수 있습니다.
