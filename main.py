from faker import Faker
import pandas as pd
import random
import streamlit as st


fake = Faker()

# Define product categories and example products
product_categories = {
    'Infrastructure': ['Server', 'Storage', 'Network Device', 'Cloud Service'],
    'Enterprise': ['Hyperconverged System', 'Cloud Platform', 'Security Service', 'App Modernization Service'],
    'Consumer': ['Laptop', 'Desktop', 'Monitor', 'Gaming System']
}

# Generate fake data
def generate_data(num_records):
    data = []
    for _ in range(num_records):
        category = random.choice(list(product_categories.keys()))
        product = random.choice(product_categories[category])
        data.append({
            'Name': fake.name(),
            'Address': fake.address(),
            'Email': fake.email(),
            'Product Category': category,
            'Product Name': product,
            'Purchase Date': fake.date_between(start_date='-2y', end_date='today'),
            'Quantity': random.randint(1, 5),
            'Price': random.uniform(100, 10000),
            'Warranty Start': fake.date_between(start_date='-1y', end_date='today'),
            'Warranty End': fake.date_between(start_date='today', end_date='+3y'),
            'Service Type': random.choice(['Standard', 'Extended']),
            'For Government': random.choice([True, False])
        })
    return pd.DataFrame(data)

# Generate 100 records
customer_data = generate_data(100)


customer_data.to_csv('/Users/melissahuff/PycharmProjects/FinalProjectMelissaHuff/customer_data.csv', index=False)


