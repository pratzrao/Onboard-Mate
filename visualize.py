
import streamlit as st
import pandas as pd
import openai
import plotly.express as px
import os
from schema_table import get_data

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def visualize_page():
    schema = st.session_state.get("selected_schema")
    table = st.session_state.get("selected_table")

    # Ensure "dashboard" is initialized before use
    if "dashboard" not in st.session_state:
        st.session_state["dashboard"] = []  # Initialize an empty list if not present

    if schema and table:
        st.header(f"Visualizing Data from {schema}.{table}")
        data, col_names = get_data(st.session_state["conn"], schema, table)  # Fetch data and column names
        
        if not data:
            st.error("No data in table")
        else:
            # Create the DataFrame using both data and column names
            columns_df = pd.DataFrame(data, columns=col_names)
            st.write("Columns Information:")
            st.dataframe(columns_df)

            # Step 1: User input for chart description
            user_input = st.text_input("Describe the chart you want to see (e.g., 'bar chart of age by gender' or 'pie chart of total donations by country'):")

            if user_input:
                st.write(f"Processing: {user_input}")
                
                # Step 2: Call OpenAI API to interpret the input
                chart_params = get_chart_params_from_openai(user_input, columns_df)

                if chart_params:
                    chart_type = chart_params.get("chart_type")

                    # Only show sorting options for bar, line, and scatter charts
                    if chart_type in ["bar", "line", "scatter"]:
                        sort_by = st.selectbox("Sort by", ["None", "X axis", "Y axis"])
                        order = st.selectbox("Order", ["Ascending", "Descending"])
                    else:
                        sort_by = "None"
                        order = "Ascending"

                    # Step 3: Generate and render the chart based on the interpreted parameters
                    chart = create_chart(chart_params, columns_df, sort_by, order)

                    # Add the "Add to Dashboard" button
                    if chart and st.button("Add to Dashboard"):
                        st.session_state["dashboard"].append(chart)
                        st.success("Chart added to dashboard!")

                else:
                    st.error("Could not generate chart parameters from your input.")
    else:
        st.error("No schema, table, or columns information available!")

    if st.button("Go Back"):
        st.session_state["current_page"] = "table_selection"
        st.rerun()

def get_chart_params_from_openai(user_input, columns_df):
    """Send the user input to OpenAI API and parse the response for chart details."""
    
    # Determine if each column is numeric or text
    column_info = {col: "numeric" if pd.api.types.is_numeric_dtype(columns_df[col]) else "text" 
                   for col in columns_df.columns}

    # Prepare the prompt to send to OpenAI
    
    # Prepare the prompt to send to OpenAI
    prompt = f"""
    You are a data visualization assistant. The user has data with the following columns: {column_info}. 
    Based on their request, generate a JSON structure with chart details. The user asked for: "{user_input}".
    The JSON should include the chart type (e.g., bar, line, scatter, pie), x-axis column, and y-axis column, and
    specify whether the columns are numeric or text using common sense. Amounts, counts, etc., are numeric. If the chart cannot be created from the raw data and 
    will need aggregations - return a description of the aggregation required but the first word of your response should be Error.
    Example output: {{"chart_type": "bar", "x": "age", "y": "gender", "y_type": "text"}}.
    """

    try:
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Use ChatCompletion with the new API structure
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful data visualization assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0,
        )

        # Extract the content from the OpenAI response
        chart_params = eval(response.choices[0].message.content.strip())
        st.write(f"Generated chart parameters: {chart_params}")

        return chart_params

    except Exception as e:
        st.error(f"Error generating chart parameters: {e}")
        return None


def create_chart(chart_params, data, sort_by, order):
    """Generate and display the chart based on the parameters and sorting options."""
    chart_type = chart_params.get("chart_type")
    x_col = chart_params.get("x")
    y_col = chart_params.get("y")
    y_type = chart_params.get("y_type")  # Get whether y-axis is numeric or text

    # Handle sorting logic based on dropdown selections
    if sort_by != "None":
        sort_column = x_col if sort_by == "X axis" else y_col
        ascending = True if order == "Ascending" else False
        data = data.sort_values(by=sort_column, ascending=ascending)

    # Plotly chart creation based on the chart type
    if chart_type == "bar":
        fig = px.bar(data, x=x_col, y=y_col, text_auto=True)
        fig.update_layout(title=f"Bar Chart: {x_col} vs {y_col}",
                          xaxis_title=x_col,
                          yaxis_title=y_col,
                          width=700, height=500)
        st.plotly_chart(fig, use_container_width=True)
        return fig

    elif chart_type == "line":
        fig = px.line(data, x=x_col, y=y_col)
        fig.update_layout(title=f"Line Chart: {x_col} vs {y_col}",
                          xaxis_title=x_col,
                          yaxis_title=y_col,
                          width=700, height=500)
        st.plotly_chart(fig, use_container_width=True)
        return fig

    elif chart_type == "scatter":
        fig = px.scatter(data, x=x_col, y=y_col)
        fig.update_layout(title=f"Scatter Plot: {x_col} vs {y_col}",
                          xaxis_title=x_col,
                          yaxis_title=y_col,
                          width=700, height=500)
        st.plotly_chart(fig, use_container_width=True)
        return fig

    elif chart_type == "pie":
        # Create a pie chart using Plotly
        fig = px.pie(data, names=x_col, values=y_col)
        fig.update_layout(title=f"Pie Chart: {x_col} vs {y_col}",
                          width=700, height=500)
        st.plotly_chart(fig, use_container_width=True)
        return fig

    else:
        st.error(f"Unsupported chart type: {chart_type}")
        return None