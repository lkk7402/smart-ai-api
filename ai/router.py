from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models import User, UsageLog
from schemas import (
    SummariseRequest,
    SummariseResponse,
    ChatRequest,
    ChatResponse,
    SentimentRequest,
    SentimentResponse,
)
from auth.utils import get_current_user
from ai.groq_client import GroqClient, get_groq_client
from middleware.rate_limit import limiter

router = APIRouter(prefix="/ai", tags=["ai"])


def _log_usage(db: Session, user_id: int, endpoint: str) -> None:
    log = UsageLog(user_id=user_id, endpoint=endpoint)
    db.add(log)
    db.commit()


@router.post("/summarise", response_model=SummariseResponse)
@limiter.limit("10/minute")
def summarise(
    request: Request,
    body: SummariseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    groq_client: GroqClient = Depends(get_groq_client),
):
    summary = groq_client.summarise(body.text)
    _log_usage(db, current_user.id, "summarise")
    return {"summary": summary}


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
def chat(
    request: Request,
    body: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    groq_client: GroqClient = Depends(get_groq_client),
):
    messages = [{"role": m.role, "content": m.content} for m in body.messages]
    reply = groq_client.chat(messages)
    _log_usage(db, current_user.id, "chat")
    return {"reply": reply}


@router.post("/sentiment", response_model=SentimentResponse)
@limiter.limit("10/minute")
def sentiment(
    request: Request,
    body: SentimentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    groq_client: GroqClient = Depends(get_groq_client),
):
    result = groq_client.sentiment(body.text)
    _log_usage(db, current_user.id, "sentiment")
    return result
