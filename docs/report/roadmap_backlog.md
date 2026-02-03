# 🗺️ ZIPSA Roadmap & Backlog

본 문서는 `docs/dev_logs/`의 개발 기록과 현재 프로젝트 상태를 분석하여 도출한 향후 계획(Roadmap)과 세부 할 일(Backlog)입니다.

---

## 🚀 1. Roadmap (Vision)

### **Phase 1: V3 안정화 및 버그 박멸 (Current)**
*   **목표**: 현재 구현된 기능(Dual-Model, V3 검색, 3-Node 에이전트)의 무결성 확보.
*   **주요 과제**: 스트리밍 노이즈 제거, 데이터 정합성(지역 코드 등) 검증, 통합 테스트 커버리지 확대.

### **Phase 2: UI/UX 고도화 & 개인화 (Next)**
*   **목표**: 사용자 경험을 한 단계 끌어올리는 "디테일" 챙기기.
*   **주요 과제**: 유기동물 정보의 카드화(Card UI), 알레르기 필터의 온보딩 UI 통합, 다크 모드 가독성 개선.

### **Phase 3: 확장 및 자동화 (Future)**
*   **목표**: 운영 효율성 증대 및 기능 확장.
*   **주요 과제**: LangSmith 기반 KPI 자동 측정, Redis 캐싱 도입, 멀티모달(Vision) 확장 고려.

---

## 📝 2. Backlog (To-Do List)

개발 로그(2026-01-31 ~ 2026-02-02)에서 식별된 구체적인 작업 항목입니다.

### 🔥 High Priority (즉시 해결 필요)
- [ ] **지역 코드 정합성 검증 (`region_codes.py`)** (from 02-02 Log)
    - 이슈: `창원시` 등의 코드가 API에서 중복(3개)으로 반환되는 현상 확인.
    - 액션: 중복 키 처리 로직 추가 및 데이터 무결성 재검증.
- [ ] **스트리밍 토큰 필터링 검증** (from 02-02 Log)
    - 이슈: `head_butler`의 라우팅 판단 과정(JSON 토큰)이 간헐적으로 화면에 노출될 위험.
    - 액션: `utils.py`의 `astream_events` 핸들러에서 `router_classification` 태그가 확실히 차단되는지 스트레스 테스트 수행.

### 🧪 Testing & QA (테스트)
- [ ] **Liaison 통합 테스트** (from 02-02 Log)
    - 시나리오: "강남구 근처 입양 가능한 고양이 보여줘" → `search_abandoned_animals` 호출 → 결과 반환 전 과정 검증.
- [ ] **Matchmaker UI 통합 테스트** (from 02-02 Log)
    - 시나리오: 품종 추천 응답 시 우측 패널에 `CatCard`가 정상적으로 렌더링되는지 확인 (특히 `tags`, `description` 필드).
- [ ] **E2E 필터 테스트** (from 01-31 Log)
    - 액션: `scripts/verify_agents_e2e.py`를 확장하여 전체 시나리오 검증.

### ✨ Feature Enhancements (기능 개선)
- [ ] **유기동물 결과 카드 UI화** (from 02-02 Log)
    - 현재: 텍스트 나열 (`보호소: OO보호소, 품종: 한국 고양이...`)
    - 개선: 사진, 보호소명, 특징을 포함한 **카드 UI**로 변환하여 가독성 강화.
- [ ] **알레르기 필터 UI 통합** (from 01-31 Log)
    - 액션: `onboarding.py`에 알레르기 유무 체크박스 추가 및 `UserProfile` DTO와 연동.
    - 백엔드: `breed_criteria.py`에 알레르기 하드 필터 로직 통합.
- [ ] **품종 매핑 테이블 구축** (from 02-02 Log)
    - 이슈: 공공데이터 API가 가끔 `kindNm`을 누락하거나 비표준 포맷으로 반환.
    - 액션: `kindCd`(코드)를 표준 품종명으로 변환하는 매핑 테이블 확보.

### 🛠️ Technical Debt (기술 부채)
- [ ] **RAG 태그 정합성 전수 조사** (from 02-01 Log)
    - 액션: MongoDB(`care_guides`)의 `specialists` 태그 값과 코드(`care_team.py`)의 라우팅 키워드가 100% 일치하는지 스크립트로 검증.
- [ ] **단위 테스트(Unit Test) 작성** (from 02-02 Log)
    - 대상: `search_abandoned_animals` 함수, DTO 변환 로직 등 핵심 유틸리티.

---
**Last Updated**: 2026-02-03 by Head Butler
