import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import requests

st.set_page_config(layout="wide", page_title="BMI & Weight Change - MacroMates")

SideBarLinks()

st.title("BMI & Weight Change")

col1, col2 = st.columns([1, 3])
with col1:
    st.image("assets/logo.png", width=200)
with col2:
    st.subheader("Body Composition & Progress Tracking")
    st.markdown(
        """
        This page displays BMI data for each athlete as well as estimated
        weight changes over time based on caloric surplus or deficit.
        """
    )

st.markdown("---")

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

st.markdown("""
### Quick Navigation
Use the sidebar to view daily macros, workout plans, or return to your home page.
""")
