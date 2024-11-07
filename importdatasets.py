import streamlit as st
import pandas as pd
import json
import xml.etree.ElementTree as ET
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
