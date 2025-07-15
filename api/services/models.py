from typing import TypedDict, List, Literal, Dict, Any, Optional

class PostState(TypedDict):
    messages: List
    summary: str
    post: str
    verify_result: Literal["pass", "revise"]
    revision_count: int
    tech_check: str
    style_check: str
    # Supervisor pattern enhancements
    supervisor_status: Optional[Dict[str, Any]] 