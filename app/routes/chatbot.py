from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.logic.advisor import advise

router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
def ask_bot(request: ChatRequest):
    answer = advise(request.query)
    return {"response": answer}
