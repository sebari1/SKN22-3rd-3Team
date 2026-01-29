from typing import Literal, Dict, Any, Optional
import unicodedata
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from langgraph.types import Command
from .state import AgentState
from src.core.prompt_manager import prompt_manager

llm = ChatOpenAI(model="gpt-4o-mini")

class RouterDecision(BaseModel):
    """전문가 팀 분류 결정 모델"""
    category: Literal["adoption", "care", "general"] = Field(description="요청 분류: 입양 관련(adoption), 건강/행동 케어(care), 일반 인사 및 기타(general)")
    reasoning: str = Field(description="이 분류를 선택한 구체적인 논리적 이유 (한국어)")

async def head_butler_node(state: AgentState) -> Command:
    """
    Root supervisor: Pure LLM Router with Few-Shot Prompting.
    """
    system_prompt = prompt_manager.get_prompt("head_butler")
    
    router = llm.with_structured_output(RouterDecision)
    decision = await router.ainvoke([SystemMessage(content=system_prompt)] + state["messages"])
    
    debug = {
        "node": "Head Butler",
        "method": "LLM Router (Few-Shot)",
        "decision": decision.category,
        "reasoning": decision.reasoning
    }
    
    if decision.category == "adoption":
        return {
            "router_decision": "adoption",
            "debug_info": debug
        }
    elif decision.category == "care":
        return {
            "router_decision": "care",
            "debug_info": debug
        }
    else:
        # Butler answers general queries with User Profile awareness
        profile = state.get("user_profile", {})
        profile_context = ""
        if profile:
            profile_context = f"\n[사용자 정보]\n- 거주지: {profile.get('housing', '미설정')}\n- 활동량: {profile.get('activity', '미설정')}\n- 선호 성향: {', '.join(profile.get('traits', [])) if profile.get('traits') else '미설정'}"

        # Fetch general prompt from YAML and inject context
        general_persona_template = prompt_manager.get_prompt("head_butler", field="general")
        general_persona = general_persona_template.format(profile_context=profile_context)

        response = await llm.ainvoke([
            SystemMessage(content=general_persona),
            *state["messages"]
        ])
        return {
            "router_decision": "general",
            "messages": [response],
            "debug_info": debug
        }
