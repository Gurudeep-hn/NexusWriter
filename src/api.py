from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.graph import app as graph_app
from datetime import date

app = FastAPI(title="NexusWriter API", version="1.0.0")

class BlogRequest(BaseModel):
    topic: str
    as_of: str = str(date.today())

@app.post("/generate")
async def generate_blog(request: BlogRequest):
    """
    Trigger the blog generation workflow.
    Note: This is a synchronous blocking call for simplicity.
    In production, use background tasks.
    """
    try:
        inputs = {
            "topic": request.topic,
            "as_of": request.as_of,
            "recency_days": 30, # Default
             # Initialize lists to avoid validation errors
            "queries": [],
            "evidence": [],
            "sections": [],
            "image_specs": [],
            "mode": "hybrid",
            "needs_research": True,
            "merged_md": "",
            "md_with_placeholders": "",
            "final": ""
        }
        
        result = await graph_app.ainvoke(inputs)
        return {
            "title": result["plan"].blog_title,
            "final_md": result["final"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
