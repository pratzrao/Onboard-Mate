import streamlit as st
import pandas as pd

# Page: Data Visualization
def visualize_page():

    schema = st.session_state.get("selected_schema")
    table = st.session_state.get("selected_table")
    columns_info = st.session_state.get("columns_info")


    if schema and table and columns_info:
        st.header(f"Visualizing Data from {schema}.{table}")
        columns_df = pd.DataFrame(columns_info, columns=["Column Name", "Data Type"])
        st.write("Columns Information:")
        st.dataframe(columns_df)
    else:
        st.error("No schema, table, or columns information available!")

    if st.button("Submit"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()