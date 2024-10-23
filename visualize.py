import streamlit

# Page: Data Visualization
def visualize_page():
    st.title("Data Visualization Page")
    st.header("This is where you'll visualize your data.")
    if st.button("Submit"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()