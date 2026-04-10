"""
SmartPredict AI — Chat Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.api.routes.upload import get_dataset_store
from app.api.routes.insights import get_insights_cache
from app.services.nlp_service import chat_with_data

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    dataset_id: int
    message: str


@router.post("/chat")
async def chat(request: ChatRequest):
    """Chat with the AI about your data."""
    
    datasets_store = get_dataset_store()
    
    if request.dataset_id not in datasets_store:
        raise HTTPException(status_code=404, detail="Dataset not found. Please upload a dataset first.")
    
    dataset = datasets_store[request.dataset_id]
    
    # Get recent insights if available
    insights_cache = get_insights_cache()
    recent_insights = insights_cache.get(request.dataset_id)
    
    try:
        result = await chat_with_data(
            question=request.message,
            data_summary=dataset["data_summary"],
            columns_info=dataset["columns_info"],
            recent_insights=recent_insights,
        )
        
        return result
        
    except Exception as e:
        return {
            "reply": "I'm having trouble processing that question. Could you try rephrasing it? You can ask about totals, trends, risks, or recommendations.",
            "suggestions": [
                "What are the main trends?",
                "Are there any risks?",
                "What should I focus on?",
            ],
        }
