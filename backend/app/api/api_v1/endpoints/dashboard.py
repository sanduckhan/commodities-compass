from datetime import datetime, date, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import logging

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.indicator import Indicator
from app.models.test_range import TestRange
from app.schemas.dashboard import (
    PositionStatusResponse,
    CommodityIndicator,
    IndicatorData,
    IndicatorRange,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def get_business_date(target_date: date) -> date:
    """
    Convert weekend dates to the previous Friday for market data.

    Markets are closed on weekends, so:
    - Saturday (weekday 5) -> Previous Friday
    - Sunday (weekday 6) -> Previous Friday
    - Weekdays (0-4) -> Return as-is

    Args:
        target_date: The requested date

    Returns:
        Business date (previous Friday if weekend, otherwise the same date)
    """
    weekday = target_date.weekday()

    if weekday == 5:  # Saturday
        return target_date - timedelta(days=1)  # Previous Friday
    elif weekday == 6:  # Sunday
        return target_date - timedelta(days=2)  # Previous Friday
    else:
        return target_date  # Weekday, return as-is


async def create_indicator_for_gauge(
    value: Optional[float], db: AsyncSession, indicator_name: str = "MACROECO"
) -> Optional[CommodityIndicator]:
    """
    Create indicator data for gauge display using raw final_indicator values.

    Args:
        value: Final indicator value from database (range: -6 to +6)
        db: Database session
        indicator_name: Name of the indicator to fetch ranges for

    Returns:
        CommodityIndicator with raw value and color ranges
    """
    if value is None:
        return None

    # Fetch ranges for this indicator from test_range table
    result = await db.execute(
        select(TestRange)
        .where(TestRange.indicator == indicator_name)
        .order_by(TestRange.range_low)
    )
    test_ranges = result.scalars().all()

    # Convert to IndicatorRange schema objects
    ranges = (
        [
            IndicatorRange(
                range_low=float(tr.range_low),
                range_high=float(tr.range_high),
                area=tr.area,
            )
            for tr in test_ranges
        ]
        if test_ranges
        else None
    )

    # Use raw values - no normalization needed
    # The gauge component will calculate percentages internally
    return CommodityIndicator(
        value=value, min=-6.0, max=6.0, label="DAY INDICATOR", ranges=ranges
    )


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

            # Convert weekend dates to previous Friday (markets are closed on weekends)
            business_date = get_business_date(parsed_date)

            # Log the conversion if weekend date was requested
            if business_date != parsed_date:
                logger.info(
                    f"Weekend date {parsed_date} converted to business date {business_date}"
                )

            query = query.where(Indicator.date == business_date)
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use YYYY-MM-DD format."
            )

    # Get the most recent indicator record
    result = await db.execute(query)
    indicator = result.scalars().first()

    if not indicator:
        raise HTTPException(status_code=404, detail="No indicator data found")

    response = PositionStatusResponse(
        date=indicator.date,
        position=indicator.conclusion or "MONITOR",  # Default to MONITOR if None
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
