"""
sql_generator.py

Generates SQL scripts for data migration, validation, and rollback based on
the provided MigrationMapping object.
"""

from typing import List
from models import MigrationMapping, TableMapping


class SQLGenerator:
    """
    Generates SQL scripts for performing data migration tasks.
    """

    def generate_migration_sql(self, mapping: MigrationMapping) -> str:
        """
        Generates SQL for migrating data from source to target.

        Args:
            mapping: MigrationMapping object.

        Returns:
            A full SQL string for data migration.
        """
        statements = []
        for table_map in mapping.table_mappings:
            cols = ", ".join([f'"{f.target_field}"' for f in table_map.field_mappings])
            src_cols = ", ".join([f'"{f.source_field}"' for f in table_map.field_mappings])
            sql = f'INSERT INTO "{table_map.target_table}" ({cols}) SELECT {src_cols} FROM "{table_map.source_table}";'
            statements.append(sql)
            if not cols or not src_cols:
                continue  # Skip if columns are missing
            sql = f"INSERT INTO {table_map.target_table} ({cols}) SELECT {src_cols} FROM {table_map.source_table};"
            statements.append(sql)
        return "\n".join(statements)

    def generate_validation_sql(self, mapping: MigrationMapping) -> str:
        """
        Generates SQL to validate row counts between source and target.

        Args:
            mapping: MigrationMapping object.

        Returns:
            A SQL string with COUNT validation queries.
        """
        validation = []
        for t in mapping.table_mappings:
            sql = f"SELECT '{t.source_table}' AS table_name, "                   f"(SELECT COUNT(*) FROM {t.source_table}) AS source_count, "                   f"(SELECT COUNT(*) FROM {t.target_table}) AS target_count;"
            validation.append(sql)
        return "\n".join(validation)

    def generate_rollback_sql(self, mapping: MigrationMapping) -> str:
        """
        Generates SQL to rollback the target tables (e.g., delete loaded rows).

        Args:
            mapping: MigrationMapping object.

        Returns:
            SQL string for rollback.
        """
        rollback = []
        for t in mapping.table_mappings:
            rollback.append(f"DELETE FROM {t.target_table};")
        return "\n".join(rollback)
