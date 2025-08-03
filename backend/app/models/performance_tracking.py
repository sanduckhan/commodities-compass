"""
Performance tracking model for trading strategies.
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, INTEGER, TIMESTAMP, VARCHAR, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


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
