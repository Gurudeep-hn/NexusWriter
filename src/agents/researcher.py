from datetime import date, timedelta
from langchain_core.messages import SystemMessage, HumanMessage
from src.config import get_llm
from src.schemas import AgentState, EvidencePack
from src.tools.research import SearchTool, iso_to_date

RESEARCHER_PROMPT = """You are a Research Assistant.
Extract Key Facts from the search results.
Return a structured EvidencePack.
"""

def researcher_node(state: AgentState) -> dict:
    tool = SearchTool()
    queries = state.get("queries", [])
    
    raw_results = []
    for q in queries:
        raw_results.extend(tool.search(q))
        
    if not raw_results:
        return {"evidence": []}
        
    # Deduplicate and Filter (using LLM for brevity or just logic)
    # Using LLM to synthesize clean evidence items
    llm = get_llm()
    extractor = llm.with_structured_output(EvidencePack)
    
    pack = extractor.invoke([
        SystemMessage(content=RESEARCHER_PROMPT),
        HumanMessage(content=f"Raw Results:\n{str(raw_results)[:30000]}")
    ])
    
    # Date filtering
    valid_evidence = []
    cutoff = date.today() - timedelta(days=state.get("recency_days", 3650))
    
    for item in pack.evidence:
        d = iso_to_date(item.published_at)
        if not d or d >= cutoff:
            valid_evidence.append(item)
            
    return {"evidence": valid_evidence}
