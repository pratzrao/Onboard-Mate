import streamlit as st
import pandas as pd

# Helper function to fetch schemas
def get_schemas(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT schema_name FROM information_schema.schemata;")
        schemas = [schema[0] for schema in cur.fetchall()]
        cur.close()
        return schemas
    except Exception as e:
        conn.rollback()  # Rollback transaction in case of failure
        st.error(f"Error fetching schemas: {str(e)}")
        return []

# Helper function to fetch tables in a schema
def get_tables(conn, schema):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}';")
        tables = [table[0] for table in cur.fetchall()]
        cur.close()
        return tables
    except Exception as e:
        conn.rollback()  # Rollback transaction in case of failure
        st.error(f"Error fetching tables: {str(e)}")
        return []

# Helper function to fetch column details
def get_column_info(conn, schema, table):
    try:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = '{schema}' AND table_name = '{table}';
        """)
        columns_info = cur.fetchall()
        cur.close()
        return columns_info
    except Exception as e:
        conn.rollback()  # Rollback transaction in case of failure
        st.error(f"Error fetching column information: {str(e)}")
        return []

# Helper function to fetch distinct values
def get_distinct_values(conn, schema, table, column):
    try:
        if column.lower() == "end":
            column = '"end"'
        else:
            column = f'"{column}"'

        cur = conn.cursor()
        cur.execute(f'SELECT DISTINCT {column} FROM "{schema}"."{table}" LIMIT 5;')
        distinct_values = cur.fetchall()
        cur.close()
        return distinct_values
    except Exception as e:
        conn.rollback()  # Rollback transaction in case of failure
        st.error(f"Error fetching distinct values for column {column}: {str(e)}")
        return []


# Step 2: Schema and Table Selection page
def schema_table_page():
    conn = st.session_state["conn"]

    st.sidebar.title("Connection Details")
    st.sidebar.write(f"Connected to: {st.session_state['database']}")

    st.title("Postgres Data Warehouse Explorer")
    st.header("Step 2: Explore the Database")

    # Select schema
    schemas = get_schemas(conn)
    schema = st.selectbox("Select Schema", schemas, key="schema")

    # Select table
    if schema:
        tables = get_tables(conn, schema)
        table = st.selectbox("Select Table", tables, key="table")

        # If table is selected, fetch column details and distinct values
        if table:
            st.write(f"Selected Table: {table}")

            columns_info = get_column_info(conn, schema, table)
            columns_df = pd.DataFrame(columns_info, columns=["Column Name", "Data Type"])
            st.write("Columns Information:")
            st.dataframe(columns_df)

            st.write("Distinct values in each column:")
            for column in columns_df["Column Name"]:
                distinct_values = get_distinct_values(conn, schema, table, column)
                st.write(f"Column: {column}")
                st.write(distinct_values)

            # Navigation options after table selection
            if st.button("Transform Data"):
                st.session_state["current_page"] = "transform"
                st.rerun()

            if st.button("Visualize Data"):
                st.session_state["current_page"] = "visualize"
                st.rerun()

