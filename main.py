import streamlit as st
import pandas as pd
from faker import Faker
import random
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="TechTrend Analytics Federal vs Non-Federal Sales Analysis", layout="wide", initial_sidebar_state="expanded")

# CSS for styling
st.markdown("""
<style>
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}
[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}
[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}
[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}
[data-testid="stMetricDeltaIcon-Up"], [data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    transform: translateX(-50%);
}
.gray-box {
    background-color: #333;  /* Dark gray background */
    color: #fff;  /* White text */
    padding: 10px;
    border-radius: 5px;
    margin-top: 5px;  /* Reduced margin to bring closer to the donut chart */
}
</style>
""", unsafe_allow_html=True)

# Faker setup for data generation
fake = Faker()
us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
             'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
             'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
             'VA', 'WA', 'WV', 'WI', 'WY']
product_categories = {
    'Enterprise': ['Data Center', 'Cloud Solutions', 'Enterprise Software'],
    'Infrastructure': ['Storage', 'Network Device', 'Servers'],
    'Client': ['Laptops', 'Desktops', 'Monitors', 'Printers']
}
lines_of_business = ['All', 'Enterprise', 'Infrastructure', 'Client']

def generate_data(num_records):
    data = []
    for _ in range(num_records):
        line_of_business = random.choice(lines_of_business[1:])  # Exclude 'All' from data generation
        product = random.choice(product_categories[line_of_business])
        state = random.choice(us_states)
        sector_choice = random.choice(['Federal', 'Non-Federal'])
        data.append({
            'State': state,
            'Product': product,
            'Sales': random.uniform(10000, 100000),
            'Sector': sector_choice,
            'Line of Business': line_of_business,
            'Year': random.randint(2010, 2022)
        })
    return pd.DataFrame(data)

# Generate and load data
customer_data = generate_data(1000)

# Sidebar for filtering
with st.sidebar:
    st.title("Dashboard Overview")
    st.text("""
        Welcome to the TechTrend Analytics Dashboard! 

        Features:
        - Displays sales across the USA, highlighting regional market trends.
        - Analyzes performance by product category.
        - Compares federal vs. non-federal sales, showcasing our government engagement.

        Use the filters to customize the data for detailed analysis and strategic planning. 
    """)

    years = sorted(customer_data['Year'].unique())
    selected_year = st.selectbox("Select Year", years)
    selected_lines = st.multiselect("Select Line of Business", lines_of_business, default=['All'])
    if 'All' in selected_lines:
        data_filtered = customer_data[customer_data['Year'] == selected_year]
    else:
        data_filtered = customer_data[(customer_data['Year'] == selected_year) & (customer_data['Line of Business'].isin(selected_lines))]

# Main dashboard layout
st.title("TechTrend Analytics - Federal vs Non-Federal Sales Distribution")

# Main visualization - Choropleth Map in the center
col1, col2, col3 = st.columns([1, 4, 2])
with col2:
    st.subheader("Sales Distribution Across the USA")
    state_sales = data_filtered.groupby('State')['Sales'].sum().reset_index()
    fig_map = px.choropleth(
        state_sales,
        locations='State',
        locationmode='USA-states',
        color='Sales',
        color_continuous_scale='Blues',
        scope='usa',
        labels={'Sales': 'Total Sales'},
        title='Total Sales per State'
    )
    fig_map.update_geos(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)')
    fig_map.update_layout(margin={"r":0, "t":0, "l":0, "b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

# Product distribution bar chart
with col1:
    st.subheader("Product Sales Distribution")
    product_sales = data_filtered.groupby('Product')['Sales'].sum().reset_index()
    fig_product = px.bar(
        product_sales,
        x='Sales',
        y='Product',
        orientation='h',
        title='Sales by Product Category'
    )
    st.plotly_chart(fig_product, use_container_width=True)

# Sales Metrics - Donut chart with total sales annotation
with col3:
    st.subheader("Sales Metrics")
    sales_data = {
        'Federal Sales': data_filtered[data_filtered['Sector'] == 'Federal']['Sales'].sum(),
        'Non-Federal Sales': data_filtered[data_filtered['Sector'] == 'Non-Federal']['Sales'].sum()
    }
    total_sales = sum(sales_data.values())
    fig_donut = go.Figure(data=[go.Pie(labels=list(sales_data.keys()), values=list(sales_data.values()), hole=.5)])
    fig_donut.update_layout(
        title_text="Sales Distribution"
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    # Display total sales below the donut chart in a styled dark gray box
    st.markdown(f"<div class='gray-box'>Total Sales: ${total_sales:,.2f}</div>", unsafe_allow_html=True)
