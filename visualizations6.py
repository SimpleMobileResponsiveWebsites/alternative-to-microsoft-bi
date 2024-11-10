import streamlit as st
import pandas as pd
import json
import xml.etree.ElementTree as ET
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

    # Helper Function for Selection
    def select_numeric_column(label):
        numeric_columns = df.select_dtypes(include=['number']).columns
        return st.selectbox(label, numeric_columns)

    def select_columns(label, multiple=False):
        return st.multiselect(label, df.columns) if multiple else st.selectbox(label, df.columns)

    # Visualization options
    visualization_type = st.selectbox("Choose a Chart Type", [
        "Simple Bar", "Stacked Bar", "Clustered Bar",
        "Line Chart", "Stacked Line", "Area Chart",
        "Pie Chart", "Donut Chart", "Scatter Plot", "Bubble Chart",
        "Line with Clustered Column", "Treemap", "Waterfall", "Funnel",
        "Gauge Chart", "Box Plot", "Histogram", "Ribbon Chart", "Sankey Diagram",
        "Radar Chart", "Sunburst", "Basic Table", "Single Number Card", "KPI",
        "Choropleth Map", "Bubble Map"
    ])

    # Implementing Charts
    if visualization_type == "Simple Bar":
        x, y = select_columns("X-Axis"), select_numeric_column("Y-Axis")
        st.plotly_chart(px.bar(df, x=x, y=y))

    elif visualization_type == "Stacked Bar":
        x, y, color = select_columns("X-Axis"), select_numeric_column("Y-Axis"), select_columns("Color By")
        st.plotly_chart(px.bar(df, x=x, y=y, color=color, barmode='stack'))

    elif visualization_type == "Clustered Bar":
        x, y, color = select_columns("X-Axis"), select_numeric_column("Y-Axis"), select_columns("Color By")
        st.plotly_chart(px.bar(df, x=x, y=y, color=color, barmode='group'))

    elif visualization_type == "Line Chart":
        x, y = select_columns("X-Axis"), select_numeric_column("Y-Axis")
        st.plotly_chart(px.line(df, x=x, y=y))

    elif visualization_type == "Stacked Line":
        x = select_columns("X-Axis")
        y_columns = st.multiselect("Y-Axis (Select multiple)", df.select_dtypes(include='number').columns)
        fig = go.Figure()
        for y in y_columns:
            fig.add_trace(go.Scatter(x=df[x], y=df[y], stackgroup='one', name=y))
        st.plotly_chart(fig)

    elif visualization_type == "Ribbon Chart":
        x = select_numeric_column("X-Axis")
        y1 = select_numeric_column("Y1 (Lower Bound)")
        y2 = select_numeric_column("Y2 (Upper Bound)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df[x], y=df[y1], mode='lines', line_color='blue'))
        fig.add_trace(go.Scatter(x=df[x], y=df[y2], fill='tonexty', mode='lines', line_color='lightblue'))
        st.plotly_chart(fig)

    elif visualization_type == "Line with Clustered Column":
        x = select_columns("X-Axis")
        y1 = select_numeric_column("Y-Axis (Bar)")
        y2 = select_numeric_column("Y-Axis (Line)")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df[x], y=df[y1], name=y1), secondary_y=False)
        fig.add_trace(go.Scatter(x=df[x], y=df[y2], name=y2), secondary_y=True)
        st.plotly_chart(fig)

    elif visualization_type == "Sankey Diagram":
        source, target, value = select_columns("Source"), select_columns("Target"), select_numeric_column("Value")
        labels = pd.concat([df[source], df[target]]).unique().tolist()
        source_idx = df[source].apply(lambda x: labels.index(x))
        target_idx = df[target].apply(lambda x: labels.index(x))
        fig = go.Figure(data=[go.Sankey(node=dict(label=labels), link=dict(source=source_idx, target=target_idx, value=df[value]))])
        st.plotly_chart(fig)

    elif visualization_type == "Radar Chart":
        y_columns = st.multiselect("Y-Axis (Select multiple)", df.select_dtypes(include='number').columns)
        if y_columns:
            mean_values = df[y_columns].mean()
            fig = px.line_polar(r=mean_values.values, theta=y_columns, line_close=True)
            st.plotly_chart(fig)

    elif visualization_type == "Sunburst":
        path = select_columns("Hierarchy Path")
        value = select_numeric_column("Values")
        fig = px.sunburst(df, path=[path], values=value)
        st.plotly_chart(fig)

    elif visualization_type == "Single Number Card":
        column = select_numeric_column("Select Column")
        total_value = df[column].sum()
        st.metric(label=f"Total {column}", value=total_value)

    elif visualization_type == "Choropleth Map":
        loc, color = select_columns("Location"), select_numeric_column("Color")
        st.plotly_chart(px.choropleth(df, locations=loc, color=color))
