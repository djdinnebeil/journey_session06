from langgraph.graph import StateGraph, END
from typing import Literal
from api.services.models import PostState
from api.services.agents import AgentFactory

class GraphBuilder:
    def __init__(self):
        self.agent_factory = AgentFactory()
    
    def verify_output_router(self, state: PostState) -> Literal["pass", "revise"]:
        """Route based on verification result."""
        return state["verify_result"]
    
    def build_graph(self):
        """Build and compile the LangGraph workflow."""
        # Create agents
        research_agent = self.agent_factory.get_research_agent()
        summarize_agent = self.agent_factory.get_summarize_agent()
        post_agent = self.agent_factory.get_post_agent()
        verify_node = self.agent_factory.get_verify_wrapper()
        
        # Build graph
        graph = StateGraph(PostState)
        
        # Add nodes
        graph.add_node("research", research_agent)
        graph.add_node("summarize", summarize_agent)
        graph.add_node("draft_post", post_agent)
        graph.add_node("verify", verify_node)
        
        # Set entry point
        graph.set_entry_point("research")
        
        # Add edges
        graph.add_edge("research", "summarize")
        graph.add_edge("summarize", "draft_post")
        graph.add_edge("draft_post", "verify")
        
        # Add conditional edges
        graph.add_conditional_edges("verify", self.verify_output_router, {
            "pass": END,
            "revise": "draft_post"
        })
        
        return graph.compile() 