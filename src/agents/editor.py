from langchain_core.messages import SystemMessage, HumanMessage
from src.config import get_llm
from src.schemas import AgentState, Plan

EDITOR_PROMPT = """You are the Editor-in-Chief of a high-end tech blog.
Create a comprehensive content plan.

Requirements:
- Structure the blog into 5-8 logical sections (Tasks).
- Each task must have a clear goal and word count.
- If 'open_book', focus on facts and citations.
- If 'closed_book', focus on depth and clarity.

Output JSON strictly matching the Plan schema."""

def editor_node(state: AgentState) -> dict:
    llm = get_llm()
    planner = llm.with_structured_output(Plan)
    
    evidence_summary = (
        "\n".join([f"- {e.title}: {e.url}" for e in state.get("evidence", [])[:10]])
        if state.get("evidence")
        else "No external research provided."
    )
    
    plan = planner.invoke([
        SystemMessage(content=EDITOR_PROMPT),
        HumanMessage(content=(
            f"Topic: {state['topic']}\n"
            f"Mode: {state['mode']}\n"
            f"Evidence Context:\n{evidence_summary}"
        ))
    ])
    
    return {"plan": plan}
