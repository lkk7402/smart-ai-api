from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from database import engine, Base
from auth.router import router as auth_router
from ai.router import router as ai_router
from routes.usage import router as usage_router
from middleware.rate_limit import limiter

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart AI API",
    description=(
        "A production-ready AI microservice with JWT authentication, "
        "per-user rate limiting, and Groq AI integration."
    ),
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router)
app.include_router(ai_router)
app.include_router(usage_router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "version": "1.0.0"}
