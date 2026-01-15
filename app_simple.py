import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from PIL import Image

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
# SIMPLE, CLEAN CSS STYLING
# ========================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Background - Simple White */
    .stApp {
        background: #f8f9fa;
    }
    
    /* Sidebar Styling - Clean Blue */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4a90e2 0%, #357abd 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Floating Emoji Decorations */
    .floating-icon {
        position: fixed;
        font-size: 3rem;
        opacity: 0.25;
        animation: floatAround 20s infinite ease-in-out;
        pointer-events: none;
        z-index: -1;
        filter: drop-shadow(0 0 10px rgba(74, 144, 226, 0.3));
    }
    
    .icon-1 {
        top: 10%;
        left: 5%;
        animation-delay: 0s;
        font-size: 3.5rem;
    }
    
    .icon-2 {
        top: 20%;
        right: 10%;
        animation-delay: 4s;
        font-size: 2.5rem;
    }
    
    .icon-3 {
        top: 50%;
        left: 15%;
        animation-delay: 8s;
        font-size: 3rem;
    }
    
    .icon-4 {
        bottom: 20%;
        right: 5%;
        animation-delay: 12s;
        font-size: 2.8rem;
    }
    
    .icon-5 {
        bottom: 10%;
        left: 10%;
        animation-delay: 16s;
        font-size: 3.2rem;
    }
    
    @keyframes floatAround {
        0%, 100% {
            transform: translate(0, 0) rotate(0deg) scale(1);
        }
        20% {
            transform: translate(30px, -30px) rotate(15deg) scale(1.1);
        }
        40% {
            transform: translate(-20px, 20px) rotate(-15deg) scale(0.9);
        }
        60% {
            transform: translate(25px, 25px) rotate(10deg) scale(1.05);
        }
        80% {
            transform: translate(-25px, -20px) rotate(-10deg) scale(0.95);
        }
    }
    
    /* Simple Header */
    .simple-header {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .simple-header h1 {
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 600;
        margin: 0;
    }
    
    .simple-header p {
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Clean Cards */
    .clean-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #4a90e2;
        transition: all 0.3s ease;
    }
    
    .clean-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .clean-card h3 {
        color: #2c3e50;
        font-size: 1.3rem;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    
    .clean-card p {
        color: #5a6c7d;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Stats Cards - Simple Colors */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #4a90e2;
    }
    
    .stat-card h3 {
        color: #4a90e2;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .stat-card p {
        color: #7f8c8d;
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem;
    }
    
    /* Simple Buttons */
    .stButton > button {
        background: #4a90e2;
        color: white;
        border: none;
        padding: 0.7rem 2rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #357abd;
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
    }
    
    /* Clean Segment Badges */
    .segment-badge {
        display: inline-block;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.3rem;
        margin: 1rem 0;
    }
    
    .high-value {
        background: #27ae60;
        color: white;
    }
    
    .regular {
        background: #3498db;
        color: white;
    }
    
    .occasional {
        background: #f39c12;
        color: white;
    }
    
    .at-risk {
        background: #e74c3c;
        color: white;
    }
    
    /* Image Container with Framer Motion Style Animation */
    .img-container {
        text-align: center;
        margin: 2rem 0;
        position: relative;
        perspective: 1000px;
    }
    
    .img-container img {
        max-width: 100%;
        border-radius: 10px;
        box-shadow: 0 10px 40px rgba(74, 144, 226, 0.15);
        /* Framer Motion style: y: [0, -20, 0] */
        animation: smoothFloat 3s ease-in-out infinite;
        transition: all 0.3s ease;
        transform-style: preserve-3d;
        position: relative;
        z-index: 2;
    }
    
    .img-container img:hover {
        transform: scale(1.08) translateY(-10px);
        box-shadow: 0 20px 60px rgba(74, 144, 226, 0.3);
    }
    
    /* Decorative Glowing Blob Background - Like React version */
    .img-container::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, 
            rgba(168, 85, 247, 0.2) 0%,
            rgba(59, 130, 246, 0.2) 50%,
            rgba(99, 102, 241, 0.2) 100%);
        border-radius: 50%;
        filter: blur(60px);
        z-index: 1;
        animation: blob 7s ease-in-out infinite;
    }
    
    /* Feature Image with Bounce Animation - Like React cards */
    .feature-img {
        position: relative;
        /* Similar to whileHover: { y: -10, scale: 1.02 } */
        animation: gentleBounce 2.5s ease-in-out infinite;
        transition: all 0.4s ease;
        perspective: 1000px;
    }
    
    .feature-img img {
        box-shadow: 0 8px 30px rgba(74, 144, 226, 0.15);
        border-radius: 15px;
    }
    
    .feature-img:hover {
        transform: translateY(-10px) scale(1.02);
        filter: brightness(1.1);
    }
    
    .feature-img:hover img {
        box-shadow: 0 15px 50px rgba(74, 144, 226, 0.3);
    }
    
    /* Smooth Float - Exact Framer Motion pattern: y: [0, -20, 0] */
    @keyframes smoothFloat {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-20px);
        }
    }
    
    /* Gentle Bounce for Feature Images */
    @keyframes gentleBounce {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-15px);
        }
    }
    
    /* Blob Animation - Like decorative blobs in React */
    @keyframes blob {
        0%, 100% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.3;
        }
        33% {
            transform: translate(-45%, -55%) scale(1.1);
            opacity: 0.4;
        }
        66% {
            transform: translate(-55%, -45%) scale(0.9);
            opacity: 0.35;
        }
    }
    
    /* Apply animations to Streamlit's actual image elements */
    .feature-img img,
    .feature-img [data-testid="stImage"] img {
        animation: gentleBounce 2.5s ease-in-out infinite !important;
        box-shadow: 0 8px 30px rgba(74, 144, 226, 0.15) !important;
        border-radius: 15px !important;
        transition: all 0.4s ease !important;
    }
    
    .img-container [data-testid="stImage"] img {
        animation: smoothFloat 3s ease-in-out infinite !important;
        box-shadow: 0 10px 40px rgba(74, 144, 226, 0.15) !important;
    }
    
    /* Make sure Streamlit's image container doesn't interfere */
    .feature-img [data-testid="stImage"],
    .img-container [data-testid="stImage"] {
        animation: inherit;
    }
    
    /* Bounce In Animation */
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3) translateY(50px);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            transform: scale(1);
        }
    }
    
    /* Pulse Animation for Icons */
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
    }
    
    /* Rotate Animation */
    @keyframes gentleRotate {
        0%, 100% {
            transform: rotate(0deg);
        }
        25% {
            transform: rotate(2deg);
        }
        75% {
            transform: rotate(-2deg);
        }
    }
    
    /* Slide In From Left */
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Slide In From Right */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Fade In Up */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Apply animations to cards */
    .clean-card {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .clean-card:hover {
        animation: wiggle 0.5s ease-in-out;
    }
    
    .stat-card {
        animation: pulse 3s ease-in-out infinite, shake 4s ease-in-out infinite;
    }
    
    .stat-card:hover {
        animation: none;
        transform: translateY(-8px) scale(1.08) rotate(2deg);
        box-shadow: 0 15px 40px rgba(74, 144, 226, 0.4);
    }
    
    /* Wiggle Animation */
    @keyframes wiggle {
        0%, 100% {
            transform: translateX(0) rotate(0deg);
        }
        25% {
            transform: translateX(-5px) rotate(-1deg);
        }
        50% {
            transform: translateX(5px) rotate(1deg);
        }
        75% {
            transform: translateX(-3px) rotate(-0.5deg);
        }
    }
    
    /* Shake Animation for Stats */
    @keyframes shake {
        0%, 100% {
            transform: rotate(0deg);
        }
        10%, 30%, 50%, 70%, 90% {
            transform: rotate(0deg);
        }
        20%, 60% {
            transform: rotate(1deg);
        }
        40%, 80% {
            transform: rotate(-1deg);
        }
    }
    
    /* Animated Header */
    .simple-header {
        animation: slideDown 1s ease-out;
    }
    
    .simple-header:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.2);
    }
    
    /* Slide Down Animation */
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ========================================
       MOBILE RESPONSIVE DESIGN
       ======================================== */
    
    /* Tablets and Small Desktop (max-width: 768px) */
    @media (max-width: 768px) {
        /* Header Adjustments */
        .simple-header h1 {
            font-size: 2rem !important;
            padding: 1rem;
        }
        
        .simple-header p {
            font-size: 0.95rem !important;
        }
        
        /* Card Spacing */
        .clean-card {
            padding: 1.2rem;
            margin: 0.8rem 0;
        }
        
        .clean-card h3 {
            font-size: 1.1rem;
        }
        
        .clean-card p {
            font-size: 0.9rem;
        }
        
        /* Stats Cards */
        .stat-card {
            padding: 1.2rem;
            margin: 0.5rem 0;
        }
        
        .stat-card h3 {
            font-size: 1.5rem;
        }
        
        .stat-card p {
            font-size: 0.85rem;
        }
        
        /* Image Container */
        .img-container {
            margin: 1.5rem 0;
        }
        
        /* Buttons */
        .stButton > button {
            padding: 0.6rem 1.5rem;
            font-size: 0.9rem;
        }
        
        /* Segment Badge */
        .segment-badge {
            font-size: 1.1rem;
            padding: 0.6rem 1.2rem;
        }
        
        /* Floating Icons - Smaller */
        .floating-icon {
            font-size: 2rem !important;
            opacity: 0.15;
        }
        
        .icon-1, .icon-2, .icon-3, .icon-4, .icon-5 {
            font-size: 2rem !important;
        }
        
        /* Reduce animation intensity */
        .img-container img:hover {
            transform: scale(1.02);
        }
        
        .feature-img:hover {
            transform: translateY(-5px) scale(1.02);
        }
        
        /* Gentler floating animation */
        @keyframes floatImage {
            0%, 100% {
                transform: translateY(0px) rotate(0deg) scale(1);
            }
            50% {
                transform: translateY(-8px);
            }
        }
        
        @keyframes floatAround {
            0%, 100% {
                transform: translate(0, 0) rotate(0deg) scale(1);
            }
            50% {
                transform: translate(10px, -10px) rotate(5deg) scale(1.05);
            }
        }
    }
    
    /* Mobile Phones (max-width: 480px) */
    @media (max-width: 480px) {
        /* Header - Extra Small */
        .simple-header {
            padding: 1.5rem 1rem;
            margin-bottom: 1rem;
        }
        
        .simple-header h1 {
            font-size: 1.5rem !important;
        }
        
        .simple-header p {
            font-size: 0.85rem !important;
        }
        
        /* Cards - Compact */
        .clean-card {
            padding: 1rem;
            margin: 0.6rem 0;
            border-left-width: 3px;
        }
        
        .clean-card h3 {
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }
        
        .clean-card p {
            font-size: 0.85rem;
            line-height: 1.5;
        }
        
        /* Stats Cards - Stacked */
        .stat-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .stat-card h3 {
            font-size: 1.3rem;
        }
        
        .stat-card p {
            font-size: 0.8rem;
        }
        
        /* Images - Smaller margins */
        .img-container {
            margin: 1rem 0;
        }
        
        /* Buttons - Full width */
        .stButton > button {
            width: 100%;
            padding: 0.7rem 1rem;
            font-size: 0.85rem;
        }
        
        /* Segment Badge - Smaller */
        .segment-badge {
            font-size: 1rem;
            padding: 0.5rem 1rem;
        }
        
        /* Hide floating icons on very small screens */
        .floating-icon {
            display: none;
        }
        
        /* Disable hover animations on touch devices */
        .img-container img:hover,
        .feature-img:hover,
        .clean-card:hover,
        .stat-card:hover {
            transform: none;
        }
        
        /* Simplify animations */
        .stat-card {
            animation: none;
        }
        
        /* Streamlit specific - Make inputs full width */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div {
            font-size: 0.9rem !important;
        }
        
        /* Reduce sidebar padding */
        [data-testid="stSidebar"] {
            padding: 1rem 0.5rem;
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
    st.markdown('## 🛒 Navigation')
    
    page = st.radio(
        "",
        ["🏠 Home", "🎁 Product Recommendations", "👥 Customer Segmentation", "📊 Analytics Dashboard"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("""
    ### 📌 About
    AI-powered e-commerce platform for customer insights and personalized recommendations.
    """)
    
    st.markdown("""
    ### 🎯 Features
    - RFM-based Segmentation
    - Collaborative Filtering
    - Real-time Predictions
    - Interactive Analytics
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-size: 0.8rem; opacity: 0.8;">
        <p>Built with ❤️ using Streamlit</p>
        <p>© 2024 Shopper Spectrum</p>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# PAGE: HOME
# ========================================
if page == "🏠 Home":
    # Add floating icons for visual appeal
    st.markdown("""
    <div class="floating-icon icon-1">🛒</div>
    <div class="floating-icon icon-2">🎁</div>
    <div class="floating-icon icon-3">👥</div>
    <div class="floating-icon icon-4">📊</div>
    <div class="floating-icon icon-5">💰</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="simple-header">
        <h1>🛒 Shopper Spectrum</h1>
        <p>AI-Powered Customer Segmentation & Product Recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Image - Modern 3D Shopping Cart
    st.markdown('<div class="img-container">', unsafe_allow_html=True)
    try:
        import base64
        from io import BytesIO
        hero_img = Image.open('C:/Users/pruth/.gemini/antigravity/brain/f11c3ee4-417d-4458-a9b1-4ede7a84a708/modern_shopping_hero_1768477624767.png')
        buffered = BytesIO()
        hero_img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        st.markdown(
            f'''<img src="data:image/png;base64,{img_str}" 
                style="width: 100%; 
                       height: auto; 
                       display: block; 
                       margin: 0 auto;
                       animation: smoothFloat 3s ease-in-out infinite;
                       box-shadow: 0 10px 40px rgba(74, 144, 226, 0.15);
                       border-radius: 10px;">''',
            unsafe_allow_html=True
        )
    except:
        # Fallback to old image
        try:
            hero_img = Image.open('C:/Users/pruth/.gemini/antigravity/brain/f11c3ee4-417d-4458-a9b1-4ede7a84a708/diverse_shoppers_hero_1768477126719.png')
            buffered = BytesIO()
            hero_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            st.markdown(
                f'''<img src="data:image/png;base64,{img_str}" 
                    style="width: 100%; 
                           height: auto; 
                           display: block; 
                           margin: 0 auto;
                           animation: smoothFloat 3s ease-in-out infinite;
                           box-shadow: 0 10px 40px rgba(74, 144, 226, 0.15);
                           border-radius: 10px;">''',
                unsafe_allow_html=True
            )
        except:
            st.info("Welcome to Shopper Spectrum - Your E-Commerce Analytics Platform!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    ## Welcome to Shopper Spectrum! 👋
    
    Your simple and powerful e-commerce analytics platform. Get customer insights and personalized recommendations with just a few clicks.
    """)
    
    # Feature cards with images
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="clean-card">
            <h3>🎁 Product Recommendations</h3>
            <p>Get personalized product suggestions using collaborative filtering. Our AI analyzes customer purchase patterns to recommend the most relevant products.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Product recommendation image with animation - Base64 HTML
        st.markdown('<div class="feature-img">', unsafe_allow_html=True)
        try:
            from io import BytesIO
            import base64
            prod_img = Image.open('C:/Users/pruth/.gemini/antigravity/brain/f11c3ee4-417d-4458-a9b1-4ede7a84a708/analytics_dashboard_visual_1768477639287.png')
            buffered = BytesIO()
            prod_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            st.markdown(f'''<img src="data:image/png;base64,{img_str}" 
                style="width: 100%; 
                       height: auto;
                       animation: gentleBounce 2.5s ease-in-out infinite;
                       box-shadow: 0 8px 30px rgba(74, 144, 226, 0.15);
                       border-radius: 15px;">''', unsafe_allow_html=True)
        except:
            try:
                prod_img = Image.open('C:/Users/pruth/.gemini/antigravity/brain/f11c3ee4-417d-4458-a9b1-4ede7a84a708/product_recommendations_icon_1768477162480.png')
                buffered = BytesIO()
                prod_img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                st.markdown(f'''<img src="data:image/png;base64,{img_str}" 
                    style="width: 100%; 
                           height: auto;
                           animation: gentleBounce 2.5s ease-in-out infinite;
                           box-shadow: 0 8px 30px rgba(74, 144, 226, 0.15);
                           border-radius: 15px;">''', unsafe_allow_html=True)
            except:
                pass
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="clean-card">
            <h3>👥 Customer Segmentation</h3>
            <p>Classify customers into strategic segments using RFM analysis. Identify High-Value, Regular, Occasional, and At-Risk customers for targeted marketing.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Customer segmentation image with animation - Base64 HTML
        st.markdown('<div class="feature-img">', unsafe_allow_html=True)
        try:
            from io import BytesIO
            import base64
            seg_img = Image.open('C:/Users/pruth/.gemini/antigravity/brain/f11c3ee4-417d-4458-a9b1-4ede7a84a708/modern_shopping_hero_1768477624767.png')
            buffered = BytesIO()
            seg_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            st.markdown(f'''<img src="data:image/png;base64,{img_str}" 
                style="width: 100%; 
                       height: auto;
                       animation: gentleBounce 2.5s ease-in-out infinite;
                       box-shadow: 0 8px 30px rgba(74, 144, 226, 0.15);
                       border-radius: 15px;">''', unsafe_allow_html=True)
        except:
            try:
                seg_img = Image.open('C:/Users/pruth/.gemini/antigravity/brain/f11c3ee4-417d-4458-a9b1-4ede7a84a708/customer_segmentation_icon_1768477144179.png')
                buffered = BytesIO()
                seg_img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                st.markdown(f'''<img src="data:image/png;base64,{img_str}" 
                    style="width: 100%; 
                           height: auto;
                           animation: gentleBounce 2.5s ease-in-out infinite;
                           box-shadow: 0 8px 30px rgba(74, 144, 226, 0.15);
                           border-radius: 15px;">''', unsafe_allow_html=True)
            except:
                pass
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics
    if rfm_data is not None:
        st.markdown("## 📈 Platform Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h3>{len(rfm_data):,}</h3>
                <p>Total Customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            high_value = len(rfm_data[rfm_data['Segment'] == 'High-Value']) if 'Segment' in rfm_data.columns else 0
            st.markdown(f"""
            <div class="stat-card">
                <h3>{high_value:,}</h3>
                <p>High-Value Customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if product_similarity is not None:
                st.markdown(f"""
                <div class="stat-card">
                    <h3>{len(product_similarity):,}</h3>
                    <p>Unique Products</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            avg_monetary = rfm_data['Monetary'].mean() if 'Monetary' in rfm_data.columns else 0
            st.markdown(f"""
            <div class="stat-card">
                <h3>£{avg_monetary:.2f}</h3>
                <p>Avg Customer Value</p>
            </div>
            """, unsafe_allow_html=True)
    
    # How it works
    st.markdown("## 🔍 How It Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="clean-card">
            <h3>1️⃣ Data Processing</h3>
            <p>We analyze transaction data from your e-commerce platform, cleaning and preparing it for insights.</p>
        </div>
        
        <div class="clean-card">
            <h3>2️⃣ RFM Analysis</h3>
            <p>Calculate Recency, Frequency, and Monetary values for each customer to understand behavior.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="clean-card">
            <h3>3️⃣ Segmentation</h3>
            <p>Apply K-Means clustering to group customers into meaningful segments for targeted strategies.</p>
        </div>
        
        <div class="clean-card">
            <h3>4️⃣ Recommendations</h3>
            <p>Use collaborative filtering to identify similar products based on customer purchase patterns.</p>
        </div>
        """, unsafe_allow_html=True)

# ========================================
# PAGE: PRODUCT RECOMMENDATIONS
# ========================================
elif page == "🎁 Product Recommendations":
    st.markdown("""
    <div class="simple-header">
        <h1>🎁 Product Recommendations</h1>
        <p>Discover Similar Products Based on AI-Powered Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    if product_similarity is None:
        st.error("⚠️ Models not loaded. Please run the analysis notebook first to train the models.")
    else:
        st.markdown("""
        ### 🔍 Find Similar Products
        Enter a product name below to get personalized recommendations based on customer purchase patterns.
        """)
        
        # Get list of available products
        available_products = sorted(product_similarity.index.tolist())
        
        # Product input
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
        
        # Number of recommendations
        num_recommendations = st.slider(
            "Number of Recommendations",
            min_value=3,
            max_value=10,
            value=5
        )
        
        if recommend_button or product_name:
            if product_name in product_similarity.index:
                st.markdown(f"""
                <div class="clean-card" style="background: #e8f4f8; border-left-color: #4a90e2;">
                    <h3>🎯 Recommendations for: "{product_name}"</h3>
                    <p>Based on collaborative filtering analysis of customer purchase patterns</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Get recommendations
                similar_products = product_similarity[product_name].sort_values(ascending=False)[1:num_recommendations+1]
                
                # Display recommendations in a clean format
                for idx, (product, similarity) in enumerate(similar_products.items(), 1):
                    similarity_percentage = similarity * 100
                    
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
                    <div class="clean-card">
                        <h3>{emoji} #{idx}. {product}</h3>
                        <p><strong>{label}</strong> - Similarity Score: {similarity_percentage:.2f}%</p>
                        <div style="background: #e0e0e0; height: 8px; border-radius: 4px; margin-top: 0.5rem;">
                            <div style="background: #4a90e2; width: {similarity_percentage}%; height: 100%; border-radius: 4px;"></div>
                        </div>
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
                        marker=dict(color='#4a90e2'),
                        text=[f"{val*100:.1f}%" for val in similar_products.values],
                        textposition='auto',
                    )
                ])
                
                fig.update_layout(
                    title="Product Similarity Scores",
                    xaxis_title="Similarity Percentage (%)",
                    yaxis_title="Products",
                    height=400,
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.error(f"❌ Product '{product_name}' not found. Please select from the dropdown.")

# ========================================
# PAGE: CUSTOMER SEGMENTATION
# ========================================
elif page == "👥 Customer Segmentation":
    st.markdown("""
    <div class="simple-header">
        <h1>👥 Customer Segmentation</h1>
        <p>Predict Customer Segments Using RFM Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
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
            st.caption("Lower values = recent purchases")
        
        with col2:
            frequency = st.number_input(
                "🔄 Frequency (Purchases)",
                min_value=1,
                max_value=1000,
                value=10,
                help="Total number of purchases"
            )
            st.caption("Higher values = loyal customers")
        
        with col3:
            monetary = st.number_input(
                "💰 Monetary (£)",
                min_value=0.0,
                max_value=100000.0,
                value=500.0,
                step=10.0,
                help="Total amount spent"
            )
            st.caption("Higher values = valuable customers")
        
        # Predict button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            predict_button = st.button("🔮 Predict Segment", use_container_width=True)
        
        if predict_button:
            # Prepare input data
            input_data = np.array([[recency, frequency, monetary]])
            input_scaled = scaler.transform(input_data)
            
            # Predict cluster
            cluster = kmeans_model.predict(input_scaled)[0]
            segment = cluster_labels[cluster]
            
            # Display result
            st.markdown(f"""
            <div class="clean-card" style="background: #e8f4f8; border-left-color: #4a90e2; text-align: center;">
                <h3>🎯 Prediction Result</h3>
                <p>Based on the provided RFM metrics, this customer belongs to:</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Segment badge
            segment_class = segment.lower().replace('-', '-').replace(' ', '-')
            st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <span class="segment-badge {segment_class}">{segment}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Segment descriptions
            segment_info = {
                'High-Value': {
                    'emoji': '💎',
                    'desc': 'Your most valuable customers! They purchase frequently, recently, and spend significantly.',
                    'strategies': [
                        '🎁 VIP treatment with exclusive offers',
                        '🌟 Early access to new products',
                        '💌 Personalized communication',
                        '🎯 Premium loyalty rewards'
                    ]
                },
                'Regular': {
                    'emoji': '⭐',
                    'desc': 'Steady and reliable customers who make consistent purchases.',
                    'strategies': [
                        '📧 Regular newsletter updates',
                        '🎉 Seasonal promotions',
                        '💳 Loyalty program enrollment',
                        '🔔 Product recommendations'
                    ]
                },
                'Occasional': {
                    'emoji': '💡',
                    'desc': 'Infrequent buyers with low purchase volume. Great potential for growth!',
                    'strategies': [
                        '🎯 Re-engagement campaigns',
                        '💰 Special discounts & offers',
                        '📱 Multi-channel marketing',
                        '🎁 Welcome back incentives'
                    ]
                },
                'At-Risk': {
                    'emoji': '⚠️',
                    'desc': "Customers who haven't purchased in a long time. Action needed!",
                    'strategies': [
                        '🚨 Win-back campaigns',
                        '💸 Attractive retention offers',
                        '📞 Direct customer outreach',
                        '🔄 Feedback surveys'
                    ]
                }
            }
            
            if segment in segment_info:
                info = segment_info[segment]
                
                st.markdown(f"""
                <div class="clean-card">
                    <h3>{info['emoji']} About This Segment</h3>
                    <p>{info['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="clean-card">
                    <h3>📋 Recommended Marketing Strategies</h3>
                """, unsafe_allow_html=True)
                
                for strategy in info['strategies']:
                    st.markdown(f"- {strategy}")
                
                st.markdown("</div>", unsafe_allow_html=True)

# ========================================
# PAGE: ANALYTICS DASHBOARD
# ========================================
elif page == "📊 Analytics Dashboard":
    st.markdown("""
    <div class="simple-header">
        <h1>📊 Analytics Dashboard</h1>
        <p>Comprehensive Business Insights & Visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    if rfm_data is None:
        st.error("⚠️ Models not loaded. Please run the analysis notebook first.")
    else:
        # Display pre-generated charts
        st.markdown("## 📈 Exploratory Data Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if os.path.exists('eda_trends.png'):
                st.markdown("### Sales Trends Over Time")
                st.image('eda_trends.png', use_container_width=True)
        
        with col2:
            if os.path.exists('eda_products.png'):
                st.markdown("### Top Products")
                st.image('eda_products.png', use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if os.path.exists('eda_countries.png'):
                st.markdown("### Sales by Country")
                st.image('eda_countries.png', use_container_width=True)
        
        with col2:
            if os.path.exists('eda_monetary.png'):
                st.markdown("### Monetary Distribution")
                st.image('eda_monetary.png', use_container_width=True)
        
        st.markdown("## 🎯 RFM Analysis")
        
        if os.path.exists('rfm_distributions.png'):
            st.image('rfm_distributions.png', use_container_width=True)
        
        st.markdown("## 🔍 Customer Clustering")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if os.path.exists('elbow_silhouette.png'):
                st.markdown("### Optimal Clusters")
                st.image('elbow_silhouette.png', use_container_width=True)
        
        with col2:
            if os.path.exists('cluster_3d.png'):
                st.markdown("### 3D Cluster Visualization")
                st.image('cluster_3d.png', use_container_width=True)
        
        if os.path.exists('cluster_analysis.png'):
            st.markdown("### Cluster Analysis")
            st.image('cluster_analysis.png', use_container_width=True)
        
        # Segment distribution
        if 'Segment' in rfm_data.columns:
            st.markdown("## 👥 Customer Segment Distribution")
            
            segment_counts = rfm_data['Segment'].value_counts()
            
            fig = px.pie(
                values=segment_counts.values,
                names=segment_counts.index,
                title="Customer Distribution by Segment",
                color_discrete_sequence=['#27ae60', '#3498db', '#f39c12', '#e74c3c']
            )
            
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
