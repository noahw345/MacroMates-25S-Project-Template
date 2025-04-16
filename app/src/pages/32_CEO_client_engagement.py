import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import altair as alt
import requests

st.set_page_config(layout="wide", page_title="Client Engagement: MacroMates")

SideBarLinks()

st.title("Client Engagement")

st.markdown("""
## Client Engagement Metrics

This page provides detailed analytics on client engagement with the MacroMates platform.
""")

API_BASE_URL = "http://host.docker.internal:4000/api" 

try:
    response = requests.get(f"{API_BASE_URL}/ceo/engagement_indicators") 
    response.raise_for_status()
    engagement_data = response.json()
    engagement_df = pd.DataFrame(engagement_data)
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching engagement indicators: {e}")
    engagement_df = pd.DataFrame()

st.subheader("Key Engagement Indicators")
if not engagement_df.empty:
    st.table(engagement_df)
else:
    st.warning("Engagement indicators not available.")

st.markdown("""---""")

try:
    response = requests.get(f"{API_BASE_URL}/ceo/daily_active_users")
    response.raise_for_status()
    chart_data = pd.DataFrame(response.json())
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching daily active users: {e}")
    chart_data = pd.DataFrame()

st.subheader("Daily Active Users Trend")
if not chart_data.empty:
    chart = alt.Chart(chart_data).mark_line().encode(
        x='Date',
        y='Users',
        tooltip=['Date', 'Users']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Daily active users data not available.")

try:
    response = requests.get(f"{API_BASE_URL}/ceo/client_activity")
    response.raise_for_status()
    client_data = response.json()
    client_df = pd.DataFrame(client_data)
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching client activity data: {e}")
    client_df = pd.DataFrame()

st.subheader("Client Activity")
if not client_df.empty:
    selected_client = st.selectbox('Select Client', options=['All'] + list(client_df['Name']))

    if selected_client == 'All':
        st.dataframe(client_df)
    else:
        st.dataframe(client_df[client_df['Name'] == selected_client])
else:
    st.warning("Client activity data not available.")