import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import requests

# Set the page configuration
st.set_page_config(layout="wide", page_title="Athlete Landing - MacroMates")

# Render your custom sidebar
SideBarLinks()

# Page title and header section
st.title("Student Athlete Landing Page")

col1, col2 = st.columns([1, 3])

with col1:
    st.image("assets/logo.png", width=200)

with col2:
    st.subheader("Welcome to the MacroMates Student Athlete Dashboard")
    st.markdown(
        """
        This page provides quick-access metrics for daily maintenance 
        and any reminders you've set.
        """
    )

st.markdown("---")

# Adjust this URL to point to your Flask API
API_BASE_URL = "http://host.docker.internal:4000/api"

# 1) Fetch estimated daily maintenance calories
st.subheader("Maintenance Calories")
try:
    response = requests.get(f"{API_BASE_URL}/athlete/maintenance_calories")
    response.raise_for_status()
    maintenance_data = pd.DataFrame(response.json())
    if not maintenance_data.empty:
        st.dataframe(maintenance_data)
    else:
        st.warning("No maintenance calorie data available.")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching maintenance calories data: {e}")

st.markdown("---")

# 2) Reminders
st.subheader("Reminders")
try:
    response = requests.get(f"{API_BASE_URL}/athlete/reminders")
    response.raise_for_status()
    reminders_data = pd.DataFrame(response.json())
    if not reminders_data.empty:
        st.dataframe(reminders_data)
    else:
        st.warning("No reminders available.")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching reminders: {e}")

st.markdown("---")

st.markdown("""
### Quick Navigation
Use the sidebar to explore BMI, weight change, macro breakdowns, workout plans, and more.
""")
