import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Nutritional Analysis",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Nutritional Analysis")

# Fetch clients list
try:
    clients_response = requests.get("http://localhost:4000/nutritionist/clients")
    if clients_response.status_code == 200:
        clients = clients_response.json()
        
        if clients:
            # Client selection
            client_names = [client["name"] for client in clients]
            selected_client = st.selectbox("Select a client", client_names)
            
            if selected_client:
                client_id = next(client["client_id"] for client in clients if client["name"] == selected_client)
                
                # Fetch client nutritional data
                nutrition_response = requests.get(f"http://localhost:4000/nutritionist/client/{client_id}/nutrition")
                
                if nutrition_response.status_code == 200:
                    nutrition_data = nutrition_response.json()
                    
                    # Macronutrient Distribution
                    st.subheader("Macronutrient Distribution")
                    if nutrition_data["macronutrients"]:
                        macros_df = pd.DataFrame(nutrition_data["macronutrients"])
                        
                        # Create pie chart
                        fig = px.pie(
                            macros_df,
                            values="amount",
                            names="nutrient_name",
                            title="Macronutrient Distribution",
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display macronutrients table
                        st.dataframe(
                            macros_df,
                            column_config={
                                "nutrient_name": "Nutrient",
                                "amount": "Amount (g)",
                                "percentage": "Percentage of Total"
                            },
                            hide_index=True
                        )
                    else:
                        st.info("No macronutrient data available")
                    
                    # Caloric Intake
                    st.subheader("Caloric Intake")
                    if nutrition_data["calories"]:
                        calories_df = pd.DataFrame(nutrition_data["calories"])
                        calories_df["date"] = pd.to_datetime(calories_df["date"])
                        
                        # Create line chart
                        fig = px.line(
                            calories_df,
                            x="date",
                            y="calories",
                            title="Daily Caloric Intake",
                            labels={
                                "date": "Date",
                                "calories": "Calories"
                            }
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display calories table
                        st.dataframe(
                            calories_df,
                            column_config={
                                "date": "Date",
                                "calories": "Calories",
                                "goal": "Daily Goal"
                            },
                            hide_index=True
                        )
                    else:
                        st.info("No caloric intake data available")
                    
                    # Recent Meals
                    st.subheader("Recent Meals")
                    if nutrition_data["recent_meals"]:
                        meals_df = pd.DataFrame(nutrition_data["recent_meals"])
                        meals_df["date"] = pd.to_datetime(meals_df["date"])
                        
                        # Display meals table
                        st.dataframe(
                            meals_df,
                            column_config={
                                "date": "Date",
                                "meal_type": "Meal Type",
                                "food_name": "Food",
                                "calories": "Calories",
                                "protein": "Protein (g)",
                                "carbs": "Carbs (g)",
                                "fat": "Fat (g)"
                            },
                            hide_index=True
                        )
                    else:
                        st.info("No recent meal data available")
                else:
                    st.error("Failed to fetch client nutritional data")
        else:
            st.info("No clients found")
    else:
        st.error("Failed to fetch clients data")
except Exception as e:
    st.error(f"Error: {str(e)}")
