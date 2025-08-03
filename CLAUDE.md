# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Commodities Compass is a Business Intelligence application for commodities trading, providing real-time market insights, technical analysis, and trading signals. This is a monorepo with a FastAPI backend and React frontend, using Auth0 for authentication and transitioning from Google Sheets to PostgreSQL for data storage.

## Development Commands

### Monorepo Commands (from root)

- `npm run install:all` - Install all dependencies (root, backend, frontend)
- `npm run dev` - Start both backend and frontend in development mode
- `npm run dev:backend` - Start only backend (<http://localhost:8000>)
- `npm run dev:frontend` - Start only frontend (<http://localhost:5173>)
- `npm run db:up` - Start PostgreSQL (port 5433) and Redis (port 6380) containers
- `npm run db:down` - Stop database containers
- `npm run lint` - Run linting for both projects
- `npm run format` - Format code for both projects
- `npm run test` - Run tests for both projects

### Backend Commands (from backend/)

- `poetry run dev` - Start FastAPI development server
- `poetry run lint` - Run pre-commit hooks (ruff, pyright)
- `poetry install` - Install Python dependencies
- `poetry run alembic upgrade head` - Run database migrations
- `poetry run pytest` - Run backend tests

### Frontend Commands (from frontend/)

- `npm run dev` - Start Vite development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run format` - Run Prettier

## Architecture

### Backend (FastAPI)

The backend follows a modular FastAPI structure:

- **`app/main.py`** - FastAPI application entry point with CORS, exception handling
- **`app/core/`** - Core functionality:
  - `config.py` - Pydantic settings with environment variable management
  - `auth.py` - Auth0 JWT token verification and user extraction
  - `database.py` - Async SQLAlchemy setup with PostgreSQL
- **`app/api/api_v1/`** - API endpoints organized by domain
- **`app/models/`** - SQLAlchemy database models:
  - `trading.py` - Core trading models (Technicals, Indicator, MarketResearch, etc.)
- **`app/schemas/`** - Pydantic request/response models (to be created)
- **`app/services/`** - Business logic layer:
  - `data_import.py` - Excel to PostgreSQL ETL service
- **`app/core/excel_mappings.py`** - Excel column to database mapping configuration

### Frontend (React + TypeScript)

The frontend uses modern React patterns:

- **Auth0 Integration** - `main.tsx` sets up Auth0Provider with shared environment variables
- **API Layer** - `src/api/` contains axios client with automatic token injection
- **State Management** - React Query (TanStack Query) for server state
- **Routing** - React Router with protected routes requiring authentication
- **UI Components** - Shadcn/ui components in `src/components/ui/`
- **Legacy Components** - Existing UI in `src/polymet/` (to be migrated)

### Environment Configuration

Environment variables are organized in three levels:

- **Root `.env`** - Shared variables (Auth0, ports, debug settings)
- **Backend `.env`** - Backend-specific (database, APIs, Google Sheets)
- **Frontend `.env`** - Frontend-specific (redirect URIs, API base URL)

Frontend code uses shared Auth0 variables (not VITE_ prefixed) from root .env.

### Database Setup

- PostgreSQL runs on custom port 5433 (not default 5432) via Docker
- Redis runs on custom port 6380 (not default 6379) via Docker
- Database URL: `postgresql+asyncpg://postgres:password@localhost:5433/commodities_compass`
- Async SQLAlchemy with asyncpg driver for performance

### Authentication Flow

1. Frontend uses Auth0 SPA client with React SDK
2. Tokens stored in localStorage and automatically added to API requests
3. Backend validates JWT tokens using Auth0's JWKS endpoint
4. User permissions extracted from token claims for role-based access

## Data Pipeline

The application transitions from Google Sheets to PostgreSQL:

1. Excel data analysis completed with schema mapping
2. ETL pipeline implemented in `app/services/data_import.py`
3. Database models created for:
   - **Technicals**: OHLCV data with 40+ technical indicators (RSI, MACD, ATR, Bollinger Bands, etc.)
   - **Indicator**: Normalized indicators and trading signals
   - **MarketResearch**: Research articles and market impact analysis
   - **WeatherData**: Agricultural weather data affecting commodity prices
   - **Config**: Trading algorithm configuration parameters
   - **PerformanceTracking**: Strategy performance metrics
   - **Podcast**: Aggregated market commentary
4. Excel to database column mapping defined in `app/core/excel_mappings.py`

## Code Quality

- **Backend**: Ruff for linting/formatting, Pyright for type checking
- **Frontend**: ESLint + Prettier for code quality
- **Pre-commit**: Hooks run on backend files only (scoped to `^backend/`)
- **Poetry**: Python dependency management with application mode (`package-mode = false`)

## API Structure

All API endpoints are prefixed with `/v1` and include:

- `/auth/*` - Authentication endpoints
- `/dashboard/*` - Trading dashboard data
- `/commodities/*` - Commodity information
- `/historical/*` - Historical data and indicators

## Development Notes

- Backend uses Poetry scripts: `poetry run dev` and `poetry run lint`
- Frontend environment variables must be accessible to Vite (no VITE_ prefix needed due to custom setup)
- Database migrations managed via Alembic (models ready for initial migration)
- Pre-commit hooks are configured to run only on backend Python files to avoid conflicts with monorepo structure
