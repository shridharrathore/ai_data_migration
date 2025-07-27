"""
schema_parser.py

Contains the SchemaAnalyzer class responsible for parsing schema definitions
from SQL, CSV, or JSON files into structured Python data models.
"""

import re
import csv
import json
from typing import List
from models import SchemaField, TableSchema


class SchemaAnalyzer:
    """
    Parses input schema files and converts them into TableSchema objects
    for use in data migration logic.
    """

    def parse_sql_schema(self, sql_text: str) -> List[TableSchema]:
        """
        Parses SQL DDL statements and extracts table definitions.

        Args:
            sql_text: Full SQL script as string.

        Returns:
            List of TableSchema objects parsed from the script.
        """
        table_blocks = re.findall(r'CREATE TABLE.*?;', sql_text, re.DOTALL | re.IGNORECASE)
        tables = [self._parse_create_table(block) for block in table_blocks]
        return [t for t in tables if t is not None]

    def parse_csv_schema(self, csv_text: str) -> TableSchema:
        """
        Infers schema from a CSV sample.

        Args:
            csv_text: Content of the CSV file as string.

        Returns:
            TableSchema object inferred from headers.
        """
        lines = csv_text.strip().splitlines()
        reader = csv.reader(lines)
        headers = next(reader)
        fields = [SchemaField(name=h.strip(), datatype="VARCHAR", nullable=True) for h in headers]
        return TableSchema(table_name="csv_input_table", fields=fields)

    def parse_json_schema(self, json_text: str) -> List[TableSchema]:
        """
        Parses schema from a structured JSON input.

        Args:
            json_text: JSON file content containing schema info.

        Returns:
            List of TableSchema objects.
        """
        raw = json.loads(json_text)
        if isinstance(raw, dict):
            raw = [raw]
        schemas = []
        for entry in raw:
            table_name = entry.get("table_name")
            fields = [
                SchemaField(
                    name=f.get("name"),
                    datatype=f.get("datatype", "VARCHAR"),
                    nullable=f.get("nullable", True),
                    primary_key=f.get("primary_key", False),
                ) for f in entry.get("fields", [])
            ]
            schemas.append(TableSchema(table_name=table_name, fields=fields))
        return schemas

    def _parse_create_table(self, ddl: str) -> TableSchema:
        """
        Helper function to parse a single CREATE TABLE block.

        Args:
            ddl: SQL DDL string for a table.

        Returns:
            TableSchema object or None.
        """
        try:
            table_name_match = re.search(r'CREATE TABLE\s+([^\s(]+)', ddl, re.IGNORECASE)
            if not table_name_match:
                return None
            table_name = table_name_match.group(1)
            column_block = ddl[ddl.find("(")+1: ddl.rfind(")")]
            lines = [l.strip().strip(",") for l in column_block.splitlines() if l.strip()]
            fields = []
            for line in lines:
                parts = line.split()
                if len(parts) < 2 or parts[0].upper() in ("PRIMARY", "FOREIGN", "CONSTRAINT"):
                    continue
                field_name = parts[0]
                datatype = parts[1]
                nullable = not ("NOT NULL" in line.upper())
                pk = "PRIMARY KEY" in line.upper()
                fields.append(SchemaField(name=field_name, datatype=datatype, nullable=nullable, primary_key=pk))
            return TableSchema(table_name=table_name, fields=fields)
        except Exception:
            return None
