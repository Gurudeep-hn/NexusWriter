import os
from datetime import date
from typing import List, Optional
from langchain_community.tools.tavily_search import TavilySearchResults
from src.schemas import EvidenceItem

class SearchTool:
    def __init__(self, max_results=5):
        self.tool = TavilySearchResults(max_results=max_results)

    def search(self, query: str) -> List[dict]:
        try:
            results = self.tool.invoke({"query": query})
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("content") or r.get("snippet", ""),
                    "published_at": r.get("published_date") or r.get("published_at"),
                    "source": r.get("source"),
                }
                for r in (results or [])
            ]
        except Exception:
            return []

def iso_to_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    try:
        return date.fromisoformat(s[:10])
    except Exception:
        return None
