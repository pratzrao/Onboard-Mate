import streamlit as st

# Page: Data Transformation
def transform_page():
    st.title("Data Transformation Page")
    st.header("This is where you'll transform your data.")
    if st.button("Submit"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()