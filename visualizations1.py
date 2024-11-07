import streamlit as st
import pandas as pd
import json
import xml.etree.ElementTree as ET
import plotly.express as px
import plotly.graph_objects as go

# Set up the page title
st.title("Data Upload and Visualization Application")

# File uploader for various formats
uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "csv", "json", "xml"])

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

    # Visualization Section
    st.write("### Visualizations")

    # Select a visualization type
    visualization_type = st.selectbox("Select a visualization type",
                                      ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Histogram", "Box Plot"])

    # Bar Chart
    if visualization_type == "Bar Chart":
        x_axis = st.selectbox("Select X-axis", df.columns)
        y_axis = st.selectbox("Select Y-axis", df.columns)
        fig = px.bar(df, x=x_axis, y=y_axis)
        st.plotly_chart(fig)

    # Line Chart
    elif visualization_type == "Line Chart":
        x_axis = st.selectbox("Select X-axis", df.columns)
        y_axis = st.selectbox("Select Y-axis", df.columns)
        fig = px.line(df, x=x_axis, y=y_axis)
        st.plotly_chart(fig)

    # Pie Chart
    elif visualization_type == "Pie Chart":
        values_column = st.selectbox("Select Values Column", df.columns)
        names_column = st.selectbox("Select Names Column", df.columns)
        fig = px.pie(df, values=values_column, names=names_column)
        st.plotly_chart(fig)

    # Scatter Plot
    elif visualization_type == "Scatter Plot":
        x_axis = st.selectbox("Select X-axis", df.columns)
        y_axis = st.selectbox("Select Y-axis", df.columns)
        fig = px.scatter(df, x=x_axis, y=y_axis)
        st.plotly_chart(fig)

    # Histogram
    elif visualization_type == "Histogram":
        column_to_plot = st.selectbox("Select Column to Plot", df.columns)
        fig = px.histogram(df, x=column_to_plot)
        st.plotly_chart(fig)

    # Box Plot
    elif visualization_type == "Box Plot":
        column_to_plot = st.selectbox("Select Column to Plot", df.columns)
        fig = px.box(df, x=column_to_plot)
        st.plotly_chart(fig)
