# %% [markdown]
# # 🛒 Shopper Spectrum: Customer Segmentation and Product Recommendations
# ## E-Commerce Analytics Project
# 
# **Author**: Data Science Team  
# **Date**: 2024  
# **Objective**: Customer Segmentation using RFM Analysis & Product Recommendation System

# %% [markdown]
# ## 📚 Step 1: Import Libraries and Load Dataset

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("✅ Libraries imported successfully!")

# %%
# Load the dataset
df = pd.read_csv('online_retail.csv', encoding='ISO-8859-1')
print(f"📊 Dataset loaded successfully!")
print(f"Shape: {df.shape}")
print("\n" + "="*80)
print("Dataset Info:")
print("="*80)
df.info()

# %%
print("\n" + "="*80)
print("First 10 rows of the dataset:")
print("="*80)
df.head(10)

# %%
print("\n" + "="*80)
print("Statistical Summary:")
print("="*80)
df.describe()

# %% [markdown]
# ## 🧹 Step 2: Data Preprocessing and Cleaning

# %%
print("\n" + "="*80)
print("Missing Values Analysis:")
print("="*80)
missing_values = df.isnull().sum()
missing_percent = (missing_values / len(df)) * 100
missing_df = pd.DataFrame({
    'Column': missing_values.index,
    'Missing Count': missing_values.values,
    'Percentage': missing_percent.values
})
print(missing_df[missing_df['Missing Count'] > 0])

# %%
# Data Cleaning Steps
print("\n" + "="*80)
print("Data Cleaning Process:")
print("="*80)

initial_rows = len(df)
print(f"Initial number of rows: {initial_rows:,}")

# 1. Remove rows with missing CustomerID
df_clean = df[df['CustomerID'].notna()].copy()
print(f"✅ After removing missing CustomerID: {len(df_clean):,} rows ({len(df_clean)/initial_rows*100:.2f}%)")

# 2. Convert CustomerID to integer
df_clean['CustomerID'] = df_clean['CustomerID'].astype(int)

# 3. Remove cancelled invoices (starting with 'C')
df_clean = df_clean[~df_clean['InvoiceNo'].astype(str).str.startswith('C')]
print(f"✅ After removing cancelled invoices: {len(df_clean):,} rows ({len(df_clean)/initial_rows*100:.2f}%)")

# 4. Remove negative or zero quantities and prices
df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['UnitPrice'] > 0)]
print(f"✅ After removing invalid quantities/prices: {len(df_clean):,} rows ({len(df_clean)/initial_rows*100:.2f}%)")

# 5. Convert InvoiceDate to datetime
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])

# 6. Create TotalAmount column
df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['UnitPrice']

print(f"\n✅ Final cleaned dataset: {len(df_clean):,} rows")
print(f"✅ Percentage retained: {len(df_clean)/initial_rows*100:.2f}%")

# %%
print("\n" + "="*80)
print("Cleaned Dataset Summary:")
print("="*80)
print(df_clean.head())

# %% [markdown]
# ## 📊 Step 3: Exploratory Data Analysis (EDA)

# %%
# EDA 1: Transaction Volume by Country
print("\n" + "="*80)
print("Top 10 Countries by Transaction Volume:")
print("="*80)

country_stats = df_clean.groupby('Country').agg({
    'InvoiceNo': 'nunique',
    'CustomerID': 'nunique',
    'TotalAmount': 'sum'
}).sort_values('InvoiceNo', ascending=False).head(10)

country_stats.columns = ['Transactions', 'Customers', 'Revenue']
print(country_stats)

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
top_countries = df_clean['Country'].value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis')
plt.title('Top 10 Countries by Transaction Count', fontsize=14, fontweight='bold')
plt.xlabel('Number of Transactions')
plt.ylabel('Country')

plt.subplot(1, 2, 2)
country_revenue = df_clean.groupby('Country')['TotalAmount'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=country_revenue.values, y=country_revenue.index, palette='plasma')
plt.title('Top 10 Countries by Revenue', fontsize=14, fontweight='bold')
plt.xlabel('Total Revenue (£)')
plt.ylabel('Country')

plt.tight_layout()
plt.savefig('eda_countries.png', dpi=300, bbox_inches='tight')
plt.show()

# %%
# EDA 2: Top-Selling Products
print("\n" + "="*80)
print("Top 20 Best-Selling Products:")
print("="*80)

product_stats = df_clean.groupby('Description').agg({
    'Quantity': 'sum',
    'InvoiceNo': 'nunique',
    'TotalAmount': 'sum'
}).sort_values('Quantity', ascending=False).head(20)

product_stats.columns = ['Total Quantity', 'Transactions', 'Revenue']
print(product_stats)

plt.figure(figsize=(12, 8))
top_products = df_clean.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(15)
sns.barplot(y=top_products.index, x=top_products.values, palette='coolwarm')
plt.title('Top 15 Best-Selling Products', fontsize=14, fontweight='bold')
plt.xlabel('Total Quantity Sold')
plt.ylabel('Product Description')
plt.tight_layout()
plt.savefig('eda_products.png', dpi=300, bbox_inches='tight')
plt.show()

# %%
# EDA 3: Purchase Trends Over Time
print("\n" + "="*80)
print("Analyzing Purchase Trends Over Time...")
print("="*80)

df_clean['Year'] = df_clean['InvoiceDate'].dt.year
df_clean['Month'] = df_clean['InvoiceDate'].dt.month
df_clean['YearMonth'] = df_clean['InvoiceDate'].dt.to_period('M')

monthly_sales = df_clean.groupby('YearMonth').agg({
    'InvoiceNo': 'nunique',
    'TotalAmount': 'sum'
}).reset_index()

monthly_sales['YearMonth'] = monthly_sales['YearMonth'].astype(str)

fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Transactions over time
axes[0].plot(monthly_sales['YearMonth'], monthly_sales['InvoiceNo'], 
             marker='o', linewidth=2, markersize=8, color='#2E86AB')
axes[0].set_title('Monthly Transaction Volume', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Number of Transactions')
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# Revenue over time
axes[1].plot(monthly_sales['YearMonth'], monthly_sales['TotalAmount'], 
             marker='s', linewidth=2, markersize=8, color='#A23B72')
axes[1].set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Total Revenue (£)')
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('eda_trends.png', dpi=300, bbox_inches='tight')
plt.show()

# %%
# EDA 4: Monetary Distribution
print("\n" + "="*80)
print("Customer Monetary Distribution Analysis:")
print("="*80)

customer_monetary = df_clean.groupby('CustomerID')['TotalAmount'].sum()
print(f"Average customer spending: £{customer_monetary.mean():.2f}")
print(f"Median customer spending: £{customer_monetary.median():.2f}")
print(f"Maximum customer spending: £{customer_monetary.max():.2f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(customer_monetary, bins=50, edgecolor='black', color='skyblue')
axes[0].set_title('Distribution of Customer Spending', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Total Spending (£)')
axes[0].set_ylabel('Number of Customers')
axes[0].axvline(customer_monetary.mean(), color='red', linestyle='--', label=f'Mean: £{customer_monetary.mean():.2f}')
axes[0].axvline(customer_monetary.median(), color='green', linestyle='--', label=f'Median: £{customer_monetary.median():.2f}')
axes[0].legend()

axes[1].boxplot(customer_monetary, vert=True)
axes[1].set_title('Customer Spending Boxplot', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Total Spending (£)')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('eda_monetary.png', dpi=300, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 🎯 Step 4: RFM Analysis & Feature Engineering

# %%
print("\n" + "="*80)
print("RFM Analysis - Feature Engineering:")
print("="*80)

# Get reference date (latest date in dataset + 1 day)
reference_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)
print(f"Reference Date for Recency Calculation: {reference_date}")

# Calculate RFM metrics for each customer
rfm = df_clean.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (reference_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',  # Frequency
    'TotalAmount': 'sum'  # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

print(f"\n✅ RFM metrics calculated for {len(rfm):,} customers")
print("\nRFM Summary Statistics:")
print(rfm.describe())

# %%
# Visualize RFM Distributions
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Recency
axes[0].hist(rfm['Recency'], bins=50, edgecolor='black', color='#FF6B6B')
axes[0].set_title('Recency Distribution', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Days Since Last Purchase')
axes[0].set_ylabel('Number of Customers')
axes[0].axvline(rfm['Recency'].mean(), color='darkred', linestyle='--', linewidth=2)

# Frequency
axes[1].hist(rfm['Frequency'], bins=50, edgecolor='black', color='#4ECDC4')
axes[1].set_title('Frequency Distribution', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Number of Purchases')
axes[1].set_ylabel('Number of Customers')
axes[1].axvline(rfm['Frequency'].mean(), color='darkblue', linestyle='--', linewidth=2)

# Monetary
axes[2].hist(rfm['Monetary'], bins=50, edgecolor='black', color='#95E1D3')
axes[2].set_title('Monetary Distribution', fontsize=14, fontweight='bold')
axes[2].set_xlabel('Total Spending (£)')
axes[2].set_ylabel('Number of Customers')
axes[2].axvline(rfm['Monetary'].mean(), color='darkgreen', linestyle='--', linewidth=2)

plt.tight_layout()
plt.savefig('rfm_distributions.png', dpi=300, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 🔧 Step 5: Data Normalization for Clustering

# %%
print("\n" + "="*80)
print("Normalizing RFM Features for Clustering:")
print("="*80)

# Standardize RFM values
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

print("✅ RFM features normalized using StandardScaler")
print(f"Shape of scaled data: {rfm_scaled.shape}")

# Create DataFrame with scaled features
rfm_scaled_df = pd.DataFrame(rfm_scaled, columns=['Recency_Scaled', 'Frequency_Scaled', 'Monetary_Scaled'])
print("\nScaled RFM Sample:")
print(rfm_scaled_df.head())

# %% [markdown]
# ## 📈 Step 6: Determining Optimal Number of Clusters

# %%
print("\n" + "="*80)
print("Finding Optimal Number of Clusters:")
print("="*80)

# Elbow Method
inertias = []
silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(rfm_scaled, kmeans.labels_))
    print(f"K={k}: Inertia={kmeans.inertia_:.2f}, Silhouette Score={silhouette_scores[-1]:.4f}")

# Plot Elbow Curve and Silhouette Scores
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Elbow curve
axes[0].plot(K_range, inertias, marker='o', linewidth=2, markersize=10, color='#E63946')
axes[0].set_title('Elbow Method for Optimal K', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Number of Clusters (K)')
axes[0].set_ylabel('Inertia (Within-Cluster Sum of Squares)')
axes[0].grid(True, alpha=0.3)

# Silhouette scores
axes[1].plot(K_range, silhouette_scores, marker='s', linewidth=2, markersize=10, color='#457B9D')
axes[1].set_title('Silhouette Score for Different K', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Number of Clusters (K)')
axes[1].set_ylabel('Silhouette Score')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('elbow_silhouette.png', dpi=300, bbox_inches='tight')
plt.show()

optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2
print(f"\n🎯 Optimal number of clusters based on Silhouette Score: {optimal_k}")

# %% [markdown]
# ## 🎪 Step 7: K-Means Clustering

# %%
print("\n" + "="*80)
print(f"Running K-Means Clustering with K={optimal_k}:")
print("="*80)

# Train final K-Means model
kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
rfm['Cluster'] = kmeans_final.fit_predict(rfm_scaled)

print(f"✅ Clustering completed!")
print(f"✅ Final Silhouette Score: {silhouette_score(rfm_scaled, rfm['Cluster']):.4f}")

# Cluster distribution
print("\nCluster Distribution:")
print(rfm['Cluster'].value_counts().sort_index())

# %% [markdown]
# ## 🏷️ Step 8: Cluster Interpretation & Labeling

# %%
print("\n" + "="*80)
print("Cluster Analysis & Interpretation:")
print("="*80)

# Analyze cluster characteristics
cluster_summary = rfm.groupby('Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean',
    'CustomerID': 'count'
}).round(2)

cluster_summary.columns = ['Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Customer_Count']
print(cluster_summary)

# Assign labels based on RFM characteristics
def assign_label(row):
    if row['Avg_Recency'] < rfm['Recency'].quantile(0.33) and row['Avg_Frequency'] > rfm['Frequency'].quantile(0.67) and row['Avg_Monetary'] > rfm['Monetary'].quantile(0.67):
        return 'High-Value'
    elif row['Avg_Frequency'] >= rfm['Frequency'].quantile(0.33) and row['Avg_Monetary'] >= rfm['Monetary'].quantile(0.33):
        return 'Regular'
    elif row['Avg_Recency'] > rfm['Recency'].quantile(0.67):
        return 'At-Risk'
    else:
        return 'Occasional'

cluster_summary['Segment'] = cluster_summary.apply(assign_label, axis=1)
print("\n" + "="*80)
print("Cluster Segments:")
print("="*80)
print(cluster_summary)

# Map labels back to RFM dataframe
cluster_label_map = cluster_summary['Segment'].to_dict()
rfm['Segment'] = rfm['Cluster'].map(cluster_label_map)

# %%
# Visualize Clusters
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(14, 10))

# 3D Scatter Plot
ax = fig.add_subplot(111, projection='3d')

colors = ['#E63946', '#F1C40F', '#457B9D', '#2A9D8F']
for cluster in rfm['Cluster'].unique():
    cluster_data = rfm[rfm['Cluster'] == cluster]
    ax.scatter(cluster_data['Recency'], cluster_data['Frequency'], cluster_data['Monetary'],
               c=colors[cluster], label=f"Cluster {cluster}: {cluster_label_map[cluster]}", 
               s=50, alpha=0.6, edgecolors='black')

ax.set_xlabel('Recency (Days)', fontsize=12, fontweight='bold')
ax.set_ylabel('Frequency (Purchases)', fontsize=12, fontweight='bold')
ax.set_zlabel('Monetary (£)', fontsize=12, fontweight='bold')
ax.set_title('Customer Segmentation - 3D Visualization', fontsize=14, fontweight='bold')
ax.legend()

plt.savefig('cluster_3d.png', dpi=300, bbox_inches='tight')
plt.show()

# %%
# 2D Visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Recency vs Frequency
for cluster in rfm['Cluster'].unique():
    cluster_data = rfm[rfm['Cluster'] == cluster]
    axes[0, 0].scatter(cluster_data['Recency'], cluster_data['Frequency'],
                       c=colors[cluster], label=cluster_label_map[cluster], 
                       s=50, alpha=0.6, edgecolors='black')
axes[0, 0].set_xlabel('Recency (Days)', fontweight='bold')
axes[0, 0].set_ylabel('Frequency (Purchases)', fontweight='bold')
axes[0, 0].set_title('Recency vs Frequency', fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Recency vs Monetary
for cluster in rfm['Cluster'].unique():
    cluster_data = rfm[rfm['Cluster'] == cluster]
    axes[0, 1].scatter(cluster_data['Recency'], cluster_data['Monetary'],
                       c=colors[cluster], label=cluster_label_map[cluster], 
                       s=50, alpha=0.6, edgecolors='black')
axes[0, 1].set_xlabel('Recency (Days)', fontweight='bold')
axes[0, 1].set_ylabel('Monetary (£)', fontweight='bold')
axes[0, 1].set_title('Recency vs Monetary', fontweight='bold')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Frequency vs Monetary
for cluster in rfm['Cluster'].unique():
    cluster_data = rfm[rfm['Cluster'] == cluster]
    axes[1, 0].scatter(cluster_data['Frequency'], cluster_data['Monetary'],
                       c=colors[cluster], label=cluster_label_map[cluster], 
                       s=50, alpha=0.6, edgecolors='black')
axes[1, 0].set_xlabel('Frequency (Purchases)', fontweight='bold')
axes[1, 0].set_ylabel('Monetary (£)', fontweight='bold')
axes[1, 0].set_title('Frequency vs Monetary', fontweight='bold')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Cluster Distribution
segment_counts = rfm['Segment'].value_counts()
axes[1, 1].pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%',
               colors=colors, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
axes[1, 1].set_title('Customer Segment Distribution', fontweight='bold')

plt.tight_layout()
plt.savefig('cluster_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 🎁 Step 9: Product Recommendation System (Collaborative Filtering)

# %%
print("\n" + "="*80)
print("Building Product Recommendation System:")
print("="*80)

# Create Customer-Product matrix
customer_product = df_clean.groupby(['CustomerID', 'Description'])['Quantity'].sum().unstack(fill_value=0)

print(f"✅ Customer-Product matrix created")
print(f"Shape: {customer_product.shape}")
print(f"Customers: {customer_product.shape[0]:,}")
print(f"Unique Products: {customer_product.shape[1]:,}")

# Calculate item-based cosine similarity
product_similarity = cosine_similarity(customer_product.T)
product_similarity_df = pd.DataFrame(product_similarity, 
                                     index=customer_product.columns,
                                     columns=customer_product.columns)

print(f"\n✅ Product similarity matrix computed using Cosine Similarity")
print(f"Matrix shape: {product_similarity_df.shape}")

# %%
# Create recommendation function
def get_product_recommendations(product_name, top_n=5):
    """
    Get top N similar products for a given product
    """
    try:
        if product_name not in product_similarity_df.index:
            return None
        
        similar_products = product_similarity_df[product_name].sort_values(ascending=False)[1:top_n+1]
        return similar_products
    except:
        return None

# Test recommendations
test_product = df_clean['Description'].value_counts().index[0]
print(f"\n📦 Testing Recommendations for: '{test_product}'")
print("="*80)

recommendations = get_product_recommendations(test_product, top_n=5)
if recommendations is not None:
    for idx, (product, similarity) in enumerate(recommendations.items(), 1):
        print(f"{idx}. {product} (Similarity: {similarity:.4f})")

# %% [markdown]
# ## 💾 Step 10: Save Models and Artifacts

# %%
print("\n" + "="*80)
print("Saving Models and Artifacts:")
print("="*80)

# Create models directory
os.makedirs('models', exist_ok=True)

# Save K-Means model
joblib.dump(kmeans_final, 'models/kmeans_model.pkl')
print("✅ K-Means model saved: models/kmeans_model.pkl")

# Save StandardScaler
joblib.dump(scaler, 'models/scaler.pkl')
print("✅ StandardScaler saved: models/scaler.pkl")

# Save product similarity matrix
joblib.dump(product_similarity_df, 'models/product_similarity.pkl')
print("✅ Product similarity matrix saved: models/product_similarity.pkl")

# Save cluster label mapping
joblib.dump(cluster_label_map, 'models/cluster_labels.pkl')
print("✅ Cluster labels saved: models/cluster_labels.pkl")

# Save RFM data with clusters
rfm.to_csv('models/rfm_data.csv', index=False)
print("✅ RFM data with clusters saved: models/rfm_data.csv")

print("\n🎉 All models and artifacts saved successfully!")

# %% [markdown]
# ## 📊 Step 11: Final Summary & Model Evaluation

# %%
print("\n" + "="*80)
print("PROJECT SUMMARY:")
print("="*80)

print("\n📊 Dataset Statistics:")
print(f"  • Initial Records: {initial_rows:,}")
print(f"  • Cleaned Records: {len(df_clean):,}")
print(f"  • Unique Customers: {df_clean['CustomerID'].nunique():,}")
print(f"  • Unique Products: {df_clean['Description'].nunique():,}")
print(f"  • Countries: {df_clean['Country'].nunique():,}")

print("\n🎯 Clustering Results:")
print(f"  • Optimal Clusters: {optimal_k}")
print(f"  • Silhouette Score: {silhouette_score(rfm_scaled, rfm['Cluster']):.4f}")

print("\n🏷️ Customer Segments:")
for segment, count in rfm['Segment'].value_counts().items():
    percentage = (count / len(rfm)) * 100
    print(f"  • {segment}: {count:,} customers ({percentage:.2f}%)")

print("\n🎁 Recommendation System:")
print(f"  • Products in similarity matrix: {product_similarity_df.shape[0]:,}")
print(f"  • Recommendation accuracy: Cosine Similarity based")

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
print("="*80)

print("\n🚀 Next Steps:")
print("  1. Run the Streamlit app: streamlit run app.py")
print("  2. Test product recommendations")
print("  3. Predict customer segments")
print("\n" + "="*80)
