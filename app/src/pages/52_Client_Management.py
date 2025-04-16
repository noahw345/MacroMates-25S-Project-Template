import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Client Management",
    page_icon="👥",
    layout="wide"
)

# Title
st.title("👥 Client Management")

# Fetch clients data
try:
    response = requests.get("http://localhost:4000/nutritionist/clients")
    if response.status_code == 200:
        clients = response.json()
        
        if clients:
            # Convert to DataFrame
            df = pd.DataFrame(clients)
            
            # Display filters
            col1, col2 = st.columns(2)
            
            with col1:
                search_query = st.text_input("Search Clients", "")
                if search_query:
                    df = df[df['name'].str.contains(search_query, case=False, na=False) | 
                           df['email'].str.contains(search_query, case=False, na=False)]
            
            with col2:
                sort_by = st.selectbox(
                    "Sort by",
                    ["Name", "Total Meals", "Average Calories"],
                    index=0
                )
                if sort_by == "Name":
                    df = df.sort_values('name')
                elif sort_by == "Total Meals":
                    df = df.sort_values('total_meals', ascending=False)
                else:
                    df = df.sort_values('avg_calories', ascending=False)
            
            # Display clients table
            st.dataframe(
                df[['name', 'email', 'total_meals', 'avg_calories']],
                column_config={
                    "name": "Client Name",
                    "email": "Email",
                    "total_meals": "Total Meals",
                    "avg_calories": "Avg. Calories"
                },
                hide_index=True
            )
            
            # Client details section
            st.subheader("Client Details")
            selected_client = st.selectbox(
                "Select a client to view details",
                df['name'].tolist()
            )
            
            if selected_client:
                client_id = df[df['name'] == selected_client]['client_id'].iloc[0]
                details_response = requests.get(f"http://localhost:4000/nutritionist/client/{client_id}")
                
                if details_response.status_code == 200:
                    client_details = details_response.json()
                    
                    # Display client information
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Basic Information**")
                        st.write(f"Name: {client_details['client']['name']}")
                        st.write(f"Email: {client_details['client']['email']}")
                        st.write(f"Phone: {client_details['client'].get('phone', 'N/A')}")
                    
                    with col2:
                        st.write("**Recent Meals**")
                        if client_details['recent_meals']:
                            meals_df = pd.DataFrame(client_details['recent_meals'])
                            st.dataframe(
                                meals_df[['date', 'calories', 'protein', 'carbs', 'fats']],
                                hide_index=True
                            )
                        else:
                            st.info("No recent meals found")
                    
                    # Nutritional Trends Chart
                    st.subheader("Nutritional Trends")
                    if client_details['nutritional_trends']:
                        trends_df = pd.DataFrame(client_details['nutritional_trends'])
                        fig = px.line(
                            trends_df,
                            x='meal_date',
                            y=['avg_calories', 'avg_protein', 'avg_carbs', 'avg_fats'],
                            title='Nutritional Trends Over Time'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No nutritional trends data available")
                else:
                    st.error("Failed to fetch client details")
        else:
            st.info("No clients found")
    else:
        st.error("Failed to fetch clients data")
except Exception as e:
    st.error(f"Error: {str(e)}") 