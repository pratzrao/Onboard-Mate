import streamlit as st

from transform import transform_page
from connection import connection_page
from schema_table import schema_table_page
from visualize import visualize_page
from dashboard import dashboard_page


# Main function to control flow
def main():
    if "connected" not in st.session_state:
        st.session_state["connected"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "connection"  # Default to connection page
    
    # Ensure "dashboard" is initialized
    if "dashboard" not in st.session_state:
        st.session_state["dashboard"] = []  # Initialize an empty dashboard list

    # Navigation between pages
    if not st.session_state["connected"]:
        connection_page()
    elif st.session_state["current_page"] == "table_selection":
        schema_table_page()
    elif st.session_state["current_page"] == "transform":
        transform_page()
    elif st.session_state["current_page"] == "visualize":
        visualize_page()
    elif st.session_state["current_page"] == "dashboard":
        dashboard_page() 


if __name__ == "__main__":
    main()
