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

The backend follows a clean architecture with separation of concerns:

- **`app/main.py`** - FastAPI application entry point with CORS, exception handling
- **`app/core/`** - Core functionality:
  - `config.py` - Pydantic settings with environment variable management
  - `auth.py` - Auth0 JWT token verification and user extraction
  - `database.py` - Async SQLAlchemy setup with PostgreSQL
  - `excel_mappings.py` - Excel column to database mapping configuration
- **`app/api/api_v1/`** - Clean API endpoints focused on HTTP concerns
  - `endpoints/dashboard.py` - Streamlined dashboard endpoints (390 lines)
- **`app/models/`** - SQLAlchemy database models split by domain:
  - `technicals.py` - Technical analysis data
  - `indicator.py` - Normalized indicators and trading signals
  - `market_research.py` - Market research articles
  - `weather_data.py` - Weather impact data
  - `test_range.py` - Indicator color ranges
- **`app/schemas/`** - Pydantic request/response models for API responses
- **`app/services/`** - Business logic layer (service-oriented architecture):
  - `data_import.py` - Excel to PostgreSQL ETL service
  - `dashboard_service.py` - Pure business logic for dashboard operations
  - `dashboard_transformers.py` - Data transformation between models and API responses
- **`app/utils/`** - Reusable utility functions:
  - `date_utils.py` - Date parsing, validation, and business date conversion

### Frontend (React + TypeScript)

The frontend uses modern React patterns:

- **Auth0 Integration** - `main.tsx` sets up Auth0Provider with shared environment variables
- **API Layer** - `src/api/` contains axios client with automatic token injection
- **State Management** - React Query (TanStack Query) for server state
- **Routing** - React Router with protected routes requiring authentication
- **UI Components** - Shadcn/ui components in `src/components/ui/`
- **Dashboard Components**:
  - `PositionStatus` - YTD performance with color-coded position badges
  - `IndicatorsGrid` - Dynamic gauge indicators with color ranges
  - `RecommendationsList` - Parsed recommendations from database
  - `PriceChart` - Interactive chart with metric selection
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
   - **TestRange**: Color ranges and thresholds for indicator visualization
4. Excel to database column mapping defined in `app/core/excel_mappings.py`

## Code Quality

- **Backend**: Ruff for linting/formatting, Pyright for type checking
- **Frontend**: ESLint + Prettier for code quality
- **Pre-commit**: Hooks run on backend files only (scoped to `^backend/`)
- **Poetry**: Python dependency management with application mode (`package-mode = false`)

## API Structure

All API endpoints are prefixed with `/v1` and include:

- `/auth/*` - Authentication endpoints
- `/dashboard/*` - Trading dashboard data:
  - `/dashboard/position-status` - YTD performance and position of the day
  - `/dashboard/indicators-grid` - All indicators with dynamic ranges
  - `/dashboard/recommendations` - Parsed recommendations from technicals.score
  - `/dashboard/chart-data` - Historical data for charting
- `/commodities/*` - Commodity information
- `/historical/*` - Historical data and indicators

## Google Drive Audio Integration

The application integrates with Google Drive to fetch daily audio files for the position status component.

### Audio File Requirements

- **File naming pattern**: `YYYYMMDD-CompassAudio.{wav|m4a|mp4}`
  - Example: `20250109-CompassAudio.wav`, `20250109-CompassAudio.m4a`, or `20250109-CompassAudio.mp4`
- **Supported formats**: `.wav`, `.m4a`, and `.mp4` files
- **Location**: Must be stored in a specific Google Drive folder

### Setting Up Google Drive Integration

1. **Find your Google Drive folder ID**:
   - Open Google Drive in your browser
   - Navigate to the folder containing your audio files
   - Look at the URL in your browser's address bar
   - The URL will look like: `https://drive.google.com/drive/folders/1A2B3C4D5E6F7G8H9I0J`
   - Copy the folder ID (the part after `/folders/`) - in this example: `1A2B3C4D5E6F7G8H9I0J`

2. **Configure environment variables**:

   ```bash
   # Required: Google Drive folder ID containing audio files
   GOOGLE_DRIVE_AUDIO_FOLDER_ID="1A2B3C4D5E6F7G8H9I0J"
   
   # Optional: Separate Google Drive credentials (defaults to Google Sheets credentials)
   GOOGLE_DRIVE_CREDENTIALS_JSON='{...}'
   ```

3. **Google Drive API permissions**:
   - The service account must have read access to the specified folder
   - Audio files will automatically be made publicly accessible when first accessed
   - Requires `https://www.googleapis.com/auth/drive.readonly` scope

### API Endpoint

- **GET** `/v1/dashboard/audio`
- **Query parameters**:
  - `target_date` (optional): Date in YYYY-MM-DD format
- **Response**: Audio file URL, title, date, and filename
- **Error handling**: Returns 404 if audio file not found with helpful error message

### Frontend Integration

The `PositionStatus` component automatically fetches and plays the audio file:

- Loads audio URL dynamically from the API
- Shows loading state while fetching
- Displays error messages if file not found
- Supports .wav, .m4a, and .mp4 formats seamlessly

## Development Notes

- Backend uses Poetry scripts: `poetry run dev` and `poetry run lint`
- Frontend environment variables must be accessible to Vite (no VITE_ prefix needed due to custom setup)
- Database migrations managed via Alembic (models ready for initial migration)
- Pre-commit hooks are configured to run only on backend Python files to avoid conflicts with monorepo structure
