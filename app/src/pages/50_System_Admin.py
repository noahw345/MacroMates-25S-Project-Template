# app/src/pages/50_System_Admin.py

import streamlit as st
import pandas as pd
import requests
import altair as alt
from modules.nav import SideBarLinks
from datetime import datetime

# Configure page layout and title
st.set_page_config(layout="wide", page_title="System Administrator - MacroMates")

# Display sidebar navigation links
SideBarLinks()

st.title("System Administrator Dashboard")
st.markdown("Monitor system performance and analyze activity logs.")

# Define your API base URL
API_BASE_URL = "http://host.docker.internal:4000/api"

# Section 1: System Performance Overview

st.header("System Performance Overview")

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_system_performance():
    try:
        response = requests.get(f"{API_BASE_URL}/system-performance", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching system performance data: {e}")
        return []

system_data = fetch_system_performance()

if system_data:
    # Create metrics for latest data
    latest_metrics = {}
    for metric in system_data:
        metric_name = metric.get('Performance_Metric')
        if metric_name not in latest_metrics or datetime.strptime(metric.get('Timestamp'), "%Y-%m-%d %H:%M:%S") > datetime.strptime(latest_metrics[metric_name].get('Timestamp'), "%Y-%m-%d %H:%M:%S"):
            latest_metrics[metric_name] = metric
    
    # Display key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    if 'CPU Usage' in latest_metrics:
        col1.metric(
            "CPU Usage", 
            latest_metrics['CPU Usage'].get('System_Status'),
            delta=f"{latest_metrics['CPU Usage'].get('New_Clients')} new clients"
        )
    
    if 'Memory Usage' in latest_metrics:
        col2.metric(
            "Memory Usage", 
            latest_metrics['Memory Usage'].get('System_Status'),
            delta=f"{latest_metrics['Memory Usage'].get('New_Clients')} new clients"
        )
    
    if 'Response Time' in latest_metrics:
        col3.metric(
            "Response Time", 
            latest_metrics['Response Time'].get('System_Status'),
            delta=f"{latest_metrics['Response Time'].get('New_Clients')} new clients"
        )
    
    if 'Uptime' in latest_metrics:
        col4.metric(
            "Uptime", 
            latest_metrics['Uptime'].get('System_Status'),
            delta=f"{latest_metrics['Uptime'].get('New_Clients')} new clients"
        )
    
    if 'Bandwidth' in latest_metrics:
        col5.metric(
            "Bandwidth", 
            latest_metrics['Bandwidth'].get('System_Status'),
            delta=f"{latest_metrics['Bandwidth'].get('New_Clients')} new clients"
        )
    
    # Create performance trend chart
    st.subheader("Performance Metrics Over Time")
    
    # Prepare data for visualization
    df = pd.DataFrame(system_data)
    
    # Convert timestamp to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Create client growth chart
    client_chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Timestamp:T', title='Date'),
        y=alt.Y('Existing_Clients:Q', title='Total Clients'),
        tooltip=['Timestamp', 'Existing_Clients', 'New_Clients', 'Performance_Metric', 'System_Status']
    ).properties(
        title='Client Growth Over Time',
        height=300
    )
    
    st.altair_chart(client_chart, use_container_width=True)
    
    # Create system status chart
    # We'll map status to numeric values for visualization
    status_map = {'Optimal': 3, 'Good': 2, 'Warning': 1, 'Critical': 0}
    df['StatusValue'] = df['System_Status'].map(status_map)
    
    # Create a pivot table for metrics
    pivot_df = df.pivot(index='Timestamp', columns='Performance_Metric', values='StatusValue')
    pivot_df = pivot_df.reset_index()
    
    # Melt the dataframe for Altair
    melted_df = pd.melt(pivot_df, id_vars=['Timestamp'], var_name='Metric', value_name='Status')
    
    # Create the chart
    status_chart = alt.Chart(melted_df).mark_line(point=True).encode(
        x=alt.X('Timestamp:T', title='Date'),
        y=alt.Y('Status:Q', title='Status (3=Optimal, 0=Critical)'),
        color='Metric:N',
        tooltip=['Timestamp', 'Metric', 'Status']
    ).properties(
        title='System Status by Metric',
        height=300
    )
    
    st.altair_chart(status_chart, use_container_width=True)
    
    # Show the full data table with filters
    st.subheader("System Performance Data")
    
    # Add filters
    metric_filter = st.multiselect(
        "Filter by Metric", 
        options=df['Performance_Metric'].unique().tolist(),
        default=df['Performance_Metric'].unique().tolist()
    )
    
    status_filter = st.multiselect(
        "Filter by Status", 
        options=df['System_Status'].unique().tolist(),
        default=df['System_Status'].unique().tolist()
    )
    
    # Apply filters
    filtered_df = df[
        df['Performance_Metric'].isin(metric_filter) & 
        df['System_Status'].isin(status_filter)
    ]
    
    # Sort by timestamp descending
    filtered_df = filtered_df.sort_values('Timestamp', ascending=False)
    
    # Display as table
    st.dataframe(
        filtered_df[['Timestamp', 'Performance_Metric', 'System_Status', 'Existing_Clients', 'New_Clients']], 
        use_container_width=True
    )
else:
    st.warning("No system performance data available. Check the API connection.")

# Section 2: System Health Alerts

st.header("System Health Alerts")
st.info("Critical alerts will appear here when system metrics indicate problems.")

# Count statuses and show warnings
if system_data:
    status_counts = df['System_Status'].value_counts()
    
    if 'Critical' in status_counts and status_counts['Critical'] > 0:
        st.error(f"⚠️ {status_counts['Critical']} critical system issues detected! Immediate attention required.")
        
        # Show critical issues
        critical_issues = df[df['System_Status'] == 'Critical'].sort_values('Timestamp', ascending=False)
        st.dataframe(
            critical_issues[['Timestamp', 'Performance_Metric', 'System_Status']],
            use_container_width=True
        )
        
    elif 'Warning' in status_counts and status_counts['Warning'] > 0:
        st.warning(f"⚠️ {status_counts['Warning']} system warnings detected. Monitor these metrics.")
        
        # Show warning issues
        warning_issues = df[df['System_Status'] == 'Warning'].sort_values('Timestamp', ascending=False)
        st.dataframe(
            warning_issues[['Timestamp', 'Performance_Metric', 'System_Status']],
            use_container_width=True
        )
    else:
        st.success("✅ All systems operating normally.")
