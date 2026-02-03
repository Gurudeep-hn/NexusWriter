from typing import List, Optional, Literal, Annotated
import operator
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

# --- Domain Models ---

class Task(BaseModel):
    id: int
    title: str
    goal: str = Field(..., description="The main objective of this section.")
    bullets: List[str] = Field(..., min_length=2)
    target_words: int = Field(..., ge=50, le=1000)
    tags: List[str] = Field(default_factory=list)
    requires_research: bool = False
    requires_citations: bool = False
    requires_code: bool = False

class Plan(BaseModel):
    blog_title: str
    audience: str
    tone: str
    blog_kind: Literal["explainer", "tutorial", "news_roundup", "comparison", "system_design"]
    constraints: List[str] = Field(default_factory=list)
    tasks: List[Task]

class EvidenceItem(BaseModel):
    title: str
    url: str
    published_at: Optional[str] = None
    snippet: Optional[str] = None
    source: Optional[str] = None

class EvidencePack(BaseModel):
    evidence: List[EvidenceItem] = Field(default_factory=list)

class ImageSpec(BaseModel):
    placeholder: str
    filename: str
    alt: str
    caption: str
    prompt: str
    size: Literal["1024x1024", "1024x1536", "1536x1024"] = "1024x1024"
    quality: Literal["low", "medium", "high"] = "medium"

class GlobalImagePlan(BaseModel):
    md_with_placeholders: str
    images: List[ImageSpec] = Field(default_factory=list)

# --- State ---

class AgentState(TypedDict):
    topic: str
    
    # Context
    as_of: str
    recency_days: int
    
    # Decisions
    mode: str
    needs_research: bool
    generate_images: bool
    queries: List[str]
    
    # Data
    evidence: List[EvidenceItem]
    plan: Optional[Plan]
    
    # Execution
    sections: Annotated[List[tuple[int, str]], operator.add]
    
    # Finalization
    merged_md: str
    md_with_placeholders: str
    image_specs: List[dict]
    final: str
