"""
orchestrator.py

Coordinates the full migration workflow from parsing schemas to generating
mappings and creating SQL scripts.
"""

import os
import json
from typing import List
from models import TableSchema, MigrationMapping
from schema_parser import SchemaAnalyzer
from ai_mapping_engine import GenAIMappingEngine
from sql_generator import SQLGenerator


class MigrationOrchestrator:
    """
    Main driver class to execute the full migration workflow.
    """

    def __init__(self):
        self.parser = SchemaAnalyzer()
        self.mapper = GenAIMappingEngine()
        self.sql_generator = SQLGenerator()

    def execute_migration_workflow(self, source_file: str, target_file: str,
                                   business_context: str, output_dir: str) -> MigrationMapping:
        """
        Full pipeline: parse input → AI mapping → SQL generation → save outputs.

        Args:
            source_file: Path to source schema file (.sql, .csv, .json)
            target_file: Path to target schema file (.sql, .csv, .json)
            business_context: Description of business purpose.
            output_dir: Directory to write outputs.

        Returns:
            MigrationMapping object with all mapping info.
        """
        source_schema = self._parse_input_file(source_file)
        target_schema = self._parse_input_file(target_file)
        mapping = self.mapper.generate_mappings(source_schema, target_schema, business_context)

        # Generate and save SQL artifacts
        migration_sql = self.sql_generator.generate_migration_sql(mapping)
        validation_sql = self.sql_generator.generate_validation_sql(mapping)
        rollback_sql = self.sql_generator.generate_rollback_sql(mapping)

        os.makedirs(output_dir, exist_ok=True)
        self._save_file(os.path.join(output_dir, "migration_mapping.json"), json.dumps(mapping, default=lambda o: o.__dict__, indent=2))
        self._save_file(os.path.join(output_dir, "migration.sql"), migration_sql)
        self._save_file(os.path.join(output_dir, "validation.sql"), validation_sql)
        self._save_file(os.path.join(output_dir, "rollback.sql"), rollback_sql)

        return mapping

    def _parse_input_file(self, file_path: str) -> List[TableSchema]:
        """
        Parses a file based on extension type.

        Args:
            file_path: File path string.

        Returns:
            List of TableSchema objects.
        """
        with open(file_path, "r") as f:
            content = f.read()

        if file_path.endswith(".sql"):
            return self.parser.parse_sql_schema(content)
        elif file_path.endswith(".csv"):
            return [self.parser.parse_csv_schema(content)]
        elif file_path.endswith(".json"):
            return self.parser.parse_json_schema(content)
        else:
            raise ValueError("Unsupported file format")

    def _save_file(self, path: str, content: str):
        """
        Saves a text file.

        Args:
            path: File path to write to.
            content: Content string.
        """
        with open(path, "w") as f:
            f.write(content)
