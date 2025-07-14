from langchain.tools import tool

@tool
def mock_paper_lookup(title: str) -> str:
    """Simulate paper retrieval and return a short abstract."""
    return (
        "LoRA is a low-rank adaptation technique for fine-tuning large language models. "
        "It enables efficient training by injecting low-rank matrices into transformer weights."
    )

@tool
def verify_technical_correctness(summary: str) -> str:
    """Returns 'pass' or 'revise' for technical accuracy (simulated)."""
    return "pass" if "LoRA" in summary else "revise"

@tool
def check_social_post_style(post: str) -> str:
    """Check post for platform-appropriate style. Simulated."""
    if len(post) > 300 or "@AIMakerspace" not in post:
        return "revise"
    return "pass" 