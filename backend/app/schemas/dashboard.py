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


class IndicatorsGridResponse(BaseModel):
    """
    Response schema for indicators grid endpoint.

    Contains all indicators with their values and ranges.
    """

    date: datetime = Field(..., description="Date of the indicators")
    indicators: dict[str, CommodityIndicator] = Field(
        ..., description="Map of indicator names to their data"
    )

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class RecommendationsResponse(BaseModel):
    """
    Response schema for recommendations endpoint.

    Contains the score text from technicals table.
    """

    date: datetime = Field(..., description="Date of the recommendations")
    recommendations: List[str] = Field(
        default_factory=list,
        description="List of recommendations parsed from the score column",
    )
    raw_score: Optional[str] = Field(
        None, description="Raw score text from technicals table"
    )

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class NewsResponse(BaseModel):
    """
    Response schema for news endpoint from market research.
    """

    date: str = Field(..., description="Date of the news article")
    title: str = Field(..., description="Title from impact_synthesis column")
    content: str = Field(..., description="Content from summary column")
    author: Optional[str] = Field(None, description="Author information")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class WeatherResponse(BaseModel):
    """
    Response schema for weather endpoint from weather data.
    """

    date: str = Field(..., description="Date of the weather update")
    description: str = Field(..., description="Weather description from summary column")
    impact: str = Field(..., description="Market impact from impact_synthesis column")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class ChartDataPoint(BaseModel):
    """
    Single data point for chart display.
    """

    date: str = Field(..., description="Date in YYYY-MM-DD format")
    close: Optional[float] = Field(None, description="Close price")
    volume: Optional[float] = Field(None, description="Volume")
    open_interest: Optional[float] = Field(None, description="Open interest")
    rsi_14d: Optional[float] = Field(None, description="RSI 14-day")
    macd: Optional[float] = Field(None, description="MACD")
    stock_us: Optional[float] = Field(None, description="US stock levels")
    com_net_us: Optional[float] = Field(None, description="Commercial net US")


class ChartDataResponse(BaseModel):
    """
    Response schema for chart data endpoint.

    Contains historical data from technicals table.
    """

    data: List[ChartDataPoint] = Field(..., description="Historical chart data points")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class AudioResponse(BaseModel):
    """
    Response schema for audio endpoint.

    Contains the publicly playable URL and metadata for audio files from Google Drive.
    """

    url: str = Field(..., description="Publicly accessible URL for the audio file")
    title: str = Field(..., description="Display title for the audio")
    date: str = Field(..., description="Date of the audio in ISO format")
    filename: str = Field(..., description="Original filename of the audio")
