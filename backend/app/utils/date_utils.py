"""
Date utility functions for the commodities trading application.

Provides reusable date handling, validation, and business logic
for market data operations.
"""

from datetime import datetime, date, timedelta
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def parse_date_string(date_str: str) -> date:
    """
    Parse a date string in YYYY-MM-DD format to a date object.

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        Parsed date object

    Raises:
        ValueError: If date format is invalid
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD format: {e}")


def validate_date_format(date_str: str) -> bool:
    """
    Validate if a date string is in correct YYYY-MM-DD format.

    Args:
        date_str: Date string to validate

    Returns:
        True if valid format, False otherwise
    """
    try:
        parse_date_string(date_str)
        return True
    except ValueError:
        return False


def get_business_date(target_date: date) -> date:
    """
    Convert a date to the nearest previous business day (Monday-Friday).

    Markets are closed on weekends, so weekend dates are converted
    to the previous Friday.

    Args:
        target_date: The date to convert

    Returns:
        The nearest previous business day
    """
    # If it's Saturday (5) or Sunday (6), go back to Friday
    if target_date.weekday() == 5:  # Saturday
        return target_date - timedelta(days=1)  # Go to Friday
    elif target_date.weekday() == 6:  # Sunday
        return target_date - timedelta(days=2)  # Go to Friday
    else:
        return target_date  # Already a weekday


def get_year_start_date(reference_date: Optional[date] = None) -> date:
    """
    Get the start date of the year for a given reference date.

    Args:
        reference_date: Reference date (defaults to today)

    Returns:
        January 1st of the reference year
    """
    if reference_date is None:
        reference_date = date.today()

    return date(reference_date.year, 1, 1)


def format_date_for_display(date_obj: date) -> str:
    """
    Format a date object for display in API responses.

    Args:
        date_obj: Date object to format

    Returns:
        Formatted date string (e.g., "January 15, 2024")
    """
    return date_obj.strftime("%B %d, %Y")


def log_business_date_conversion(original_date: date, business_date: date) -> None:
    """
    Log weekend to business date conversions for debugging.

    Args:
        original_date: Original requested date
        business_date: Converted business date
    """
    if business_date != original_date:
        logger.info(
            f"Weekend date {original_date} converted to business date {business_date}"
        )
