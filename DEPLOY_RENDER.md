# 🚀 Deploy Backend to Render + Streamlit Cloud

Perfect setup: Backend on Render, Frontend on Streamlit Cloud

## 📊 Architecture

```
User Browser
    ↓
Streamlit Cloud (Frontend)
    ↓
Render (Backend API)
    ↓
SQLite Database
```

---

## 🎯 RECOMMENDED SETUP: Render + Streamlit Cloud

**Why?**
- ✅ Backend runs independently on Render
- ✅ Streamlit frontend on Streamlit Cloud (free tier)
- ✅ Auto-deploys on git push
- ✅ Easy environment variables management
- ✅ Built-in monitoring and logs

---

## 📝 Step 1: Prepare Backend for Render

### 1.1 Create `Procfile` (for Render to know how to run)
```bash
# In SmartDox/backend/ directory, create Procfile:
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 1.2 Create/Update `requirements.txt` for backend
```bash
# In SmartDox/backend/ directory:
pip freeze > requirements.txt

# Or manually create with all dependencies:
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
groq==0.4.2
pillow==10.0.1
PyMuPDF==1.24.2
pytesseract==0.3.10
deep-translator==1.11.4
pydantic==2.5.0
EOF
```

### 1.3 Create `render.yaml` (Infrastructure as Code - Optional but recommended)
```bash
# In SmartDox root directory:
cat > render.yaml << 'EOF'
services:
  - type: web
    name: smartdox-backend
    env: python
    plan: free
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GROQ_API_KEY
        scope: all
        sync: false
      - key: DATABASE_URL
        value: sqlite:///./smartdox.db
        scope: all
EOF
```

### 1.4 Update backend `.env` handling
Edit `backend/main.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Make sure API_KEY is optional
api_key = os.getenv("GROQ_API_KEY", "")
if not api_key:
    print("⚠️ Warning: GROQ_API_KEY not set")

# Render provides PORT environment variable
PORT = int(os.getenv("PORT", 8000))
```

---

## 🚀 Step 2: Deploy Backend to Render

### 2.1 Sign Up on Render
1. Go to https://render.com
2. Sign up with GitHub account
3. Authorize Render to access your repos

### 2.2 Create New Web Service
1. Click "New +" → "Web Service"
2. Select repository: `shivangi71/SmartDox`
3. Fill form:
   - **Name:** `smartdox-backend`
   - **Environment:** Python 3.10
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free (or paid for production)

### 2.3 Add Environment Variables
1. In Render dashboard, go to your service
2. Settings → Environment
3. Add variables:
   ```
   GROQ_API_KEY = your_groq_api_key_here
   DATABASE_URL = sqlite:///./smartdox.db
   ```

### 2.4 Deploy
1. Click "Deploy"
2. Wait for build (2-3 minutes)
3. Get your backend URL: `https://smartdox-backend.onrender.com`

### 2.5 Verify Backend is Running
```bash
# Test the API
curl https://smartdox-backend.onrender.com/

# Expected response:
# {"status": "SmartDOX API is Online"}
```

---

## 💻 Step 3: Deploy Frontend to Streamlit Cloud

### 3.1 Push Code to GitHub
```bash
git add .
git commit -m "Add Render deployment configs"
git push origin main
```

### 3.2 Deploy on Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click "New App"
3. Select repository: `shivangi71/SmartDox`
4. Select branch: `main`
5. Select file: `app.py`
6. Click "Deploy"

### 3.3 Update Streamlit Secrets
1. Click gear icon (Settings) on the app
2. Go to "Secrets"
3. Add your backend URL:
```toml
API_BASE_URL = "https://smartdox-backend.onrender.com"
```

### 3.4 Done!
Your app is live! Share the URL with your team.

---

## 🔄 How to Update

**Whenever you push to GitHub:**
1. **Backend automatically redeploys** on Render (if using auto-deploy)
2. **Frontend automatically redeploys** on Streamlit Cloud

### Enable Auto-Deploy on Render
1. Service Settings → Auto-Deploy
2. Select branch: `main`
3. Enable toggle

---

## ⚠️ Render Free Tier Limitations

| Feature | Free | Paid |
|---------|------|------|
| **Requests** | Limited | Unlimited |
| **Sleep** | Spins down after 15 min inactivity | Always running |
| **Storage** | Temporary (lost on redeploy) | Persistent |
| **Compute** | Shared | Dedicated |
| **Price** | Free | $7+/month |

### Workaround for Persistent Database
Use external database on Render:
```bash
# Create PostgreSQL database on Render
# Connect via DATABASE_URL environment variable
DATABASE_URL=postgresql://user:pass@host:5432/smartdox
```

---

## 🔧 Advanced: PostgreSQL Database on Render

### Create PostgreSQL Database
1. Render dashboard → "New +" → "PostgreSQL"
2. Name: `smartdox-db`
3. Select region
4. Click "Create Database"

### Update Backend to Use PostgreSQL
Edit `backend/database.py`:
```python
import os
from sqlalchemy import create_engine

# Use Render's PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./smartdox.db"  # Fallback for local dev
)

# For PostgreSQL, SQLAlchemy needs psycopg2
if "postgresql" in DATABASE_URL:
    # URL format from Render dashboard
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

engine = create_engine(DATABASE_URL)
```

### Add PostgreSQL Driver to requirements.txt
```bash
echo "psycopg2-binary==2.9.9" >> backend/requirements.txt
```

### Add to Render Environment Variables
```
DATABASE_URL = postgresql://user:pass@host:5432/smartdox
```

---

## 📊 Render vs Alternatives

| Platform | Backend | Frontend | Free | Notes |
|----------|---------|----------|------|-------|
| **Render** | ✅ Yes | ✅ Yes | ✅ Limited | Best for this setup |
| **Railway** | ✅ Yes | ✅ Yes | ✅ $5 credit | Good alternative |
| **Heroku** | ✅ Yes | ✅ Yes | ❌ No | Free tier removed |
| **Fly.io** | ✅ Yes | ✅ Yes | ✅ Generous | Very good option |
| **Replit** | ✅ Yes | ✅ Yes | ✅ Limited | Easy for beginners |
| **AWS** | ✅ Yes | ❌ No | ✅ Limited | Enterprise grade |

---

## 🛠️ Configuration File Updates Needed

### 1. Create/Update `backend/requirements.txt`
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
groq==0.4.2
pillow==10.0.1
PyMuPDF==1.24.2
pytesseract==0.3.10
deep-translator==1.11.4
pydantic==2.5.0
```

### 2. Create `backend/Procfile`
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3. Update `app.py` to use environment variable
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Use environment variable for API URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
```

### 4. In `app.py`, update requests to handle timeouts
```python
# Add timeouts for cloud API calls
response = requests.post(
    f"{API_BASE_URL}/login",
    json={"email": email, "password": password},
    timeout=10  # Add timeout
)
```

---

## 🔐 Security: Add API Authentication

To protect your backend from unauthorized access:

### Update `backend/main.py`
```python
from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY", "")

@app.post("/login")
async def login(
    request: Request,
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    # ... rest of code
```

### Update `app.py`
```python
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "")

def login_user(email, password):
    headers = {}
    if API_KEY:
        headers["x-api-key"] = API_KEY
    
    response = requests.post(
        f"{API_BASE_URL}/login",
        json={"email": email, "password": password},
        headers=headers,
        timeout=10
    )
    return response.json()
```

### Add to Streamlit Secrets
```toml
API_BASE_URL = "https://smartdox-backend.onrender.com"
API_KEY = "your_secret_api_key_here"
```

---

## 📋 Step-by-Step Deployment Checklist

### Backend (Render)
- [ ] Create `backend/requirements.txt`
- [ ] Create `backend/Procfile`
- [ ] Update `backend/main.py` for environment variables
- [ ] Push code to GitHub
- [ ] Sign up on Render.com
- [ ] Create Web Service on Render
- [ ] Add GROQ_API_KEY environment variable
- [ ] Deploy and get URL
- [ ] Test: `curl https://smartdox-backend.onrender.com/`

### Frontend (Streamlit Cloud)
- [ ] Update `app.py` to use API_BASE_URL from env
- [ ] Push code to GitHub (if not already)
- [ ] Sign up on Streamlit Cloud
- [ ] Connect GitHub repository
- [ ] Deploy app
- [ ] Add `API_BASE_URL` in Secrets
- [ ] Test login and document processing

### Verification
- [ ] Backend responds at `/`
- [ ] Frontend loads in browser
- [ ] User can sign up
- [ ] User can login
- [ ] Document upload works
- [ ] Evaluation completes

---

## 🐛 Troubleshooting

### Issue: "Connection refused" or timeout
**Cause:** Backend not responding  
**Solution:**
```bash
# Check Render logs
# Render Dashboard → Your Service → Logs

# Verify backend URL
curl https://smartdox-backend.onrender.com/

# Check if service is still running
# Render spins down free tier after 15 min inactivity
# Solution: Use paid tier or keep-alive service
```

### Issue: "GROQ_API_KEY not found"
**Solution:** Add environment variable in Render dashboard

### Issue: Database errors
**Solution:** Use PostgreSQL instead of SQLite
- Create PostgreSQL on Render
- Update DATABASE_URL
- Restart service

### Issue: Slow first request
**Solution:** Render free tier spins down services
- This is normal - first request after idle takes 10-30 seconds
- Upgrade to paid tier to avoid

---

## 🚀 Production Ready Setup

For production with high availability:

```bash
# 1. Use PostgreSQL instead of SQLite
# 2. Add caching layer (Redis)
# 3. Setup monitoring and alerts
# 4. Use paid tier on Render ($7+/month)
# 5. Setup backups
# 6. Add CDN for static files
# 7. Enable CORS properly
```

---

## 📚 Resources

- **Render Docs:** https://render.com/docs
- **Streamlit Deployment:** https://docs.streamlit.io/deploy/streamlit-community-cloud
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/
- **Railway (Alternative):** https://railway.app
- **Fly.io (Alternative):** https://fly.io

---

## 🎉 You're Done!

Your SmartDOX system is now:
- ✅ Backend running on Render
- ✅ Frontend on Streamlit Cloud  
- ✅ Auto-deploying from GitHub
- ✅ Accessible from anywhere
- ✅ Ready for production use

**Share your Streamlit Cloud URL with your team!**

---

## 💡 Next Steps

1. **Monitor performance** in Render dashboard
2. **Setup alerts** for errors
3. **Scale to paid tier** if needed
4. **Add more features** based on feedback
5. **Consider PostgreSQL** for better data persistence

Happy deploying! 🚀
