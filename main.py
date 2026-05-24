from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import Config
from src.agents.verification_agent import SelfVerificationAgent, VerificationReport

app = FastAPI(
    title="PAMAS - Module 3 Verification Framework",
    version="1.0.0",
    description="Automated self-verification and retrieval-augmented validation extensions."
)

# Initialize our specialized agent
verification_agent = SelfVerificationAgent()

class VerificationRequest(BaseModel):
    draft_text: str
    target_format: str = "IEEE"

@app.get("/health")
def health_check():
    """Service health status endpoint."""
    return {"status": "online", "module": Config.MODULE_NAME}

@app.post("/api/v1/verify", response_model=VerificationReport)
async def verify_draft(request: VerificationRequest):
    """
    Ingests raw manuscript drafts and returns a structured validation evaluation.
    """
    if not request.draft_text.strip():
        raise HTTPException(status_code=400, detail="Manuscript draft content cannot be empty.")
        
    try:
        report = verification_agent.verify_manuscript(
            draft_text=request.draft_text, 
            target_format=request.target_format
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification agent error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Start the module server on a distinct port (8001) to avoid conflicts with Module 2
    uvicorn.run("main:app", host="0.0.0.0", port=Config.PORT, reload=True)
