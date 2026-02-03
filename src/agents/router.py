from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from typing import Literal, List
from src.config import get_llm
from src.schemas import AgentState

class RouterDecision(BaseModel):
    needs_research: bool
    mode: Literal["closed_book", "hybrid", "open_book"]
    queries: List[str] = Field(default_factory=list)

ROUTER_PROMPT = """You are the 'Nexus' routing engine.
Analyze the request and decide the research strategy.

Modes:
- closed_book: For well-known concepts (e.g., "Python inheritance").
- hybrid: For concepts needing fresh examples (e.g., "LangGraph patterns").
- open_book: For news/volatile topics (e.g., "GPT-5 release date").

If research is needed, generate 3-5 precise search queries."""

def router_node(state: AgentState) -> dict:
    llm = get_llm()
    decision_chain = llm.with_structured_output(RouterDecision)
    
    result = decision_chain.invoke([
        SystemMessage(content=ROUTER_PROMPT),
        HumanMessage(content=f"Topic: {state['topic']}\nDate: {state['as_of']}")
    ])
    
    recency = 3650 # Default 10 years
    if result.mode == "open_book":
        recency = 7
    elif result.mode == "hybrid":
        recency = 90
        
    return {
        "needs_research": result.needs_research,
        "mode": result.mode,
        "queries": result.queries,
        "recency_days": recency
    }

def route_next(state: AgentState) -> str:
    return "research" if state["needs_research"] else "editor"
