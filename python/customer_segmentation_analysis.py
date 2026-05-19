import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Dataset
df = pd.read_csv(
    "OnlineRetail.csv",
    encoding='ISO-8859-1',
    low_memory=False
)

# Display first 5 rows
print("\nFirst 5 Rows:")
print(df.head())

# Dataset Information
print("\nDataset Info:")
print(df.info())

# Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove missing Customer IDs
df = df.dropna(subset=['CustomerID'])

# Remove rows with missing descriptions
df = df.dropna(subset=['Description'])

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(
    df['InvoiceDate'],
    format='mixed',
    dayfirst=True
)

# Create Revenue Column
df['Revenue'] = df['Quantity'] * df['UnitPrice']

# Remove negative quantities and prices
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Basic KPIs
total_revenue = round(df['Revenue'].sum(), 2)
total_customers = df['CustomerID'].nunique()
total_orders = df['InvoiceNo'].nunique()

print("\nBasic KPIs")
print("Total Revenue:", total_revenue)
print("Total Customers:", total_customers)
print("Total Orders:", total_orders)

# Top 10 Countries by Revenue
top_countries = (
    df.groupby('Country')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,5))
top_countries.plot(kind='bar')

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Country")
plt.ylabel("Revenue")

plt.savefig("top_countries_revenue.png")

plt.show()

# Monthly Revenue Trend
df['Month'] = df['InvoiceDate'].dt.month

monthly_sales = (
    df.groupby('Month')['Revenue']
    .sum()
)

plt.figure(figsize=(10,5))
monthly_sales.plot(marker='o')

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.savefig("monthly_revenue_trend.png")

plt.show()

# Top 10 Customers by Revenue
top_customers = (
    df.groupby('CustomerID')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Customers by Revenue")
print(top_customers)

# RFM Analysis
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'Revenue': 'sum'
})

# Rename Columns
rfm.columns = ['Recency', 'Frequency', 'Monetary']

print("\nRFM Analysis")
print(rfm.head())

# Top 10 Products by Revenue
top_products = (
    df.groupby('Description')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,5))
top_products.plot(kind='bar')

plt.title("Top 10 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")

plt.savefig("top_products_revenue.png")

plt.show()

# Revenue Distribution
plt.figure(figsize=(8,5))

plt.hist(df['Revenue'], bins=50)

plt.title("Revenue Distribution")
plt.xlabel("Revenue")
plt.ylabel("Frequency")

plt.savefig("revenue_distribution.png")

plt.show()

print("\nAnalysis Completed Successfully")
