# 🚀 DEPLOYMENT GUIDE - Shopper Spectrum

## 🏆 RECOMMENDED: Streamlit Community Cloud (FREE!)

### ✅ Why Streamlit Cloud?
- **100% FREE** - No credit card needed
- **Made for Streamlit** - Zero configuration
- **Auto-deploy** - Push to GitHub = instant update
- **Custom URL** - Get your own .streamlit.app domain
- **Easy management** - Simple dashboard

---

## 📋 STEP-BY-STEP DEPLOYMENT

### STEP 1: Prepare Your Files

#### 1.1 Handle Large Files (IMPORTANT!)

Your project has files > 100MB which GitHub won't accept:
- `product_similarity.pkl` = 120 MB ❌
- `online_retail.csv` = 48.5 MB ❌

**Option A: Use Git LFS (Large File Storage)**
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.pkl"
git lfs track "*.csv"
git add .gitattributes
```

**Option B: Upload to Cloud Storage (Recommended)**
1. Upload large files to Google Drive / Dropbox
2. Get shareable links
3. Download them in your app on startup

**Option C: Reduce File Sizes**
```python
# Use a sample dataset instead of full 48MB
# Compress the similarity matrix
```

#### 1.2 Create .gitattributes (for Git LFS)
```bash
echo "*.pkl filter=lfs diff=lfs merge=lfs -text" > .gitattributes
echo "*.csv filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
```

#### 1.3 Update .gitignore (if needed)
Make sure you're NOT ignoring important files:
```
__pycache__/
*.pyc
.env
.DS_Store
```

---

### STEP 2: Push to GitHub

#### 2.1 Create GitHub Repository
1. Go to https://github.com
2. Click "New repository"
3. Name: `shopper-spectrum`
4. Description: "E-Commerce Customer Segmentation & Product Recommendations"
5. Public or Private
6. Click "Create repository"

#### 2.2 Push Your Code
```bash
# Navigate to your project
cd "c:\Users\pruth\OneDrive\Desktop\Shopper Spectrum Customer Segmentation"

# Initialize Git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Shopper Spectrum ML App"

# Add remote (replace with YOUR GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/shopper-spectrum.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

### STEP 3: Deploy to Streamlit Cloud

#### 3.1 Sign Up
1. Go to: https://share.streamlit.io/
2. Click "Sign in"
3. Authorize with GitHub

#### 3.2 Deploy App
1. Click "New app" button
2. Fill in details:
   - **Repository**: Select `shopper-spectrum`
   - **Branch**: `main`
   - **Main file path**: `app_simple.py`
   - **App URL** (optional): `shopper-spectrum` or custom name

3. Click "Deploy!"

#### 3.3 Wait for Deployment
- Initial deployment: 3-5 minutes
- Streamlit will install dependencies from `requirements.txt`
- Watch the logs in realtime

#### 3.4 Done! 🎉
Your app will be live at:
```
https://YOUR-USERNAME-shopper-spectrum.streamlit.app
```

---

## 🔧 TROUBLESHOOTING

### Issue 1: Large Files Error
**Error:** "File exceeds GitHub's 100 MB file size limit"

**Solution:**
```bash
# Option 1: Use Git LFS
git lfs install
git lfs track "*.pkl"
git lfs track "*.csv"
git add .gitattributes
git add .
git commit --amend -m "Add large files with Git LFS"
git push -f origin main
```

**Solution 2: Download files at runtime**
```python
import requests
import os

def download_large_files():
    if not os.path.exists('online_retail.csv'):
        # Download from Google Drive or Dropbox
        url = 'YOUR_GOOGLE_DRIVE_LINK'
        response = requests.get(url)
        with open('online_retail.csv', 'wb') as f:
            f.write(response.content)
```

### Issue 2: Module Not Found
**Error:** "ModuleNotFoundError: No module named 'X'"

**Solution:** Make sure `requirements.txt` has all dependencies:
```txt
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
scipy>=1.11.0
streamlit>=1.26.0
plotly>=5.16.0
joblib>=1.3.0
Pillow>=10.0.0
```

### Issue 3: App Crashes
**Error:** App shows error on startup

**Solution:** Check Streamlit Cloud logs:
1. Go to your app dashboard
2. Click "Manage app"
3. View logs
4. Fix errors shown

### Issue 4: Slow Loading
**Problem:** App takes too long to load

**Solutions:**
1. Use `@st.cache_resource` for models (already done!)
2. Reduce model file sizes
3. Use sample dataset instead of full data
4. Lazy load heavy components

---

## 🎯 ALTERNATIVE DEPLOYMENT OPTIONS

### OPTION 2: Render.com (Free Tier)

**Pros:** Good performance, free tier
**Cons:** Slower than Streamlit Cloud

**Steps:**
1. Push to GitHub
2. Go to https://render.com
3. New → Web Service
4. Connect GitHub repo
5. Settings:
   - **Name:** shopper-spectrum
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app_simple.py --server.port=$PORT --server.address=0.0.0.0`
6. Create Web Service

**URL:** `https://shopper-spectrum.onrender.com`

---

### OPTION 3: Hugging Face Spaces (ML Focused)

**Pros:** Great for ML projects, good community
**Cons:** Different workflow

**Steps:**
1. Go to https://huggingface.co/spaces
2. Create new Space
3. Select "Streamlit" as SDK
4. Upload files or connect GitHub
5. Done!

**URL:** `https://huggingface.co/spaces/YOUR-USERNAME/shopper-spectrum`

---

### OPTION 4: Railway.app (Modern Platform)

**Pros:** Modern platform, simple
**Cons:** Limited free tier

**Steps:**
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select your repo
4. Add start command: `streamlit run app_simple.py --server.port=$PORT`
5. Deploy

---

## 📝 POST-DEPLOYMENT CHECKLIST

After deployment, verify:

- [ ] ✅ App loads without errors
- [ ] ✅ All 4 pages work (Home, Recommendations, Segmentation, Analytics)
- [ ] ✅ Models load successfully
- [ ] ✅ Images display correctly
- [ ] ✅ Animations are smooth
- [ ] ✅ Mobile responsive works
- [ ] ✅ Charts render properly
- [ ] ✅ Predictions work
- [ ] ✅ No console errors
- [ ] ✅ Loading time is reasonable (<10s)

---

## 🎨 CUSTOM DOMAIN (Optional)

### For Streamlit Cloud:
1. Go to app settings
2. Add custom domain
3. Update DNS records
4. Example: `shoppers.yourdomain.com`

---

## 🔄 AUTO-DEPLOYMENT

With Streamlit Cloud:
1. Make changes locally
2. Commit: `git commit -am "Update feature X"`
3. Push: `git push`
4. **App auto-updates!** ✨

No manual re-deployment needed!

---

## 💰 COST COMPARISON

| Platform | Free Tier | Pros | Best For |
|----------|-----------|------|----------|
| **Streamlit Cloud** | ✅ Free forever | Zero config, auto-deploy | Streamlit apps |
| **Render** | ✅ 750hrs/month | Good performance | Full-stack apps |
| **Hugging Face** | ✅ Free | ML community | ML showcases |
| **Railway** | ✅ $5 credit | Modern UI | New projects |
| **Heroku** | ❌ Paid only | Industry standard | Production apps |

---

## 🎯 RECOMMENDED PATH

```
1. Handle Large Files
   └─> Use Git LFS OR Upload to Google Drive

2. Push to GitHub
   └─> Create repo and push code

3. Deploy to Streamlit Cloud
   └─> Connect GitHub and deploy

4. Share Your Link!
   └─> https://YOUR-APP.streamlit.app

5. Keep Updating
   └─> Push to GitHub = Auto-deploy
```

---

## 🚀 QUICK START COMMANDS

```bash
# 1. Install Git LFS (one-time)
git lfs install

# 2. Track large files
git lfs track "models/*.pkl"
git lfs track "*.csv"

# 3. Add and commit
git add .
git commit -m "Shopper Spectrum - Production Ready"

# 4. Create GitHub repo, then:
git remote add origin https://github.com/YOUR-USERNAME/shopper-spectrum.git
git push -u origin main

# 5. Go to share.streamlit.io and deploy!
```

---

## ❓ NEED HELP?

**Streamlit Community:**
- Forum: https://discuss.streamlit.io
- Docs: https://docs.streamlit.io/streamlit-community-cloud

**GitHub Issues:**
- Create issue in your repo
- Community can help!

---

## 🎊 SUCCESS!

Once deployed, share your link:
```
🌐 https://YOUR-USERNAME-shopper-spectrum.streamlit.app
```

**Add to:**
- LinkedIn portfolio
- Resume
- GitHub README
- Personal website

---

**Good luck with deployment! 🚀✨**

*Made with ❤️ for Shopper Spectrum*
