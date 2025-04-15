import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import altair as alt
import requests

st.set_page_config(layout="wide", page_title="System Performance: MacroMates")

SideBarLinks()

st.title("System Performance")

st.markdown("""
## System Performance Metrics

This page provides insights into the performance and health of the MacroMates system.
""")

API_BASE_URL = "http://host.docker.internal:4000/api"

try:
    response = requests.get(f"{API_BASE_URL}/ceo/performance_indicators")  
    response.raise_for_status()
    performance_data = response.json()
    performance_df = pd.DataFrame(performance_data)
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching performance indicators: {e}")
    performance_df = pd.DataFrame()

st.subheader("Key Performance Indicators")
if not performance_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    for i, metric in enumerate(performance_df.to_dict('records')):
        cols[i].metric(label=metric['Metric'], value=metric['Value'])
else:
    st.warning("Performance indicators not available.")

st.markdown("""---""")

try:
    response = requests.get(f"{API_BASE_URL}/ceo/api_response_time")
    response.raise_for_status()
    response_time_data = pd.DataFrame(response.json())
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching API response time: {e}")
    response_time_data = pd.DataFrame()

st.subheader("API Response Time (Last 24 Hours)")
if not response_time_data.empty:
    chart = alt.Chart(response_time_data).mark_line().encode(
        x='Time',
        y='ResponseTime',
        tooltip=['Time', 'ResponseTime']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("API response time data not available.")

try:
    response = requests.get(f"{API_BASE_URL}/ceo/user_traffic") 
    response.raise_for_status()
    traffic_data = pd.DataFrame(response.json())
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching user traffic data: {e}")
    traffic_data = pd.DataFrame()

st.subheader("User Traffic by Hour")
if not traffic_data.empty:
    chart = alt.Chart(traffic_data).mark_bar().encode(
        x='Hour:O',
        y='Traffic',
        tooltip=['Hour', 'Traffic']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("User traffic data not available.")