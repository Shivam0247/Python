import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from matplotlib import cm  # Ensure proper import

# Load the dataset from the Excel file
input_file = r'C:\Data\workspace\Advance Python\Practical 8\Online Retail.xlsx'
df = pd.read_excel(input_file)

# Data Cleaning: Check for missing values and duplicates
missing_values = df.isnull().sum()
duplicates = df.duplicated().sum()
print(f"Missing values:\n{missing_values}")
print(f"Number of duplicate rows: {duplicates}")

df = df.drop_duplicates()
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
print(df.describe())

# Calculate the total amount for each sale
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# Group by CustomerID to get total items purchased per customer
df['TotalItemsPurchased'] = df.groupby('CustomerID')['Quantity'].transform('sum')

# Calculate total amount spent by each customer
df['TotalAmountSpent'] = df.groupby('CustomerID')['TotalAmount'].transform('sum')

# Keep only CustomerID, TotalItemsPurchased, and TotalAmountSpent for clustering
result_df = df[['CustomerID', 'TotalItemsPurchased', 'TotalAmountSpent']].drop_duplicates()
print(result_df)

# Normalize the features
scaler = StandardScaler()
scaled_data = scaler.fit_transform(result_df[['TotalItemsPurchased', 'TotalAmountSpent']])

# Determine the optimal number of clusters using the Elbow Method
inertia = []
k_values = range(1, 11)
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

# Plot the elbow curve
plt.figure(figsize=(8, 5))
plt.plot(k_values, inertia, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.show()

# Based on the elbow curve, choose the optimal number of clusters (e.g., 3)
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
result_df['Cluster'] = kmeans.fit_predict(scaled_data)

# Display the customers with their assigned cluster
print(result_df.head())

# Analyze the clusters by looking at their means
cluster_summary = result_df.groupby('Cluster').mean().reset_index()
print(cluster_summary)

# ================= Visualization Code ===================

# Scatter plot of Customer Segments based on TotalItemsPurchased and TotalAmountSpent
plt.figure(figsize=(10, 6))
plt.scatter(result_df['TotalItemsPurchased'], result_df['TotalAmountSpent'], c=result_df['Cluster'], cmap='viridis', alpha=0.6)
plt.title('Customer Segments: Total Items Purchased vs. Total Amount Spent')
plt.xlabel('Total Items Purchased')
plt.ylabel('Total Amount Spent')
plt.colorbar(label='Cluster')
plt.show()

# Bar chart of average TotalItemsPurchased and TotalAmountSpent for each segment
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Bar chart for Total Items Purchased
sns.barplot(x='Cluster', y='TotalItemsPurchased', data=cluster_summary, ax=ax[0], palette='viridis')
ax[0].set_title('Average Total Items Purchased per Segment')
ax[0].set_xlabel('Cluster')
ax[0].set_ylabel('Average Items Purchased')

# Bar chart for Total Amount Spent
sns.barplot(x='Cluster', y='TotalAmountSpent', data=cluster_summary, ax=ax[1], palette='viridis')
ax[1].set_title('Average Total Amount Spent per Segment')
ax[1].set_xlabel('Cluster')
ax[1].set_ylabel('Average Amount Spent')

plt.tight_layout()
plt.show()

# Pie chart to represent the proportion of customers in each cluster
cluster_counts = result_df['Cluster'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(cluster_counts, labels=[f'Cluster {i}' for i in range(optimal_k)], autopct='%1.1f%%', colors=sns.color_palette('viridis', n_colors=optimal_k))
plt.title('Customer Distribution by Cluster')
plt.show()
