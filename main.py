# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from faker import Faker
import random

# Set page configuration
st.set_page_config(page_title="Federal vs Non-Federal Sales Analysis", layout="wide", initial_sidebar_state="expanded")

# Faker setup for data generation
fake = Faker()

# Define product categories and example products
product_categories = {
    'Infrastructure': ['Server', 'Storage', 'Network Device', 'Cloud Service'],
    'Enterprise': ['Hyperconverged System', 'Cloud Platform', 'Security Service', 'App Modernization Service'],
    'Consumer': ['Laptop', 'Desktop', 'Monitor', 'Gaming System']
}

# Define U.S. states for sales mapping
us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
             'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
             'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
             'VA', 'WA', 'WV', 'WI', 'WY']

@st.cache_data
def generate_data(num_records):
    data = []
    for _ in range(num_records):
        state = random.choice(us_states)
        category = random.choice(list(product_categories.keys()))
        product = random.choice(product_categories[category])
        sector_choice = random.choice(['Federal', 'Non-Federal'])
        data.append({
            'Customer Name': fake.company(),
            'State': state,
            'Email': fake.email(),
            'Product Category': category,
            'Product Name': product,
            'Purchase Date': fake.date_between(start_date='-2y', end_date='today').isoformat(),
            'ASUs': random.randint(1, 10),
            'Price': random.uniform(10000, 100000),
            'Warranty Start': fake.date_between(start_date='-1y', end_date='today').isoformat(),
            'Warranty End': fake.date_between(start_date='today', end_date='+3y').isoformat(),
            'Service Type': random.choice(['Standard', 'Extended']),
            'Sector': sector_choice
        })
    return pd.DataFrame(data)

# Generate and load data
customer_data = generate_data(500)
customer_data['Purchase Date'] = pd.to_datetime(customer_data['Purchase Date'])

# Sidebar for filtering by sector
with st.sidebar:
    st.title('Sales Dashboard')
    sector_options = ['Federal', 'Non-Federal', 'Both']
    selected_sector = st.selectbox('Select Sector', sector_options)
    if selected_sector != 'Both':
        filtered_data = customer_data[customer_data['Sector'] == selected_sector]
    else:
        filtered_data = customer_data

# Dashboard Main Panel
col1, col2, col3 = st.columns(3)
with col1:
    # Choropleth map showing sales distribution by state
    state_sales = filtered_data.groupby('State')['Price'].sum().reset_index()
    choropleth_fig = px.choropleth(
        state_sales,
        locations='State',
        locationmode='USA-states',
        color='Price',
        color_continuous_scale='Blues',
        scope='usa',
        labels={'Price': 'Total Sales'},
        title='Sales Distribution Across the USA'
    )
    choropleth_fig.update_layout(margin={"r":0, "t":30, "l":0, "b":0})
    st.plotly_chart(choropleth_fig, use_container_width=True)

with col2:
    # Line Chart for Sales Over Time
    monthly_sales = filtered_data.groupby(filtered_data['Purchase Date'].dt.to_period("M"))['Price'].sum().reset_index()
    monthly_sales['Month'] = monthly_sales['Purchase Date'].dt.strftime('%Y-%m')
    line_fig = px.line(
        monthly_sales,
        x='Month',
        y='Price',
        title='Monthly Sales Trends'
    )
    st.plotly_chart(line_fig, use_container_width=True)

    with col3:
        # Bar Chart for Sales Distribution by Product Category
        category_sales = filtered_data.groupby('Product Category')['Price'].sum().reset_index()
        bar_fig = px.bar(
            category_sales,
            x='Product Category',
            y='Price',
            title='Sales Distribution by Product Category'
        )
        st.plotly_chart(bar_fig, use_container_width=True)
