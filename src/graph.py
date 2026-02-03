from langgraph.graph import StateGraph, START, END
from src.schemas import AgentState
from src.agents.router import router_node, route_next
from src.agents.researcher import researcher_node
from src.agents.editor import editor_node
from src.agents.writer import worker_node, fanout_to_workers
from src.agents.visualizer import visualizer_node, generation_node

def build_graph():
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("router", router_node)
    workflow.add_node("research", researcher_node)
    workflow.add_node("editor", editor_node)
    workflow.add_node("worker", worker_node)
    workflow.add_node("visualizer", visualizer_node)
    workflow.add_node("generator", generation_node)
    
    # Add Edges
    workflow.add_edge(START, "router")
    
    workflow.add_conditional_edges(
        "router", 
        route_next, 
        {
            "research": "research", 
            "editor": "editor"
        }
    )
    
    workflow.add_edge("research", "editor")
    
    workflow.add_conditional_edges(
        "editor", 
        fanout_to_workers, 
        ["worker"]
    )
    
    workflow.add_edge("worker", "visualizer")
    workflow.add_edge("visualizer", "generator")
    workflow.add_edge("generator", END)
    
    return workflow.compile()

app = build_graph()
