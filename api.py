from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestrator import run_research_pipeline
import uvicorn

app = FastAPI(
    title="Multi-Agent Research API",
    description="RAG-powered research system using Groq + Tavily + ChromaDB",
    version="1.0.0"
)

class ResearchRequest(BaseModel):
    topic: str
    num_results: int = 10

class ResearchResponse(BaseModel):
    topic:        str
    total_sources: int
    total_chunks:  int
    report:        str

@app.get("/")
def root():
    return {
        "message": "Multi-Agent Research API is running!",
        "endpoints": {
            "POST /research": "Run full research pipeline",
            "GET /health":    "Check API health"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/research", response_model=ResearchResponse)
def run_research(request: ResearchRequest):
    if not request.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="Topic cannot be empty"
        )

    try:
        result = run_research_pipeline(request.topic)
        return ResearchResponse(
            topic=result["topic"],
            total_sources=len(result["sources"]),
            total_chunks=result["total_chunks"],
            report=result["report"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)