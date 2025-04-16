import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Nutritional Analysis",
    page_icon="🔬",
    layout="wide"
)

# Title
st.title("🔬 Nutritional Analysis")

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
                
                # Fetch client details
                details_response = requests.get(f"http://localhost:4000/nutritionist/client/{client_id}")
                
                if details_response.status_code == 200:
                    client_data = details_response.json()
                    
                    # Macronutrient Distribution
                    st.subheader("Macronutrient Distribution")
                    if client_data['nutritional_trends']:
                        trends_df = pd.DataFrame(client_data['nutritional_trends'])
                        
                        # Calculate average macronutrient distribution
                        avg_protein = trends_df['avg_protein'].mean()
                        avg_carbs = trends_df['avg_carbs'].mean()
                        avg_fats = trends_df['avg_fats'].mean()
                        
                        # Create pie chart
                        fig = px.pie(
                            values=[avg_protein, avg_carbs, avg_fats],
                            names=['Protein', 'Carbohydrates', 'Fats'],
                            title='Average Macronutrient Distribution'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Create line chart for macronutrient trends
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=trends_df['meal_date'],
                            y=trends_df['avg_protein'],
                            name='Protein',
                            line=dict(color='blue')
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=trends_df['meal_date'],
                            y=trends_df['avg_carbs'],
                            name='Carbohydrates',
                            line=dict(color='green')
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=trends_df['meal_date'],
                            y=trends_df['avg_fats'],
                            name='Fats',
                            line=dict(color='red')
                        ))
                        
                        fig.update_layout(
                            title='Macronutrient Trends Over Time',
                            xaxis_title='Date',
                            yaxis_title='Grams'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Caloric Intake Analysis
                    st.subheader("Caloric Intake Analysis")
                    if client_data['nutritional_trends']:
                        # Create caloric intake chart
                        fig = px.line(
                            trends_df,
                            x='meal_date',
                            y='avg_calories',
                            title='Average Daily Caloric Intake'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Calculate statistics
                        avg_calories = trends_df['avg_calories'].mean()
                        min_calories = trends_df['avg_calories'].min()
                        max_calories = trends_df['avg_calories'].max()
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Average Calories", f"{avg_calories:.0f}")
                        with col2:
                            st.metric("Minimum Calories", f"{min_calories:.0f}")
                        with col3:
                            st.metric("Maximum Calories", f"{max_calories:.0f}")
                    
                    # Recent Meals Analysis
                    st.subheader("Recent Meals Analysis")
                    if client_data['recent_meals']:
                        meals_df = pd.DataFrame(client_data['recent_meals'])
                        meals_df['date'] = pd.to_datetime(meals_df['date'])
                        
                        # Display meals table
                        st.dataframe(
                            meals_df[['date', 'calories', 'protein', 'carbs', 'fats']],
                            column_config={
                                "date": "Date",
                                "calories": "Calories",
                                "protein": "Protein (g)",
                                "carbs": "Carbs (g)",
                                "fats": "Fats (g)"
                            },
                            hide_index=True
                        )
                    else:
                        st.info("No recent meals data available")
                else:
                    st.error("Failed to fetch client data")
        else:
            st.info("No clients found")
    else:
        st.error("Failed to fetch clients data")
except Exception as e:
    st.error(f"Error: {str(e)}") 