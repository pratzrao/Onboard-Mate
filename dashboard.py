import streamlit as st

def dashboard_page():
    st.title("Dashboard")

    if not st.session_state.get("dashboard"):
        st.write("No charts added to the dashboard yet.")
    else:
        st.write(f"Displaying {len(st.session_state['dashboard'])} chart(s) from the dashboard:")
        
        for i, chart in enumerate(st.session_state["dashboard"], start=1):
            st.write(f"### Chart {i}")
            st.plotly_chart(chart, use_container_width=True)
    
    if st.button("Back to Table Selection"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()