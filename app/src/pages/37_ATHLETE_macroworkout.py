import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import requests

st.set_page_config(layout="wide", page_title="Macro & Workout Plan - MacroMates")

SideBarLinks()

st.title("Daily Macro & Workout Plan")

col1, col2 = st.columns([1, 3])
with col1:
    st.image("assets/logo.png", width=200)
with col2:
    st.subheader("Macro Tracking & Workout Plans")
    st.markdown(
        """
        This page provides your daily macro breakdown details
        and shows how they align with your current workout plan.
        """
    )

st.markdown("---")

API_BASE_URL = "http://host.docker.internal:4000/api"

# 2) Workout plan alongside calorie intake
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

st.markdown("""
### Quick Navigation
Use the sidebar to switch between BMI, weight change, reminders, or head back to the landing page.
""")
