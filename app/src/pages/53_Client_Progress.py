import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.nav import SideBarLinks

# Set page config
st.set_page_config(
    page_title="Client Progress",
    page_icon="📈",
    layout="wide"
)

# Display the appropriate sidebar links
SideBarLinks()

# Title
st.title("📈 Client Progress")

# Fetch clients list
try:
    clients_response = requests.get("http://localhost:4000/nutritionist/clients")
    if clients_response.status_code == 200:
        clients = clients_response.json()
        
        if clients:
            # Client selection
            client_names = [client['name'] for client in clients]
            selected_client = st.selectbox("Select a client", client_names)
            
            if selected_client:
                client_id = next(client['client_id'] for client in clients if client['name'] == selected_client)
                
                # Fetch client progress data
                progress_response = requests.get(f"http://localhost:4000/nutritionist/client/{client_id}/progress")
                
                if progress_response.status_code == 200:
                    progress_data = progress_response.json()
                    
                    # Weight and Body Fat Progress
                    st.subheader("Weight and Body Composition")
                    if progress_data['measurements']:
                        measurements_df = pd.DataFrame(progress_data['measurements'])
                        measurements_df['date'] = pd.to_datetime(measurements_df['date'])
                        
                        # Create a figure with secondary y-axis
                        fig = go.Figure()
                        
                        # Add weight trace
                        fig.add_trace(
                            go.Scatter(
                                x=measurements_df['date'],
                                y=measurements_df['weight'],
                                name="Weight (kg)",
                                line=dict(color='blue')
                            )
                        )
                        
                        # Add body fat trace
                        fig.add_trace(
                            go.Scatter(
                                x=measurements_df['date'],
                                y=measurements_df['body_fat_percentage'],
                                name="Body Fat %",
                                line=dict(color='red'),
                                yaxis="y2"
                            )
                        )
                        
                        # Update layout
                        fig.update_layout(
                            title="Weight and Body Fat Progress",
                            xaxis_title="Date",
                            yaxis_title="Weight (kg)",
                            yaxis2=dict(
                                title="Body Fat %",
                                overlaying="y",
                                side="right"
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No measurement data available")
                    
                    # Nutritional Deficiencies
                    st.subheader("Nutritional Deficiencies")
                    if progress_data['deficiencies']:
                        deficiencies_df = pd.DataFrame(progress_data['deficiencies'])
                        
                        # Create a bar chart for deficiencies
                        fig = px.bar(
                            deficiencies_df,
                            x='nutrient_name',
                            y='deficiency',
                            title="Nutritional Deficiencies",
                            labels={
                                'nutrient_name': 'Nutrient',
                                'deficiency': 'Deficiency Amount'
                            }
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display deficiencies table
                        st.dataframe(
                            deficiencies_df,
                            column_config={
                                "nutrient_name": "Nutrient",
                                "recommended_amount": "Recommended Amount",
                                "average_intake": "Average Intake",
                                "deficiency": "Deficiency"
                            },
                            hide_index=True
                        )
                    else:
                        st.info("No nutritional deficiencies found")
                else:
                    st.error("Failed to fetch client progress data")
        else:
            st.info("No clients found")
    else:
        st.error("Failed to fetch clients data")
except Exception as e:
    st.error(f"Error: {str(e)}") 