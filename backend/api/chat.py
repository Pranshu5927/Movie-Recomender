from fastapi import APIRouter

from agents.schemas import ChatRequest, ChatResponse
from agents.recommendation_agent import handle_chat


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    return handle_chat(
        message=request.message,
        history=request.history
    )
