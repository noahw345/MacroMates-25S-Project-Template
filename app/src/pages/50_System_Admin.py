# app/src/pages/50_System_Admin.py

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

# Configure page layout and title
st.set_page_config(layout="wide", page_title="System Administrator - MacroMates")

# Display sidebar navigation links
SideBarLinks()

st.title("System Administrator Dashboard")
st.markdown("Manage system performance, datasets, and security protocols here.")

# Define your API base URL (adjust if needed)
API_BASE_URL = "http://host.docker.internal:4001/api"


# Section 1: System Performance

st.header("System Performance Metrics")

@st.cache_data(ttl=60)
def fetch_system_performance():
    try:
        response = requests.get(f"{API_BASE_URL}/system-performance", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching system metrics: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

system_data = fetch_system_performance()
if system_data:
    df_system = pd.DataFrame(system_data)
    st.dataframe(df_system, use_container_width=True)
else:
    st.info("No system performance data available.")


# Section 2: Manage Datasets

st.header("Manage Datasets")

@st.cache_data(ttl=60)
def fetch_datasets():
    try:
        response = requests.get(f"{API_BASE_URL}/datasets", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching datasets: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

datasets = fetch_datasets()
if datasets:
    df_datasets = pd.DataFrame(datasets)
    st.dataframe(df_datasets, use_container_width=True)
else:
    st.info("No datasets available.")

st.subheader("Update a Dataset Entry")
with st.form("update_dataset_form"):
    dataset_id = st.number_input("Dataset ID to update", min_value=1, step=1)
    new_description = st.text_input("New Data Description")
    update_submit = st.form_submit_button("Update Dataset")
    if update_submit:
        if not dataset_id or not new_description:
            st.error("Please provide Dataset ID and new description.")
        else:
            try:
                url = f"{API_BASE_URL}/datasets/{dataset_id}"
                data = {"data_description": new_description}
                response = requests.put(url, json=data, timeout=5)
                if response.status_code == 200:
                    st.success("Dataset updated successfully!")
                else:
                    st.error(f"Update failed: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error connecting to API: {e}")

st.subheader("Remove Unused Dataset Entry")
with st.form("delete_dataset_form"):
    delete_dataset_id = st.number_input("Dataset ID to delete", min_value=1, step=1, key="delete_dataset")
    delete_submit = st.form_submit_button("Delete Dataset")
    if delete_submit:
        try:
            url = f"{API_BASE_URL}/datasets/{delete_dataset_id}"
            response = requests.delete(url, timeout=5)
            if response.status_code == 200:
                st.success("Dataset deleted successfully!")
            else:
                st.error(f"Deletion failed: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error connecting to API: {e}")


# Section 3: Security Protocols

st.header("Security Protocols")
@st.cache_data(ttl=60)
def fetch_security_status():
    try:
        response = requests.get(f"{API_BASE_URL}/security", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching security protocols: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

security_data = fetch_security_status()
if security_data:
    df_security = pd.DataFrame(security_data)
    st.dataframe(df_security, use_container_width=True)
else:
    st.info("No security protocol data available.")

st.subheader("Add Security Protocol")
with st.form("add_security_protocol_form"):
    security_status = st.selectbox("Security Status", ["Normal", "Alert", "Warning"])
    log_id = st.number_input("Associated Log ID", min_value=1, step=1)
    protocol_submit = st.form_submit_button("Add Protocol")
    if protocol_submit:
        try:
            url = f"{API_BASE_URL}/security"
            data = {"status": security_status, "log_id": log_id}
            response = requests.post(url, json=data, timeout=5)
            if response.status_code == 201:
                st.success("Security protocol added successfully!")
            else:
                st.error(f"Failed to add protocol: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("### Data Integrity Checks")
st.info("Ensure data is valid by reviewing system logs and dataset entries.")
