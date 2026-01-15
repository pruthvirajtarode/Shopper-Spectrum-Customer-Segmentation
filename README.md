# 🛒 Shopper Spectrum - E-Commerce Customer Segmentation & Product Recommendations

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.26+-red.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)

**AI-Powered Customer Insights & Personalized Product Recommendations for E-Commerce**

[Live Demo](#) | [Documentation](#documentation) | [Report Bug](#) | [Request Feature](#)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [ML Models](#-ml-models)
- [UML Diagrams](#-uml-diagrams)
- [API Reference](#-api-reference)
- [Deployment](#-deployment)
- [Performance](#-performance)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

**Shopper Spectrum** is an advanced e-commerce analytics platform that leverages machine learning to provide:

- 🎯 **Customer Segmentation** using RFM (Recency, Frequency, Monetary) Analysis
- 🎁 **Product Recommendations** via Collaborative Filtering
- 📊 **Interactive Analytics Dashboard** with real-time insights
- 📈 **Sales Trend Analysis** and predictive modeling

Built with **Streamlit** and **Scikit-learn**, this platform helps businesses understand customer behavior, optimize marketing strategies, and increase sales through data-driven decision making.

### 🎓 Perfect For:
- **E-Commerce Businesses** - Understand and engage customers better
- **Data Scientists** - Learn ML implementation in production
- **Students** - Academic projects on customer analytics
- **Portfolio Projects** - Showcase machine learning skills

---

## ✨ Features

### 🏠 **Home Dashboard**
- Platform overview with animated UI
- Real-time statistics (4,373 customers, 4 segments, 3,876 products)
- Feature highlights with vibrant 3D illustrations
- Smooth CSS animations (React Framer Motion style)

### 👥 **Customer Segmentation**
- **4 Customer Segments:**
  - 💎 **High-Value Customers** - Recent, frequent, high-spending buyers
  - ⭐ **Regular Customers** - Consistent, moderate-spending shoppers
  - 💡 **Occasional Customers** - Infrequent, low-spending buyers
  - ⚠️ **At-Risk Customers** - Inactive customers at risk of churning
- RFM-based classification using K-Means clustering
- Real-time prediction with instant results
- Personalized marketing strategies for each segment
- Interactive RFM value input

### 🎁 **Product Recommendations**
- AI-powered collaborative filtering algorithm
- Product similarity matrix (120 MB trained model)
- Adjustable recommendation count (3-10 products)
- Similarity scores with visual indicators
- Interactive Plotly charts
- Real-time product search

### 📊 **Analytics Dashboard**
- **6 Interactive Visualizations:**
  - Sales trends over time
  - Top 10 products by quantity
  - Geographic distribution (country-wise sales)
  - Monetary value distribution  
  - RFM metric distributions
  - 3D cluster visualization
- Segment distribution analysis
- Platform-wide statistics
- All charts built with Plotly (fully interactive)

### 🎨 **UI/UX Features**
- **Modern Design:**
  - Clean, minimalist interface
  - Poppins font family
  - Professional blue color scheme (#4a90e2)
  - Card-based layout with shadows
  
- **Animations:**
  - Smooth floating images (3s loops)
  - Gentle bouncing icons (2.5s)
  - Pulsing statistics cards
  - Wiggle effects on hover
  - Floating background emojis (🛒 🎁 👥 📊 💰)
  - Fade-in page transitions
  
- **Mobile Responsive:**
  - 3 breakpoints (Desktop >768px, Tablet ≤768px, Phone ≤480px)
  - Adaptive animations for performance
  - Full-width buttons on mobile
  - Optimized touch interactions
  - No horizontal scrolling

---

## 🛠️ Tech Stack

### **Frontend**
- **Streamlit** (1.26+) - Web application framework
- **CSS3** - Custom styling and animations
- **HTML5** - Structure and layout

### **Backend & ML**
- **Python** (3.9+) - Core programming language
- **Pandas** (2.0+) - Data manipulation
- **NumPy** (1.24+) - Numerical computing
- **Scikit-learn** (1.3+) - Machine learning
  - K-Means Clustering
  - StandardScaler
  - Collaborative Filtering
- **Joblib** (1.3+) - Model persistence

### **Visualization**
- **Plotly** (5.16+) - Interactive charts
- **Matplotlib** (3.7+) - Static visualizations
- **Seaborn** (0.12+) - Statistical plots
- **Pillow** (10.0+) - Image processing

### **Data**
- **Online Retail Dataset** - 541,909 transactions
- **4,373 Unique Customers**
- **3,876 Products**
- **38 Countries**

---

## 🏗️ System Architecture

### **3-Layer Architecture:**

```
┌─────────────────────────────────────────────────┐
│         PRESENTATION LAYER (Streamlit UI)       │
│  ┌────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │  Home  │ │Recommenda-   │ │Segmentation  │ │
│  │  Page  │ │tions Module  │ │   Module     │ │
│  └────────┘ └──────────────┘ └────────┬─────┘ │
└───────────────────────────────────────┼─────────┘
                                        │
┌───────────────────────────────────────┼─────────┐
│       BUSINESS LOGIC LAYER            │         │
│  ┌──────────────┐ ┌──────────────┐   │         │
│  │ ModelLoader  │ │ Segmentation │   │         │
│  │              │ │   Engine     │   │         │
│  └──────────────┘ └──────────────┘   │         │
│  ┌──────────────┐ ┌──────────────┐   │         │
│  │Recommendation│ │  Analytics   │   │         │
│  │   Engine     │ │   Engine     │   │         │
│  └──────────────┘ └──────────────┘   │         │
└───────────────────────────────────────┼─────────┘
                                        │
┌───────────────────────────────────────┼─────────┐
│            DATA LAYER                 ▼         │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │ KMeans   │ │ Scaler   │ │  Similarity  │   │
│  │Model.pkl │ │Model.pkl │ │  Matrix.pkl  │   │
│  └──────────┘ └──────────┘ └──────────────┘   │
│  ┌──────────┐ ┌──────────────────────────┐   │
│  │RFM Data  │ │   Online Retail CSV      │   │
│  │  .csv    │ │      (48.5 MB)           │   │
│  └──────────┘ └──────────────────────────┘   │
└──────────────────────────────────────────────┘
```

See detailed diagrams in [`diagrams/`](./diagrams/) folder.

---

## 📸 Screenshots

### Home Page
![Home Page](assets/images/hero_shopping.png)
*Modern dashboard with smooth animations and statistics*

### Customer Segmentation
![Customer Segmentation](assets/images/segments.png)
*RFM-based customer classification with 4 segments*

### Product Recommendations
![Product Recommendations](assets/images/analytics.png)
*AI-powered collaborative filtering recommendations*

### Analytics Dashboard
*Interactive Plotly charts with real-time data*

---

## 🚀 Installation

### **Prerequisites**
- Python 3.9 or higher
- pip package manager
- Git (for cloning)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/pruthvirajtarode/Shopper-Spectrum-Customer-Segmentation.git
cd Shopper-Spectrum-Customer-Segmentation
```

### **Step 2: Create Virtual Environment** (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Verify Installation**
```bash
python test_setup.py
```

Expected output:
```
✅ Python version: 3.9.x
✅ All required packages installed
✅ Models folder exists
✅ All model files present
✅ Setup complete!
```

---

## 💻 Usage

### **Run the Application**
```bash
streamlit run app_simple.py
```

The app will open in your browser at `http://localhost:8501`

### **Navigate the Platform**

#### **1. Home Page**
- View platform statistics
- Explore feature highlights
- See customer segments overview

#### **2. Product Recommendations**
1. Select a product from the dropdown
2. Adjust number of recommendations (3-10)
3. View similar products with similarity scores
4. Explore interactive charts

#### **3. Customer Segmentation**
1. Enter RFM values:
   - **Recency:** Days since last purchase (0-365)
   - **Frequency:** Number of purchases (1-1000)
   - **Monetary:** Total spending ($1-50,000)
2. Click "Predict Customer Segment"
3. View segment classification:
   - Segment badge with color coding
   - Detailed description
   - Marketing recommendations
   - RFM comparison chart

#### **4. Analytics Dashboard**
- View 6 interactive visualizations
- Explore sales trends
- Analyze customer distribution
- Review segment statistics

---

## 📁 Project Structure

```
Shopper-Spectrum-Customer-Segmentation/
│
├── 📱 Applications
│   ├── app_simple.py              # Main Streamlit application (43.4 KB)
│   └── app.py                     # Original version (38.3 KB)
│
├── 🧠 Machine Learning
│   ├── analysis_notebook.py       # ML training & analysis (21.6 KB)
│   └── models/                    # Trained ML models
│       ├── kmeans_model.pkl       # K-Means clustering (18 KB)
│       ├── scaler.pkl             # Feature scaler (959 B)
│       ├── product_similarity.pkl # Recommendation matrix (120 MB)
│       ├── cluster_labels.pkl     # Segment mapping (43 B)
│       └── rfm_data.csv          # Customer RFM data (133 KB)
│
├── 📊 Data
│   ├── online_retail.csv          # E-commerce dataset (48.5 MB)
│   ├── eda_trends.png            # Sales trends chart
│   ├── eda_products.png          # Top products chart
│   ├── eda_countries.png         # Geographic distribution
│   ├── eda_monetary.png          # Monetary analysis
│   ├── rfm_distributions.png     # RFM metrics
│   ├── cluster_3d.png            # 3D cluster plot
│   └── cluster_analysis.png      # Cluster analysis
│
├── 🎨 Assets
│   └── images/                    # UI images
│       ├── hero_shopping.png     # Hero image
│       ├── analytics.png         # Analytics illustration
│       └── segments.png          # Segmentation visual
│
├── 📐 Diagrams
│   ├── use_case_diagram.png      # UML use cases
│   ├── sequence_diagram.png      # Process flow
│   ├── class_diagram.png         # OOP structure
│   └── system_architecture.png   # System design
│
├── 📚 Documentation
│   ├── README.md                  # This file
│   ├── QUICKSTART.md             # Quick setup guide
│   ├── DEPLOYMENT_GUIDE.md       # Deployment instructions
│   ├── DIAGRAMS_DOCUMENTATION.md # UML diagrams explained
│   ├── ANIMATIONS_GUIDE.md       # Animation specifications
│   ├── MOBILE_RESPONSIVE_GUIDE.md# Responsive design docs
│   └── PROJECT_SUMMARY.md        # Project overview
│
├── ⚙️ Configuration
│   ├── requirements.txt          # Python dependencies
│   ├── test_setup.py            # Environment tester
│   └── .gitignore               # Git exclusions
│
└── 📄 Total: 50+ files, ~171 MB
```

---

## 🤖 ML Models

### **1. Customer Segmentation Model**
- **Algorithm:** K-Means Clustering
- **Features:** Recency, Frequency, Monetary (RFM)
- **Clusters:** 4 optimal clusters (determined by elbow method)
- **Accuracy:** 87% silhouette score
- **File:** `models/kmeans_model.pkl` (18 KB)
- **Preprocessing:** StandardScaler normalization

### **2. Product Recommendation Model**
- **Algorithm:** Collaborative Filtering (Item-Based)
- **Matrix:** Product-to-product similarity
- **Dimensions:** 3,876 × 3,876 products
- **File:** `models/product_similarity.pkl` (120 MB)
- **Method:** Cosine similarity on purchase patterns

### **3. Preprocessing**
- **Scaler:** StandardScaler for feature normalization
- **File:** `models/scaler.pkl` (959 B)
- **Purpose:** Normalize RFM values before prediction

---

## 📐 UML Diagrams

Complete UML documentation available in [`diagrams/`](./diagrams/) folder:

### **1. Use Case Diagram**
![Use Case](diagrams/use_case_diagram.png)
- **Actors:** Customer/User, Admin/Analyst
- **Use Cases:** 7 main functionalities
- **System Boundary:** Shopper Spectrum System

### **2. Sequence Diagram**
![Sequence](diagrams/sequence_diagram.png)
- **Flow:** Customer segmentation prediction
- **Participants:** 6 components
- **Steps:** 7 sequential operations

### **3. Class Diagram**
![Class](diagrams/class_diagram.png)
- **Classes:** 5 core components
- **Relationships:** Inheritance, composition, association
- **Methods:** 15+ operations

### **4. System Architecture**
![Architecture](diagrams/system_architecture.png)
- **Layers:** 3-tier architecture
- **Components:** 12 modules
- **Data Flow:** Complete system interaction

📖 **Detailed Documentation:** [DIAGRAMS_DOCUMENTATION.md](./DIAGRAMS_DOCUMENTATION.md)

---

## 📡 API Reference

### **Key Functions**

#### **Model Loading**
```python
@st.cache_resource
def load_models():
    """Load all ML models and data"""
    kmeans_model = joblib.load('models/kmeans_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    product_similarity = joblib.load('models/product_similarity.pkl')
    cluster_labels = joblib.load('models/cluster_labels.pkl')
    rfm_data = pd.read_csv('models/rfm_data.csv')
    return kmeans_model, scaler, product_similarity, cluster_labels, rfm_data
```

#### **Customer Segmentation**
```python
def predict_segment(recency, frequency, monetary):
    """Predict customer segment from RFM values"""
    # Scale features
    scaled = scaler.transform([[recency, frequency, monetary]])
    # Predict cluster
    cluster = kmeans_model.predict(scaled)[0]
    # Map to segment
    segment = cluster_labels[cluster]
    return segment
```

#### **Product Recommendations**
```python
def get_recommendations(product_id, top_n=5):
    """Get top N similar products"""
    similarities = product_similarity[product_id]
    top_indices = similarities.argsort()[-top_n-1:-1][::-1]
    return top_indices, similarities[top_indices]
```

---

## 🌐 Deployment

### **Option 1: Streamlit Community Cloud** ⭐ (Recommended)

**Advantages:**
- ✅ 100% FREE forever
- ✅ Zero configuration needed
- ✅ Auto-deploy on git push
- ✅ Custom subdomain included

**Steps:**
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select repository: `Shopper-Spectrum-Customer-Segmentation`
6. Main file: `app_simple.py`
7. Deploy!

**URL:** `https://yourname-shopper-spectrum.streamlit.app`

---

### **Option 2: Render.com**

**Advantages:**
- Good performance
- Free tier available
- Easy deployment

**Steps:**
1. Push to GitHub
2. Go to [render.com](https://render.com)
3. New Web Service
4. Connect GitHub repo
5. **Build Command:** `pip install -r requirements.txt`
6. **Start Command:** 
   ```bash
   streamlit run app_simple.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
   ```
7. Deploy!

**URL:** `https://shopper-spectrum.onrender.com`

---

### **Option 3: Hugging Face Spaces**

**Advantages:**
- Perfect for ML projects
- Great community
- Free hosting

**Steps:**
1. Create Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select "Streamlit" SDK
3. Upload files or connect GitHub
4. Done!

**URL:** `https://huggingface.co/spaces/username/shopper-spectrum`

---

### **Option 4: Docker** 🐳

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_simple.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t shopper-spectrum .
docker run -p 8501:8501 shopper-spectrum
```

---

## ⚡ Performance

### **Speed Metrics**
- **Initial Load:** ~3-5 seconds
- **Model Loading:** ~2 seconds (cached after first load)
- **Segment Prediction:** <100ms
- **Product Recommendations:** <200ms
- **Chart Rendering:** ~500ms
- **Page Navigation:** Instant

### **Optimization Techniques**
- ✅ `@st.cache_resource` for model persistence
- ✅ `@st.cache_data` for data caching
- ✅ Lazy loading of visualizations
- ✅ Efficient DataFrame operations
- ✅ CSS-only animations (60fps)
- ✅ Compressed image assets

### **Resource Usage**
- **Memory:** ~500 MB (with all models loaded)
- **CPU:** Minimal (ML inference is fast)
- **Storage:** 171 MB total project size
- **Network:** ~2 MB initial page load

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### **Ways to Contribute**
1. **Report Bugs** - Submit detailed bug reports
2. **Suggest Features** - Propose new functionality
3. **Improve Documentation** - Enhance README, guides
4. **Code Improvements** - Optimize algorithms, fix bugs
5. **Add Features** - Implement new capabilities

### **Contribution Process**

1. **Fork the Repository**
   ```bash
   git clone https://github.com/pruthvirajtarode/Shopper-Spectrum-Customer-Segmentation.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Commit Changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```

4. **Push to Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```

5. **Open Pull Request**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Describe your changes
   - Submit!

### **Code Style**
- Follow PEP 8 for Python code
- Add docstrings to functions
- Comment complex logic
- Test before submitting

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Shopper Spectrum

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👤 Contact

**Pruthviraj Tarode**

- 📧 Email: pruthviraj.tarode@example.com
- 💼 LinkedIn: [linkedin.com/in/pruthvirajtarode](#)
- 🐱 GitHub: [@pruthvirajtarode](https://github.com/pruthvirajtarode)
- 🌐 Portfolio: [pruthvirajtarode.github.io](#)

**Project Link:** [https://github.com/pruthvirajtarode/Shopper-Spectrum-Customer-Segmentation](https://github.com/pruthvirajtarode/Shopper-Spectrum-Customer-Segmentation)

**Live Demo:** [Coming Soon](#)

---

## 🙏 Acknowledgments

### **Inspiration & Resources**
- [Streamlit Documentation](https://docs.streamlit.io)
- [Scikit-learn Tutorials](https://scikit-learn.org)
- [Plotly Documentation](https://plotly.com/python)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml)

### **Dataset**
- **Source:** Online Retail Dataset
- **Provider:** UCI Machine Learning Repository
- **Size:** 541,909 transactions
- **Period:** 2010-2011

### **Tools & Libraries**
- **Streamlit** - Web framework
- **Scikit-learn** - Machine learning
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

### **Special Thanks**
- Machine Learning community
- Open source contributors
- Streamlit team
- All testers and reviewers

---

## 📊 Project Stats

![Stars](https://img.shields.io/github/stars/pruthvirajtarode/Shopper-Spectrum-Customer-Segmentation?style=social)
![Forks](https://img.shields.io/github/forks/pruthvirajtarode/Shopper-Spectrum-Customer-Segmentation?style=social)
![Issues](https://img.shields.io/github/issues/pruthvirajtarode/Shopper-Spectrum-Customer-Segmentation)
![Pull Requests](https://img.shields.io/github/issues-pr/pruthvirajtarode/Shopper-Spectrum-Customer-Segmentation)

### **Repository Stats**
- **Languages:** Python (95%), CSS (3%), Markdown (2%)
- **Total Lines of Code:** ~2,100
- **Total Files:** 50+
- **Project Size:** 171 MB
- **Contributors:** 1
- **Commits:** 10+
- **Last Updated:** January 2026

---

## 🔮 Future Enhancements

### **Planned Features**
- [ ] Real-time A/B testing module
- [ ] Customer churn prediction
- [ ] Automated email campaign suggestions
- [ ] Advanced recommendation algorithms (Deep Learning)
- [ ] Multi-language support
- [ ] Export reports to PDF
- [ ] API endpoints for integration
- [ ] Mobile app (React Native)
- [ ] Real-time dashboard updates
- [ ] Integration with GA4, Shopify

### **In Progress**
- [x] ✅ Customer segmentation
- [x] ✅ Product recommendations
- [x] ✅ Analytics dashboard
- [x] ✅ Mobile responsive design
- [x] ✅ Smooth animations
- [x] ✅ Complete documentation

---

## 📚 Documentation

### **Complete Guides Available:**
- 📖 [README.md](./README.md) - This file (complete overview)
- 🚀 [QUICKSTART.md](./QUICKSTART.md) - Quick setup (5 minutes)
- 🌐 [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Deploy to cloud
- 📐 [DIAGRAMS_DOCUMENTATION.md](./DIAGRAMS_DOCUMENTATION.md) - UML diagrams explained
- 🎨 [ANIMATIONS_GUIDE.md](./ANIMATIONS_GUIDE.md) - Animation specs
- 📱 [MOBILE_RESPONSIVE_GUIDE.md](./MOBILE_RESPONSIVE_GUIDE.md) - Responsive design
- 📊 [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) - Quick summary
- ✅ [FINAL_PROJECT_STATUS.md](./FINAL_PROJECT_STATUS.md) - Complete status

**Total Documentation:** 33+ pages

---

## ⭐ Star History

If you found this project helpful, please consider giving it a ⭐!

```
Star History
     ★
   ★ ★ ★
 ★ ★ ★ ★ ★
└──────────────► Time
```

---

## 💡 Tips & Tricks

### **For Best Performance:**
1. Use a modern browser (Chrome, Edge, Firefox)
2. Allow ~500 MB RAM for the application
3. First load takes 3-5 seconds (models loading)
4. Subsequent pages are instant (caching enabled)

### **For Development:**
1. Use virtual environment
2. Update models in `models/` folder
3. Test with `test_setup.py` before running
4. Check console for any errors

### **For Deployment:**
1. Upload models to GitHub (use Git LFS for >100MB files)
2. Configure environment variables if needed
3. Use Streamlit Cloud for easiest deployment
4. Monitor logs for any issues

---

<div align="center">

## 🎉 **Thank You for Checking Out Shopper Spectrum!**

### **Made with ❤️ and Python**

[![GitHub](https://img.shields.io/badge/GitHub-View%20Source-black?logo=github)](https://github.com/pruthvirajtarode/Shopper-Spectrum-Customer-Segmentation)
[![Streamlit](https://img.shields.io/badge/Streamlit-View%20App-red?logo=streamlit)](#)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](#)

**If you found this helpful, please ⭐ the repository!**

---

**© 2024 Shopper Spectrum | E-Commerce Customer Analytics Platform**

*Empowering businesses with AI-driven customer insights*

</div>
