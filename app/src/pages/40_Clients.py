import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks
import os

# Configure the page
st.set_page_config(layout="wide", page_title="Clients - MacroMates")

# Display the appropriate sidebar links for the logged in user
SideBarLinks()

st.title("Clients")
st.subheader("View and manage nutrition clients")

# API configuration
# We're using host.docker.internal which is a special DNS name that Docker provides
# to allow containers to access services running on the host machine
API_BASE_URL = "http://host.docker.internal:4001"

# Function to fetch clients from API
def fetch_clients():
    try:
        url = f"{API_BASE_URL}/api/clients"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch clients: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

# Create search filters
st.subheader("Search Filters")
col1, col2 = st.columns(2)

with col1:
    name_filter = st.text_input("Search by Name")

with col2:
    email_filter = st.text_input("Search by Email")

# Button to search with filters
if st.button("Search", type="primary"):
    # If filters are provided, use the search endpoint
    if name_filter or email_filter:
        try:
            params = {}
            if name_filter:
                params['name'] = name_filter
            if email_filter:
                params['email'] = email_filter
                
            url = f"{API_BASE_URL}/api/clients"
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                clients = response.json()
            else:
                st.error(f"Failed to search clients: {response.status_code} - {response.text}")
                clients = []
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")
            clients = []
    else:
        # If no filters, fetch all clients
        clients = fetch_clients()
else:
    # Initial load - fetch all clients
    clients = fetch_clients()

# Display clients in a table
if clients:
    # Convert to DataFrame for better display
    df = pd.DataFrame(clients)
    
    # Rename columns for better display
    if not df.empty:
        df = df.rename(columns={
            'id': 'ID',
            'name': 'Name',
            'dob': 'Date of Birth',
            'email': 'Email'
        })
    
    # Show the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "ID": st.column_config.NumberColumn(
                "ID",
                help="Client ID",
                format="%d",
            ),
            "Name": st.column_config.TextColumn(
                "Name",
                help="Client's full name",
            ),
            "Date of Birth": st.column_config.DateColumn(
                "Date of Birth",
                help="Client's date of birth",
                format="YYYY-MM-DD",
            ),
            "Email": st.column_config.TextColumn(
                "Email",
                help="Client's email address",
            ),
        },
        hide_index=True,
    )
    
    st.caption(f"Total clients: {len(clients)}")
else:
    st.info("No clients found. Try adjusting your search filters or add a new client.")

# Add a new client section
with st.expander("Add New Client"):
    with st.form("new_client_form"):
        st.write("Enter client details")
        
        new_name = st.text_input("Name", key="new_name")
        new_email = st.text_input("Email", key="new_email")
        new_dob = st.date_input("Date of Birth (optional)", value=None, key="new_dob")
        
        submit = st.form_submit_button("Add Client")
        
        if submit:
            if not new_name or not new_email:
                st.error("Name and email are required")
            else:
                try:
                    data = {
                        "name": new_name,
                        "email": new_email
                    }
                    
                    if new_dob:
                        data["dob"] = new_dob.strftime("%Y-%m-%d")
                    
                    url = f"{API_BASE_URL}/api/clients"
                    response = requests.post(url, json=data, timeout=5)
                    
                    if response.status_code == 201:
                        st.success("Client added successfully!")
                    else:
                        st.error(f"Failed to add client: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to API: {str(e)}") 