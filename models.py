"""
models.py

Contains data model classes used across the MA Migration System.
Each class represents a structured entity such as a field, table, or full migration mapping.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class SchemaField:
    """
    Represents a single column/field in a database table.

    Attributes:
        name: Name of the field.
        datatype: Data type of the field (e.g., VARCHAR, INT).
        nullable: Whether the field is nullable.
        primary_key: Whether this field is a primary key.
    """
    name: str
    datatype: str
    nullable: bool = True
    primary_key: bool = False


@dataclass
class TableSchema:
    """
    Represents a database table schema including its fields and foreign key relationships.

    Attributes:
        table_name: Name of the table.
        fields: List of SchemaField objects.
        relationships: Foreign key relationships to other tables (optional).
    """
    table_name: str
    fields: List[SchemaField]
    relationships: Optional[Dict[str, str]] = field(default_factory=dict)


@dataclass
class FieldMapping:
    """
    Maps a single field from a source to a target system.

    Attributes:
        source_field: Field name in the source system.
        target_field: Field name in the target system.
        transformation: Optional transformation logic.
    """
    source_field: str
    target_field: str
    transformation: Optional[str] = None


@dataclass
class TableMapping:
    """
    Maps a table between source and target systems with associated field mappings.

    Attributes:
        source_table: Name of the source table.
        target_table: Name of the target table.
        field_mappings: List of FieldMapping objects.
        strategy: Migration strategy (e.g., full load, incremental).
        complexity: Estimated complexity (e.g., low, medium, high).
    """
    source_table: str
    target_table: str
    field_mappings: List[FieldMapping]
    strategy: Optional[str] = "full_load"
    complexity: Optional[str] = "medium"


@dataclass
class MigrationMapping:
    """
    Represents the complete migration plan for a system.

    Attributes:
        source_system: Name of the source system.
        target_system: Name of the target system.
        confidence_score: AI-generated confidence score (optional).
        table_mappings: List of TableMapping objects.
        notes: Any human or AI-generated notes.
    """
    source_system: str
    target_system: str
    confidence_score: Optional[float]
    table_mappings: List[TableMapping]
    notes: Optional[str] = ""
