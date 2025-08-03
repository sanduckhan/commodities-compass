"""
Dashboard API schemas for position status and indicators.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class CommodityIndicator(BaseModel):
    """
    Indicator gauge display data.

    Used for displaying normalized indicator values in gauge components.
    """

    value: float = Field(..., description="Current indicator value")
    min: float = Field(..., description="Minimum value for the gauge scale")
    max: float = Field(..., description="Maximum value for the gauge scale")
    label: str = Field(..., description="Display label for the indicator")


class PositionStatusResponse(BaseModel):
    """
    Response schema for position status endpoint.

    Contains current trading position and day indicator data.
    """

    date: datetime = Field(..., description="Date of the current position")
    position: str = Field(..., description="Current position: OPEN, HEDGE, or MONITOR")
    day_indicator: Optional[CommodityIndicator] = Field(
        None, description="Normalized day indicator for gauge display"
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
