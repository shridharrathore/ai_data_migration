# ai_data_migration

This app can migrate data from source to target using LLM to generate mappings and sql scripts

# MA Data Migration System

This project automates schema mapping and SQL generation for data migration scenarios in mergers & acquisitions (M&A).

## 📁 Project Structure

| File                   | Description                                                   |
| ---------------------- | ------------------------------------------------------------- |
| `models.py`            | Contains data model classes used throughout the system        |
| `schema_parser.py`     | Parses SQL, CSV, JSON schema files into structured models     |
| `ai_mapping_engine.py` | Simulates GenAI to generate mappings from source to target    |
| `sql_generator.py`     | Generates SQL scripts for migration, validation, and rollback |
| `orchestrator.py`      | Coordinates the full migration workflow                       |
| `main.py`              | CLI entry point to run the orchestrator                       |
| `README.md`            | Project usage instructions and structure                      |

## 🚀 How to Run

```bash
python main.py source_schema.sql target_schema.csv "Customer system migration" ./output
```

## 📦 Outputs

- `migration_mapping.json` – Field & table mappings
- `migration.sql` – SQL to migrate data
- `validation.sql` – SQL to validate migrated data
- `rollback.sql` – Rollback SQL script

## ✅ Requirements

- Python 3.7+
- No external dependencies (only standard library)

## 🧪 Testing

You can extend the system by adding unit tests to verify parser, mapping, and generator behavior.
