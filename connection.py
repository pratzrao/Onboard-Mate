import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv

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
    # Load environment variables from .env file (if available)
    load_dotenv(dotenv_path="details.env")

    # Debug: print environment variables to ensure they are being loaded
    print("Loaded environment variables:")
    print("DBHOST:", os.getenv("DBHOST"))
    print("DBPORT:", os.getenv("DBPORT"))
    print("DBNAME:", os.getenv("DBNAME"))
    print("DBUSER:", os.getenv("DBUSER"))
    print("DBPASSWORD:", os.getenv("DBPASSWORD"))

    # Set default values from environment variables or keep them empty
    env_host = os.getenv("DBHOST", "")
    env_port = os.getenv("DBPORT", "5432")
    env_database = os.getenv("DBNAME", "")
    env_user = os.getenv("DBUSER", "")
    env_password = os.getenv("DBPASSWORD", "")

    st.title("Postgres Data Warehouse Explorer")
    st.header("Step 1: Connect to the Database")

    # Initialize session state with environment variables if they are not already set
    if "host" not in st.session_state:
        st.session_state["host"] = env_host
    if "port" not in st.session_state:
        st.session_state["port"] = env_port
    if "database" not in st.session_state:
        st.session_state["database"] = env_database
    if "user" not in st.session_state:
        st.session_state["user"] = env_user
    if "password" not in st.session_state:
        st.session_state["password"] = env_password

    # Input fields for connection (pre-filled with session state values or environment variables)
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