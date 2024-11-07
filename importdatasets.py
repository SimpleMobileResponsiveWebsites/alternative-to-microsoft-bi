import streamlit as st
import pandas as pd
import json
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
import pdfplumber
import io

# Set up the page title
st.title("Data Upload Application")

# File uploader for various formats
uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "csv", "json", "xml", "pdf"])

if uploaded_file:
    # Determine file type and process accordingly
    if uploaded_file.name.endswith('.xlsx'):
        # Load Excel file
        df = pd.read_excel(uploaded_file)
        st.write("### Excel File Data")
        st.dataframe(df)

    elif uploaded_file.name.endswith('.csv'):
        # Load CSV file
        df = pd.read_csv(uploaded_file)
        st.write("### CSV File Data")
        st.dataframe(df)

    elif uploaded_file.name.endswith('.json'):
        # Load JSON file
        data = json.load(uploaded_file)
        st.write("### JSON File Data")
        st.json(data)
        df = pd.json_normalize(data)  # Converts JSON to DataFrame if needed
        st.dataframe(df)

    elif uploaded_file.name.endswith('.xml'):
        # Load XML file
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        xml_data = []
        for elem in root:
            xml_data.append({child.tag: child.text for child in elem})
        st.write("### XML File Data")
        df = pd.DataFrame(xml_data)
        st.dataframe(df)

    elif uploaded_file.name.endswith('.pdf'):
        # Load PDF file
        with pdfplumber.open(uploaded_file) as pdf:
            pdf_text = ""
            for page in pdf.pages:
                pdf_text += page.extract_text()
        st.write("### PDF File Text")
        st.text(pdf_text)

# Optional: Connect to SQL databases if needed
st.write("---")
st.write("### Connect to SQL Database")

# Set up database connection fields
db_type = st.selectbox("Database Type", ["MySQL", "PostgreSQL", "SQLite", "SQL Server"])
db_host = st.text_input("Database Host")
db_user = st.text_input("Username")
db_pass = st.text_input("Password", type="password")
db_name = st.text_input("Database Name")

if st.button("Connect to Database"):
    # Construct the database URL based on the selected type
    if db_type == "MySQL":
        db_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
    elif db_type == "PostgreSQL":
        db_url = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    elif db_type == "SQLite":
        db_url = f"sqlite:///{db_name}"
    elif db_type == "SQL Server":
        db_url = f"mssql+pyodbc://{db_user}:{db_pass}@{db_host}/{db_name}?driver=SQL+Server"
    
    try:
        engine = create_engine(db_url)
        st.success("Connected to the database!")
        query = st.text_area("Enter SQL Query")
        if st.button("Execute Query"):
            query_result = pd.read_sql_query(query, engine)
            st.write("### Query Result")
            st.dataframe(query_result)
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
