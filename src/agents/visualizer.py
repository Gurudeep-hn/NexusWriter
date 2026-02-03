from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage
from src.config import get_llm
from src.schemas import AgentState, GlobalImagePlan
from src.tools.images import ImageGenerator

VISUALIZER_PROMPT = """You are a Data Visualization Specialist.
Review the blog post and suggest 1-3 impactful diagrams or images.

Rules:
- Placeholders: [[IMAGE_1]], [[IMAGE_2]]
- Prompts: Detailed, high-quality, 'tech diagram', 'minimalist'.
- Do NOT suggest generic stock photos.
"""

def visualizer_node(state: AgentState) -> dict:
    # 1. Merge
    ordered = sorted(state["sections"], key=lambda x: x[0])
    body = "\n\n".join([content for _, content in ordered])
    
    title = state["plan"].blog_title if state["plan"] else "Blog Post"
    full_md = f"# {title}\n\n{body}"
    
    # 2. Plan Images (LLM) - Only if requested
    if not state.get("generate_images", True):
        return {
            "merged_md": full_md,
            "md_with_placeholders": full_md,
            "image_specs": []
        }

    llm = get_llm()
    plan_chain = llm.with_structured_output(GlobalImagePlan)
    
    image_plan = plan_chain.invoke([
        SystemMessage(content=VISUALIZER_PROMPT),
        HumanMessage(content=f"Content for analysis:\n\n{full_md[:20000]}") # Truncate if gigantic
    ])
    
    return {
        "merged_md": full_md,
        "md_with_placeholders": image_plan.md_with_placeholders,
        "image_specs": [img.model_dump() for img in image_plan.images]
    }

def generation_node(state: AgentState) -> dict:
    generator = ImageGenerator()
    final_md = state["md_with_placeholders"]
    
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    for spec in state.get("image_specs", []):
        try:
            # Check for existing
            path = images_dir / spec["filename"]
            if not path.exists():
                generator.save_image(spec["prompt"], path)
                
            replacement = f"![{spec['alt']}](images/{spec['filename']})\n*{spec['caption']}*"
            final_md = final_md.replace(spec["placeholder"], replacement)
            
        except Exception as e:
            fallback = f"> [Image Generation Failed: {e}]"
            final_md = final_md.replace(spec["placeholder"], fallback)
            
    return {"final": final_md}
