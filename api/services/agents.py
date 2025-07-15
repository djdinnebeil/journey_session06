from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from typing import List, Dict, Any
import os
from api.services.tools import mock_paper_lookup, verify_technical_correctness, check_social_post_style

class AgentFactory:
    def __init__(self):
        self.llm = None
    
    def _ensure_llm(self):
        """Ensure LLM is initialized with current API key"""
        # Always recreate LLM to get the current API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key must be set in environment variable OPENAI_API_KEY")
        self.llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
    
    def create_tool_agent(self, system_prompt: str, tools: List):
        """Create an agent that can use tools."""
        def agent_runner(state):
            # Initialize LLM with current API key when actually running
            self._ensure_llm()
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder("messages"),
                MessagesPlaceholder("agent_scratchpad"),
            ])
            agent = create_openai_functions_agent(llm=self.llm, tools=tools, prompt=prompt)
            executor = AgentExecutor(agent=agent, tools=tools)
            return executor.invoke(state)
        
        return RunnableLambda(agent_runner)

    def create_prompt_only_agent(self, system_prompt: str, output_key: str):
        """Create an agent that only uses prompts (no tools)."""
        def agent_runner(state: Dict[str, Any]):
            # Initialize LLM with current API key when actually running
            self._ensure_llm()
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ])
            chain = prompt | self.llm
            
            messages = state.get("messages", [])
            if not isinstance(messages, list):
                raise ValueError("Expected 'messages' to be a list")
            response = chain.invoke({"messages": messages})
            return {
                **state,
                output_key: response.content
            }
        
        return RunnableLambda(agent_runner)
    
    def get_research_agent(self):
        """Get the research agent."""
        return self.create_tool_agent(
            "You are a researcher. Use available tools to find ML paper content.", 
            [mock_paper_lookup]
        )
    
    def get_summarize_agent(self):
        """Get the summarization agent."""
        return self.create_prompt_only_agent(
            "You are a scientific summarizer. Generate a short, accurate summary.", 
            "summary"
        )
    
    def get_post_agent(self):
        """Get the social media post agent."""
        return self.create_prompt_only_agent(
            "You are a social media strategist. Write a LinkedIn post using the summary. "
            "The post MUST mention @AIMakerspace and MUST be under 300 characters. "
            "If you are revising, make sure to fix any issues with these requirements.",
            "post"
        )
    
    def get_verify_wrapper(self):
        """Get the verification wrapper function."""
        def verify_wrapper(state):
            summary = state.get("summary", "")
            post = state.get("post", "")
            tech_result = verify_technical_correctness.invoke(summary)
            style_result = check_social_post_style.invoke(post)
            revision_count = state.get("revision_count", 0)
            
            if tech_result == "pass" and style_result == "pass":
                verify_result = "pass"
            elif revision_count >= 3:
                verify_result = "pass"
            else:
                verify_result = "revise"
            
            return {
                **state,
                "verify_result": verify_result,
                "revision_count": revision_count + 1,
                "tech_check": tech_result,
                "style_check": style_result
            }
        
        return RunnableLambda(verify_wrapper) 