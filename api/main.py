from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from api.services.post_generator import PostGeneratorService

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Social Media Post Generator", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service will be initialized per request

class PostRequest(BaseModel):
    paper_title: str
    openai_api_key: str

class PostResponse(BaseModel):
    summary: str
    post: str
    verify_result: str
    revision_count: int
    tech_check: str
    style_check: str

@app.get("/")
async def root():
    return {"message": "AI Social Media Post Generator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/generate-post", response_model=PostResponse)
async def generate_post(request: PostRequest):
    try:
        # Validate OpenAI API key from request
        if not request.openai_api_key or not request.openai_api_key.strip():
            raise HTTPException(status_code=400, detail="OpenAI API key is required")
        
        # Set the API key for this request
        os.environ["OPENAI_API_KEY"] = request.openai_api_key
        
        # Create service instance for this request
        post_generator = PostGeneratorService()
        result = await post_generator.generate_post(request.paper_title)
        return PostResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating post: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 