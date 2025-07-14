import os
from typing import Dict, Any, List, Literal
from langchain_core.messages import HumanMessage
from api.services.graph_builder import GraphBuilder
from api.services.models import PostState

class PostGeneratorService:
    def __init__(self):
        pass
    
    async def generate_post(self, paper_title: str) -> Dict[str, Any]:
        """
        Generate a social media post for a given paper title.
        
        Args:
            paper_title: The title of the academic paper
            
        Returns:
            Dict containing the generated post and metadata
        """
        # Create graph for this request (after API key is set)
        graph_builder = GraphBuilder()
        graph = graph_builder.build_graph()
        
        input_messages = [
            HumanMessage(content=f"Please write a LinkedIn post about the paper '{paper_title}'")
        ]
        
        # Run the graph
        result = graph.invoke({
            "messages": input_messages, 
            "revision_count": 0
        })
        
        return {
            "summary": result.get("summary", ""),
            "post": result.get("post", ""),
            "verify_result": result.get("verify_result", ""),
            "revision_count": result.get("revision_count", 0),
            "tech_check": result.get("tech_check", ""),
            "style_check": result.get("style_check", "")
        } 