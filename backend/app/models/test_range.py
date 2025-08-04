"""
Test Range model for defining indicator color thresholds.

This model stores the range boundaries for each indicator that determine
whether values fall into RED, ORANGE, or GREEN zones for trading decisions.
"""

from sqlalchemy import Column, Integer, String, DECIMAL, UniqueConstraint
from sqlalchemy.orm import validates

from .base import Base


class TestRange(Base):
    """
    Test Range table for indicator color zone definitions.

    Each row defines a range (low to high) for a specific indicator
    and assigns it a color zone (RED, ORANGE, GREEN) used for
    trading signal interpretation.
    """

    __tablename__ = "test_range"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Indicator name (MACROECO, RSI, MACD, %K, ATR, CLOSE/PIVOT, VOL/OI)
    indicator = Column(
        String(50),
        nullable=False,
        comment="Name of the indicator (e.g., MACROECO, RSI, MACD, %K, ATR, CLOSE/PIVOT, VOL/OI)",
    )

    # Range boundaries
    range_low = Column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Lower boundary of the range (inclusive)",
    )

    range_high = Column(
        DECIMAL(15, 6),
        nullable=False,
        comment="Upper boundary of the range (inclusive)",
    )

    # Color zone
    area = Column(
        String(10),
        nullable=False,
        comment="Color zone for this range (RED, ORANGE, GREEN)",
    )

    # Ensure unique combination of indicator and range
    __table_args__ = (
        UniqueConstraint(
            "indicator", "range_low", "range_high", name="uq_indicator_range"
        ),
    )

    @validates("area")
    def validate_area(self, key, value):
        """Validate that area is one of the allowed values."""
        allowed_values = ["RED", "ORANGE", "GREEN"]
        if value and value.upper() not in allowed_values:
            raise ValueError(f"Area must be one of {allowed_values}")
        return value.upper() if value else value

    @validates("range_low", "range_high")
    def validate_range(self, key, value):
        """Ensure range values are valid."""
        if value is None:
            raise ValueError(f"{key} cannot be None")
        return value

    def __repr__(self):
        return (
            f"<TestRange(indicator='{self.indicator}', "
            f"range=[{self.range_low}, {self.range_high}], "
            f"area='{self.area}')>"
        )
