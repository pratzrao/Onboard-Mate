import streamlit as st
import pandas as pd

from schema_table import get_data


# Page: Data Visualization
def visualize_page():

    schema = st.session_state.get("selected_schema")
    table = st.session_state.get("selected_table")

    if schema and table:
        st.header(f"Visualizing Data from {schema}.{table}")
        data = get_data(st.session_state["conn"], schema, table)
        if not data:
            st.error("no data in table")
        else:
            columns_df = pd.DataFrame(data)
            st.write("Columns Information:")

            if len(columns_df.columns) == 2:
                st.bar_chart(columns_df.set_index(columns_df.columns[0]), height=900)
    else:
        st.error("No schema, table, or columns information available!")

    if st.button("Submit"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()
