import os
from typing import Dict, Any, List, Literal, Optional
from langchain_core.messages import HumanMessage
from api.services.supervised_graph_builder import SupervisedGraphBuilder
from api.services.models import PostState

class SupervisedPostGeneratorService:
    """
    Enhanced post generator service using supervisor pattern.
    Provides better orchestration, error handling, and monitoring capabilities.
    """
    
    def __init__(self, use_supervisor: bool = True):
        """
        Initialize the service.
        
        Args:
            use_supervisor: Whether to use supervisor pattern (True) or legacy linear flow (False)
        """
        self.use_supervisor = use_supervisor
        self.graph_builder = SupervisedGraphBuilder()
        self._graph = None
    
    def _get_graph(self):
        """Get the appropriate graph (supervised or legacy)."""
        if self._graph is None:
            if self.use_supervisor:
                self._graph = self.graph_builder.build_supervised_graph()
            else:
                self._graph = self.graph_builder.build_legacy_graph()
        return self._graph
    
    async def generate_post(self, paper_title: str, **kwargs) -> Dict[str, Any]:
        """
        Generate a social media post for a given paper title using supervisor pattern.
        
        Args:
            paper_title: The title of the academic paper
            **kwargs: Additional options like max_retries, quality_threshold, etc.
            
        Returns:
            Dict containing the generated post and metadata including supervisor insights
        """
        graph = self._get_graph()
        
        input_messages = [
            HumanMessage(content=f"Please write a LinkedIn post about the paper '{paper_title}'")
        ]
        
        # Enhanced initial state
        initial_state = {
            "messages": input_messages, 
            "revision_count": 0,
            "supervisor_status": None
        }
        
        # Run the graph with supervisor orchestration
        try:
            result = graph.invoke(initial_state)
            
            # Extract supervisor insights if available
            supervisor_insights = self._extract_supervisor_insights(result)
            
            return {
                "summary": result.get("summary", ""),
                "post": result.get("post", ""),
                "verify_result": result.get("verify_result", ""),
                "revision_count": result.get("revision_count", 0),
                "tech_check": result.get("tech_check", ""),
                "style_check": result.get("style_check", ""),
                # Enhanced supervisor pattern data
                "supervisor_insights": supervisor_insights,
                "workflow_pattern": "supervised" if self.use_supervisor else "linear",
                "quality_metrics": self._calculate_quality_metrics(result)
            }
            
        except Exception as e:
            # Enhanced error handling with supervisor pattern
            return {
                "error": str(e),
                "summary": "",
                "post": "Error occurred during generation",
                "verify_result": "error",
                "revision_count": 0,
                "tech_check": "error",
                "style_check": "error",
                "supervisor_insights": {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "recovery_suggestions": self._get_recovery_suggestions(e)
                },
                "workflow_pattern": "supervised" if self.use_supervisor else "linear",
                "quality_metrics": {}
            }
    
    def _extract_supervisor_insights(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract insights from supervisor's workflow management.
        
        Args:
            result: Graph execution result
            
        Returns:
            Supervisor insights and workflow analytics
        """
        supervisor_status = result.get("supervisor_status", {})
        
        return {
            "completed_steps": supervisor_status.get("completed_steps", []),
            "workflow_efficiency": len(supervisor_status.get("completed_steps", [])) / 4.0,  # 4 total steps
            "revision_efficiency": 1.0 / max(1, result.get("revision_count", 1)),
            "verification_details": supervisor_status.get("verification_status", {}),
            "completion_reason": self._determine_completion_reason(result),
            "supervisor_decisions": supervisor_status.get("supervisor_decisions", [])
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
            return "unknown"
    
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
    
    def _get_recovery_suggestions(self, error: Exception) -> List[str]:
        """Get recovery suggestions based on error type."""
        suggestions = []
        
        if "API" in str(error) or "key" in str(error).lower():
            suggestions.append("Check OpenAI API key validity")
            suggestions.append("Verify API quota and billing")
        
        if "timeout" in str(error).lower():
            suggestions.append("Retry with shorter timeout")
            suggestions.append("Check network connectivity")
        
        if "model" in str(error).lower():
            suggestions.append("Try different model version")
            suggestions.append("Check model availability")
        
        if not suggestions:
            suggestions.append("Try again with different input")
            suggestions.append("Check system logs for details")
        
        return suggestions
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """
        Get current workflow configuration and capabilities.
        
        Returns:
            Workflow status information
        """
        return {
            "supervisor_enabled": self.use_supervisor,
            "pattern_type": "supervised" if self.use_supervisor else "linear",
            "capabilities": {
                "intelligent_routing": self.use_supervisor,
                "error_recovery": self.use_supervisor,
                "quality_monitoring": True,
                "adaptive_workflow": self.use_supervisor
            },
            "agent_count": 4,  # research, summarize, post, verify
            "supervisor_features": [
                "Dynamic routing",
                "Quality assessment",
                "Error handling",
                "Workflow optimization"
            ] if self.use_supervisor else []
        }
    
    def switch_pattern(self, use_supervisor: bool) -> bool:
        """
        Switch between supervisor and linear patterns.
        
        Args:
            use_supervisor: Whether to use supervisor pattern
            
        Returns:
            True if pattern was switched successfully
        """
        if self.use_supervisor != use_supervisor:
            self.use_supervisor = use_supervisor
            self._graph = None  # Force graph rebuild
            return True
        return False 