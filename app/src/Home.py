##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide', page_title="MacroMates - Nutrition Buddy")

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

logger.info("Loading the MacroMates Home page")

# Header with logo and welcome message
col1, col2 = st.columns([1, 2])

with col1:
    st.image("assets/logo.png", width=200)
    
with col2:
    st.title('MacroMates')

st.markdown("""
### Welcome to MacroMates!

MacroMates helps you track your meals, analyze macronutrients, and optimize your diet based on personalized goals.
Our intelligent system provides meal recommendations and nutrition insights to help you achieve your health goals.

Log in below to get started!
""")

st.write('\n\n')

# User role selection
st.subheader("Select your role to log in")

col1, col2 = st.columns(2)

with col1:
    if st.button("Log in as a Nutrition Client", 
                type = 'primary', 
                use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'nutrition_client'
        st.session_state['first_name'] = 'Alex'
        logger.info("Logging in as Nutrition Client")
        st.switch_page('pages/40_Clients.py')

    if st.button('Log in as a Nutritionist', 
                type = 'primary', 
                use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'nutritionist'
        st.session_state['first_name'] = 'Jamie'
        st.switch_page('pages/40_Clients.py')

with col2:
    if st.button('Log in as System Administrator', 
                type = 'primary', 
                use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'administrator'
        st.session_state['first_name'] = 'Admin'
        st.switch_page('pages/40_Clients.py')



