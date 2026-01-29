import streamlit as st
import yaml
import os
import sys

# 프로젝트 루트 경로 추가
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.core.prompt_manager import prompt_manager

st.set_page_config(page_title="ZIPSA Prompt Editor", page_icon="🕵️‍♂️", layout="wide")

st.title("🕵️‍♂️ Agent Prompt Control Center")
st.markdown("""
에이전트별 시스템 프롬프트를 실시간으로 수정하고 반영할 수 있습니다. 
수정 후 **Save & Sync** 버튼을 누르면 즉시 서비스에 반영됩니다.
""")

# 에이전트 목록 정의
AGENTS = {
    "Head Butler (Router)": "head_butler",
    "Adoption Supervisor": "adoption_supervisor",
    "Care Supervisor": "care_supervisor",
    "Physician (Expert)": "physician",
    "Peacekeeper (Expert)": "peacekeeper",
    "Matchmaker (Expert)": "matchmaker"
}

# 사이드바에서 에이전트 선택
selected_agent_label = st.sidebar.selectbox("Select Agent to Edit", list(AGENTS.keys()))
selected_agent_key = AGENTS[selected_agent_label]

# 필드 선택 (system or persona)
field = "persona" if "Expert" in selected_agent_label else "system"

# 현재 프롬프트 로드
current_prompt = prompt_manager.get_prompt(selected_agent_key, field=field)

# 에이드 터 영역
st.subheader(f"📝 Editing: {selected_agent_label}")
new_prompt = st.text_area(
    label=f"Edit {field.capitalize()} Prompt",
    value=current_prompt,
    height=400,
    help=f"{selected_agent_label}의 {field} 프롬프트입니다."
)

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("💾 Save & Sync", type="primary"):
        prompt_manager.update_prompt(selected_agent_key, new_prompt, field=field)
        st.success(f"✅ {selected_agent_label} prompt updated and persisted!")

with col2:
    if st.button("🔄 Reload from Disk"):
        prompt_manager.reload()
        st.info("Re-loaded all prompts from YAML.")

# 테스트 샌드박스 (Preview)
st.divider()
st.subheader("🧪 Live Preview")
with st.expander("Show Currently Loaded Prompt Structure"):
    st.code(yaml.dump({selected_agent_key: {field: new_prompt}}, allow_unicode=True), language="yaml")

st.info("💡 수정된 프롬프트는 즉시 메모리에 반영되어 차기 대화부터 적용됩니다. 서비스 재시작이 필요하지 않습니다.")
