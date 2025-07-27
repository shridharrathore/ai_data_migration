"""
Unit tests for the SchemaAnalyzer class.
"""

import pytest
from schema_parser import SchemaAnalyzer

def test_parse_sql_schema():
    sql_input = """
    CREATE TABLE users (
        id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100)
    );
    """
    analyzer = SchemaAnalyzer()
    result = analyzer.parse_sql_schema(sql_input)
    assert len(result) == 1
    assert result[0].table_name == "users"
    assert len(result[0].fields) == 3
    assert result[0].fields[0].name == "id"
    assert result[0].fields[1].nullable is False

def test_parse_csv_schema():
    csv_input = "id,name,email\n1,Alice,alice@example.com"
    analyzer = SchemaAnalyzer()
    schema = analyzer.parse_csv_schema(csv_input)
    assert schema.table_name == "csv_input_table"
    assert len(schema.fields) == 3
    assert schema.fields[0].name == "id"

def test_parse_json_schema():
    json_input = """
    [
        {
            "table_name": "orders",
            "fields": [
                {"name": "order_id", "datatype": "INT", "primary_key": true},
                {"name": "amount", "datatype": "DECIMAL", "nullable": false}
            ]
        }
    ]
    """
    analyzer = SchemaAnalyzer()
    schemas = analyzer.parse_json_schema(json_input)
    assert len(schemas) == 1
    assert schemas[0].table_name == "orders"
    assert schemas[0].fields[0].primary_key is True
