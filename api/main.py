from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from api.services.post_generator import PostGeneratorService
from api.services.supervised_post_generator import SupervisedPostGeneratorService

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Social Media Post Generator", version="2.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostRequest(BaseModel):
    paper_title: str
    openai_api_key: str
    use_supervisor: bool = True  # Default to supervisor pattern

class PostResponse(BaseModel):
    summary: str
    post: str
    verify_result: str
    revision_count: int
    tech_check: str
    style_check: str
    # Enhanced fields for supervisor pattern
    supervisor_insights: dict = {}
    workflow_pattern: str = "supervised"
    quality_metrics: dict = {}

@app.get("/")
@app.get("/api/")
async def root():
    return {"message": "AI Social Media Post Generator API v2.0 - Now with Supervisor Pattern!"}

@app.get("/health")
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0", "features": ["supervisor_pattern", "enhanced_monitoring"]}

@app.get("/workflow-info")
@app.get("/api/workflow-info")
async def workflow_info(use_supervisor: bool = Query(True, description="Whether to use supervisor pattern")):
    """Get information about the available workflow patterns."""
    if use_supervisor:
        service = SupervisedPostGeneratorService(use_supervisor=True)
        return {
            "pattern": "supervisor",
            "description": "AI supervisor coordinates specialized agents for optimal workflow",
            "benefits": [
                "Intelligent routing and decision making",
                "Enhanced error handling and recovery",
                "Quality monitoring and optimization",
                "Adaptive workflow based on content quality"
            ],
            "status": service.get_workflow_status()
        }
    else:
        return {
            "pattern": "linear", 
            "description": "Sequential execution of agents in fixed order",
            "benefits": [
                "Simple and predictable workflow",
                "Lower computational overhead",
                "Easier debugging and monitoring"
            ],
            "status": {"pattern_type": "linear", "supervisor_enabled": False}
        }

@app.post("/generate-post", response_model=PostResponse)
@app.post("/api/generate-post", response_model=PostResponse)
async def generate_post(request: PostRequest):
    """Generate a social media post using supervisor or linear pattern."""
    try:
        # Validate OpenAI API key from request
        if not request.openai_api_key or not request.openai_api_key.strip():
            raise HTTPException(status_code=400, detail="OpenAI API key is required")
        
        # Set the API key for this request
        os.environ["OPENAI_API_KEY"] = request.openai_api_key
        
        # Choose service based on request
        if request.use_supervisor:
            # Use enhanced supervisor pattern service
            post_generator = SupervisedPostGeneratorService(use_supervisor=True)
            result = await post_generator.generate_post(request.paper_title)
        else:
            # Use legacy linear service
            post_generator = PostGeneratorService()
            result = await post_generator.generate_post(request.paper_title)
            
            # Add missing fields for compatibility
            result.setdefault("supervisor_insights", {})
            result.setdefault("workflow_pattern", "linear")
            result.setdefault("quality_metrics", {})
        
        return PostResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating post: {str(e)}")

@app.post("/generate-post-legacy", response_model=PostResponse)
@app.post("/api/generate-post-legacy", response_model=PostResponse)
async def generate_post_legacy(request: PostRequest):
    """Generate a post using the original linear workflow (for comparison)."""
    try:
        # Validate OpenAI API key
        if not request.openai_api_key or not request.openai_api_key.strip():
            raise HTTPException(status_code=400, detail="OpenAI API key is required")
        
        # Set the API key
        os.environ["OPENAI_API_KEY"] = request.openai_api_key
        
        # Force legacy service
        post_generator = PostGeneratorService()
        result = await post_generator.generate_post(request.paper_title)
        
        # Add compatibility fields
        result.setdefault("supervisor_insights", {"note": "Legacy workflow - no supervisor insights"})
        result.setdefault("workflow_pattern", "linear")
        result.setdefault("quality_metrics", {"note": "Legacy workflow - limited metrics"})
        
        return PostResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating post: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 