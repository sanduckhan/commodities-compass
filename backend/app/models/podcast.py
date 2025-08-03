"""
Podcast and media content aggregation model.
"""

from datetime import datetime

from sqlalchemy import INTEGER, TEXT, TIMESTAMP, VARCHAR, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


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
