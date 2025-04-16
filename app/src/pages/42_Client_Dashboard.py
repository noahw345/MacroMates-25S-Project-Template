import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Import navigation module
from modules.nav import SideBarLinks

# Ensure the user is authenticated
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.switch_page('Home.py')

# Set up the sidebar navigation
SideBarLinks()

# Page header
st.title('Client Dashboard')
st.write('A consolidated view of all clients with nutrition metrics and alerts')

# Time period selector
col1, col2 = st.columns([1, 3])
with col1:
    days = st.selectbox(
        'Time Period',
        [7, 14, 30, 60, 90],
        index=2,  # Default to 30 days
        format_func=lambda x: f'Last {x} days'
    )

with col2:
    include_archived = st.checkbox('Include archived clients', value=False)

# Function to fetch client dashboard data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_client_data(days, include_archived):
    try:
        response = requests.get(
            'http://api:5000/clients/nutrition-dashboard',
            params={
                'days': days,
                'include_archived': str(include_archived).lower()
            }
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching client data: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to the API: {e}")
        return []

# Get the data
clients_data = fetch_client_data(days, include_archived)

# Create a custom container for client metrics dashboard
if clients_data:
    # Display key stats
    st.subheader('Client Overview')
    
    # Prepare dataframe for stats
    clients_df = pd.json_normalize(clients_data)
    
    # Count clients with alerts
    clients_with_alerts = sum(1 for client in clients_data 
                             if client.get('alerts') and 
                             (client['alerts'].get('deficiencies') or 
                              client['alerts'].get('adherence_issues')))
    
    # Basic stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Clients", len(clients_data))
    with col2:
        st.metric("Clients with Alerts", clients_with_alerts)
    with col3:
        alert_percentage = round((clients_with_alerts / len(clients_data)) * 100) if clients_data else 0
        st.metric("Alert Percentage", f"{alert_percentage}%")
    
    # Aggregate metrics
    if 'metrics.avg_protein' in clients_df.columns:
        avg_protein = clients_df['metrics.avg_protein'].mean()
        avg_carbs = clients_df['metrics.avg_carbs'].mean()
        avg_fat = clients_df['metrics.avg_fat'].mean()
        avg_fiber = clients_df['metrics.avg_fiber'].mean()
        
        st.subheader('Average Nutrient Intake Across All Clients')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Protein", f"{avg_protein:.1f}g")
        with col2:
            st.metric("Carbohydrates", f"{avg_carbs:.1f}g")
        with col3:
            st.metric("Fat", f"{avg_fat:.1f}g")
        with col4:
            st.metric("Fiber", f"{avg_fiber:.1f}g")
    
    # Create a detailed clients table
    st.subheader('Client Details and Alerts')
    
    # Get data for table display
    table_data = []
    for client in clients_data:        
        # Get macronutrient metrics
        metrics = client.get('metrics', {})
        protein = metrics.get('avg_protein', 0)
        carbs = metrics.get('avg_carbs', 0)
        fat = metrics.get('avg_fat', 0)
        fiber = metrics.get('avg_fiber', 0)
        
        # Get activity data
        activity = client.get('activity', {})
        log_count = activity.get('log_count', 0)
        last_logged = activity.get('last_logged', 'Never')
        
        # Format last_logged for display
        if last_logged != 'Never':
            try:
                logged_date = datetime.strptime(last_logged, '%Y-%m-%d %H:%M:%S')
                days_ago = (datetime.now() - logged_date).days
                if days_ago == 0:
                    last_logged = 'Today'
                elif days_ago == 1:
                    last_logged = 'Yesterday'
                else:
                    last_logged = f"{days_ago} days ago"
            except:
                pass
        
        # Get nutrition plan info
        plan = client.get('nutrition_plan', {})
        calories_goal = plan.get('calories_goal', 'No Plan') if plan else 'No Plan'
        
        # Add to table data
        table_data.append({
            'Client ID': client['id'],
            'Name': client['name'],
            'Age': client['age'] or 'Unknown',
            'Protein (g)': f"{protein:.1f}",
            'Carbs (g)': f"{carbs:.1f}",
            'Fat (g)': f"{fat:.1f}",
            'Fiber (g)': f"{fiber:.1f}",
            'Meal Logs': log_count,
            'Last Activity': last_logged,
            'Calorie Goal': calories_goal,
            'Alerts': '\n'.join(alerts) if alerts else 'None'
        })
    
    # Convert to DataFrame
    table_df = pd.DataFrame(table_data)
    
    # Add color highlighting for alerts
    def highlight_alerts(val):
        if '⚠️' in str(val):
            return 'background-color: #ffcccc'
        return ''
    
    # Display as dataframe with styling
    st.dataframe(
        table_df.style.applymap(highlight_alerts, subset=['Alerts']),
        use_container_width=True,
        hide_index=True
    )
    
    # Add visualizations
    st.subheader('Client Nutrient Metrics Visualization')
    
    # Prepare data for bar chart
    chart_data = []
    for client in clients_data:
        metrics = client.get('metrics', {})
        if metrics:
            chart_data.append({
                'Client': client['name'],
                'Protein': metrics.get('avg_protein', 0),
                'Carbohydrates': metrics.get('avg_carbs', 0),
                'Fat': metrics.get('avg_fat', 0),
                'Fiber': metrics.get('avg_fiber', 0)
            })
    
    chart_df = pd.DataFrame(chart_data)
    
    # Create tabs for different chart types
    tab1, tab2 = st.tabs(["Macronutrient Comparison", "Client Activity"])
    
    with tab1:
        if not chart_df.empty:
            # Create the bar chart
            fig = px.bar(
                chart_df,
                x='Client',
                y=['Protein', 'Carbohydrates', 'Fat', 'Fiber'],
                title='Average Daily Macronutrients by Client',
                barmode='group',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No macronutrient data available for visualization.")
    
    with tab2:
        # Prepare data for activity chart
        activity_data = []
        for client in clients_data:
            activity = client.get('activity', {})
            if activity:
                activity_data.append({
                    'Client': client['name'],
                    'Meal Logs': activity.get('log_count', 0)
                })
        
        activity_df = pd.DataFrame(activity_data)
        
        if not activity_df.empty:
            # Sort by meal log count
            activity_df = activity_df.sort_values('Meal Logs', ascending=False)
            
            # Create the bar chart
            fig = px.bar(
                activity_df,
                x='Client',
                y='Meal Logs',
                title=f'Meal Logging Activity in Last {days} Days',
                color='Meal Logs',
                color_continuous_scale=px.colors.sequential.Viridis,
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No activity data available for visualization.")
    
    # Add export functionality
    st.download_button(
        label="Export Client Data to CSV",
        data=table_df.to_csv(index=False).encode('utf-8'),
        file_name=f"client_dashboard_export_{datetime.now().strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
    )
    
else:
    st.info("No client data available. Please check your connection to the API or verify that clients exist in the database.")

# Notes section
with st.expander("About this Dashboard"):
    st.markdown("""
    This dashboard provides a comprehensive overview of all clients' nutrition metrics and alerts:
    
    - **Client Overview**: Displays total clients, those with alerts, and alert percentage
    - **Average Nutrient Intake**: Shows average macronutrient intake across all clients
    - **Client Details and Alerts**: Detailed table with client information, nutrient metrics, and alerts
    - **Visualizations**: Compare macronutrient intake and meal logging activity across clients
    
    Alerts are automatically generated for:
    - **Nutrient Deficiencies**: Based on recorded nutrient intake compared to recommended values
    - **Adherence Issues**: When clients aren't logging meals regularly
    
    Use the time period selector to change the analysis window and include/exclude archived clients.
    """) 