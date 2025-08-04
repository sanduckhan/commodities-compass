"""
Dashboard API schemas for position status and indicators.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


class IndicatorRange(BaseModel):
    """Range definition for indicator color zones."""

    range_low: float = Field(..., description="Lower boundary of the range")
    range_high: float = Field(..., description="Upper boundary of the range")
    area: str = Field(..., description="Color zone: RED, ORANGE, or GREEN")


class CommodityIndicator(BaseModel):
    """
    Indicator gauge display data.

    Used for displaying normalized indicator values in gauge components.
    """

    value: float = Field(..., description="Current indicator value")
    min: float = Field(..., description="Minimum value for the gauge scale")
    max: float = Field(..., description="Maximum value for the gauge scale")
    label: str = Field(..., description="Display label for the indicator")
    ranges: Optional[List[IndicatorRange]] = Field(
        None, description="Color zone ranges for this indicator"
    )


class PositionStatusResponse(BaseModel):
    """
    Response schema for position status endpoint.

    Contains current trading position and YTD performance.
    """

    date: datetime = Field(..., description="Date of the current position")
    position: str = Field(..., description="Current position: OPEN, HEDGE, or MONITOR")
    ytd_performance: float = Field(
        ..., description="Year-to-date performance percentage"
    )

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), Decimal: lambda v: float(v)}


class IndicatorData(BaseModel):
    """
    Raw indicator data from database.
    """

    date: datetime
    conclusion: Optional[str] = None
    final_indicator: Optional[Decimal] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v) if v is not None else None,
        }
