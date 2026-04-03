# Trading News Analysis Service

## Overview

This service provides news sentiment analysis for crypto trading signals. It ingests news articles, social media posts, and other textual content, then uses ML/NLP to extract sentiment and generate trading signals.

**Owner:** ML Engineer
**Port:** 8040
**Stack:** Python 3.11 · FastAPI · Transformers/Torch · PostgreSQL · Redis

---

## Tech Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Web framework | FastAPI 0.115+ | Async HTTP API |
| ASGI server | Uvicorn | Production server |
| ML/NLP | `transformers`, `torch`, `scikit-learn` | Sentiment analysis |
| DB | `asyncpg` | PostgreSQL async driver |
| Config | `pydantic-settings` | Environment-based settings |
| Logging | `structlog` | Structured logging |

**Python:** 3.11+ (enforced in `pyproject.toml` and Dockerfile)

---

## Architecture

```
trading-news-analysis/
├── src/app/
│   ├── api/
│   │   └── v1.py              # FastAPI v1 routes
│   ├── core/
│   │   └── config.py          # Pydantic Settings (env prefix: NEWS_)
│   ├── services/
│   │   └── sentiment.py       # SentimentAnalyzer (stub)
│   └── main.py                # FastAPI app entry point
├── tests/
│   └── test_api.py            # TestClient tests
├── Dockerfile
├── pyproject.toml
└── CLAUDE.md
```

### Data Flow

```
News Sources → Ingestion (TODO) → SentimentAnalyzer → Redis Cache (TODO) → PostgreSQL
                                        ↓
                               Trading Core (:8010)
```

### Key Components

| Component | Path | Responsibility |
|-----------|------|----------------|
| `SentimentAnalyzer` | `src/app/services/sentiment.py` | Core ML service — stub returning uniform sentiment scores |
| `Settings` | `src/app/core/config.py` | Env config with `NEWS_` prefix (database_url, redis_url, log_level) |
| API v1 router | `src/app/api/v1.py` | `/api/v1/sentiment/{symbol}`, `/api/v1/analyze` |
| FastAPI app | `src/app/main.py` | App factory, `/health`, startup logger |

### SentimentResponse Schema

```python
{
    "sentiment": str,      # "positive" | "negative" | "neutral"
    "score": float,        # Raw sentiment score (-1.0 to 1.0)
    "confidence": float     # Model confidence (0.0 to 1.0)
}
```

---

## Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL (or set `NEWS_DATABASE_URL`)
- Redis (or set `NEWS_REDIS_URL`)

### Setup

```bash
# Clone and enter repo
cd services/trading-news-analysis

# Install with dev deps
pip install -e ".[dev]"

# Lint
ruff check .

# Type-check
mypy .
```

### Running

```bash
# Direct (development — reload enabled)
uvicorn app.main:app --reload --port 8040

# With Docker
docker build -t trading-news-analysis .
docker run -p 8040:8040 trading-news-analysis
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEWS_DATABASE_URL` | `postgresql://localhost/trading_news` | PostgreSQL DSN |
| `NEWS_REDIS_URL` | `redis://localhost/2` | Redis DSN |
| `NEWS_LOG_LEVEL` | `INFO` | Logging level |

---

## Testing

```bash
# All tests
pytest

# Specific test
pytest tests/test_api.py::test_health_check

# With coverage
pytest --cov=app --cov-report=html
```

**Current test coverage:** `test_health_check` only — `test_sentiment_endpoint` and `test_analyze_endpoint` stubs exist but are not yet implemented.

---

## API Reference

### Endpoints

| Method | Path | Description | Response |
|--------|------|-------------|----------|
| `GET` | `/health` | Liveness probe | `{"status": "healthy"}` |
| `GET` | `/api/v1/sentiment/{symbol}` | Sentiment for trading symbol | `SentimentResponse` |
| `POST` | `/api/v1/analyze` | Analyze arbitrary text | `SentimentResponse` |

All responses: `200 OK` with JSON body.

---

## Integration

- **Port:** 8040 (internal)
- **Health check:** `GET /health`
- **Depends on:** PostgreSQL, Redis
- **Consumes:** News feeds (to be integrated)
- **Produces:** Sentiment signals → Trading Core (:8010) via REST

### Cross-Service Contract (TODO)

```
POST /api/v1/analyze
Body: {"text": "BTC surge expected after ETF approval"}
Response: {"sentiment": "positive", "score": 0.82, "confidence": 0.91}
```

---

## ML/NLP Notes

- `SentimentAnalyzer` is a **stub** — returns uniform `0.33/0.33/0.34` distribution
- HuggingFace `transformers` and `torch` are installed but not yet wired up
- Next step: integrate a fine-tuned crypto-sentiment model (e.g., `Elulalysis/crypto-sentiment` or custom)
- Model loading should happen in `on_event("startup")` to warm the model before first request

---

## Tooling

| Tool | Config | Strictness |
|------|--------|------------|
| `ruff` | `pyproject.toml` | PEP 8, py311 target |
| `mypy` | `pyproject.toml` | strict mode enabled |
| `pytest` | `pyproject.toml` | `asyncio_mode = auto` |

---

## TODO

- [ ] Integrate Hugging Face sentiment model into `SentimentAnalyzer`
- [ ] Add news feed ingestion pipeline
- [ ] Implement Redis caching for sentiment results
- [ ] Add `test_sentiment_endpoint` and `test_analyze_endpoint`
- [ ] Document ML model training/update process
- [ ] Wire up `Settings` (currently imported but not used in routes)
