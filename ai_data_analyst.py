import tempfile
import csv
import streamlit as st
import pandas as pd
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckdb import DuckDbTools
from agno.tools.pandas import PandasTools

# Function to preprocess and save the uploaded file
def preprocess_and_save(file):
    try:
        if file.name.endswith('.csv'):
            try:
                df = pd.read_csv(file, encoding='utf-8', na_values=['NA', 'N/A', 'missing'])
            except UnicodeDecodeError:
                file.seek(0)
                df = pd.read_csv(file, encoding='latin1', na_values=['NA', 'N/A', 'missing'])
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file, na_values=['NA', 'N/A', 'missing'])
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None, None, None

        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)

        for col in df.columns:
            if 'date' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass

        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_path = temp_file.name
            df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)

        return temp_path, df.columns.tolist(), df
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None, None, None

# Streamlit app
st.title("📊 Data Analyst Agent")

# Sidebar for API key
with st.sidebar:
    st.header("API Key")
    groq_key = st.text_input("Enter your Groq API key:", type="password")
    if groq_key:
        st.session_state.groq_key = groq_key
        st.success("API key saved!")
    else:
        st.warning("Please enter your Groq API key to proceed.")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None and "groq_key" in st.session_state:
    temp_path, columns, df = preprocess_and_save(uploaded_file)

    if temp_path and columns and df is not None:
        st.write("Uploaded Data:")
        st.dataframe(df)
        st.write("Uploaded columns:", columns)

        duckdb_tools = DuckDbTools()
        duckdb_tools.load_local_csv_to_table(
            path=temp_path,
            table="uploaded_data",
        )

        data_analyst_agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile", api_key=st.session_state.groq_key),
            tools=[duckdb_tools, PandasTools()],
            system_message="You are an expert data analyst. Use the 'uploaded_data' table to answer user queries. Generate SQL queries using DuckDB tools to solve the user's query. Provide clear and concise answers with the results.",
            markdown=True,
        )

        if "generated_code" not in st.session_state:
            st.session_state.generated_code = None

        user_query = st.text_area("Ask a query about the data:")
        st.info("💡 Check your terminal for a clearer output of the agent's response")

        if st.button("Submit Query"):
            if user_query.strip() == "":
                st.warning("Please enter a query.")
            else:
                try:
                    with st.spinner('Processing your query...'):
                        response = data_analyst_agent.run(user_query)
                        if hasattr(response, 'content'):
                            response_content = response.content
                        else:
                            response_content = str(response)
                    st.markdown(response_content)
                except Exception as e:
                    st.error(f"Error generating response from the agent: {e}")
                    st.error("Please try rephrasing your query or check if the data format is correct.")