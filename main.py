import streamlit as st
import pandas as pd
from faker import Faker
import random
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Federal vs Non-Federal Sales Analysis", layout="wide", initial_sidebar_state="expanded")

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
</style>
""", unsafe_allow_html=True)

# Faker setup for data generation
fake = Faker()
us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
             'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
             'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
             'VA', 'WA', 'WV', 'WI', 'WY']
product_categories = ['Server', 'Storage', 'Network Device', 'Cloud Service', 'Laptop', 'Desktop', 'Monitor', 'Gaming System']

def generate_data(num_records):
    data = []
    for _ in range(num_records):
        state = random.choice(us_states)
        product = random.choice(product_categories)
        sector_choice = random.choice(['Federal', 'Non-Federal'])
        data.append({
            'State': state,
            'Product': product,
            'Sales': random.uniform(10000, 100000),
            'Sector': sector_choice,
            'Year': random.randint(2010, 2022)
        })
    return pd.DataFrame(data)

# Generate and load data
customer_data = generate_data(1000)

# Sidebar for filtering by year
with st.sidebar:
    st.title("Filter Options")
    years = sorted(customer_data['Year'].unique())
    selected_year = st.selectbox("Select Year", years)
    data_filtered = customer_data[customer_data['Year'] == selected_year]

# Main dashboard layout
st.title("Federal vs Non-Federal Sales Distribution")

# Main visualization - Choropleth Map in the center
col1, col2, col3 = st.columns([1, 3, 1])
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

with col3:
    st.subheader("Sales Metrics")
    total_sales = data_filtered['Sales'].sum()
    fed_sales = data_filtered[data_filtered['Sector'] == 'Federal']['Sales'].sum()
    non_fed_sales = data_filtered[data_filtered['Sector'] == 'Non-Federal']['Sales'].sum()

    # Display metrics
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Federal Sales", f"${fed_sales:,.2f}")
    st.metric("Non-Federal Sales", f"${non_fed_sales:,.2f}")


