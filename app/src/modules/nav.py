# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


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


#### ------------------------ Nutritionist Pages ------------------------
def NutritionistDashboardNav():
    st.sidebar.page_link("pages/51_Nutritionist_landing.py", label="Dashboard", icon="🥗")


def ClientManagementNav():
    st.sidebar.page_link("pages/52_Client_Management.py", label="Client Management", icon="👥")


def ClientProgressNav():
    st.sidebar.page_link("pages/53_Client_Progress.py", label="Client Progress", icon="📈")


def NutritionalAnalysisNav():
    st.sidebar.page_link("pages/54_Nutritional_Analysis.py", label="Nutritional Analysis", icon="🔬")


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
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )

#### ------------------------ CEO Role ------------------------
def CEOHomeNav():
    st.sidebar.page_link("pages/31_CEO_landing.py", label="CEO Home", icon="💼")

def CEOClientEngagementNav():
    st.sidebar.page_link("pages/32_CEO_client_engagement.py", label="Client Engagement", icon="📈")

def CEOFinancialOverviewNav():
    st.sidebar.page_link("pages/33_CEO_financial_overview.py", label="Financial Overview", icon="💰")

def CEOSystemPerformanceNav():
    st.sidebar.page_link("pages/34_CEO_system_performance.py", label="System Performance", icon="⚙️")

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:
        # Show navigation based on user role
        if st.session_state["role"] == "nutritionist":
            NutritionistDashboardNav()
            ClientManagementNav()
            ClientProgressNav()
            NutritionalAnalysisNav()
        elif st.session_state["role"] == "pol_strat_advisor":
            PolStratAdvHomeNav()
            WorldBankVizNav()
            MapDemoNav()
        elif st.session_state["role"] == "usaid_worker":
            PredictionNav()
            ApiTestNav()
            ClassificationNav()
        elif st.session_state["role"] == "administrator":
            AdminPageNav()
        else:
            # Default navigation for other roles
            ClientsNav()
            MealLogsNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
