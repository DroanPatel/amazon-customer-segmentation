import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# LOAD DATASET
df = pd.read_csv(
    "OnlineRetail.csv",
    encoding='ISO-8859-1',
    low_memory=False
)

# DISPLAY BASIC INFORMATION
print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

# DATA CLEANING
# Remove missing Customer IDs
df = df.dropna(subset=['CustomerID'])

# Remove missing Descriptions
df = df.dropna(subset=['Description'])

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(
    df['InvoiceDate'],
    format='mixed',
    dayfirst=True
)

# Remove negative Quantity and UnitPrice values
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Create Revenue column
df['Revenue'] = df['Quantity'] * df['UnitPrice']

# BASIC KPIs
total_revenue = round(df['Revenue'].sum(), 2)
total_customers = df['CustomerID'].nunique()
total_orders = df['InvoiceNo'].nunique()

print("\n===== BASIC KPIs =====")
print("Total Revenue:", total_revenue)
print("Total Customers:", total_customers)
print("Total Orders:", total_orders)

# TOP 10 COUNTRIES BY REVENUE
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

# MONTHLY REVENUE TREND
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

# TOP 10 CUSTOMERS BY REVENUE
top_customers = (
    df.groupby('CustomerID')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 CUSTOMERS BY REVENUE =====")
print(top_customers)

# TOP 10 PRODUCTS BY REVENUE
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

# REVENUE DISTRIBUTION
plt.figure(figsize=(8,5))

plt.hist(df['Revenue'], bins=50)

plt.title("Revenue Distribution")
plt.xlabel("Revenue")
plt.ylabel("Frequency")

plt.savefig("revenue_distribution.png")

plt.show()

# RFM ANALYSIS
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'Revenue': 'sum'
})

# Rename columns
rfm.columns = ['Recency', 'Frequency', 'Monetary']

print("\n===== RFM ANALYSIS =====")
print(rfm.head())

# K-MEANS CLUSTERING
# Select RFM Features
rfm_data = rfm[['Recency', 'Frequency', 'Monetary']]

# Scale Data
scaler = StandardScaler()

rfm_scaled = scaler.fit_transform(rfm_data)

# Apply K-Means
kmeans = KMeans(
    n_clusters=4,
    random_state=42
)

rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

# CLUSTER RESULTS
print("\n===== CUSTOMER SEGMENTS =====")
print(rfm['Cluster'].value_counts())

cluster_summary = rfm.groupby('Cluster').mean()

print("\n===== CLUSTER SUMMARY =====")
print(cluster_summary)

# CUSTOMER SEGMENTATION VISUALIZATION
plt.figure(figsize=(8,5))

scatter = plt.scatter(
    rfm['Frequency'],
    rfm['Monetary'],
    c=rfm['Cluster']
)

plt.title("Customer Segmentation using K-Means")
plt.xlabel("Frequency")
plt.ylabel("Monetary")

plt.savefig("customer_segmentation_clusters.png")

plt.show()
