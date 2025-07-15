from langgraph.graph import StateGraph, END
from typing import Literal
from api.services.models import PostState
from api.services.agents import AgentFactory
from api.services.supervisor import SupervisorAgent

class SupervisedGraphBuilder:
    """
    Enhanced graph builder that implements supervisor pattern for better workflow orchestration.
    The supervisor agent coordinates all other agents and makes routing decisions.
    """
    
    def __init__(self):
        self.agent_factory = AgentFactory()
        self.supervisor = SupervisorAgent()
    
    def supervisor_router(self, state: PostState) -> Literal["research", "summarize", "draft_post", "verify", END]:
        """
        Supervisor-based router that intelligently decides the next step.
        
        Args:
            state: Current workflow state
            
        Returns:
            Next node to execute or END
        """
        # First check basic completion logic before involving supervisor
        if not state.get("summary"):
            # Need research and summary first
            if not state.get("messages"):
                return END  # Invalid state
            return "research" if "research" not in str(state.get("messages", [])) else "summarize"
        
        if not state.get("post"):
            # Need to draft post
            return "draft_post"
        
        # Check if verification is complete
        verify_result = state.get("verify_result")
        if verify_result == "pass":
            return END
        elif verify_result == "revise" and state.get("revision_count", 0) < 3:
            return "draft_post"  # Revise the post
        elif state.get("revision_count", 0) >= 3:
            return END  # Max retries reached
        else:
            # Need verification
            return "verify"
    
    def enhanced_verify_wrapper(self, state: PostState) -> PostState:
        """
        Enhanced verification with supervisor oversight.
        """
        summary = state.get("summary", "")
        post = state.get("post", "")
        revision_count = state.get("revision_count", 0)
        
        # Run verification tools
        from api.services.tools import verify_technical_correctness, check_social_post_style
        tech_result = verify_technical_correctness.invoke(summary)
        style_result = check_social_post_style.invoke(post)
        
        # Supervisor evaluates the results
        verification_passed = tech_result == "pass" and style_result == "pass"
        max_retries_reached = revision_count >= 3
        
        if verification_passed:
            verify_result = "pass"
        elif max_retries_reached:
            # Supervisor decision: accept after max retries
            verify_result = "pass"
        else:
            verify_result = "revise"
        
        # Update state with verification results
        updated_state = {
            **state,
            "verify_result": verify_result,
            "revision_count": revision_count + 1,
            "tech_check": tech_result,
            "style_check": style_result
        }
        
        # Add supervisor status for monitoring
        supervisor_status = self.supervisor.get_workflow_status(updated_state)
        updated_state["supervisor_status"] = supervisor_status
        
        return updated_state
    
    def build_supervised_graph(self):
        """
        Build and compile the supervised LangGraph workflow.
        
        Returns:
            Compiled graph with supervisor pattern
        """
        # Create agents
        research_agent = self.agent_factory.get_research_agent()
        summarize_agent = self.agent_factory.get_summarize_agent()
        post_agent = self.agent_factory.get_post_agent()
        
        # Build graph with supervisor pattern
        graph = StateGraph(PostState)
        
        # Add agent nodes
        graph.add_node("research", research_agent)
        graph.add_node("summarize", summarize_agent)
        graph.add_node("draft_post", post_agent)
        graph.add_node("verify", self.enhanced_verify_wrapper)
        
        # Set entry point
        graph.set_entry_point("research")
        
        # Add sequential edges for the main flow
        graph.add_edge("research", "summarize")
        graph.add_edge("summarize", "draft_post")
        graph.add_edge("draft_post", "verify")
        
        # Add conditional edge from verify for revision loop
        graph.add_conditional_edges(
            "verify",
            self.supervisor_router,
            {
                "draft_post": "draft_post",
                END: END
            }
        )
        
        return graph.compile()
    
    def build_legacy_graph(self):
        """
        Build the original linear graph for comparison/fallback.
        
        Returns:
            Compiled graph with original linear workflow
        """
        # Create agents
        research_agent = self.agent_factory.get_research_agent()
        summarize_agent = self.agent_factory.get_summarize_agent()
        post_agent = self.agent_factory.get_post_agent()
        verify_node = self.agent_factory.get_verify_wrapper()
        
        # Build original linear graph
        graph = StateGraph(PostState)
        
        # Add nodes
        graph.add_node("research", research_agent)
        graph.add_node("summarize", summarize_agent)
        graph.add_node("draft_post", post_agent)
        graph.add_node("verify", verify_node)
        
        # Set entry point
        graph.set_entry_point("research")
        
        # Linear flow
        graph.add_edge("research", "summarize")
        graph.add_edge("summarize", "draft_post")
        graph.add_edge("draft_post", "verify")
        
        # Simple conditional edge
        def verify_output_router(state: PostState) -> Literal["draft_post", END]:
            """Route based on verification result."""
            return "draft_post" if state["verify_result"] == "revise" else END
        
        graph.add_conditional_edges("verify", verify_output_router, {
            "draft_post": "draft_post",
            END: END
        })
        
        return graph.compile() 