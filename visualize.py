from dataclasses import dataclass, fields

import pandas as pd
import streamlit as st

from autogen_module_visualize import generate_charts

@dataclass
class DatabaseState:
    selected_schema: str
    selected_table: str
    columns_info: list

    def __str__(self):
        return f'{self.selected_schema}.{self.selected_table}'

    def to_frame(self):
        return pd.DataFrame(
            self.columns_info,
            columns=['Column name', 'Data Type'],
        )

    @classmethod
    def from_state(cls, state):
        kwargs = { x.name: state.get(x.name) for x in fields(cls) }
        return cls(**kwargs)

# Page: Data Visualization
def visualize_page():
    db = DatabaseState.from_state(st.session_state
    if not db:
        st.error('Schema, data, and column information required')
        st.exception(ValueError())

    st.header(f'Visualizing Data from {db}')

    columns_df = db.to_frame()
    st.write("Columns Information:")
    st.dataframe(columns_df)

    message = st.text_area('What would you like to see from your data?')
    if st.button("Submit"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()