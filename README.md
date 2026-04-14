# Smart AI API

A production-ready AI REST API microservice built with FastAPI, PostgreSQL, and Groq AI. Features JWT authentication, per-user rate limiting, and full test coverage.

**Live API:** https://smart-ai-api-c1bp.onrender.com/docs

---

## Features

- **JWT Authentication** — secure register/login with bcrypt password hashing
- **AI Endpoints** — text summarisation, multi-turn chat, and sentiment analysis powered by Groq (Llama 3)
- **Rate Limiting** — 10 requests/minute per user on all AI endpoints
- **PostgreSQL** — SQLAlchemy ORM with per-user usage tracking
- **Docker** — fully containerised with docker-compose (API + database)
- **CI/CD** — GitHub Actions runs the full test suite on every push
- **15 pytest tests** — 80%+ coverage with mocked AI client

---

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | No | Create account, returns JWT |
| POST | `/auth/login` | No | Login, returns JWT |
| POST | `/ai/summarise` | Yes | Summarise any text |
| POST | `/ai/chat` | Yes | Multi-turn conversation |
| POST | `/ai/sentiment` | Yes | Sentiment analysis |
| GET | `/usage` | Yes | Your API usage stats |

---

## Tech Stack

- **FastAPI** — Python web framework
- **PostgreSQL** + SQLAlchemy — database and ORM
- **python-jose** — JWT token creation and validation
- **passlib + bcrypt** — password hashing
- **Groq** — LLM inference (Llama 3.1 8B)
- **slowapi** — rate limiting
- **pytest + httpx** — testing
- **Docker + docker-compose** — containerisation
- **GitHub Actions** — CI pipeline
- **Render** — cloud deployment

---

## Run Locally

**1. Clone and install:**
```bash
git clone https://github.com/lkk7402/smart-ai-api.git
cd smart-ai-api
pip install -r requirements.txt
```

**2. Create a `.env` file:**
```
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**3. Start the server:**
```bash
uvicorn main:app --reload
```

Open `http://localhost:8000/docs` for the interactive API docs.

---

## Run with Docker

```bash
docker-compose up --build
```

API available at `http://localhost:8000/docs`

---

## Run Tests

```bash
pytest tests/ -v
```

---

## Project Structure

```
smart-ai-api/
├── main.py                  # App entry point
├── database.py              # SQLAlchemy engine and session
├── models.py                # Database models
├── schemas.py               # Pydantic schemas
├── auth/
│   ├── router.py            # /auth endpoints
│   └── utils.py             # JWT and password utilities
├── ai/
│   ├── router.py            # /ai endpoints
│   └── groq_client.py       # Groq API wrapper
├── routes/
│   └── usage.py             # /usage endpoint
├── middleware/
│   └── rate_limit.py        # Rate limiter setup
├── tests/                   # Full test suite
├── Dockerfile
└── docker-compose.yml
```
