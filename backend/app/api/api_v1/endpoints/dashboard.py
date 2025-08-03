from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import logging

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.indicator import Indicator
from app.schemas.dashboard import (
    PositionStatusResponse,
    CommodityIndicator,
    IndicatorData,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def create_indicator_for_gauge(
    value: Optional[float],
) -> Optional[CommodityIndicator]:
    """
    Create indicator data for gauge display using raw final_indicator values.

    Args:
        value: Final indicator value from database (range: -6 to +6)

    Returns:
        CommodityIndicator with raw value for gauge component
    """
    if value is None:
        return None

    # Use raw values - no normalization needed
    # The gauge component will calculate percentages internally
    return CommodityIndicator(value=value, min=-6.0, max=6.0, label="DAY INDICATOR")


@router.get("/position-status", response_model=PositionStatusResponse)
async def get_position_status(
    target_date: Optional[str] = Query(
        default=None, description="Specific date for position data (YYYY-MM-DD format)"
    ),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PositionStatusResponse:
    """
    Get current position status and day indicator.

    Returns the latest trading position (OPEN/HEDGE/MONITOR) and normalized
    day indicator value for gauge display.

    Args:
        target_date: Optional specific date. If not provided, returns latest data.
        current_user: Authenticated user
        db: Database session

    Returns:
        Current position status and day indicator data

    Raises:
        HTTPException: If no data found
    """
    # Build query for latest indicator data
    query = select(Indicator).order_by(desc(Indicator.date))

    if target_date:
        try:
            # Parse the date string to date object
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            query = query.where(Indicator.date == parsed_date)
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use YYYY-MM-DD format."
            )

    # Get the most recent indicator record
    result = await db.execute(query)
    indicator = result.scalars().first()

    if not indicator:
        raise HTTPException(status_code=404, detail="No indicator data found")

    # Create indicator data for gauge display
    day_indicator = create_indicator_for_gauge(
        float(indicator.final_indicator) if indicator.final_indicator else None
    )

    response = PositionStatusResponse(
        date=indicator.date,
        position=indicator.conclusion or "MONITOR",  # Default to MONITOR if None
        day_indicator=day_indicator,
    )

    return response


@router.get("/latest-indicator", response_model=IndicatorData)
async def get_latest_indicator(
    current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)
) -> IndicatorData:
    """
    Get the latest indicator data.

    Returns raw indicator data from the database for debugging or detailed views.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        Latest indicator record

    Raises:
        HTTPException: If no data found
    """
    result = await db.execute(select(Indicator).order_by(desc(Indicator.date)).limit(1))
    indicator = result.scalars().first()

    if not indicator:
        raise HTTPException(status_code=404, detail="No indicator data found")

    return IndicatorData.model_validate(indicator)


@router.get("/")
async def get_dashboard_data(
    target_date: Optional[date] = Query(
        default=None, description="Date for dashboard data"
    ),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get dashboard data for a specific date"""
    if not target_date:
        target_date = date.today()

    # TODO: Implement database queries to fetch real data
    # For now, return mock data structure
    return {
        "date": target_date.isoformat(),
        "positionOfDay": "OPEN",
        "ytdPerformance": 72.12,
        "indicators": {
            "dayIndicator": {
                "value": 2.22,
                "min": 0,
                "max": 3,
                "label": "DAY INDICATOR",
            },
            "macroeco": {"value": 1.1, "min": 0, "max": 3, "label": "DAY MACROECO"},
            "rsi": {"value": 0.59, "min": 0, "max": 3, "label": "DAY RSI"},
            "macd": {"value": 1.11, "min": 0, "max": 3, "label": "DAY MACD"},
            "percentK": {"value": 0.08, "min": 0, "max": 3, "label": "DAY %K"},
            "atr": {"value": -0.39, "min": -3, "max": 3, "label": "DAY ATR"},
            "volOi": {"value": 0.11, "min": 0, "max": 3, "label": "DAY VOL/OI"},
        },
        "recommendations": [
            {
                "id": 1,
                "text": "Market analysis placeholder - will be generated from real data",
            }
        ],
        "lastPress": {
            "id": 1,
            "date": target_date.isoformat(),
            "author": "System",
            "title": "Latest market news will appear here",
            "content": "News content placeholder",
        },
        "weatherUpdates": [
            {
                "id": 1,
                "date": target_date.isoformat(),
                "region": "West Africa",
                "description": "Weather data will be integrated",
                "impact": "Impact analysis placeholder",
            }
        ],
    }


@router.get("/summary")
async def get_dashboard_summary(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get quick summary for dashboard"""
    # TODO: Implement database query
    return {
        "lastUpdate": datetime.utcnow().isoformat(),
        "activePositions": 1,
        "totalCommodities": 1,
        "alerts": [],
    }
