import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import requests

# Set the page configuration
st.set_page_config(layout="wide", page_title="Student Athlete Home - MacroMates")

# Render your custom sidebar
SideBarLinks()

# Page title and header section
st.title("Student Athlete Dashboard")

col1, col2 = st.columns([1, 3])

with col1:
    st.image("assets/logo.png", width=200)

with col2:
    st.subheader("Welcome to the MacroMates Student Athlete Dashboard")
    st.markdown(
        """
        This dashboard provides an overview of individual athletes' body composition, 
        calorie needs, workout plans, and more to help manage their health and performance.
        """
    )

st.markdown("---")

# Adjust this URL to point to your Flask API
API_BASE_URL = "http://host.docker.internal:4000/api"

# 1) Fetch BMI data
st.subheader("BMI Data")
try:
    response = requests.get(f"{API_BASE_URL}/athlete/bmi")
    response.raise_for_status()
    bmi_data = pd.DataFrame(response.json())
    if not bmi_data.empty:
        st.dataframe(bmi_data)
    else:
        st.warning("No BMI data available.")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching BMI data: {e}")

st.markdown("---")

# 2) Fetch estimated daily maintenance calories
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

# 3) Fetch estimated weight change over time
st.subheader("Estimated Weight Change")
try:
    response = requests.get(f"{API_BASE_URL}/athlete/weight_change")
    response.raise_for_status()
    weight_change_data = pd.DataFrame(response.json())
    if not weight_change_data.empty:
        st.dataframe(weight_change_data)
    else:
        st.warning("No weight change data available.")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching weight change data: {e}")

st.markdown("---")

# 4) Daily macro breakdown for a specific athlete (example for athlete_id=1)
st.subheader("Daily Macro Breakdown")
try:
    response = requests.get(f"{API_BASE_URL}/athlete/daily_macro_breakdown")
    response.raise_for_status()
    macro_data = pd.DataFrame(response.json())
    if not macro_data.empty:
        st.dataframe(macro_data)
    else:
        st.warning("No daily macro breakdown available.")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching daily macro breakdown: {e}")

st.markdown("---")

# 5) Workout plan alongside calorie intake
st.subheader("Workout Plan & Calorie Intake")
try:
    response = requests.get(f"{API_BASE_URL}/athlete/workout_plan_intake")
    response.raise_for_status()
    plan_intake_data = pd.DataFrame(response.json())
    if not plan_intake_data.empty:
        st.dataframe(plan_intake_data)
    else:
        st.warning("No workout plan and calorie intake data available.")
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching workout plan intake data: {e}")

st.markdown("---")

# 6) Reminders
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

st.markdown(
    """
    ## Quick Navigation
    Use the sidebar to access more detailed athlete-specific or advanced reports.
    """
)
