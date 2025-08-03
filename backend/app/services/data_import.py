"""
Data import service for Excel to PostgreSQL migration.

This service handles the ETL pipeline for importing data from the Excel file
into the PostgreSQL database using the defined SQLAlchemy models.
"""

import pandas as pd
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_async_session
from app.core.excel_mappings import EXCEL_MAPPINGS


class DataTransforms:
    """Data transformation utilities for cleaning Excel data."""

    @staticmethod
    def parse_datetime(value) -> Optional[datetime]:
        """Parse various datetime formats from Excel."""
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
        """Parse decimal values from Excel."""
        if pd.isna(value) or value is None:
            return None

        try:
            return Decimal(str(value))
        except Exception:
            return None

    @staticmethod
    def parse_decimal_from_string(value) -> Optional[Decimal]:
        """
        Parse decimal from string that may contain Excel formulas.

        This handles cases where Excel cells contain formulas like
        '=A1/B1' instead of computed values.
        """
        if pd.isna(value) or value is None:
            return None

        # If it's already a number, convert directly
        if isinstance(value, (int, float)):
            return Decimal(str(value))

        # If it's a string, try to extract numerical value
        if isinstance(value, str):
            # Remove Excel formula markers
            cleaned = value.replace("=", "").strip()

            # Try to parse as number
            try:
                return Decimal(cleaned)
            except Exception:
                # If it contains formula elements, log for manual review
                return None

        return None


class ExcelDataImporter:
    """Service for importing Excel data into PostgreSQL."""

    def __init__(self, excel_path: str):
        self.excel_path = Path(excel_path)
        self.transforms = DataTransforms()

    async def import_all_sheets(self, session: AsyncSession) -> Dict[str, Any]:
        """Import data from all sheets in the Excel file."""
        results = {}

        # Load Excel file
        workbook = pd.ExcelFile(self.excel_path)

        for mapping_key, config in EXCEL_MAPPINGS.items():
            sheet_name = config["sheet_name"]

            if sheet_name not in workbook.sheet_names:
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

        # Read Excel sheet
        df = pd.read_excel(self.excel_path, sheet_name=sheet_name)

        # Track import statistics
        stats = {
            "sheet_name": sheet_name,
            "total_rows": len(df),
            "imported_rows": 0,
            "skipped_rows": 0,
            "errors": [],
        }

        # Clear existing data (for full refresh)
        # TODO: Consider incremental updates in the future
        await session.execute(f"DELETE FROM {table_model.__tablename__}")

        # Process each row
        for index, row in df.iterrows():
            try:
                # Transform row data according to mapping
                model_data = {}

                for excel_col, db_col in column_mapping.items():
                    if excel_col in df.columns:
                        raw_value = row[excel_col]

                        # Apply transformation if specified
                        if db_col in transforms:
                            transform_func = getattr(
                                self.transforms, transforms[db_col]
                            )
                            transformed_value = transform_func(raw_value)
                        else:
                            transformed_value = raw_value

                        model_data[db_col] = transformed_value

                # Create model instance
                model_instance = table_model(**model_data)
                session.add(model_instance)
                stats["imported_rows"] += 1

            except Exception as e:
                stats["skipped_rows"] += 1
                stats["errors"].append(f"Row {index}: {str(e)}")

        # Commit changes
        await session.commit()

        return stats

    async def validate_import(self, session: AsyncSession) -> Dict[str, Any]:
        """Validate the imported data."""
        validation_results = {}

        for mapping_key, config in EXCEL_MAPPINGS.items():
            table_model = config["table_model"]

            # Count records
            result = await session.execute(select(table_model))
            count = len(result.all())

            validation_results[mapping_key] = {
                "table_name": table_model.__tablename__,
                "record_count": count,
            }

        return validation_results


# CLI function for running the import
async def run_excel_import(
    excel_path: str = "../../excel-sheet/commodities-compass.xlsx",
):
    """Run the Excel import process."""
    print("Starting Excel to PostgreSQL import...")

    # Initialize importer
    importer = ExcelDataImporter(excel_path)

    # Get database session
    async with get_async_session() as session:
        # Run import
        results = await importer.import_all_sheets(session)

        # Print results
        print("\nImport Results:")
        print("=" * 50)

        for sheet, result in results.items():
            if "error" in result:
                print(f"❌ {sheet}: {result['error']}")
            else:
                print(
                    f"✅ {sheet}: {result['imported_rows']}/{result['total_rows']} rows imported"
                )
                if result["skipped_rows"] > 0:
                    print(f"   ⚠️  {result['skipped_rows']} rows skipped")

        # Validate
        validation = await importer.validate_import(session)
        print("\nValidation Results:")
        print("=" * 30)

        for table, stats in validation.items():
            print(f"{stats['table_name']}: {stats['record_count']} records")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_excel_import())
