import streamlit as st
from autogen_module_transform import generate_dbt_code
import os
from modelgeneration import run_dbt_project, create_new_model, create_or_append_source_yml

def clean_sql_file_inplace(file_path: str):
    # Read the contents of the SQL file
    with open(file_path, 'r') as file:
        sql_content = file.readlines()
    
    # Remove the 'TERMINATE' keyword and any commented lines
    cleaned_sql_content = []
    for line in sql_content:
        # Skip lines that are commented or contain 'TERMINATE'
        if not line.strip().startswith('--') and not line.strip().startswith('#') and 'TERMINATE' not in line and not line.strip().startswith('```'):
            cleaned_sql_content.append(line)

    # Join the cleaned SQL content
    cleaned_sql = ''.join(cleaned_sql_content)

    # Write the cleaned SQL back to the original file (in-place modification)
    with open(file_path, 'w') as file:
        file.write(cleaned_sql)

def transform_page():
    schema = st.session_state.get("selected_schema")
    table = st.session_state.get("selected_table")
    columns_info = st.session_state.get("columns_sample")

    # Check if columns_info exists
    if not columns_info:
        st.error("No columns information found. Please go back and select a table.")
        return

    # Create metadata from schema, table, and columns
    metadata = f"Schema: {schema}\nTable: {table}\nColumns: " + ", ".join([f"{col[0]} ({col[1]})" for col in columns_info])

    st.title("Data Transformation Page")
    st.header(f"Modify the table: {table} in schema: {schema}")

    # User input for the transformation prompt
    user_prompt = st.text_area("Describe the transformation you want (e.g., 'Drop timestamp column'):")

    # User input for the new table name
    new_table_name = st.text_input("Enter a new table name (it should not match the existing table):")

    if st.button("Generate and Submit DBT Code"):
        if not user_prompt or not new_table_name:
            st.error("Please provide both the transformation prompt and a new table name.")
        elif new_table_name == table:
            st.error("The new table name cannot be the same as the existing table.")
        else:
            # Combine metadata with the user prompt
            

            # Call autogen to generate DBT code
            result = generate_dbt_code(user_prompt, metadata, new_table_name)
            if result == "Error":
                st.error("Your request does not seem like a legitimate transformation request. Please rephrase and try again.")
            elif result:
                # Create dbt directory if it doesn't exist
                os.makedirs("dbt", exist_ok=True)

                # Save the DBT code to a file
                dbt_file_path = f"dbt/{new_table_name}.sql"
                with open(dbt_file_path, "w") as f:
                    f.write(str(result["result"]))

                st.success(f"DBT code generated!")
                clean_sql_file_inplace(f"dbt/{new_table_name}.sql")
                create_or_append_source_yml(schema, table)

                create_new_model(new_table_name, str(result["result"]))
                clean_sql_file_inplace(f"dbt_project/models/{new_table_name}.sql")

                # Run the dbt project
                run_dbt_project()

                
            else:
                st.error("Failed to generate DBT code. Please check your input and try again.")
    
    if st.button("Go Back"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()