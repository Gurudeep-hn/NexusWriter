from langgraph.types import Send
from langchain_core.messages import SystemMessage, HumanMessage
from src.config import get_llm
from src.schemas import AgentState, Task, Plan, EvidenceItem

WRITER_PROMPT = """You are a senior technical writer.
Write a single section of the blog post.

Guidelines:
- Follow the exact bullets provided.
- Maintain the requested tone.
- Use Markdown formatting.
- If citations are required, hyperlink them using the provided Evidence URLs.
- Start with '## Section Title'.
"""

def worker_node(payload: dict) -> dict:
    # Hydrate models from payload
    task = Task(**payload["task"])
    plan = Plan(**payload["plan"])
    evidence = [EvidenceItem(**e) for e in payload.get("evidence", [])]
    
    llm = get_llm()
    
    # Construct Context
    bullets = "\n".join([f"- {b}" for b in task.bullets])
    sources = "\n".join([f"[{e.title}]({e.url})" for e in evidence[:5]])
    
    content = llm.invoke([
        SystemMessage(content=WRITER_PROMPT),
        HumanMessage(content=(
            f"Blog Context: {plan.blog_title} ({plan.blog_kind})\n"
            f"Section Goal: {task.goal}\n"
            f"Requirements: {task.target_words} words\n"
            f"Bullets to Cover:\n{bullets}\n\n"
            f"Available Sources:\n{sources}"
        ))
    ]).content
    
    return {"sections": [(task.id, content)]}

def fanout_to_workers(state: AgentState):
    """Generates parallel tasks for workers."""
    if not state["plan"]:
        return []
        
    return [
        Send(
            "worker",
            {
                "task": task.model_dump(),
                "plan": state["plan"].model_dump(),
                "evidence": [e.model_dump() for e in state.get("evidence", [])]
            }
        )
        for task in state["plan"].tasks
    ]
