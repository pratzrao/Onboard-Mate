import os
from pathlib import Path
import logging
import streamlit as st
from autogen_module_transform import generate_dbt_code
from modelgeneration import (
    run_dbt_project,
    create_new_model,
    create_or_append_source_yml,
)


def clean_sql_output(sql_content: str):

    logging.info(
        "========================================================================"
    )
    logging.info(sql_content)
    logging.info(
        "========================================================================"
    )

    # Remove the 'TERMINATE' keyword and any commented lines
    cleaned_sql_content = []
    for line in sql_content.split("\n"):
        # Skip lines that are commented or contain 'TERMINATE'
        line = line.strip()
        if not (
            line.startswith("--")
            or line.startswith("#")
            or line.startswith("```")
            or "TERMINATE" in line
        ):
            line = line.replace(";", "")
            cleaned_sql_content.append(line)

    return "\n".join(cleaned_sql_content)


def transform_page():
    schema = st.session_state.get("selected_schema")
    table = st.session_state.get("selected_table")
    columns_info = st.session_state.get("columns_sample")

    target_dir = Path(os.getenv("DBT_PROJECT_DIR"))
    dbt_venv = Path(os.getenv("DBT_VENV_DIR"))

    # Check if columns_info exists
    if not columns_info:
        st.error("No columns information found. Please go back and select a table.")
        return

    create_or_append_source_yml(target_dir, schema, table)

    # Create metadata from schema, table, and columns
    metadata = f"Schema: {schema}\nTable: {table}\nColumns: " + ", ".join(
        [f"{col[0]} ({col[1]})" for col in columns_info]
    )

    st.title("Data Transformation Page")
    st.header(f"Modify the table: {table} in schema: {schema}")

    # User input for the transformation prompt
    user_prompt = st.text_area(
        "Describe the transformation you want (e.g., 'Drop timestamp column'):"
    )

    # User input for the new table name
    new_table_name = st.text_input(
        "Enter a new table name (it should not match the existing table):"
    )

    if st.button("Generate and Submit DBT Code"):
        if not user_prompt or not new_table_name:
            st.error(
                "Please provide both the transformation prompt and a new table name."
            )
        elif new_table_name == table:
            st.error("The new table name cannot be the same as the existing table.")
        else:
            # Combine metadata with the user prompt

            # Call autogen to generate DBT code
            result = generate_dbt_code(user_prompt, metadata, new_table_name)
            if result == "Error":
                st.error(
                    "Your request does not seem like a legitimate transformation request. Please rephrase and try again."
                )
            elif result:

                # Save the DBT code to a file
                sql_output = clean_sql_output(str(result["result"]))
                logging.info(sql_output)
                create_new_model(target_dir, new_table_name, sql_output)

                st.success("DBT code generated!")
                # Run the dbt project
                run_dbt_project(target_dir, dbt_venv)

            else:
                st.error(
                    "Failed to generate DBT code. Please check your input and try again."
                )

    if st.button("Go Back"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()
