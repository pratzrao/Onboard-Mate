from dataclasses import dataclass, fields, asdict

import pandas as pd
import streamlit as st

from autogen_module_visualize import ChartCreator

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
            columns=[
                'Column name',
                'Data Type',
            ],
        )

    @classmethod
    def from_state(cls, state):
        kwargs = { x.name: state.get(x.name) for x in fields(cls) }
        return cls(**kwargs)

@dataclass
class ChatMessage:
    role: str
    content: str

def present_chat(creator):
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m.role):
            st.markdown(m.content)

    prompt = st.chat_input("What is up?")
    if prompt:
        st.session_state.messages.append(ChatMessage('user', prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        messages = list(map(asdict, st.session_state.messages))
        with st.chat_message("assistant"):
            # stream = client.chat.completions.create(
            #     model=st.session_state["openai_model"],
            #     messages=messages,
            #     stream=True,
            # )
            # response = st.write_stream(stream)
            response = creator(messages[-1]['content'])
        st.session_state.messages.append(ChatMessage('assistant', response))

def show_db_info():
    db = DatabaseState.from_state(st.session_state)
    if not db:
        st.error('Schema, data, and column information required')
        st.exception(ValueError())

    st.sidebar.header(f'Visualizing Data from {db}')

    columns_df = db.to_frame()
    st.sidebar.write('Columns Information:')
    st.sidebar.dataframe(columns_df)

# Page: Data Visualization
def visualize_page():
    creator = ChartCreator()

    show_db_info()
    present_chat(creator)
