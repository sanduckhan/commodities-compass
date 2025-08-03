#!/usr/bin/env python3
"""
Excel Data Analysis Script for Commodities Compass Database Schema Design

This script analyzes the commodities-compass.xlsx file to understand data structure
and generate PostgreSQL database schema recommendations.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class ExcelDataAnalyzer:
    def __init__(self, excel_path: str):
        self.excel_path = Path(excel_path)
        self.workbook = None
        self.sheet_analysis = {}
        
    def load_workbook(self):
        """Load the Excel workbook and get sheet names."""
        try:
            self.workbook = pd.ExcelFile(self.excel_path)
            print(f"Successfully loaded workbook: {self.excel_path}")
            print(f"Available sheets: {self.workbook.sheet_names}")
            return True
        except Exception as e:
            print(f"Error loading workbook: {e}")
            return False
    
    def analyze_sheet(self, sheet_name: str) -> Dict[str, Any]:
        """Analyze a single sheet and return structure information."""
        try:
            df = pd.read_excel(self.workbook, sheet_name=sheet_name)
            
            analysis = {
                'sheet_name': sheet_name,
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'columns': {},
                'sample_data': {},
                'potential_relationships': [],
                'suggested_table_name': self.suggest_table_name(sheet_name)
            }
            
            # Analyze each column
            for col in df.columns:
                col_analysis = self.analyze_column(df[col], col)
                analysis['columns'][col] = col_analysis
                
                # Get sample data (first 5 non-null values)
                sample_values = df[col].dropna().head(5).tolist()
                analysis['sample_data'][col] = [str(val) for val in sample_values]
            
            # Detect potential foreign keys
            analysis['potential_relationships'] = self.detect_relationships(df)
            
            return analysis
            
        except Exception as e:
            return {'error': f"Failed to analyze sheet {sheet_name}: {e}"}
    
    def analyze_column(self, series: pd.Series, col_name: str) -> Dict[str, Any]:
        """Analyze a single column to determine data type and constraints."""
        analysis = {
            'column_name': col_name,
            'suggested_db_name': self.suggest_column_name(col_name),
            'pandas_dtype': str(series.dtype),
            'non_null_count': series.count(),
            'null_count': series.isnull().sum(),
            'unique_count': series.nunique(),
            'suggested_sql_type': None,
            'constraints': [],
            'is_potential_primary_key': False,
            'is_potential_foreign_key': False
        }
        
        # Determine SQL data type
        if pd.api.types.is_integer_dtype(series):
            analysis['suggested_sql_type'] = 'INTEGER'
            if analysis['unique_count'] == analysis['non_null_count'] and 'id' in col_name.lower():
                analysis['is_potential_primary_key'] = True
                analysis['constraints'].append('PRIMARY KEY')
        
        elif pd.api.types.is_float_dtype(series):
            analysis['suggested_sql_type'] = 'DECIMAL(15,6)'
        
        elif pd.api.types.is_datetime64_any_dtype(series):
            analysis['suggested_sql_type'] = 'TIMESTAMP'
        
        elif pd.api.types.is_bool_dtype(series):
            analysis['suggested_sql_type'] = 'BOOLEAN'
        
        else:  # String/object type
            max_length = series.astype(str).str.len().max() if not series.empty else 0
            if max_length <= 50:
                analysis['suggested_sql_type'] = f'VARCHAR({max(max_length * 2, 100)})'
            elif max_length <= 255:
                analysis['suggested_sql_type'] = f'VARCHAR({max_length * 2})'
            else:
                analysis['suggested_sql_type'] = 'TEXT'
            
            # Check for potential foreign keys
            if any(keyword in col_name.lower() for keyword in ['id', 'key', 'ref']):
                analysis['is_potential_foreign_key'] = True
        
        # Add NOT NULL constraint if no nulls
        if analysis['null_count'] == 0:
            analysis['constraints'].append('NOT NULL')
        
        return analysis
    
    def detect_relationships(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect potential relationships between columns."""
        relationships = []
        
        for col in df.columns:
            col_lower = col.lower()
            
            # Look for foreign key patterns
            if any(pattern in col_lower for pattern in ['_id', 'id_', 'ref_', '_ref']):
                relationships.append({
                    'type': 'potential_foreign_key',
                    'column': col,
                    'description': f'{col} appears to be a foreign key reference'
                })
            
            # Look for categorical data that might need lookup tables
            if df[col].nunique() < 20 and df[col].nunique() > 1:
                relationships.append({
                    'type': 'potential_lookup_table',
                    'column': col,
                    'unique_values': df[col].unique().tolist()[:10],
                    'description': f'{col} has {df[col].nunique()} unique values, consider lookup table'
                })
        
        return relationships
    
    def suggest_table_name(self, sheet_name: str) -> str:
        """Suggest a PostgreSQL-friendly table name."""
        # Convert to lowercase and replace spaces/special chars with underscores
        name = re.sub(r'[^a-zA-Z0-9_]', '_', sheet_name.lower())
        # Remove multiple consecutive underscores
        name = re.sub(r'_+', '_', name)
        # Remove leading/trailing underscores
        name = name.strip('_')
        return name
    
    def suggest_column_name(self, col_name: str) -> str:
        """Suggest a PostgreSQL-friendly column name."""
        # Convert to lowercase and replace spaces/special chars with underscores
        name = re.sub(r'[^a-zA-Z0-9_]', '_', col_name.lower())
        # Remove multiple consecutive underscores
        name = re.sub(r'_+', '_', name)
        # Remove leading/trailing underscores
        name = name.strip('_')
        return name
    
    def analyze_all_sheets(self) -> Dict[str, Any]:
        """Analyze all sheets in the workbook."""
        if not self.load_workbook():
            return {'error': 'Failed to load workbook'}
        
        analysis = {
            'workbook_info': {
                'file_path': str(self.excel_path),
                'sheet_count': len(self.workbook.sheet_names),
                'sheet_names': self.workbook.sheet_names,
                'analysis_timestamp': datetime.now().isoformat()
            },
            'sheets': {},
            'database_schema_suggestions': {}
        }
        
        # Analyze each sheet
        for sheet_name in self.workbook.sheet_names:
            print(f"\nAnalyzing sheet: {sheet_name}")
            sheet_analysis = self.analyze_sheet(sheet_name)
            analysis['sheets'][sheet_name] = sheet_analysis
            
            if 'error' not in sheet_analysis:
                print(f"  - Rows: {sheet_analysis['total_rows']}")
                print(f"  - Columns: {sheet_analysis['total_columns']}")
                print(f"  - Suggested table: {sheet_analysis['suggested_table_name']}")
        
        # Generate database schema suggestions
        analysis['database_schema_suggestions'] = self.generate_schema_suggestions(analysis['sheets'])
        
        return analysis
    
    def generate_schema_suggestions(self, sheets_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate PostgreSQL schema suggestions based on analysis."""
        suggestions = {
            'tables': {},
            'relationships': [],
            'indexes': [],
            'general_recommendations': []
        }
        
        for sheet_name, sheet_data in sheets_analysis.items():
            if 'error' in sheet_data:
                continue
                
            table_name = sheet_data['suggested_table_name']
            
            # Generate CREATE TABLE statement
            create_table = f"CREATE TABLE {table_name} (\n"
            columns = []
            
            for col_name, col_data in sheet_data['columns'].items():
                col_def = f"    {col_data['suggested_db_name']} {col_data['suggested_sql_type']}"
                
                if 'NOT NULL' in col_data['constraints']:
                    col_def += " NOT NULL"
                
                if 'PRIMARY KEY' in col_data['constraints']:
                    col_def += " PRIMARY KEY"
                
                columns.append(col_def)
            
            create_table += ",\n".join(columns)
            create_table += "\n);"
            
            suggestions['tables'][table_name] = {
                'create_statement': create_table,
                'source_sheet': sheet_name,
                'estimated_rows': sheet_data['total_rows']
            }
            
            # Suggest indexes
            for col_name, col_data in sheet_data['columns'].items():
                if col_data['is_potential_foreign_key']:
                    suggestions['indexes'].append(
                        f"CREATE INDEX idx_{table_name}_{col_data['suggested_db_name']} "
                        f"ON {table_name}({col_data['suggested_db_name']});"
                    )
        
        # Add general recommendations
        suggestions['general_recommendations'] = [
            "Review suggested data types and adjust precision as needed",
            "Validate foreign key relationships between tables",
            "Consider adding created_at/updated_at timestamps to tables",
            "Add appropriate constraints and check constraints",
            "Review indexes for query optimization",
            "Consider partitioning for large tables (>1M rows)"
        ]
        
        return suggestions
    
    def save_analysis(self, analysis: Dict[str, Any], output_path: str = None):
        """Save analysis results to JSON file."""
        if output_path is None:
            output_path = self.excel_path.parent / "excel_analysis_results.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nAnalysis results saved to: {output_path}")
    
    def print_summary(self, analysis: Dict[str, Any]):
        """Print a summary of the analysis."""
        print("\n" + "="*80)
        print("EXCEL DATA ANALYSIS SUMMARY")
        print("="*80)
        
        workbook_info = analysis['workbook_info']
        print(f"File: {workbook_info['file_path']}")
        print(f"Sheets analyzed: {workbook_info['sheet_count']}")
        print(f"Analysis timestamp: {workbook_info['analysis_timestamp']}")
        
        print(f"\nSheets found: {', '.join(workbook_info['sheet_names'])}")
        
        for sheet_name, sheet_data in analysis['sheets'].items():
            if 'error' in sheet_data:
                print(f"\n❌ {sheet_name}: {sheet_data['error']}")
                continue
                
            print(f"\n📊 {sheet_name}:")
            print(f"   Suggested table: {sheet_data['suggested_table_name']}")
            print(f"   Dimensions: {sheet_data['total_rows']} rows × {sheet_data['total_columns']} columns")
            
            # Show column summary
            print("   Columns:")
            for col_name, col_data in sheet_data['columns'].items():
                constraints_str = ', '.join(col_data['constraints']) if col_data['constraints'] else 'None'
                print(f"     - {col_name} → {col_data['suggested_db_name']} ({col_data['suggested_sql_type']}) [{constraints_str}]")
        
        # Show schema suggestions summary
        schema_suggestions = analysis['database_schema_suggestions']
        print(f"\n🗄️  DATABASE SCHEMA SUGGESTIONS:")
        print(f"   Tables to create: {len(schema_suggestions['tables'])}")
        print(f"   Indexes suggested: {len(schema_suggestions['indexes'])}")
        
        print("\n📝 GENERAL RECOMMENDATIONS:")
        for rec in schema_suggestions['general_recommendations']:
            print(f"   • {rec}")


def main():
    """Main function to run the analysis."""
    excel_path = "../excel-sheet/commodities-compass.xlsx"
    
    print("Commodities Compass - Excel Data Analysis")
    print("="*50)
    
    analyzer = ExcelDataAnalyzer(excel_path)
    analysis_results = analyzer.analyze_all_sheets()
    
    if 'error' in analysis_results:
        print(f"❌ Analysis failed: {analysis_results['error']}")
        return
    
    # Print summary
    analyzer.print_summary(analysis_results)
    
    # Save detailed results
    analyzer.save_analysis(analysis_results)
    
    # Generate SQL schema file
    schema_file = Path("database_schema_suggestions.sql")
    with open(schema_file, 'w') as f:
        f.write("-- PostgreSQL Database Schema Suggestions for Commodities Compass\n")
        f.write("-- Generated from Excel analysis\n\n")
        
        for table_name, table_info in analysis_results['database_schema_suggestions']['tables'].items():
            f.write(f"-- Table: {table_name} (from sheet: {table_info['source_sheet']})\n")
            f.write(f"-- Estimated rows: {table_info['estimated_rows']}\n")
            f.write(table_info['create_statement'])
            f.write("\n\n")
        
        f.write("-- Suggested Indexes\n")
        for index in analysis_results['database_schema_suggestions']['indexes']:
            f.write(f"{index}\n")
    
    print(f"\n💾 SQL schema suggestions saved to: {schema_file}")
    
    print("\n✅ Analysis complete! Review the generated files:")
    print("   • excel_analysis_results.json - Detailed analysis data")
    print("   • database_schema_suggestions.sql - PostgreSQL schema suggestions")


if __name__ == "__main__":
    main()