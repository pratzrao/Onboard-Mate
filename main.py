import streamlit as st
import psycopg2
import pandas as pd

# Helper function to connect to the Postgres database
def connect_to_db(host, port, database, user, password):
    try:
        conn = psycopg2.connect(
            host=host, port=port, dbname=database, user=user, password=password
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to Postgres: {str(e)}")
        return None

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

# Page: Data Transformation
def transform_page():
    st.title("Data Transformation Page")
    st.header("This is where you'll transform your data.")
    if st.button("Submit"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()

# Page: Data Visualization
def visualize_page():
    st.title("Data Visualization Page")
    st.header("This is where you'll visualize your data.")
    if st.button("Submit"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()

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

# Page: Connection page
def connection_page():
    st.title("Postgres Data Warehouse Explorer")
    st.header("Step 1: Connect to the Database")

    if "host" not in st.session_state:
        st.session_state["host"] = ""
    if "port" not in st.session_state:
        st.session_state["port"] = "5432"
    if "database" not in st.session_state:
        st.session_state["database"] = ""
    if "user" not in st.session_state:
        st.session_state["user"] = ""
    if "password" not in st.session_state:
        st.session_state["password"] = ""

    # Input fields for connection
    st.session_state["host"] = st.text_input("Host", value=st.session_state["host"])
    st.session_state["port"] = st.text_input("Port", value=st.session_state["port"])
    st.session_state["database"] = st.text_input("Database", value=st.session_state["database"])
    st.session_state["user"] = st.text_input("Username", value=st.session_state["user"])
    st.session_state["password"] = st.text_input("Password", type="password", value=st.session_state["password"])

    if st.button("Connect"):
        conn = connect_to_db(
            st.session_state["host"],
            st.session_state["port"],
            st.session_state["database"],
            st.session_state["user"],
            st.session_state["password"]
        )
        if conn:
            st.session_state["conn"] = conn
            st.session_state["connected"] = True
            st.session_state["current_page"] = "table_selection"  # Set initial page after connection
            st.success("Connected to Postgres database!")
            st.rerun()

# Main function to control flow
def main():
    if "connected" not in st.session_state:
        st.session_state["connected"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "connection"  # Default to connection page

    # Navigation between pages
    if not st.session_state["connected"]:
        connection_page()
    elif st.session_state["current_page"] == "table_selection":
        schema_table_page()
    elif st.session_state["current_page"] == "transform":
        transform_page()
    elif st.session_state["current_page"] == "visualize":
        visualize_page()

if __name__ == "__main__":
    main()