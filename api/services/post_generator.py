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
            Dict containing the generated post and metadata with enhanced metrics
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
        
        # Calculate metrics for linear pattern
        linear_insights = self._calculate_linear_insights(result)
        quality_metrics = self._calculate_quality_metrics(result)
        
        return {
            "summary": result.get("summary", ""),
            "post": result.get("post", ""),
            "verify_result": result.get("verify_result", ""),
            "revision_count": result.get("revision_count", 0),
            "tech_check": result.get("tech_check", ""),
            "style_check": result.get("style_check", ""),
            # Enhanced linear pattern data
            "supervisor_insights": linear_insights,  # Using same field name for consistency
            "workflow_pattern": "linear",
            "quality_metrics": quality_metrics
        }
    
    def _calculate_linear_insights(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate workflow insights for the linear pattern.
        
        Args:
            result: Graph execution result
            
        Returns:
            Linear workflow insights
        """
        # Determine completed steps based on result data
        completed_steps = []
        if result.get("summary"):
            completed_steps.extend(["research", "summarize"])
        if result.get("post"):
            completed_steps.append("post")
        if result.get("verify_result"):
            completed_steps.append("verify")
        
        return {
            "completed_steps": completed_steps,
            "workflow_efficiency": len(completed_steps) / 4.0,  # 4 total steps
            "revision_efficiency": 1.0 / max(1, result.get("revision_count", 1)),
            "completion_reason": self._determine_completion_reason(result),
            "workflow_type": "linear_sequential"
        }
    
    def _calculate_quality_metrics(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate quality metrics for the generated content.
        
        Args:
            result: Graph execution result
            
        Returns:
            Quality metrics
        """
        post = result.get("post", "")
        summary = result.get("summary", "")
        
        return {
            "post_length": len(post),
            "summary_length": len(summary),
            "character_efficiency": len(post) / 300.0 if post else 0,  # Target 300 chars
            "mention_compliance": "@AIMakerspace" in post if post else False,
            "technical_accuracy": result.get("tech_check") == "pass",
            "style_compliance": result.get("style_check") == "pass",
            "overall_quality": self._calculate_overall_quality(result)
        }
    
    def _determine_completion_reason(self, result: Dict[str, Any]) -> str:
        """Determine why the workflow completed."""
        if result.get("verify_result") == "pass" and result.get("revision_count", 0) == 1:
            return "perfect_first_attempt"
        elif result.get("verify_result") == "pass":
            return "quality_achieved"
        elif result.get("revision_count", 0) >= 3:
            return "max_retries_reached"
        else:
            return "completed_successfully"
    
    def _calculate_overall_quality(self, result: Dict[str, Any]) -> float:
        """Calculate overall quality score (0-1)."""
        factors = [
            result.get("tech_check") == "pass",
            result.get("style_check") == "pass",
            result.get("revision_count", 0) <= 2,
            "@AIMakerspace" in result.get("post", ""),
            50 <= len(result.get("post", "")) <= 300
        ]
        return sum(factors) / len(factors) 