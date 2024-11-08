import streamlit as st
import pandas as pd
import json
import xml.etree.ElementTree as ET
import plotly.express as px
import plotly.graph_objects as go

# Set up the page title
st.title("Enhanced Data Visualization Application")

# File uploader for various formats
uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "csv", "json", "xml"])

if uploaded_file:
    # Load file based on type
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.json'):
        data = json.load(uploaded_file)
        df = pd.json_normalize(data)
    elif uploaded_file.name.endswith('.xml'):
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        xml_data = [{child.tag: child.text for child in elem} for elem in root]
        df = pd.DataFrame(xml_data)

    st.write("### Data Preview")
    st.dataframe(df)

    # Visualization options
    visualization_type = st.selectbox("Choose a Chart Type", [
        "Simple Bar", "Stacked Bar", "Clustered Bar",
        "Line Chart", "Stacked Line", "Area Chart",
        "Pie Chart", "Donut Chart",
        "Scatter Plot", "Bubble Chart",
        "Line with Clustered Column", "Treemap", "Waterfall", "Funnel",
        "Gauge Chart", "Box Plot", "Histogram",
        "Ribbon Chart", "Sankey Diagram", "Radar Chart", "Sunburst",
        "Basic Table", "Single Number Card", "KPI",
        "Choropleth Map", "Bubble Map"
    ])

    # Simple Bar Chart
    if visualization_type == "Simple Bar":
        x = st.selectbox("X-Axis", df.columns)
        y = st.selectbox("Y-Axis", df.columns)
        fig = px.bar(df, x=x, y=y)
        st.plotly_chart(fig)

    # Stacked Bar Chart
    elif visualization_type == "Stacked Bar":
        x = st.selectbox("X-Axis", df.columns)
        y = st.selectbox("Y-Axis", df.columns)
        color = st.selectbox("Color By", df.columns)
        fig = px.bar(df, x=x, y=y, color=color, barmode='stack')
        st.plotly_chart(fig)

    # Clustered Bar Chart
    elif visualization_type == "Clustered Bar":
        x = st.selectbox("X-Axis", df.columns)
        y = st.selectbox("Y-Axis", df.columns)
        color = st.selectbox("Color By", df.columns)
        fig = px.bar(df, x=x, y=y, color=color, barmode='group')
        st.plotly_chart(fig)

    # Line Chart
    elif visualization_type == "Line Chart":
        x = st.selectbox("X-Axis", df.columns)
        y = st.selectbox("Y-Axis", df.columns)
        fig = px.line(df, x=x, y=y)
        st.plotly_chart(fig)

    # Area Chart
    elif visualization_type == "Area Chart":
        x = st.selectbox("X-Axis", df.columns)
        y = st.selectbox("Y-Axis", df.columns)
        fig = px.area(df, x=x, y=y)
        st.plotly_chart(fig)

    # Donut Chart
    elif visualization_type == "Donut Chart":
        values = st.selectbox("Values", df.columns)
        names = st.selectbox("Names", df.columns)
        fig = px.pie(df, values=values, names=names, hole=0.4)
        st.plotly_chart(fig)

    # Scatter Plot
    elif visualization_type == "Scatter Plot":
        x = st.selectbox("X-Axis", df.columns)
        y = st.selectbox("Y-Axis", df.columns)
        fig = px.scatter(df, x=x, y=y)
        st.plotly_chart(fig)

    # Bubble Chart
    elif visualization_type == "Bubble Chart":
        x = st.selectbox("X-Axis", df.columns)
        y = st.selectbox("Y-Axis", df.columns)
        size = st.selectbox("Bubble Size", df.columns)
        fig = px.scatter(df, x=x, y=y, size=size)
        st.plotly_chart(fig)

    # Treemap
    elif visualization_type == "Treemap":
        path = st.selectbox("Path", df.columns)
        values = st.selectbox("Values", df.columns)
        fig = px.treemap(df, path=[path], values=values)
        st.plotly_chart(fig)

    # KPI Card
    elif visualization_type == "Single Number Card":
        column = st.selectbox("Select Column for KPI", df.columns)
        st.metric(label=f"KPI for {column}", value=df[column].sum())

    # Choropleth Map
    elif visualization_type == "Choropleth Map":
        location = st.selectbox("Location Column", df.columns)
        color = st.selectbox("Color Column", df.columns)
        fig = px.choropleth(df, locations=location, color=color)
        st.plotly_chart(fig)
