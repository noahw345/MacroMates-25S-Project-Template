import streamlit as st
from modules.nav import SideBarLinks

# Configure the page
st.set_page_config(layout="wide", page_title="About - MacroMates")

# Display the appropriate sidebar links - show Home button
SideBarLinks(show_home=True)

st.title("About Nutrition Buddy")

col1, col2 = st.columns([1, 3])

with col1:
    st.image("assets/logo.png", width=200)
    
with col2:
    st.subheader("Your Intelligent Nutrition Companion")
    st.markdown(
        """
        Nutrition Buddy is a data-driven nutrition tracking app designed to help users make informed dietary choices without the guesswork.
        """
    )

st.markdown("""
## Our Mission

At MacroMates, we believe that nutrition shouldn't be complicated. Our mission is to empower individuals to achieve their health and fitness goals through personalized nutrition tracking and intelligent recommendations.

## Key Features

- **Smart Meal Logging**: Easily track your meals and automatically calculate nutritional content
- **Personalized Goal Setting**: Set and track progress towards your specific nutrition goals
- **Intelligent Recommendations**: Receive suggestions for meal adjustments to meet your goals
- **Progress Tracking**: Monitor your nutrition journey with intuitive visualizations

""")


