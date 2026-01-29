# 고양이 카드 (Cat Card) 기능 명세

## 1. 개요
고양이 품종에 대한 상세 정보를 시각적으로 제공하는 UI 컴포넌트('고양이 카드')를 구현한다.
챗봇 대화 중 추천되거나 언급된 품종을 강조하고, 사용자 인터랙션(Hover) 시 카드를 노출하여 직관적인 정보를 전달한다.

## 2. 인터페이스 설계 (Extensibility)
향후 '사용자의 고양이' 정보도 동일한 UI 틀에서 보여줄 수 있도록, 공통 인터페이스(`CatCardSchema`)를 정의하여 구현한다.

### 2.1. 공통 스키마 (CatCard Interface)
모든 고양이 카드는 아래 데이터 구조를 따른다.
*   **Header**:
    *   `title` (이름/품종명)
    *   `subtitle` (부제/애칭/학명)
    *   `image_url` (대표 이미지)
*   **Body**:
    *   `tags` (특성 태그 리스트: 성격, 묘종 등)
    *   `description` (소개글)
    *   `stats` (시각화할 수치 데이터 Key-Value Map)
    *   `meta_info` (추가 정보: 출처, 생년월일 등)

### 2.2. 구현체 (Implementation Types)
*   **Type A: 품종 카드 (Breed Card)**
    *   **Data Source**: `cat_breeds_integrated.json`
    *   `title`: 품종명 (한글)
    *   `stats`: `adaptability`, `intelligence` 등 고정 스탯 방사형 차트.
*   **Type B: 마이 캣 카드 (User Cat Card)** *[Future]*
    *   **Data Source**: User DB (회원가입/프로필 입력 데이터)
    *   `title`: 고양이 이름 (예: "레오")
    *   `subtitle`: 품종 (예: "샴")
    *   `stats`: `health_status` (건강 상태), `age` 등 사용자 정의 수치 또는 D-Day(접종일) 시각화.

## 3. 데이터 소스 상세 (Breed Card 기준)
DB(`cat_breeds_integrated.json` / Atlas `catfit_v2.breeds`) 데이터를 매핑한다.

### 3.1. 매핑 상세
*   **이미지 (Breed Image)**:
    *   TheCatAPI를 활용하여 해당 품종의 고해상도 이미지 확보.
    *   **전략**: API를 매번 호출하는 대신, 초기 1회 크롤링하여 로컬 또는 CDN에 저장(캐싱)하여 사용. (비용 및 속도 최적화)
*   **특성 (Traits)**:
    *   `temperament` (성격) 키워드 태그 나열 (예: '애교 많은', '활동적인').
    *   **설명**: `summary_ko` (한글 요약) 활용.
    *   **출처**: `source_urls`의 위키피디아(Wiki) 링크 제공.
*   **스탯 (Stats) 시각화**:
    *   주요 수치 데이터를 방사형(Radar) 차트 또는 막대(Bar) 그래프로 표현.
    *   항목 예시: `adaptability` (적응력), `affection_level` (애정도), `energy_level` (활동량), `intelligence` (지능) 등.

## 3. 기능 시나리오

### 3.1. 챗봇 연동 (Contextual Highlight)
*   **트리거**: 챗봇 응답 텍스트 내 "품종명"이 포함될 경우 자동 감지.
*   **동작**:
    1.  해당 텍스트에 하이라이팅(밑줄 또는 색상 변경) 적용.
    2.  사용자가 **마우스 오버(Hover)** 시 '고양이 카드' 팝오버(Popover) 또는 툴팁 노출.
    3.  클릭 시 상세 페이지 또는 모달 확장 (선택 사항).

### 3.2. 카드 UI 구성 (Mock-up)
*   헤더: 품종 이름 및 대표 이미지.
*   바디:
    *   핵심 키워드 태그 (Traits).
    *   능력치 그래프 (Stats).
    *   간단한 설명.
