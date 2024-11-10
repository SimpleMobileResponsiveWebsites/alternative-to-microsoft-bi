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
        "Pie Chart", "Donut Chart", "Scatter Plot", "Bubble Chart",
        "Line with Clustered Column", "Treemap", "Waterfall", "Funnel",
        "Gauge Chart", "Box Plot", "Histogram", "Ribbon Chart", "Sankey Diagram",
        "Radar Chart", "Sunburst", "Basic Table", "Single Number Card", "KPI",
        "Choropleth Map", "Bubble Map"
    ])

    # Helper Function for Selection
    def select_columns(label, multiple=False):
        return st.multiselect(label, df.columns) if multiple else st.selectbox(label, df.columns)

    # Implementing Charts
    if visualization_type == "Simple Bar":
        x, y = select_columns("X-Axis"), select_columns("Y-Axis")
        st.plotly_chart(px.bar(df, x=x, y=y))

    elif visualization_type == "Stacked Bar":
        x, y, color = select_columns("X-Axis"), select_columns("Y-Axis"), select_columns("Color By")
        st.plotly_chart(px.bar(df, x=x, y=y, color=color, barmode='stack'))

    elif visualization_type == "Clustered Bar":
        x, y, color = select_columns("X-Axis"), select_columns("Y-Axis"), select_columns("Color By")
        st.plotly_chart(px.bar(df, x=x, y=y, color=color, barmode='group'))

    elif visualization_type == "Line Chart":
        x, y = select_columns("X-Axis"), select_columns("Y-Axis")
        st.plotly_chart(px.line(df, x=x, y=y))

    elif visualization_type == "Stacked Line":
        x, y_columns = select_columns("X-Axis"), st.multiselect("Y-Axis (Select multiple)", df.columns)
        fig = go.Figure()
        for y in y_columns:
            fig.add_trace(go.Scatter(x=df[x], y=df[y], stackgroup='one', name=y))
        st.plotly_chart(fig)

    elif visualization_type == "Area Chart":
        x, y = select_columns("X-Axis"), select_columns("Y-Axis")
        st.plotly_chart(px.area(df, x=x, y=y))

    elif visualization_type == "Pie Chart":
        values, names = select_columns("Values"), select_columns("Names")
        st.plotly_chart(px.pie(df, values=values, names=names))

    elif visualization_type == "Donut Chart":
        values, names = select_columns("Values"), select_columns("Names")
        st.plotly_chart(px.pie(df, values=values, names=names, hole=0.4))

    elif visualization_type == "Scatter Plot":
        x, y = select_columns("X-Axis"), select_columns("Y-Axis")
        st.plotly_chart(px.scatter(df, x=x, y=y))

    elif visualization_type == "Bubble Chart":
        x, y, size = select_columns("X-Axis"), select_columns("Y-Axis"), select_columns("Size Column")
        st.plotly_chart(px.scatter(df, x=x, y=y, size=size))

    elif visualization_type == "Treemap":
        path, values = select_columns("Path"), select_columns("Values")
        st.plotly_chart(px.treemap(df, path=[path], values=values))

    elif visualization_type == "Waterfall":
        x, y = select_columns("X-Axis"), select_columns("Y-Axis")
        st.plotly_chart(go.Figure(go.Waterfall(x=df[x], y=df[y])))

    elif visualization_type == "Funnel":
        x, y = select_columns("X-Axis"), select_columns("Values")
        st.plotly_chart(px.funnel(df, x=x, y=y))

    elif visualization_type == "Gauge Chart":
        col = select_columns("Select Column")
        avg_val = df[col].astype(float).mean()
        fig = go.Figure(go.Indicator(mode="gauge+number", value=avg_val))
        st.plotly_chart(fig)

    elif visualization_type == "Box Plot":
        x, y = select_columns("X-Axis"), select_columns("Y-Axis")
        st.plotly_chart(px.box(df, x=x, y=y))

    elif visualization_type == "Histogram":
        x = select_columns("X-Axis")
        st.plotly_chart(px.histogram(df, x=x))

    elif visualization_type == "Sankey Diagram":
        source, target, value = select_columns("Source"), select_columns("Target"), select_columns("Value")
        fig = go.Figure(go.Sankey(node=dict(label=df[source].unique()), link=dict(source=df[source], target=df[target], value=df[value])))
        st.plotly_chart(fig)

    elif visualization_type == "Radar Chart":
        y_columns = st.multiselect("Y-Axis (Select multiple)", df.columns)
        st.plotly_chart(px.line_polar(df, r=df[y_columns].mean(), theta=y_columns))

    elif visualization_type == "Basic Table":
        st.table(df)

    elif visualization_type == "KPI":
        col = select_columns("Select Column for KPI")
        st.metric(label=f"KPI of {col}", value=df[col].sum())

    elif visualization_type == "Bubble Map":
        lat, lon, size = select_columns("Latitude"), select_columns("Longitude"), select_columns("Size")
        st.plotly_chart(px.scatter_geo(df, lat=lat, lon=lon, size=size))

    elif visualization_type == "Choropleth Map":
        loc, color = select_columns("Location"), select_columns("Color Column")
        st.plotly_chart(px.choropleth(df, locations=loc, color=color))
