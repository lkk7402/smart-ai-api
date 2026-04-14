from pydantic import BaseModel, EmailStr
from typing import List, Optional


# --- Auth ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# --- AI ---

class SummariseRequest(BaseModel):
    text: str


class SummariseResponse(BaseModel):
    summary: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: str


class SentimentRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    sentiment: str
    score: float
    explanation: str


# --- Usage ---

class EndpointUsage(BaseModel):
    endpoint: str
    count: int


class UsageStatsResponse(BaseModel):
    total: int
    breakdown: List[EndpointUsage]
