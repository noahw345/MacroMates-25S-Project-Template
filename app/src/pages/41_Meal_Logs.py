import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import datetime, timedelta
from modules.nav import SideBarLinks
import os

# Configure the page
st.set_page_config(layout="wide", page_title="Meal Logs - MacroMates")

# Display the appropriate sidebar links for the logged in user
SideBarLinks()

st.title("Meal Logs")
st.subheader("View and manage client meal logs")

# API configuration
# We're using host.docker.internal which is a special DNS name that Docker provides
# to allow containers to access services running on the host machine
API_BASE_URL = "http://host.docker.internal:4000"

# For debugging
st.info(f"Using API at: {API_BASE_URL}/api/clients")

# First, we need to get the list of clients for the client selector
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

# Get client list for dropdown
clients = fetch_clients()

# Create client and date filters
st.subheader("Filters")
col1, col2, col3 = st.columns(3)

with col1:
    # If clients were fetched successfully, create a dropdown
    if clients:
        client_options = {client['id']: client['name'] for client in clients}
        client_options[0] = "-- Select Client --"  # Add a default option
        
        selected_client_id = st.selectbox(
            "Select Client",
            options=list(client_options.keys()),
            format_func=lambda x: client_options.get(x, "Unknown"),
            index=0  # Default to the first item (Select Client)
        )
    else:
        st.warning("Could not load clients")
        selected_client_id = None

with col2:
    date_from = st.date_input("From Date", value=datetime.now() - timedelta(days=7))

with col3:
    date_to = st.date_input("To Date", value=datetime.now())

# Function to fetch meal logs with filters
def fetch_meal_logs(client_id, date_from, date_to):
    if not client_id or client_id == 0:  # If no client selected
        return []
    
    try:
        params = {
            'client_id': client_id
        }
        
        if date_from:
            params['date_from'] = date_from.strftime('%Y-%m-%d')
        
        if date_to:
            params['date_to'] = date_to.strftime('%Y-%m-%d')
        
        url = f"{API_BASE_URL}/api/meal-logs"
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch meal logs: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

# Button to search with filters
if st.button("View Meal Logs", type="primary", disabled=(selected_client_id == 0 or selected_client_id is None)):
    # Fetch meal logs with selected filters
    meal_logs = fetch_meal_logs(selected_client_id, date_from, date_to)
    
    # Store meal logs in session state
    st.session_state['meal_logs'] = meal_logs
else:
    # Check if meal logs are already in session state
    if 'meal_logs' not in st.session_state:
        st.session_state['meal_logs'] = []
    
    meal_logs = st.session_state['meal_logs']

# Display meal logs
if meal_logs:
    # Process meal logs for display
    display_data = []
    for log in meal_logs:
        # Count nutrients by categories
        nutrient_counts = {}
        for nutrient in log.get('nutrients', []):
            category = nutrient.get('category', 'Other')
            if category not in nutrient_counts:
                nutrient_counts[category] = 0
            nutrient_counts[category] += 1
        
        # Format the data
        log_data = {
            'id': log.get('id'),
            'datetime': log.get('datetime'),
            'notes': log.get('notes', ''),
            'nutrient_count': len(log.get('nutrients', [])),
        }
        
        # Add nutrient categories counts
        for category, count in nutrient_counts.items():
            log_data[f"{category}_count"] = count
        
        display_data.append(log_data)
    
    # Convert to DataFrame
    if display_data:
        df = pd.DataFrame(display_data)
        
        # Show the dataframe
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "id": st.column_config.NumberColumn(
                    "ID",
                    help="Meal Log ID",
                    format="%d",
                ),
                "datetime": st.column_config.DatetimeColumn(
                    "Date & Time",
                    help="When the meal was logged",
                    format="MMM DD, YYYY, hh:mm a",
                ),
                "notes": st.column_config.TextColumn(
                    "Notes",
                    help="Description or notes about the meal",
                ),
                "nutrient_count": st.column_config.NumberColumn(
                    "Total Nutrients",
                    help="Total number of nutrients in this meal",
                ),
                "Macronutrient_count": st.column_config.NumberColumn(
                    "Macronutrients",
                    help="Number of macronutrients in this meal",
                ) if "Macronutrient_count" in df.columns else None,
                "Vitamin_count": st.column_config.NumberColumn(
                    "Vitamins",
                    help="Number of vitamins in this meal",
                ) if "Vitamin_count" in df.columns else None,
                "Mineral_count": st.column_config.NumberColumn(
                    "Minerals",
                    help="Number of minerals in this meal",
                ) if "Mineral_count" in df.columns else None,
            },
            hide_index=True,
        )
        
        st.caption(f"Total meal logs: {len(meal_logs)}")
    else:
        st.info("No meal logs found for the selected filters.")

    # Add details section for viewing nutrients in a specific meal
    with st.expander("View Meal Details"):
        meal_id = st.number_input("Enter Meal Log ID to View Details", min_value=1, step=1)
        
        if st.button("View Details"):
            # Find the meal log in our existing data first
            selected_meal = next((meal for meal in meal_logs if meal.get('id') == meal_id), None)
            
            if not selected_meal:
                # If not found in current set, try to fetch it
                try:
                    url = f"{API_BASE_URL}/api/meal-logs/{meal_id}"
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        selected_meal = response.json()
                    else:
                        st.error(f"Failed to fetch meal details: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to API: {str(e)}")
            
            # Display the meal details if found
            if selected_meal:
                st.subheader(f"Meal Log #{selected_meal.get('id')}")
                
                # Display basic meal info
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Date & Time:** {selected_meal.get('datetime')}")
                with col2:
                    st.write(f"**Notes:** {selected_meal.get('notes', 'No notes')}")
                
                # Display nutrients table
                if 'nutrients' in selected_meal and selected_meal['nutrients']:
                    # Convert nutrients to DataFrame
                    nutrients_df = pd.DataFrame(selected_meal['nutrients'])
                    
                    # Rename columns
                    nutrients_df = nutrients_df.rename(columns={
                        'id': 'ID',
                        'name': 'Name',
                        'category': 'Category',
                        'quantity': 'Quantity',
                        'unit': 'Unit'
                    })
                    
                    # Display nutrients table
                    st.subheader("Nutrients")
                    st.dataframe(
                        nutrients_df,
                        use_container_width=True,
                        column_config={
                            "ID": st.column_config.NumberColumn(
                                "ID", 
                                help="Nutrient ID"
                            ),
                            "Name": st.column_config.TextColumn(
                                "Name",
                                help="Nutrient name"
                            ),
                            "Category": st.column_config.TextColumn(
                                "Category",
                                help="Nutrient category"
                            ),
                            "Quantity": st.column_config.NumberColumn(
                                "Quantity",
                                help="Quantity of the nutrient",
                                format="%.2f"
                            ),
                            "Unit": st.column_config.TextColumn(
                                "Unit",
                                help="Unit of measurement"
                            )
                        },
                        hide_index=True
                    )
                else:
                    st.info("No nutrients found for this meal log.")
            else:
                st.warning(f"Meal log with ID {meal_id} not found.")
else:
    st.info("Select a client and date range to view meal logs.") 