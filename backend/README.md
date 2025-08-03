# Commodities Compass Backend

FastAPI backend for the Commodities Compass trading analysis platform.

## Setup

### Prerequisites
- Python 3.11+
- Poetry (for dependency management)
- Docker (for PostgreSQL and Redis)
- Auth0 account for authentication

### Installation

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start PostgreSQL and Redis:
```bash
# From project root
npm run db:up
```

6. Run database migrations (once we create them):
```bash
poetry run alembic upgrade head
```

### Auth0 Setup

1. Create an Auth0 application (Single Page Application)
2. Create an API in Auth0
3. Update `.env` with:
   - AUTH0_DOMAIN
   - AUTH0_API_AUDIENCE
   - AUTH0_ISSUER

### Running the Application

Development mode:
```bash
poetry run dev
```

Production mode:
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core functionality (auth, config, db)
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── utils/         # Utilities
├── scripts/           # Data import and maintenance scripts
├── tests/             # Test files
└── alembic/           # Database migrations
```

## Testing

Run tests:
```bash
poetry run pytest
```

With coverage:
```bash
poetry run pytest --cov=app tests/
```

## Code Quality

Run linting and pre-commit hooks:
```bash
poetry run lint
```

Format code manually:
```bash
poetry run black .
poetry run isort .
```
