# import logging
from dataclasses import dataclass, fields, asdict

import pandas as pd
import streamlit as st

from autogen_module_visualize import ChartCreator

@dataclass
class DatabaseConnection:
    user: str
    password: str
    host: str
    database: str

    def __str__(self):
        return 'postgresql://{}:{}@{}?dbname={}'.format(
            self.user,
            self.password,
            self.host,
            self.database,
        )

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

    def select(self):
        con = dc_from_state(DatabaseConnection)
        return pd.read_sql_query(f'SELECT * FROM {self}', con=str(con))

@dataclass
class ChatMessage:
    role: str
    content: str

def dc_from_state(cls):
    kwargs = { x.name: st.session_state[x.name] for x in fields(cls) }
    return cls(**kwargs)

def present_chat(db, creator):
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m.role):
            st.markdown(m.content)

    prompt = st.chat_input("What is up?")
    if prompt:
        _prompt = f'''
<instructions>
You will be presented with a table from database. The table will be represented in two ways:

1. A database schema describing columns and column types
2. A dump of the database as JSON

Use the database schema and values to answer the user request.
</instructions>

<database_schema>
{db.to_frame().to_json(orient='records')}
</database_schema>

<database_json_dump>
{db.select().to_json(orient='records')}
</database_json_dump>

<user_request>
{prompt}
</user_request>
'''
        st.session_state.messages.append(ChatMessage('user', _prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        messages = list(map(asdict, st.session_state.messages))
        with st.chat_message("assistant"):
            response = creator(messages[-1]['content'])
        st.session_state.messages.append(ChatMessage('assistant', response))

def show_db_info(db):
    st.sidebar.header(f'Visualizing Data from {db}')
    st.sidebar.write('Columns Information:')
    st.sidebar.dataframe(db.to_frame())

# Page: Data Visualization
def visualize_page():
    db = dc_from_state(DatabaseState)
    if not db:
        st.error('Schema, data, and column information required')
        st.exception(ValueError())
    show_db_info(db)
    present_chat(db, ChartCreator())
