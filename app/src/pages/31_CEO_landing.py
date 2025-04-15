import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import altair as alt
import requests

st.set_page_config(layout="wide", page_title="CEO Home - MacroMates")

SideBarLinks()

st.title("CEO Dashboard")

col1, col2 = st.columns([1, 3])

with col1:
    st.image("assets/logo.png", width=200)

with col2:
    st.subheader("Welcome to the MacroMates CEO Dashboard")
    st.markdown(
    """
    This dashboard provides a high-level overview of MacroMates performance, 
    key metrics, and strategic insights to support executive decision-making.
    """
    )

st.markdown("""---""")

API_BASE_URL = "http://host.docker.internal:4000/api"
try:
    response = requests.get(f"{API_BASE_URL}/ceo/key_metrics") 
    response.raise_for_status()
    metrics_data = response.json()
    metrics_df = pd.DataFrame(metrics_data)
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching key metrics: {e}")
    metrics_df = pd.DataFrame() 

st.subheader("Key Metrics")
if not metrics_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    for i, metric in enumerate(metrics_df.to_dict('records')):
        cols[i].metric(label=metric['Metric'], value=metric['Value'])
else:
    st.warning("Key metrics not available.")

st.markdown("""---""")

try:
    response = requests.get(f"{API_BASE_URL}/ceo/growth_trend")
    response.raise_for_status()
    chart_data = pd.DataFrame(response.json())
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching growth trend data: {e}")
    chart_data = pd.DataFrame()

st.subheader("Growth Trend")
if not chart_data.empty:
    st.line_chart(chart_data)
else:
    st.warning("Growth trend data not available.")

st.markdown("""
## Quick Navigation
Use the sidebar to access detailed reports.
""")