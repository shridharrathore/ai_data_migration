"""
ai_mapping_engine.py

Provides the GenAIMappingEngine class which uses GenAI models to
generate intelligent mappings between source and target schemas.
"""

import json
from typing import List
from models import TableSchema, FieldMapping, TableMapping, MigrationMapping


class GenAIMappingEngine:
    """
    Simulates the use of a GenAI engine to auto-generate field and table mappings
    based on schema context and business logic.
    """

    def generate_mappings(
        self,
        source_schema: List[TableSchema],
        target_schema: List[TableSchema],
        business_context: str
    ) -> MigrationMapping:
        """
        Generates migration mappings using GenAI.

        Args:
            source_schema: Parsed source schema tables.
            target_schema: Parsed target schema tables.
            business_context: Business use case driving the migration.

        Returns:
            A fully populated MigrationMapping object.
        """
        prompt = self._prepare_mapping_context(source_schema, target_schema, business_context)
        response = self._call_ai_for_mappings(prompt)
        return self._parse_ai_mapping_response(response)

    def _prepare_mapping_context(
        self,
        source: List[TableSchema],
        target: List[TableSchema],
        context: str
    ) -> str:
        """
        Prepares AI prompt string.

        Args:
            source: Source schema.
            target: Target schema.
            context: Business context string.

        Returns:
            Prompt string.
        """
        return json.dumps({
            "source": [t.__dict__ for t in source],
            "target": [t.__dict__ for t in target],
            "business_context": context
        })

    def _call_ai_for_mappings(self, prompt: str) -> str:
        """
        Placeholder function to simulate AI response.

        Args:
            prompt: AI input string.

        Returns:
            Simulated JSON response.
        """
        # Simulated AI output
        return json.dumps({
            "source_system": "SourceSystem",
            "target_system": "TargetSystem",
            "confidence_score": 0.95,
            "notes": "Auto-mapped using GenAI",
            "table_mappings": [
                {
                    "source_table": "users",
                    "target_table": "customers",
                    "field_mappings": [
                        {"source_field": "id", "target_field": "cust_id"},
                        {"source_field": "name", "target_field": "full_name"}
                    ],
                    "strategy": "full_load",
                    "complexity": "medium"
                }
            ]
        })

    def _parse_ai_mapping_response(self, response: str) -> MigrationMapping:
        """
        Parses the AI JSON response into data model objects.

        Args:
            response: Raw JSON string from GenAI.

        Returns:
            MigrationMapping instance.
        """
        data = json.loads(response)
        table_mappings = []
        for t in data.get("table_mappings", []):
            field_mappings = [
                FieldMapping(**f) for f in t.get("field_mappings", [])
            ]
            table_mappings.append(TableMapping(
                source_table=t["source_table"],
                target_table=t["target_table"],
                field_mappings=field_mappings,
                strategy=t.get("strategy"),
                complexity=t.get("complexity")
            ))
        return MigrationMapping(
            source_system=data["source_system"],
            target_system=data["target_system"],
            confidence_score=data.get("confidence_score"),
            table_mappings=table_mappings,
            notes=data.get("notes", "")
        )
