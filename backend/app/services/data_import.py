"""
Data import service for Google Sheets to PostgreSQL migration.

This service handles the ETL pipeline for importing data from Google Sheets
into the PostgreSQL database using the defined SQLAlchemy models.
"""

import pandas as pd
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from app.core.database import AsyncSessionLocal
from app.core.excel_mappings import EXCEL_MAPPINGS
from app.core.config import settings


class DataTransforms:
    """Data transformation utilities for cleaning Google Sheets data."""

    @staticmethod
    def parse_datetime(value) -> Optional[datetime]:
        """Parse various datetime formats from Google Sheets."""
        if pd.isna(value) or value is None:
            return None

        if isinstance(value, datetime):
            return value

        try:
            return pd.to_datetime(value)
        except Exception:
            return None

    @staticmethod
    def parse_decimal(value) -> Optional[Decimal]:
        """Parse decimal values from Google Sheets."""
        if pd.isna(value) or value is None or value == "":
            return None

        try:
            # Handle percentage values
            if isinstance(value, str) and value.endswith("%"):
                # Convert percentage to decimal (e.g., "9.06%" -> 0.0906)
                return Decimal(value.rstrip("%")) / 100

            # Handle US number format with commas as thousand separators
            if isinstance(value, str) and "," in value:
                value = value.replace(",", "")

            return Decimal(str(value))
        except Exception:
            return None

    @staticmethod
    def parse_decimal_from_string(value) -> Optional[Decimal]:
        """
        Parse decimal from string that may contain Google Sheets formulas.

        This handles cases where Google Sheets cells contain formulas like
        '=A1/B1' instead of computed values.
        """
        if pd.isna(value) or value is None or value == "":
            return None

        # If it's already a number, convert directly
        if isinstance(value, (int, float)):
            return Decimal(str(value))

        # If it's a string, try to extract numerical value
        if isinstance(value, str):
            # Handle percentage values first
            if value.endswith("%"):
                try:
                    return Decimal(value.rstrip("%")) / 100
                except Exception:
                    return None

            # Remove Google Sheets formula markers
            cleaned = value.replace("=", "").strip()

            # Try to parse as number
            try:
                return Decimal(cleaned)
            except Exception:
                # If it contains formula elements, log for manual review
                return None

        return None

    @staticmethod
    def parse_integer(value) -> Optional[int]:
        """Parse integer values from Google Sheets."""
        if pd.isna(value) or value is None or value == "":
            return None

        try:
            # Handle US number format with commas as thousand separators
            if isinstance(value, str) and "," in value:
                value = value.replace(",", "")

            return int(float(str(value)))
        except Exception:
            return None


class GoogleSheetsDataImporter:
    """Service for importing Google Sheets data into PostgreSQL."""

    def __init__(self, spreadsheet_id: str, credentials_path: str):
        self.spreadsheet_id = spreadsheet_id
        self.credentials_path = credentials_path
        self.transforms = DataTransforms()
        self.service = None

    def _get_service(self):
        """Initialize Google Sheets service with authentication."""
        if self.service is None:
            scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
            credentials = Credentials.from_service_account_file(
                self.credentials_path, scopes=scopes
            )
            self.service = build("sheets", "v4", credentials=credentials)
        return self.service

    async def import_all_sheets(self, session: AsyncSession) -> Dict[str, Any]:
        """Import data from all sheets in the Google Spreadsheet."""
        results = {}
        service = self._get_service()

        # Get spreadsheet metadata to check available sheets
        try:
            spreadsheet = (
                service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
            )
            available_sheets = [
                sheet["properties"]["title"] for sheet in spreadsheet["sheets"]
            ]
        except Exception as e:
            return {"error": f"Failed to access spreadsheet: {str(e)}"}

        for mapping_key, config in EXCEL_MAPPINGS.items():
            sheet_name = config["sheet_name"]

            if sheet_name not in available_sheets:
                results[mapping_key] = {"error": f"Sheet {sheet_name} not found"}
                continue

            try:
                result = await self.import_sheet(session, mapping_key, config)
                results[mapping_key] = result
            except Exception as e:
                results[mapping_key] = {"error": str(e)}

        return results

    async def import_sheet(
        self, session: AsyncSession, mapping_key: str, config: Dict
    ) -> Dict[str, Any]:
        """Import data from a single sheet."""
        sheet_name = config["sheet_name"]
        table_model = config["table_model"]
        column_mapping = config["column_mapping"]
        transforms = config["transforms"]
        service = self._get_service()

        # Read Google Sheet data
        try:
            result = (
                service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"{sheet_name}!A:ZZ",  # Get all data
                )
                .execute()
            )
            values = result.get("values", [])
        except Exception as e:
            return {"error": f"Failed to read sheet {sheet_name}: {str(e)}"}

        if not values:
            return {"error": f"Sheet {sheet_name} is empty"}

        # Convert to DataFrame for easier processing
        df = pd.DataFrame(values[1:], columns=values[0] if values else [])

        # Track import statistics
        stats = {
            "sheet_name": sheet_name,
            "total_rows": len(df),
            "imported_rows": 0,
            "skipped_rows": 0,
            "errors": [],
        }

        # Clear existing data (for full refresh) - FIXED: Use proper SQLAlchemy delete
        await session.execute(delete(table_model))

        # Process each row
        for index, row in df.iterrows():
            try:
                # Transform row data according to mapping
                model_data = {}

                for excel_col, db_col in column_mapping.items():
                    if excel_col in df.columns:
                        raw_value = (
                            row[excel_col] if not pd.isna(row[excel_col]) else None
                        )

                        # Convert empty strings to None
                        if raw_value == "" or raw_value == "nan":
                            raw_value = None

                        # Apply transformation if specified
                        if db_col in transforms:
                            transform_func = getattr(
                                self.transforms, transforms[db_col]
                            )
                            transformed_value = transform_func(raw_value)
                        else:
                            transformed_value = raw_value

                        # Final check: ensure empty strings become None for optional fields
                        if transformed_value == "":
                            transformed_value = None

                        # Additional cleanup for percentage values that might not be in transforms
                        if isinstance(
                            transformed_value, str
                        ) and transformed_value.endswith("%"):
                            try:
                                transformed_value = (
                                    Decimal(transformed_value.rstrip("%")) / 100
                                )
                            except Exception:
                                transformed_value = None

                        # No longer need to validate score fields since they now use DECIMAL(8,2)

                        model_data[db_col] = transformed_value

                # Add default values for required fields if not present
                if (
                    hasattr(table_model, "commodity_symbol")
                    and "commodity_symbol" not in model_data
                ):
                    model_data["commodity_symbol"] = "CC"

                # Handle required fields that might be missing from Google Sheets
                if table_model.__name__ == "Indicator":
                    # close_pivot is required but might be missing
                    if (
                        "close_pivot" not in model_data
                        or model_data["close_pivot"] is None
                    ):
                        model_data["close_pivot"] = Decimal("0.0")  # Default value

                    # close_pivot_norm is required but might be missing
                    if (
                        "close_pivot_norm" not in model_data
                        or model_data["close_pivot_norm"] is None
                    ):
                        model_data["close_pivot_norm"] = Decimal("0.0")  # Default value

                    # macroeco_bonus is required but might be missing
                    if (
                        "macroeco_bonus" not in model_data
                        or model_data["macroeco_bonus"] is None
                    ):
                        model_data["macroeco_bonus"] = Decimal("0.0")  # Default value

                    # eco is required but might be missing
                    if "eco" not in model_data or model_data["eco"] is None:
                        model_data["eco"] = ""  # Default empty string

                # Handle performance_tracking required fields
                if table_model.__name__ == "PerformanceTracking":
                    if "limit" not in model_data or model_data["limit"] is None:
                        model_data["limit"] = ""  # Default empty string

                # Create model instance
                model_instance = table_model(**model_data)
                session.add(model_instance)
                stats["imported_rows"] += 1

            except Exception as e:
                stats["skipped_rows"] += 1
                stats["errors"].append(
                    f"Row {index + 2}: {str(e)}"
                )  # +2 for header and 0-based index

        # Commit changes
        await session.commit()

        return stats

    async def validate_import(self, session: AsyncSession) -> Dict[str, Any]:
        """Validate the imported data."""
        validation_results = {}

        for mapping_key, config in EXCEL_MAPPINGS.items():
            table_model = config["table_model"]

            # Count records efficiently using func.count()
            result = await session.execute(
                select(func.count()).select_from(table_model)
            )
            count = result.scalar()

            validation_results[mapping_key] = {
                "table_name": table_model.__tablename__,
                "record_count": count,
            }

        return validation_results


# CLI function for running the import
async def run_google_sheets_import(
    spreadsheet_id: str = None,
    credentials_path: str = None,
):
    """Run the Google Sheets import process."""
    print("Starting Google Sheets to PostgreSQL import...")

    # Get configuration from settings if not provided
    if spreadsheet_id is None:
        spreadsheet_id = settings.SPREADSHEET_ID

    if credentials_path is None:
        credentials_path = settings.GOOGLE_SHEETS_CREDENTIALS_PATH

    # Initialize importer
    importer = GoogleSheetsDataImporter(spreadsheet_id, credentials_path)

    # Get database session
    async with AsyncSessionLocal() as session:
        # Run import
        results = await importer.import_all_sheets(session)

        # Print results
        print(f"\nImport Results for Spreadsheet: {spreadsheet_id}")
        print("=" * 60)

        for mapping_key, result in results.items():
            if "error" in result:
                print(f"❌ {mapping_key}: {result['error']}")
            else:
                print(
                    f"✅ {mapping_key}: {result['imported_rows']}/{result['total_rows']} rows imported"
                )
                if result["skipped_rows"] > 0:
                    print(f"   ⚠️  {result['skipped_rows']} rows skipped")
                if result.get("errors"):
                    print(f"   📝 First few errors: {result['errors'][:3]}")

        # Validate
        validation = await importer.validate_import(session)
        print("\nValidation Results:")
        print("=" * 30)

        for mapping_key, stats in validation.items():
            print(f"{stats['table_name']}: {stats['record_count']} records")


def main():
    """Entry point for Poetry script."""
    import asyncio

    asyncio.run(run_google_sheets_import())


if __name__ == "__main__":
    main()
