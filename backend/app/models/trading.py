"""
Trading-related database models for Commodities Compass.

This module contains SQLAlchemy models representing the core trading data
extracted from the Excel analysis. Each model corresponds to a sheet in the
original commodities-compass.xlsx file.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DECIMAL, INTEGER, TEXT, TIMESTAMP, VARCHAR, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class Technicals(Base):
    """
    Technical analysis data for commodities trading.

    This table stores raw OHLCV data along with calculated technical indicators
    for each time period. Currently focused on cocoa (ICE contracts) with daily frequency.
    Data updated daily via Make.com automation at 8:30 PM.

    Source: TECHNICALS sheet from Excel file
    """

    __tablename__ = "technicals"

    # Primary key and timestamp
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        index=True,
        comment="Date and time of the trading period (daily frequency)",
    )

    # Commodity identifier
    commodity_symbol: Mapped[str] = mapped_column(
        VARCHAR(10),
        nullable=False,
        default="CC",
        index=True,
        comment="Commodity symbol (CC for Cocoa, expandable for other commodities)",
    )

    # === CORE OHLCV DATA ===
    # Standard trading data - Open, High, Low, Close, Volume
    close: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Closing price of the commodity for this period",
    )
    high: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Highest price during this trading period",
    )
    low: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Lowest price during this trading period",
    )
    volume: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        comment="Trading volume - number of contracts/units traded",
    )
    open_interest: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        comment="Open interest - total number of outstanding derivative contracts",
    )

    # === MARKET DATA & FUNDAMENTALS ===
    implied_volatility: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Implied volatility derived from options pricing"
    )
    stock_us: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="US stock values regulated by ICE, available daily online, expressed in bags (x70/1000 to convert to kgs)",
    )
    com_net_us: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="Net commercial positions from COT (Commitments of Traders) report - commercial long minus short positions",
    )

    # === PIVOT POINTS ===
    # Support and resistance levels calculated from previous period's OHLC
    r3: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Resistance level 3 - strongest resistance",
    )
    r2: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Resistance level 2 - intermediate resistance",
    )
    r1: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Resistance level 1 - nearest resistance above pivot",
    )
    pivot: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Central pivot point - key support/resistance level",
    )
    s1: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Support level 1 - nearest support below pivot",
    )
    s2: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6), nullable=False, comment="Support level 2 - intermediate support"
    )
    s3: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6), nullable=False, comment="Support level 3 - strongest support"
    )

    # === MOVING AVERAGES & MACD ===
    ema12: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6), nullable=False, comment="12-period Exponential Moving Average"
    )
    ema26: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6), nullable=False, comment="26-period Exponential Moving Average"
    )
    macd: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="MACD line (EMA12 - EMA26) - trend following momentum indicator",
    )
    signal: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="MACD Signal line (EMA of MACD) - generates buy/sell signals",
    )

    # === RSI & STOCHASTIC OSCILLATORS ===
    rsi_14d: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="14-day Relative Strength Index (0-100) - momentum oscillator",
    )
    stochastic_k_14: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="14-period Stochastic %K - fast stochastic oscillator"
    )
    stochastic_d_14: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="14-period Stochastic %D - slow stochastic (SMA of %K)"
    )
    # Note: Removed duplicate 'd' field - expert confirmed it's the same as stochastic_d_14

    # === VOLATILITY MEASURES ===
    atr: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Average True Range - different period than ATR 14d"
    )
    atr_14d: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="14-day Average True Range - calculated from formulas, converted to numerical",
    )
    volatility: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="General volatility measure (calculation method needs clarification)",
    )

    # === BOLLINGER BANDS ===
    bollinger: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Bollinger Band middle line (typically 20-period SMA)",
    )
    bollinger_upper: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Bollinger Band upper band (middle + 2*standard deviation)",
    )
    bollinger_lower: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Bollinger Band lower band (middle - 2*standard deviation)",
    )
    bollinger_width: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Bollinger Band width (limites de bolinger) - difference between upper and lower bands",
    )

    # === CALCULATED RATIOS & RELATIONSHIPS ===
    close_pivot_ratio: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="Ratio of close price to pivot point - position relative to pivot",
    )
    volume_oi_ratio: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Volume to Open Interest ratio (Volume / Open Interest) - liquidity indicator",
    )

    # === GAIN/LOSS CALCULATIONS ===
    gain_14d: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="14-day average gain - calculated from formulas, converted to numerical for RSI calculation",
    )
    loss_14d: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="14-day average loss - calculated from formulas, converted to numerical for RSI calculation",
    )
    rs: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Relative Strength (gain/loss ratio) - component of RSI"
    )

    # === TRADING SIGNALS & DECISIONS ===
    decision: Mapped[Optional[str]] = mapped_column(
        VARCHAR(100), comment="Trading decision: OPEN, HEDGE, or MONITOR"
    )
    confidence: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(5, 2),
        comment="Confidence level in the trading decision as percentage (0-100%)",
    )
    direction: Mapped[Optional[str]] = mapped_column(
        VARCHAR(100), comment="Expected price direction: BULLISH or BEARISH"
    )
    score: Mapped[Optional[str]] = mapped_column(
        TEXT, comment="Structured data containing composite trading score calculations"
    )
    conclusion: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Final numerical conclusion/score for this period"
    )

    # === METADATA ===
    row_number: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        comment="Original row number from Excel sheet for reference",
    )

    # === AUDIT FIELDS ===
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), comment="Record creation timestamp"
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Record last update timestamp",
    )


class Indicator(Base):
    """
    Normalized indicators and final trading signals.

    This table contains processed and normalized versions of technical indicators,
    along with macroeconomic factors and final trading recommendations.
    Individual scores range from -6 to +6. Updated daily at 11 PM via Make.com automation.
    Historical data preservation is critical for algorithm testing.

    Source: INDICATOR sheet from Excel file
    """

    __tablename__ = "indicator"

    # Primary key and timestamp
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        index=True,
        comment="Date for this indicator calculation (synchronized with technicals.timestamp)",
    )

    # Commodity identifier
    commodity_symbol: Mapped[str] = mapped_column(
        VARCHAR(10),
        nullable=False,
        default="CC",
        index=True,
        comment="Commodity symbol (CC for Cocoa)",
    )

    # === RAW INDICATOR SCORES (-6 to +6) ===
    # Individual scores for each technical indicator on -6 to +6 scale
    rsi_score: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(4, 2), comment="Individual score for RSI indicator (-6 to +6 scale)"
    )
    macd_score: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(4, 2), comment="Individual score for MACD indicator (-6 to +6 scale)"
    )
    stochastic_score: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(4, 2),
        comment="Individual score for Stochastic oscillator (-6 to +6 scale)",
    )
    atr_score: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(4, 2),
        comment="Individual score for ATR (volatility measure) (-6 to +6 scale)",
    )

    # === MARKET POSITION SCORES ===
    close_pivot: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Close/Pivot ratio score - position relative to pivot point",
    )
    volume_oi: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Volume/Open Interest ratio score"
    )

    # === NORMALIZED INDICATORS (0-1 SCALE) ===
    # All technical indicators normalized to comparable scale
    rsi_norm: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="RSI normalized to 0-1 scale for comparison"
    )
    macd_norm: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="MACD normalized to 0-1 scale for comparison"
    )
    stoch_k_norm: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Stochastic %K normalized to 0-1 scale"
    )
    atr_norm: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="ATR normalized to 0-1 scale"
    )
    close_pivot_norm: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Close/Pivot ratio normalized to 0-1 scale",
    )
    vol_oi_norm: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Volume/OI ratio normalized to 0-1 scale"
    )

    # === COMPOSITE INDICATORS ===
    indicator: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="Combined technical indicator score - weighted average of normalized indicators",
    )
    momentum: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="Momentum score - combination of trend-following indicators",
    )
    macroeco_bonus: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Macroeconomic bonus/penalty applied to technical signals",
    )
    final_indicator: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="Final combined indicator including technical + macroeconomic factors",
    )

    # === MACROECONOMIC ANALYSIS ===
    macroeco_score: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(4, 2), comment="OpenAI-generated macroeconomic score: 0.9, 1.0, or 1.1"
    )
    eco: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
        comment="Macroeconomic analysis text/description generated by OpenAI",
    )

    # === LATEST VALUES FOR COMPARISON ===
    # These fields store the most recent values for trend analysis
    final_indicator_previous: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Previous period's final indicator value"
    )
    previous_macroeco: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Previous period's macroeconomic score"
    )
    previous_rsi: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Previous period's RSI value"
    )
    previous_macd: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Previous period's MACD value"
    )
    previous_k: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Previous period's Stochastic %K value"
    )
    previous_atr: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Previous period's ATR value"
    )
    previous_close_pivot: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Previous period's Close/Pivot ratio"
    )
    previous_vol_oi: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Previous period's Volume/OI ratio"
    )

    # === FINAL CONCLUSIONS ===
    conclusion: Mapped[Optional[str]] = mapped_column(
        VARCHAR(100), comment="Current period's trading conclusion/recommendation"
    )
    previous_conclusion: Mapped[Optional[str]] = mapped_column(
        VARCHAR(100), comment="Previous period's trading conclusion for comparison"
    )

    # === AUDIT FIELDS ===
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )


class MarketResearch(Base):
    """
    Market research and analyst reports with impact analysis.

    This table stores research articles, analyst reports, and industry publications
    focused on cocoa markets. Impact synthesis generated by OpenAI summarization.
    Updated daily at 10:30 PM via Make.com automation.

    Source: BIBLIO_ALL sheet from Excel file
    """

    __tablename__ = "market_research"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        index=True,
        comment="Publication or analysis date of the research",
    )
    author: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        comment="Author or source of the research/publication",
    )
    summary: Mapped[str] = mapped_column(
        TEXT, nullable=False, comment="Summary or abstract of the research content"
    )
    keywords: Mapped[Optional[str]] = mapped_column(
        TEXT, comment="Keywords or tags associated with this research"
    )
    impact_synthesis: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
        comment="Synthesized market impact assessment - how this research affects trading decisions",
    )
    date_text: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        comment="Date in text format (might include additional context like 'Q1 2024')",
    )

    # === AUDIT FIELDS ===
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )


class WeatherData(Base):
    """
    Weather and agricultural conditions affecting cocoa markets.

    This table stores weather reports and agricultural conditions from Ghana and
    Côte d'Ivoire (10 locations) that impact cocoa prices. Updated daily at 10:30 PM
    via Make.com automation. Impact analysis generated by OpenAI.

    Source: METEO_ALL sheet from Excel file
    """

    __tablename__ = "weather_data"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        index=True,
        comment="Date of the weather report or agricultural update",
    )
    text: Mapped[str] = mapped_column(
        TEXT, nullable=False, comment="Full text of the weather/agricultural report"
    )
    summary: Mapped[str] = mapped_column(
        TEXT, nullable=False, comment="Summary of key weather/agricultural conditions"
    )
    keywords: Mapped[str] = mapped_column(
        VARCHAR(500),
        nullable=False,
        comment="Keywords describing weather conditions, crop types, regions affected",
    )
    impact_synthesis: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
        comment="Synthesized market impact - how weather conditions affect commodity prices",
    )

    # === AUDIT FIELDS ===
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )


class Config(Base):
    """
    Application configuration parameters for trading algorithms.

    This table stores configuration settings for various trading indicators
    and algorithm parameters. New champion values are updated monthly or less
    frequently and tested one week before implementation.

    Source: CONFIG sheet from Excel file
    """

    __tablename__ = "config"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    parameter: Mapped[Optional[str]] = mapped_column(
        VARCHAR(100), unique=True, comment="Name of the configuration parameter"
    )
    indicator: Mapped[Optional[str]] = mapped_column(
        VARCHAR(100),
        comment="Which indicator this parameter applies to (RSI, MACD, etc.)",
    )
    val_min: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Minimum allowed value for this parameter"
    )
    val_max: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Maximum allowed value for this parameter"
    )
    step: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Step size for parameter optimization"
    )
    current: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Current active value being used"
    )
    new_champion: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6),
        comment="New optimal value found through backtesting/optimization",
    )
    test: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 6), comment="Test value being evaluated"
    )

    # === AUDIT FIELDS ===
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )


class PerformanceTracking(Base):
    """
    Best performance tracking for trading strategies.

    This table tracks the best performing parameter combinations
    and their associated performance metrics for strategy optimization.
    Performance metrics cover 100-day periods. Testing linked to Colab calculator
    for frequent algorithm challenges and validation.

    Source: BEST PERF sheet from Excel file
    """

    __tablename__ = "performance_tracking"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    performance: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        comment="Performance metric name (ROI, Sharpe ratio, Win rate, etc.)",
    )
    current: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6), nullable=False, comment="Current performance value"
    )
    new: Mapped[Decimal] = mapped_column(
        DECIMAL(15, 6), nullable=False, comment="New/improved performance value"
    )
    limit: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        comment="Minimum score tested with Colab calculator (https://colab.research.google.com/drive/1EwQYZ7TtyhsaAArECwsGfyDkqREKbndd) - performance threshold",
    )

    # === AUDIT FIELDS ===
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )


class Podcast(Base):
    """
    Podcast and media content aggregation for market analysis.

    This table aggregates content from various sources (weather, press, analysis)
    into podcast-style summaries for market commentary.
    Contains 1 aggregated record (likely updated regularly).

    Source: PODCAST sheet from Excel file
    """

    __tablename__ = "podcast"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        index=True,
        comment="Date of the podcast/summary compilation",
    )
    conclusion: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
        comment="Overall market conclusion and trading recommendation",
    )

    # === WEATHER DATA INTEGRATION ===
    meteo_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        comment="Date of the weather data used in this summary",
    )
    meteo_conclusion: Mapped[str] = mapped_column(
        TEXT, nullable=False, comment="Weather-related market impact conclusion"
    )

    # === PRESS DATA INTEGRATION ===
    press_date: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, comment="Date of the press/news data used"
    )
    press_author: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        comment="Author or source of the press information",
    )
    press_text: Mapped[str] = mapped_column(
        TEXT, nullable=False, comment="Press/news content summary"
    )

    # === TRADING POSITION & DIALOGUE ===
    position: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        comment="Recommended trading position (LONG/SHORT/NEUTRAL)",
    )
    dialogue: Mapped[str] = mapped_column(
        TEXT, nullable=False, comment="Podcast dialogue or script content"
    )

    # === AUDIT FIELDS ===
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )
