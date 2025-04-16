import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Import navigation module
from modules.nav import SideBarLinks

# Ensure the user is authenticated
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.switch_page('Home.py')

# Set up the sidebar navigation
SideBarLinks()

# Page header
st.title('Trend Analysis Tools')
st.write('Analyze dietary habits over time (weekly/monthly/yearly)')

# Function to fetch clients
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_clients():
    try:
        response = requests.get('http://api:5000/clients')
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching clients: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to the API: {e}")
        return []

# Function to fetch trend analysis data
@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_trend_analysis(client_id, period, start_date, end_date, nutrients):
    try:
        response = requests.get(
            'http://api:5000/trend-analysis',
            params={
                'client_id': client_id,
                'period': period,
                'start_date': start_date,
                'end_date': end_date,
                'nutrients': nutrients
            }
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching trend data: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to the API: {e}")
        return None

# Sidebar for analysis options
st.sidebar.header('Analysis Options')

# Get all clients for selector
clients = fetch_clients()

if clients:
    # Client selection
    client_options = [{'id': c['id'], 'name': f"{c['name']} (ID: {c['id']})"} for c in clients]
    selected_client = st.sidebar.selectbox(
        'Select Client',
        options=client_options,
        format_func=lambda x: x['name']
    )
    
    # Time period selection
    period = st.sidebar.radio('Time Grouping', ['weekly', 'monthly', 'yearly'])
    
    # Date range selection
    st.sidebar.subheader('Date Range')
    
    # Default to 90 days ago for start date
    default_start = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    start_date = st.sidebar.date_input('Start Date', value=datetime.strptime(default_start, '%Y-%m-%d'))
    end_date = st.sidebar.date_input('End Date', value=datetime.now())
    
    # Convert dates to string format
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    # Nutrient selection
    st.sidebar.subheader('Nutrients to Analyze')
    nutrients_list = [
        'Protein', 'Carbohydrates', 'Fat', 'Fiber',
        'Vitamin A', 'Vitamin C', 'Vitamin D', 'Calcium', 'Iron'
    ]
    
    selected_nutrients = []
    for nutrient in nutrients_list:
        # Default select the macronutrients
        default = nutrient in ['Protein', 'Carbohydrates', 'Fat', 'Fiber']
        if st.sidebar.checkbox(nutrient, value=default):
            selected_nutrients.append(nutrient)
    
    # Convert nutrient list to comma-separated string
    nutrients_str = ','.join(selected_nutrients)
    
    # Analysis button
    if st.sidebar.button('Run Analysis', type='primary'):
        if selected_client and selected_nutrients:
            with st.spinner('Analyzing trend data...'):
                # Fetch the trend analysis data
                trend_data = fetch_trend_analysis(
                    selected_client['id'],
                    period,
                    start_date_str,
                    end_date_str,
                    nutrients_str
                )
                
                if trend_data:
                    # Display summary
                    st.subheader('Trend Analysis Summary')
                    st.info(trend_data['summary_text'])
                    
                    # Display macronutrient summary if available
                    if trend_data['summary']:
                        st.subheader('Nutrient Summary')
                        
                        # Create columns for metrics
                        cols = st.columns(len(trend_data['summary']))
                        
                        # Display each nutrient summary
                        for i, (nutrient, data) in enumerate(trend_data['summary'].items()):
                            with cols[i]:
                                # Determine color based on trend direction
                                if data['trend'] == 'increasing':
                                    delta_color = 'normal'
                                elif data['trend'] == 'decreasing':
                                    delta_color = 'inverse'
                                else:
                                    delta_color = 'off'
                                
                                st.metric(
                                    label=nutrient, 
                                    value=f"{data['avg']} {data['unit']}",
                                    delta=data['trend'],
                                    delta_color=delta_color
                                )
                    
                    # Display recommendations if any
                    if trend_data.get('recommendations'):
                        st.subheader('Recommendations')
                        for rec in trend_data['recommendations']:
                            st.warning(f"**{rec['category']}**: {rec['message']}")
                    
                    # Create trend visualizations
                    st.subheader('Trend Visualization')
                    
                    # Create tabs for different visualizations
                    tabs = ['Line Chart', 'Bar Chart', 'Heatmap']
                    tab1, tab2, tab3 = st.tabs(tabs)
                    
                    # Prepare data for charts
                    all_chart_data = []
                    
                    for nutrient, data in trend_data['nutrients'].items():
                        for point in data['data']:
                            all_chart_data.append({
                                'Period': point['period'],
                                'Nutrient': nutrient,
                                'Value': point['avg_value'],
                                'Unit': data['unit'],
                                'Meals Logged': point['meal_count'],
                                'Days with Logs': point['days_with_logs']
                            })
                    
                    chart_df = pd.DataFrame(all_chart_data)
                    
                    # 1. Line Chart
                    with tab1:
                        # Create one line per nutrient
                        fig = px.line(
                            chart_df, 
                            x='Period', 
                            y='Value', 
                            color='Nutrient',
                            markers=True,
                            title=f'{period.capitalize()} Trend of Nutrient Intake',
                            labels={'Value': 'Amount', 'Period': period.capitalize()},
                            hover_data=['Meals Logged', 'Days with Logs', 'Unit']
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # 2. Bar Chart
                    with tab2:
                        # Grouped bar chart
                        fig = px.bar(
                            chart_df,
                            x='Period',
                            y='Value',
                            color='Nutrient',
                            barmode='group',
                            title=f'{period.capitalize()} Comparison of Nutrient Intake',
                            labels={'Value': 'Amount', 'Period': period.capitalize()},
                            hover_data=['Meals Logged', 'Days with Logs', 'Unit']
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # 3. Heatmap
                    with tab3:
                        # Pivot the data for heatmap
                        pivot_df = chart_df.pivot(index='Nutrient', columns='Period', values='Value')
                        
                        # Create heatmap
                        fig = px.imshow(
                            pivot_df,
                            labels=dict(x=period.capitalize(), y="Nutrient", color="Value"),
                            title=f"Heatmap of {period.capitalize()} Nutrient Trends",
                            color_continuous_scale='Viridis'
                        )
                        
                        # Update layout
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Show meal logging consistency
                    st.subheader('Meal Logging Consistency')
                    
                    # Extract meal logging data
                    logging_data = []
                    for nutrient, data in trend_data['nutrients'].items():
                        # Just use the first nutrient's data since meal counts are the same for all nutrients
                        if nutrient == selected_nutrients[0]:
                            for point in data['data']:
                                logging_data.append({
                                    'Period': point['period'],
                                    'Meals Logged': point['meal_count'],
                                    'Days with Logs': point['days_with_logs']
                                })
                    
                    logging_df = pd.DataFrame(logging_data)
                    
                    # Create bar chart for meal logging
                    fig = px.bar(
                        logging_df,
                        x='Period',
                        y=['Meals Logged', 'Days with Logs'],
                        barmode='group',
                        title=f'Meal Logging Activity by {period.capitalize()}',
                        labels={'value': 'Count', 'Period': period.capitalize(), 'variable': 'Metric'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add export functionality
                    st.download_button(
                        label="Export Trend Data to CSV",
                        data=chart_df.to_csv(index=False).encode('utf-8'),
                        file_name=f"trend_analysis_{period}_{datetime.now().strftime('%Y-%m-%d')}.csv",
                        mime="text/csv",
                    )
        else:
            if not selected_nutrients:
                st.sidebar.error("Please select at least one nutrient to analyze.")
else:
    st.warning("No clients available. Please add clients first.")

# Notes section
with st.expander("About Trend Analysis"):
    st.markdown("""
    This tool allows you to analyze nutrition trends over time for individual clients. The analysis provides insights into:
    
    - **Nutrient Intake Patterns**: Track how macronutrient and micronutrient intake changes over weeks, months, or years
    - **Meal Logging Consistency**: Monitor how regularly clients are logging their meals
    - **Trend Direction**: Identify increasing, decreasing, or stable patterns in nutrient consumption
    - **Recommendations**: Get suggestions based on observed trends and nutritional goals
    
    **How to use this tool:**
    1. Select a client from the dropdown menu
    2. Choose a time grouping (weekly, monthly, or yearly)
    3. Set your date range for analysis
    4. Select the nutrients you want to analyze
    5. Click "Run Analysis" to generate the report
    
    The visualizations help identify patterns that might not be obvious in daily logs, making it easier to adjust nutrition plans for better outcomes.
    """) 