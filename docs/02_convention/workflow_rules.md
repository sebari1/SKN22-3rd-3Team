# 🔄 Workflow Rules (작업 규칙)

프로젝트의 안정적인 운영과 데이터 정합성을 위해, 모든 기여자는 아래의 워크플로우 규칙을 준수해야 합니다.

---

## 1. Data Preprocessing (데이터 전처리)
> **⚠️ Critical Rule**

데이터 전처리 파이프라인(`scripts/process/`)을 실행하거나 전처리 로직을 수정할 경우, 반드시 **Data Preprocessing Report**를 최신화해야 합니다.

- **대상 파일**: `docs/04_data/data_preprocessing_report_v2.md` (V2) 또는 `_v1.md` (V1)
- **필수 포함 항목**:
    1. **Execution Date**: 전처리 실행 일시
    2. **Source Data Stats**: 원본 데이터 수 (Count)
    3. **Filtered/Cleaned Stats**: 전처리 후 데이터 수
    4. **Change Log**: 로직 변경 사항 요약

---

## 2. Git & Commit (버전 관리)
- **Commit Message**: [Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따릅니다.
    - `feat: `: 새로운 기능 추가
    - `fix: `: 버그 수정
    - `docs: `: 문서 수정
    - `refactor: `: 코드 리팩토링 (기능 변경 없음)
    - `chore: `: 빌드, 패키지 매니저 설정 등

---

## 3. Pull Requests (PR)
- PR 생성 시 관련 Issue가 있다면 링크합니다.
- 변경 사항의 목적과 영향을 받는 컴포넌트를 명시합니다.
- 새로운 기능 추가 시, 관련 문서(`docs/`) 업데이트가 포함되어야 Merge 가능합니다.
