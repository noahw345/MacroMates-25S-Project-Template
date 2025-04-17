import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

# Set page config
st.set_page_config(
    page_title="Nutritionist Dashboard",
    page_icon="🥗",
    layout="wide"
)

# Display the appropriate sidebar links
SideBarLinks()

# Title
st.title("🥗 Nutritionist Dashboard")

# Fetch dashboard data
try:
    response = requests.get("http://localhost:4000/nutritionist/dashboard")
    if response.status_code == 200:
        data = response.json()
        
        # Create columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Clients", data['total_clients'])
        
        with col2:
            active_clients = len([c for c in data['recent_activities'] if c['last_meal_date']])
            st.metric("Active Clients", active_clients)
        
        with col3:
            avg_meals = sum(c['total_meals'] for c in data['recent_activities']) / len(data['recent_activities']) if data['recent_activities'] else 0
            st.metric("Avg. Meals per Client", f"{avg_meals:.1f}")
        
        # Recent Activities Table
        st.subheader("Recent Client Activities")
        if data['recent_activities']:
            df = pd.DataFrame(data['recent_activities'])
            df['last_meal_date'] = pd.to_datetime(df['last_meal_date'])
            st.dataframe(
                df[['name', 'email', 'total_meals', 'last_meal_date']],
                column_config={
                    "name": "Client Name",
                    "email": "Email",
                    "total_meals": "Total Meals",
                    "last_meal_date": "Last Meal Date"
                },
                hide_index=True
            )
        else:
            st.info("No recent client activities found.")
            
    else:
        st.error("Failed to fetch dashboard data")
except Exception as e:
    st.error(f"Error: {str(e)}")

# Quick Actions
st.subheader("Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("View All Clients", use_container_width=True):
        st.switch_page("pages/52_Client_Management.py")

with col2:
    if st.button("View Client Progress", use_container_width=True):
        st.switch_page("pages/53_Client_Progress.py")

with col3:
    if st.button("Nutritional Analysis", use_container_width=True):
        st.switch_page("pages/54_Nutritional_Analysis.py") 