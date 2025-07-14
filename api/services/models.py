from typing import TypedDict, List, Literal

class PostState(TypedDict):
    messages: List
    summary: str
    post: str
    verify_result: Literal["pass", "revise"]
    revision_count: int
    tech_check: str
    style_check: str 