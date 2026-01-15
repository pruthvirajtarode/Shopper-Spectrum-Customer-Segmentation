import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="Shopper Spectrum | E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CUSTOM CSS FOR PREMIUM STYLING
# ========================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Main Container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: fadeIn 1s ease-in;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    
    /* Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .info-box h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .info-box p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #13b0f5 0%, #2575fc 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(37, 117, 252, 0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    .success-box h2 {
        margin: 0 0 1rem 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Recommendation Cards */
    .rec-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .rec-card:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(252, 182, 159, 0.3);
    }
    
    .rec-card h4 {
        margin: 0 0 0.5rem 0;
        color: #8e2de2;
        font-weight: 600;
    }
    
    .rec-card p {
        margin: 0;
        color: #555;
        font-size: 0.9rem;
    }
    
    /* Segment Badge */
    .segment-badge {
        display: inline-block;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .high-value {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .regular {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .occasional {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
    }
    
    .at-risk {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.2);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Sidebar Title */
    .sidebar-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Sidebar Info */
    .sidebar-info {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .sidebar-info h4 {
        color: white;
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }
    
    .sidebar-info p {
        color: rgba(255, 255, 255, 0.8);
        margin: 0;
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-container {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# LOAD MODELS AND DATA
# ========================================
@st.cache_resource
def load_models():
    """Load all saved models and data"""
    try:
        # Check if models directory exists
        if not os.path.exists('models'):
            return None, None, None, None, None
        
        kmeans_model = joblib.load('models/kmeans_model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        product_similarity = joblib.load('models/product_similarity.pkl')
        cluster_labels = joblib.load('models/cluster_labels.pkl')
        rfm_data = pd.read_csv('models/rfm_data.csv')
        
        return kmeans_model, scaler, product_similarity, cluster_labels, rfm_data
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, None, None, None

# Load models
kmeans_model, scaler, product_similarity, cluster_labels, rfm_data = load_models()

# ========================================
# SIDEBAR
# ========================================
with st.sidebar:
    st.markdown('<p class="sidebar-title">🛒 Navigation</p>', unsafe_allow_html=True)
    
    page = st.radio(
        "",
        ["🏠 Home", "🎁 Product Recommendations", "👥 Customer Segmentation", "📊 Analytics Dashboard"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sidebar-info">
        <h4>📌 About</h4>
        <p>AI-powered e-commerce platform for customer insights and personalized recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-info">
        <h4>🎯 Features</h4>
        <p>• RFM-based Segmentation<br>
        • Collaborative Filtering<br>
        • Real-time Predictions<br>
        • Interactive Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 0.8rem;">
        <p>Built with ❤️ using Streamlit</p>
        <p>© 2024 Shopper Spectrum</p>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# PAGE: HOME
# ========================================
if page == "🏠 Home":
    st.markdown("""
    <div class="main-header">
        <h1>🛒 Shopper Spectrum</h1>
        <p>AI-Powered Customer Segmentation & Product Recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    ## Welcome to Shopper Spectrum! 👋
    
    Your comprehensive e-commerce analytics platform powered by advanced machine learning algorithms.
    Unlock the power of customer insights and personalized recommendations.
    """)
    
    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎁 Product Recommendations</h3>
            <p>Get personalized product suggestions using collaborative filtering. 
            Our AI algorithm analyzes customer purchase patterns to recommend the most relevant products.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Advanced Analytics</h3>
            <p>Explore comprehensive analytics dashboards with interactive visualizations. 
            Gain deep insights into customer behavior and business trends.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>👥 Customer Segmentation</h3>
            <p>Classify customers into strategic segments using RFM analysis. 
            Identify High-Value, Regular, Occasional, and At-Risk customers for targeted marketing.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Real-time Predictions</h3>
            <p>Get instant predictions and recommendations powered by pre-trained machine learning models. 
            Fast, accurate, and scalable for business needs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Statistics
    if rfm_data is not None:
        st.markdown("## 📈 Platform Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <h3>{len(rfm_data):,}</h3>
                <p>Total Customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            high_value = len(rfm_data[rfm_data['Segment'] == 'High-Value']) if 'Segment' in rfm_data.columns else 0
            st.markdown(f"""
            <div class="info-box">
                <h3>{high_value:,}</h3>
                <p>High-Value Customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if product_similarity is not None:
                st.markdown(f"""
                <div class="info-box">
                    <h3>{len(product_similarity):,}</h3>
                    <p>Unique Products</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            avg_monetary = rfm_data['Monetary'].mean() if 'Monetary' in rfm_data.columns else 0
            st.markdown(f"""
            <div class="info-box">
                <h3>£{avg_monetary:.2f}</h3>
                <p>Avg Customer Value</p>
            </div>
            """, unsafe_allow_html=True)
    
    # How it works
    st.markdown("## 🔍 How It Works")
    
    st.markdown("""
    <div class="feature-card">
        <h4>1️⃣ Data Collection & Processing</h4>
        <p>We analyze transaction data from your e-commerce platform, cleaning and preprocessing it for optimal insights.</p>
    </div>
    
    <div class="feature-card">
        <h4>2️⃣ RFM Analysis</h4>
        <p>Calculate Recency, Frequency, and Monetary values for each customer to understand their purchasing behavior.</p>
    </div>
    
    <div class="feature-card">
        <h4>3️⃣ Customer Segmentation</h4>
        <p>Apply K-Means clustering algorithm to group customers into meaningful segments for targeted strategies.</p>
    </div>
    
    <div class="feature-card">
        <h4>4️⃣ Product Recommendations</h4>
        <p>Use collaborative filtering to identify similar products based on customer purchase patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================
# PAGE: PRODUCT RECOMMENDATIONS
# ========================================
elif page == "🎁 Product Recommendations":
    st.markdown("""
    <div class="main-header">
        <h1>🎁 Product Recommendations</h1>
        <p>Discover Similar Products Based on AI-Powered Collaborative Filtering</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    if product_similarity is None:
        st.error("⚠️ Models not loaded. Please run the analysis notebook first to train the models.")
    else:
        st.markdown("""
        ### 🔍 Find Similar Products
        Enter a product name below to get personalized recommendations based on customer purchase patterns.
        """)
        
        # Get list of available products
        available_products = sorted(product_similarity.index.tolist())
        
        # Product input with autocomplete
        col1, col2 = st.columns([3, 1])
        
        with col1:
            product_name = st.selectbox(
                "Select or Search Product",
                options=available_products,
                help="Start typing to search for a product"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            recommend_button = st.button("🔮 Get Recommendations", use_container_width=True)
        
        # Number of recommendations slider
        num_recommendations = st.slider(
            "Number of Recommendations",
            min_value=3,
            max_value=10,
            value=5,
            help="Select how many similar products you want to see"
        )
        
        if recommend_button or product_name:
            if product_name in product_similarity.index:
                st.markdown(f"""
                <div class="success-box">
                    <h2>🎯 Recommendations for: "{product_name}"</h2>
                    <p>Based on collaborative filtering analysis of customer purchase patterns</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Get recommendations
                similar_products = product_similarity[product_name].sort_values(ascending=False)[1:num_recommendations+1]
                
                # Display recommendations
                for idx, (product, similarity) in enumerate(similar_products.items(), 1):
                    similarity_percentage = similarity * 100
                    
                    # Create color gradient based on similarity
                    if similarity_percentage >= 80:
                        emoji = "🔥"
                        label = "Highly Similar"
                    elif similarity_percentage >= 60:
                        emoji = "⭐"
                        label = "Very Similar"
                    elif similarity_percentage >= 40:
                        emoji = "👍"
                        label = "Similar"
                    else:
                        emoji = "💡"
                        label = "Somewhat Similar"
                    
                    st.markdown(f"""
                    <div class="rec-card">
                        <h4>{emoji} #{idx}. {product}</h4>
                        <p><strong>{label}</strong> - Similarity Score: {similarity_percentage:.2f}%</p>
                        <div style="background: linear-gradient(90deg, #667eea {similarity_percentage}%, #e0e0e0 {similarity_percentage}%); 
                                    height: 8px; 
                                    border-radius: 4px; 
                                    margin-top: 0.5rem;"></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Visualization
                st.markdown("### 📊 Similarity Visualization")
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=similar_products.values * 100,
                        y=[f"{i}. {prod[:40]}..." if len(prod) > 40 else f"{i}. {prod}" 
                           for i, prod in enumerate(similar_products.index, 1)],
                        orientation='h',
                        marker=dict(
                            color=similar_products.values * 100,
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="Similarity %")
                        ),
                        text=[f"{val*100:.1f}%" for val in similar_products.values],
                        textposition='auto',
                    )
                ])
                
                fig.update_layout(
                    title="Product Similarity Scores",
                    xaxis_title="Similarity Percentage (%)",
                    yaxis_title="Products",
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter")
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.error(f"❌ Product '{product_name}' not found in our database. Please select from the dropdown.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================
# PAGE: CUSTOMER SEGMENTATION
# ========================================
elif page == "👥 Customer Segmentation":
    st.markdown("""
    <div class="main-header">
        <h1>👥 Customer Segmentation</h1>
        <p>Predict Customer Segments Using RFM Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    if kmeans_model is None or scaler is None or cluster_labels is None:
        st.error("⚠️ Models not loaded. Please run the analysis notebook first to train the models.")
    else:
        st.markdown("""
        ### 📝 Enter Customer RFM Metrics
        Provide the Recency, Frequency, and Monetary values to predict the customer segment.
        """)
        
        # Create input form
        col1, col2, col3 = st.columns(3)
        
        with col1:
            recency = st.number_input(
                "📅 Recency (Days)",
                min_value=0,
                max_value=1000,
                value=30,
                help="Number of days since last purchase"
            )
            st.caption("Lower values indicate recent purchases")
        
        with col2:
            frequency = st.number_input(
                "🔄 Frequency (Purchases)",
                min_value=1,
                max_value=1000,
                value=10,
                help="Total number of purchases"
            )
            st.caption("Higher values indicate loyal customers")
        
        with col3:
            monetary = st.number_input(
                "💰 Monetary (£)",
                min_value=0.0,
                max_value=100000.0,
                value=500.0,
                step=10.0,
                help="Total amount spent"
            )
            st.caption("Higher values indicate valuable customers")
        
        # Predict button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            predict_button = st.button("🔮 Predict Customer Segment", use_container_width=True)
        
        if predict_button:
            # Prepare input data
            input_data = np.array([[recency, frequency, monetary]])
            
            # Scale the input
            input_scaled = scaler.transform(input_data)
            
            # Predict cluster
            cluster = kmeans_model.predict(input_scaled)[0]
            segment = cluster_labels[cluster]
            
            # Display result
            st.markdown(f"""
            <div class="success-box">
                <h2>🎯 Prediction Result</h2>
                <p>Based on the provided RFM metrics, this customer belongs to:</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Segment badge with styling
            segment_class = segment.lower().replace('-', '-').replace(' ', '-')
            st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <span class="segment-badge {segment_class}">{segment}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Segment description
            segment_descriptions = {
                'High-Value': {
                    'emoji': '💎',
                    'description': 'These are your most valuable customers! They purchase frequently, recently, and spend significantly.',
                    'strategy': [
                        '🎁 VIP treatment with exclusive offers',
                        '🌟 Early access to new products',
                        '💌 Personalized communication',
                        '🎯 Premium loyalty rewards'
                    ]
                },
                'Regular': {
                    'emoji': '⭐',
                    'description': 'Steady and reliable customers who make consistent purchases with moderate spending.',
                    'strategy': [
                        '📧 Regular newsletter updates',
                        '🎉 Seasonal promotions',
                        '💳 Loyalty program enrollment',
                        '🔔 Product recommendations'
                    ]
                },
                'Occasional': {
                    'emoji': '💡',
                    'description': 'Infrequent buyers with low purchase volume. Great potential for growth!',
                    'strategy': [
                        '🎯 Re-engagement campaigns',
                        '💰 Special discounts & offers',
                        '📱 Multi-channel marketing',
                        '🎁 Welcome back incentives'
                    ]
                },
                'At-Risk': {
                    'emoji': '⚠️',
                    'description': 'Customers who haven\'t purchased in a long time. Action needed to prevent churn!',
                    'strategy': [
                        '🚨 Win-back campaigns',
                        '💸 Attractive retention offers',
                        '📞 Direct customer outreach',
                        '🔄 Feedback surveys'
                    ]
                }
            }
            
            if segment in segment_descriptions:
                info = segment_descriptions[segment]
                
                st.markdown(f"""
                <div class="feature-card">
                    <h3>{info['emoji']} About This Segment</h3>
                    <p>{info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="feature-card">
                    <h3>📋 Recommended Marketing Strategies</h3>
                """, unsafe_allow_html=True)
                
                for strategy in info['strategy']:
                    st.markdown(f"- {strategy}")
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # RFM Comparison with segment averages
            if rfm_data is not None and 'Segment' in rfm_data.columns:
                st.markdown("### 📊 RFM Comparison with Segment Average")
                
                segment_avg = rfm_data[rfm_data['Segment'] == segment][['Recency', 'Frequency', 'Monetary']].mean()
                
                comparison_data = pd.DataFrame({
                    'Metric': ['Recency (Days)', 'Frequency (Purchases)', 'Monetary (£)'],
                    'Your Values': [recency, frequency, monetary],
                    'Segment Average': [segment_avg['Recency'], segment_avg['Frequency'], segment_avg['Monetary']]
                })
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Your Values',
                    x=comparison_data['Metric'],
                    y=comparison_data['Your Values'],
                    marker_color='#667eea'
                ))
                
                fig.add_trace(go.Bar(
                    name='Segment Average',
                    x=comparison_data['Metric'],
                    y=comparison_data['Segment Average'],
                    marker_color='#764ba2'
                ))
                
                fig.update_layout(
                    barmode='group',
                    title="Your RFM Metrics vs Segment Average",
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter")
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================
# PAGE: ANALYTICS DASHBOARD
# ========================================
elif page == "📊 Analytics Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Analytics Dashboard</h1>
        <p>Comprehensive Customer Insights & Business Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    if rfm_data is None:
        st.error("⚠️ Data not loaded. Please run the analysis notebook first.")
    else:
        # Summary Statistics
        st.markdown("## 📈 Key Metrics Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_customers = len(rfm_data)
            st.markdown(f"""
            <div class="info-box">
                <h3>{total_customers:,}</h3>
                <p>Total Customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_recency = rfm_data['Recency'].mean()
            st.markdown(f"""
            <div class="info-box">
                <h3>{avg_recency:.0f}</h3>
                <p>Avg Recency (Days)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_frequency = rfm_data['Frequency'].mean()
            st.markdown(f"""
            <div class="info-box">
                <h3>{avg_frequency:.1f}</h3>
                <p>Avg Frequency</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_revenue = rfm_data['Monetary'].sum()
            st.markdown(f"""
            <div class="info-box">
                <h3>£{total_revenue:,.0f}</h3>
                <p>Total Revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Customer Segment Distribution
        if 'Segment' in rfm_data.columns:
            st.markdown("## 🎯 Customer Segment Distribution")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                segment_counts = rfm_data['Segment'].value_counts()
                
                fig = go.Figure(data=[go.Pie(
                    labels=segment_counts.index,
                    values=segment_counts.values,
                    hole=0.4,
                    marker=dict(colors=['#E63946', '#F1C40F', '#457B9D', '#2A9D8F']),
                    textinfo='label+percent',
                    textfont=dict(size=14, family="Inter")
                )])
                
                fig.update_layout(
                    title="Segment Distribution",
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter")
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Bar chart
                fig = go.Figure(data=[go.Bar(
                    x=segment_counts.index,
                    y=segment_counts.values,
                    marker=dict(
                        color=['#E63946', '#F1C40F', '#457B9D', '#2A9D8F'],
                        line=dict(color='white', width=2)
                    ),
                    text=segment_counts.values,
                    textposition='auto',
                )])
                
                fig.update_layout(
                    title="Customer Count by Segment",
                    xaxis_title="Segment",
                    yaxis_title="Number of Customers",
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter")
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Segment-wise RFM Analysis
            st.markdown("## 📊 Segment-wise RFM Metrics")
            
            segment_analysis = rfm_data.groupby('Segment').agg({
                'Recency': 'mean',
                'Frequency': 'mean',
                'Monetary': 'mean',
                'CustomerID': 'count'
            }).round(2)
            
            segment_analysis.columns = ['Avg Recency', 'Avg Frequency', 'Avg Monetary', 'Customer Count']
            
            # Display as table
            st.dataframe(
                segment_analysis.style.background_gradient(cmap='RdYlGn_r', subset=['Avg Recency'])
                                      .background_gradient(cmap='RdYlGn', subset=['Avg Frequency', 'Avg Monetary']),
                use_container_width=True
            )
            
            # RFM Metrics Comparison
            col1, col2, col3 = st.columns(3)
            
            with col1:
                fig = go.Figure(data=[go.Bar(
                    x=segment_analysis.index,
                    y=segment_analysis['Avg Recency'],
                    marker_color='#FF6B6B',
                    text=segment_analysis['Avg Recency'].round(1),
                    textposition='auto',
                )])
                
                fig.update_layout(
                    title="Average Recency by Segment",
                    xaxis_title="Segment",
                    yaxis_title="Days",
                    height=300,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=10)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[go.Bar(
                    x=segment_analysis.index,
                    y=segment_analysis['Avg Frequency'],
                    marker_color='#4ECDC4',
                    text=segment_analysis['Avg Frequency'].round(1),
                    textposition='auto',
                )])
                
                fig.update_layout(
                    title="Average Frequency by Segment",
                    xaxis_title="Segment",
                    yaxis_title="Purchases",
                    height=300,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=10)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col3:
                fig = go.Figure(data=[go.Bar(
                    x=segment_analysis.index,
                    y=segment_analysis['Avg Monetary'],
                    marker_color='#95E1D3',
                    text=['£' + str(round(val, 0)) for val in segment_analysis['Avg Monetary']],
                    textposition='auto',
                )])
                
                fig.update_layout(
                    title="Average Monetary by Segment",
                    xaxis_title="Segment",
                    yaxis_title="Revenue (£)",
                    height=300,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=10)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # RFM Distribution Histograms
        st.markdown("## 📉 RFM Distributions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig = go.Figure(data=[go.Histogram(
                x=rfm_data['Recency'],
                nbinsx=30,
                marker_color='#E63946',
                opacity=0.7
            )])
            
            fig.update_layout(
                title="Recency Distribution",
                xaxis_title="Days Since Last Purchase",
                yaxis_title="Count",
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter")
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure(data=[go.Histogram(
                x=rfm_data['Frequency'],
                nbinsx=30,
                marker_color='#457B9D',
                opacity=0.7
            )])
            
            fig.update_layout(
                title="Frequency Distribution",
                xaxis_title="Number of Purchases",
                yaxis_title="Count",
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter")
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            fig = go.Figure(data=[go.Histogram(
                x=rfm_data['Monetary'],
                nbinsx=30,
                marker_color='#2A9D8F',
                opacity=0.7
            )])
            
            fig.update_layout(
                title="Monetary Distribution",
                xaxis_title="Total Spending (£)",
                yaxis_title="Count",
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter")
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255, 255, 255, 0.8); padding: 1rem;">
    <p style="font-size: 0.9rem;">
        <strong>🛒 Shopper Spectrum</strong> - AI-Powered E-Commerce Analytics Platform<br>
        Built with Python, Scikit-learn, and Streamlit | © 2024
    </p>
</div>
""", unsafe_allow_html=True)
