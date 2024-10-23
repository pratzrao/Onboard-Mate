import streamlit as st
from autogen_module_transform import generate_dbt_code
import os

def clean_sql_file_inplace(file_path: str):
    # Read the contents of the SQL file
    with open(file_path, 'r') as file:
        sql_content = file.readlines()
    
    # Remove the 'TERMINATE' keyword and any commented lines
    cleaned_sql_content = []
    for line in sql_content:
        # Skip lines that are commented or contain 'TERMINATE'
        if not line.strip().startswith('--') and 'TERMINATE' not in line and not line.strip().startswith('```'):
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
            full_prompt = (
                f"I need you to write code for a dbt model based on table details and user information that you'll find below. "
                f"We are using a Postgres database. Make sure the model is accurate and will execute with no changes necessary. "
                f"Return only the dbt code. NOTHING ELSE. Don't say anything. Don't acknowledge my question, say yes or sure—just give me the code.\n"
                f"Table Metadata:\n{metadata}\n\nTransformation Instructions:\n{user_prompt}\n\nNew Table: {new_table_name}"
            )

            # Call autogen to generate DBT code
            result = generate_dbt_code(full_prompt, user_prompt)
            if result == "Error":
                st.error("Your request does not seem like a legitimate transformation request. Please rephrase and try again.")
            elif result:
                # Create dbt directory if it doesn't exist
                os.makedirs("dbt", exist_ok=True)

                # Save the DBT code to a file
                dbt_file_path = f"dbt/{new_table_name}.sql"
                with open(dbt_file_path, "w") as f:
                    f.write(str(result["result"]))

                st.success(f"DBT code generated and saved to {dbt_file_path}")
                clean_sql_file_inplace(f"dbt/{new_table_name}.sql")

                
            else:
                st.error("Failed to generate DBT code. Please check your input and try again.")
    
    if st.button("Go Back"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()