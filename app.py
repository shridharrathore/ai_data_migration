import streamlit as st
import json
from sql_generator import SQLGenerator
from models import TableSchema

st.title("SQL Generation Tester")

# Upload JSON
uploaded_file = st.file_uploader("Upload JSON Mapping File", type=["json"])

if uploaded_file:
    try:
        raw_json = json.load(uploaded_file)
        st.subheader("Parsed JSON Input")
        st.json(raw_json)

        # Validate schema using Pydantic
        schema = TableSchema(**raw_json)

        # Generate SQL using class
        sql_gen = SQLGenerator()
        sql_script = sql_gen.generate_migration_sql(schema)

        st.subheader("🔧 Generated SQL Script")
        st.code(sql_script, language="sql")

        st.subheader("🧠 Explanation")
        st.markdown(f"- This script creates a table named **`{schema.table_name}`**.")
        st.markdown("- It includes the following columns:")

        for col in schema.columns:
            st.markdown(f"  - **{col.name}**: `{col.type}`")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
