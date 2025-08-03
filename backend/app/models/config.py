"""
Application configuration parameters model.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DECIMAL, INTEGER, TIMESTAMP, VARCHAR, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


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
