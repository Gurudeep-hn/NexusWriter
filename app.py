import streamlit as st
import datetime
from src.graph import app as graph_app

# --- UI Config ---
st.set_page_config(
    page_title="NexusWriter",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .reportview-container {
        background: #0E1117;
    }
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=64)
    st.title("NexusWriter")
    st.markdown("### AI-Powered Blog Orchestrator")
    
    st.divider()
    
    mode = st.radio("Strategy", ["Auto-Detect", "Deep Dive (Closed Book)", "News Flash (Open Book)"])
    model = st.selectbox("Model", ["openai/gpt-oss-120b", "llama-3.3-70b", "mixtral-8x7b"])
    use_images = st.toggle("Generate AI Images", value=True)
    
    st.info("Powered by Groq & LangGraph")

# --- Main Area ---
st.title("What should we write about today?")

topic = st.text_area("Enter your topic or rough idea...", height=100, placeholder="e.g., The future of quantum computing in pharmaceutical discovery")

col1, col2 = st.columns([1, 4])
with col1:
    run_btn = st.button("🚀 Launch Agent", use_container_width=True)

if run_btn and topic:
    with st.status("Initializing NexusWriter Protocol...", expanded=True) as status:
        
        inputs = {
            "topic": topic,
            "as_of": str(datetime.date.today()),
             # Defaults used by graph
            "queries": [],
            "evidence": [],
            "sections": [],
            "image_specs": [],
            "merged_md": "",
            "md_with_placeholders": "",
            "final": "",
             # Placeholder initial values
            "mode": "hybrid",
            "needs_research": True,
            "generate_images": use_images,
            "recency_days": 30
        }
        
        # Override based on UI
        if mode == "Deep Dive (Closed Book)":
             inputs["mode"] = "closed_book"
             inputs["needs_research"] = False
        elif mode == "News Flash (Open Book)":
             inputs["mode"] = "open_book"
             inputs["needs_research"] = True
        
        container = st.empty()
        
        # Streaming Execution
        try:
            for step in graph_app.stream(inputs):
                node_name = list(step.keys())[0]
                status.write(f"✅ Completed: **{node_name}**")
                
                # Extract partial state
                state = step[node_name]
                
                # Dynamic Preview
                if node_name == "router":
                     status.write(f"📝 Strategy: **{state.get('mode')}**")
                elif node_name == "editor":
                     st.toast(f"Plan Created: {len(state['plan'].tasks)} Sections")
                elif node_name == "worker":
                     # Worker outputs chunks; maybe show progress count
                     pass
                elif node_name == "generator":
                     container.markdown(state['final'])

            status.update(label="Mission Complete", state="complete")
        except Exception as e:
            status.update(label="Mission Failed", state="error")
            st.error(f"An error occurred: {str(e)}")
