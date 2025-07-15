from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain.tools import tool
from typing import List, Dict, Any, Literal
import os
from api.services.tools import mock_paper_lookup, verify_technical_correctness, check_social_post_style

class SupervisorAgent:
    """
    Supervisor agent that coordinates the entire post generation workflow.
    Uses LangGraph's supervisor pattern for better orchestration and error handling.
    """
    
    def __init__(self):
        self.llm = None
        self.supervisor = None
    
    def _ensure_llm(self):
        """Ensure LLM is initialized with current API key"""
        # Always recreate LLM to get the current API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key must be set in environment variable OPENAI_API_KEY")
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)
    
    def _create_supervisor(self):
        """Create the supervisor agent that routes tasks to appropriate agents."""
        @tool
        def route_to_agent(agent_name: str, reasoning: str) -> str:
            """
            Route the current task to the specified agent.
            
            Args:
                agent_name: The name of the agent to route to ('research', 'summarize', 'post', 'verify', 'complete')
                reasoning: Brief explanation of why this agent was chosen
            
            Returns:
                Confirmation message
            """
            return f"Routing to {agent_name}: {reasoning}"
        
        system_prompt = """You are a supervisor managing a team of AI agents for generating social media posts from academic papers.

Your team consists of:
1. RESEARCH agent - Finds and retrieves academic paper content
2. SUMMARIZE agent - Creates concise, accurate summaries
3. POST agent - Writes engaging LinkedIn posts with @AIMakerspace mention
4. VERIFY agent - Checks technical accuracy and style compliance

Your responsibilities:
- Route tasks to the most appropriate agent based on current state
- Monitor progress and decide on next steps
- Handle errors and coordinate retries
- Ensure quality standards are met
- Make final decisions on completion

Current workflow state information will be provided. Analyze the state and decide which agent should handle the next step.

Use the route_to_agent tool to make routing decisions. Consider:
- What has been completed already
- What information is missing or needs improvement
- Whether quality checks have passed
- If retry limits have been reached

Always provide clear reasoning for your routing decisions."""

        self._ensure_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("messages"),
            MessagesPlaceholder("agent_scratchpad"),
        ])
        
        agent = create_openai_functions_agent(
            llm=self.llm, 
            tools=[route_to_agent], 
            prompt=prompt
        )
        self.supervisor = AgentExecutor(agent=agent, tools=[route_to_agent])
    
    def route_next_agent(self, state: Dict[str, Any]) -> Literal["research", "summarize", "post", "verify", "complete"]:
        """
        Use the supervisor to determine the next agent to execute.
        
        Args:
            state: Current workflow state
            
        Returns:
            Name of the next agent to execute
        """
        # Only create supervisor when actually needed (when API key is available)
        if self.supervisor is None:
            try:
                self._create_supervisor()
            except ValueError:
                # If no API key available, use simple logic
                return self._simple_routing_logic(state)
        
        # Create status message for supervisor
        status_parts = []
        
        # Check what's been completed
        if state.get("summary"):
            status_parts.append("✅ Research and summary completed")
        else:
            status_parts.append("❌ No summary yet - need research")
            
        if state.get("post"):
            status_parts.append(f"✅ Post drafted (length: {len(state.get('post', ''))} chars)")
        else:
            status_parts.append("❌ No post yet")
            
        if state.get("verify_result"):
            tech_check = state.get("tech_check", "unknown")
            style_check = state.get("style_check", "unknown")
            revision_count = state.get("revision_count", 0)
            status_parts.append(f"✅ Verification done: tech={tech_check}, style={style_check}, revisions={revision_count}")
        else:
            status_parts.append("❌ Not verified yet")
        
        status_message = "Current workflow status:\n" + "\n".join(status_parts)
        
        # Get supervisor's routing decision
        from langchain_core.messages import HumanMessage
        try:
            response = self.supervisor.invoke({
                "messages": [HumanMessage(content=status_message)]
            })
            
            # Extract agent name from response
            response_text = response["output"].lower()
            
            if "research" in response_text:
                return "research"
            elif "summarize" in response_text:
                return "summarize"
            elif "post" in response_text:
                return "post"
            elif "verify" in response_text:
                return "verify"
            else:
                return "complete"
        except Exception:
            # Fallback to simple logic if supervisor fails
            return self._simple_routing_logic(state)
    
    def _simple_routing_logic(self, state: Dict[str, Any]) -> Literal["research", "summarize", "post", "verify", "complete"]:
        """Simple routing logic fallback when supervisor is not available."""
        if not state.get("summary"):
            return "research"
        elif not state.get("post"):
            return "post"
        elif not state.get("verify_result"):
            return "verify"
        else:
            return "complete"
    
    def should_continue(self, state: Dict[str, Any]) -> bool:
        """
        Supervisor decision on whether to continue the workflow.
        
        Args:
            state: Current workflow state
            
        Returns:
            True if workflow should continue, False if complete
        """
        # Check completion criteria
        verify_result = state.get("verify_result")
        revision_count = state.get("revision_count", 0)
        
        # Complete if verification passed or max retries reached
        if verify_result == "pass":
            return False
        elif revision_count >= 3:
            return False
        elif not state.get("summary"):
            return True  # Still need basic content
        elif not state.get("post"):
            return True  # Still need post
        else:
            return True  # Need verification or revision
    
    def get_workflow_status(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive workflow status for monitoring.
        
        Args:
            state: Current workflow state
            
        Returns:
            Status information
        """
        return {
            "completed_steps": [
                step for step, condition in [
                    ("research", bool(state.get("summary"))),
                    ("summarize", bool(state.get("summary"))),
                    ("post", bool(state.get("post"))),
                    ("verify", bool(state.get("verify_result")))
                ] if condition
            ],
            "current_revision": state.get("revision_count", 0),
            "verification_status": {
                "tech_check": state.get("tech_check", "not_done"),
                "style_check": state.get("style_check", "not_done"),
                "overall": state.get("verify_result", "not_done")
            },
            "ready_for_completion": not self.should_continue(state)
        } 