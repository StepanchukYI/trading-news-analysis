# Trading News Analysis Service

## Overview

This service provides news sentiment analysis for crypto trading signals. It ingests news articles, social media posts, and other textual content, then uses ML/NLP to extract sentiment and generate trading signals.

## Tech Stack

- **Python**: 3.11+
- **Framework**: FastAPI
- **ML/NLP**:
  - `transformers` - Hugging Face models for sentiment analysis
  - `torch` - PyTorch for model inference
  - `scikit-learn` - Additional ML utilities
- **Database**: PostgreSQL (via `asyncpg`)
- **Caching**: Redis
- **Logging**: `structlog`

## Architecture

```
trading-news-analysis/
├── src/app/
│   ├── api/
│   │   └── v1.py          # FastAPI routes (/api/v1/*)
│   ├── core/
│   │   └── config.py      # Configuration management
│   ├── services/
│   │   └── sentiment.py   # Sentiment analysis business logic
│   └── main.py            # Application entry point
├── tests/
│   └── test_api.py        # API tests
├── Dockerfile
└── pyproject.toml
```

### Key Components

- **`SentimentAnalyzer`** (`services/sentiment.py`): Core ML service for text sentiment analysis
- **API v1 routes** (`api/v1.py`):
  - `GET /api/v1/sentiment/{symbol}` - Get sentiment for trading symbol
  - `POST /api/v1/analyze` - Analyze arbitrary news text
- **FastAPI app** (`main.py`): HTTP server on port 8040

## Local Development

### Setup

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

### Running

```bash
# Direct (for development)
uvicorn app.main:app --reload

# With Docker
docker build -t trading-news-analysis .
docker run -p 8040:8040 trading-news-analysis
```

### Environment Variables

- `NEWS_DATABASE_URL` - PostgreSQL connection string
- `NEWS_REDIS_URL` - Redis connection string
- `NEWS_LOG_LEVEL` - Logging level (default: INFO)

## Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_api.py::test_health_check

# With coverage report
pytest --cov=app --cov-report=html
```

## API Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/sentiment/{symbol}` | GET | Get sentiment for symbol |
| `/api/v1/analyze` | POST | Analyze news text |

## Integration

- **Port**: 8040
- **Health check**: `GET /health`
- **Depends on**: PostgreSQL, Redis
- **Consumes**: News feeds (to be integrated)
- **Produces**: Sentiment signals (to trading-core)

## TODO

- [ ] Integrate Hugging Face sentiment model
- [ ] Add news feed ingestion
- [ ] Implement Redis caching for results
- [ ] Add comprehensive integration tests
- [ ] Document ML model training/update process
