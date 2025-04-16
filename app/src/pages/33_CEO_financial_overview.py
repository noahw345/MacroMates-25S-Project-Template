import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import altair as alt
import requests

st.set_page_config(layout="wide", page_title="Financial Overview: MacroMates")

SideBarLinks()

st.title("Financial Overview")

st.markdown("""
## Financial Performance

This page provides insights into MacroMates' financial performance.
""")

API_BASE_URL = "http://host.docker.internal:4000/api"

try:
    response = requests.get(f"{API_BASE_URL}/ceo/financial_indicators") 
    response.raise_for_status()
    financial_data = response.json()
    financial_df = pd.DataFrame(financial_data)
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching financial indicators: {e}")
    financial_df = pd.DataFrame()

## Display Financial Metrics
st.subheader("Key Financial Indicators")
if not financial_df.empty:
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for i, metric in enumerate(financial_df.to_dict('records')):
        cols[i].metric(label=metric['Metric'], value=f"{metric['Unit']} {metric['Value']}")
else:
    st.warning("Financial indicators not available.")

st.markdown("""---""")

try:
    response = requests.get(f"{API_BASE_URL}/ceo/revenue_trend") 
    response.raise_for_status()
    revenue_data = pd.DataFrame(response.json())
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching revenue trend: {e}")
    revenue_data = pd.DataFrame()

st.subheader("Monthly Revenue Trend")
if not revenue_data.empty:
    chart = alt.Chart(revenue_data).mark_bar().encode(
        x='Month',
        y='Revenue',
        tooltip=['Month', 'Revenue']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Revenue trend data not available.")

try:
    response = requests.get(f"{API_BASE_URL}/ceo/expense_breakdown")
    response.raise_for_status()
    expenses_data = response.json()
    expenses_df = pd.DataFrame(expenses_data)
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching expense breakdown: {e}")
    expenses_df = pd.DataFrame()

st.subheader("Expense Breakdown")
if not expenses_df.empty:
    chart = alt.Chart(expenses_df).mark_arc(theta="Percentage").encode(
        color=alt.Color("Category"),
        tooltip=["Category", "Percentage"]
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Expense breakdown data not available.")