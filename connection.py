import streamlit as st
import psycopg2

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

    # # Input fields for connection - Actual
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