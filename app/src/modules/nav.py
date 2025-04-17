# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st
import inspect
import logging

logger = logging.getLogger(__name__)

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ MacroMates Pages ------------------------
def ClientsNav():
    st.sidebar.page_link("pages/40_Clients.py", label="Clients", icon="👤")


def MealLogsNav():
    st.sidebar.page_link("pages/41_Meal_Logs.py", label="Meal Logs", icon="🍽️")


#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link(
        "pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤"
    )


def WorldBankVizNav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")


## ------------------------ Examples for Role of usaid_worker ------------------------
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/50_System_Admin.py", label="System Admin", icon="🖥️")

#### ------------------------ CEO Role ------------------------
def CEOHomeNav():
    st.sidebar.page_link("pages/31_CEO_landing.py", label="CEO Home", icon="💼")

def CEOClientEngagementNav():
    st.sidebar.page_link("pages/32_CEO_client_engagement.py", label="Client Engagement", icon="📈")

def CEOFinancialOverviewNav():
    st.sidebar.page_link("pages/33_CEO_financial_overview.py", label="Financial Overview", icon="💰")

def CEOSystemPerformanceNav():
    st.sidebar.page_link("pages/34_CEO_system_performance.py", label="System Performance", icon="⚙️")

#### ------------------------ Student Athlete Role ------------------------
def StudentAthleteLandingNav():
    st.sidebar.page_link("pages/35_ATHLETE_landing.py", label="Student Athlete Landing Home", icon="🧍")
    st.sidebar.page_link("pages/36_ATHLETE_weight.py", label="Student Athlete Weight Management", icon="⚖️")
    st.sidebar.page_link("pages/37_ATHLETE_macroworkout.py", label="Student Athlete Macros and Workout", icon="🏋️")

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    Add links to the sidebar based on the user's role.
    
    Inputs:
        show_home - boolean, controls whether to add a link back to 
                    home in the sidebar
    """
    # if we don't have 'authenticated' in the session_state, 
    # that means we're probably on the home page
    role = st.session_state.get('role', None)
    
    # Create the Home link in the sidebar
    if show_home:
        st.sidebar.page_link("Home.py", label="Home")

    # Even if not authenticated, include the About link
    st.sidebar.page_link("pages/30_About.py", label="About")
    
    # Add links to the sidebar based on the user's role
    if st.session_state.get('authenticated', False):
        # Only show the following links if the user is authenticated
        
        # Add a divider and welcome message
        st.sidebar.divider()
        st.sidebar.write(f"Welcome, {st.session_state.get('first_name', 'User')}")
        st.sidebar.divider()

        # Add role-specific links
        if role == 'administrator':
            SysAdminLinks()
        elif role == 'ceo':
            CEOLinks()
        elif role == 'nutrition_client':
            ClientLinks()
        elif role == 'nutritionist':
            NutritionistLinks()

        # Add a divider for spacing
        st.sidebar.divider()
        
        # Display the username and a logout button
        logout_container = st.sidebar.container()
        logout_container.caption("Click below to logout")
        
        if logout_container.button("Logout"):
            # Clear the session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
                
            # Redirect to the home page
            st.rerun()


def SysAdminLinks():
    """Add System Administrator links to the sidebar"""
    st.sidebar.page_link("pages/50_System_Admin.py", label="System Admin")
    st.sidebar.page_link("pages/40_Clients.py", label="Clients")
    st.sidebar.page_link("pages/41_Meal_Logs.py", label="Meal Logs")


def CEOLinks():
    """Add CEO links to the sidebar"""
    st.sidebar.page_link("pages/31_CEO_landing.py", label="CEO Dashboard")
    st.sidebar.page_link("pages/32_CEO_client_engagement.py", label="Client Engagement")
    st.sidebar.page_link("pages/33_CEO_financial_overview.py", label="Financial Overview")
    st.sidebar.page_link("pages/34_CEO_system_preferences.py", label="System Preferences")
    st.sidebar.page_link("pages/40_Clients.py", label="Clients")


def ClientLinks():
    """Add client links to the sidebar"""
    st.sidebar.page_link("pages/35_ATHLETE_landing.py", label="My Dashboard")
    st.sidebar.page_link("pages/36_ATHLETE_weight.py", label="Weight Tracking")
    st.sidebar.page_link("pages/37_ATHLETE_macroworkout.py", label="Macros & Workouts")
    st.sidebar.page_link("pages/41_Meal_Logs.py", label="My Meal Logs")


def NutritionistLinks():
    """Add nutritionist links to the sidebar"""
    st.sidebar.page_link("pages/40_Clients.py", label="Clients")
    st.sidebar.page_link("pages/41_Meal_Logs.py", label="Meal Logs")
