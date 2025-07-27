"""
main.py

Entry point to run the full MA Migration workflow from command line.
"""

import sys
from orchestrator import MigrationOrchestrator

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python main.py <source_file> <target_file> <business_context> <output_dir>")
        sys.exit(1)

    source_file = sys.argv[1]
    target_file = sys.argv[2]
    business_context = sys.argv[3]
    output_dir = sys.argv[4]

    orchestrator = MigrationOrchestrator()
    mapping = orchestrator.execute_migration_workflow(
        source_file=source_file,
        target_file=target_file,
        business_context=business_context,
        output_dir=output_dir
    )

    print("Migration mapping and SQL scripts generated successfully.")
