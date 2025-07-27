"""
Unit tests for the SQLGenerator class.
"""

import json
from sql_generator import SQLGenerator
from models import MigrationMapping, TableMapping, FieldMapping

def test_generate_sql_from_sample_json():
    with open("sample_migration_mapping.json", "r") as f:
        data = json.load(f)
        print(f"Loaded data: {data}")
    table_mappings = []
    for t in data["table_mappings"]:
        fields = [FieldMapping(**f) for f in t["field_mappings"]]
        table_mappings.append(TableMapping(
            source_table=t["source_table"],
            target_table=t["target_table"],
            field_mappings=fields,
            strategy=t.get("strategy"),
            complexity=t.get("complexity")
        ))

    mapping = MigrationMapping(
        source_system=data["source_system"],
        target_system=data["target_system"],
        confidence_score=data.get("confidence_score"),
        table_mappings=table_mappings,
        notes=data.get("notes", "")
    )

    generator = SQLGenerator()
    migration_sql = generator.generate_migration_sql(mapping)
    validation_sql = generator.generate_validation_sql(mapping)
    rollback_sql = generator.generate_rollback_sql(mapping)

    print(migration_sql)
    print(validation_sql)
    print(rollback_sql)

    assert "INSERT INTO users_new" in migration_sql
    assert "SELECT COUNT(*) FROM users_old" in validation_sql
    assert "DELETE FROM users_new" in rollback_sql
