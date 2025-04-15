# 50_System_Admin.py
import streamlit as st
from modules.nav import SideBarLinks

# Configure the page layout and title
st.set_page_config(layout="wide", page_title="System Administrator - MacroMates")

# Display sidebar navigation links
SideBarLinks()

# Basic Page Content
st.title("System Administrator")
st.markdown("This is the initial version of the System Administrator page. More features coming soon!")
