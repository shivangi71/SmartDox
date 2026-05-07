# 🚀 QUICK START: Render Deployment (5 Minutes)

## The Setup

```
┌─────────────────────┐
│  GitHub Repository  │
│  (Your Code)        │
└──────────┬──────────┘
           │
      ┌────┴────┐
      │          │
┌─────▼─────┐  ┌┴──────────────┐
│   Render  │  │ Streamlit     │
│ (Backend) │  │ Cloud         │
│  API      │  │ (Frontend)    │
└─────┬─────┘  └┬──────────────┘
      │         │
      └────┬────┘
           │
        Users 👥
```

---

## ✅ Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `backend/requirements.txt` exists
- [ ] `Procfile` exists in root
- [ ] `.env.example` in root
- [ ] Streamlit app uses `API_BASE_URL` env variable

---

## 🔧 Files You Need

```
SmartDox/
├── Procfile                           ← NEW: Tells Render how to run
├── backend/
│   ├── requirements.txt               ← NEW: Backend dependencies
│   ├── main.py                        ← Existing: Your FastAPI app
│   └── ...
├── app.py                             ← Updated: Uses API_BASE_URL env var
├── requirements_streamlit.txt         ← Existing: Frontend dependencies
└── .env.example                       ← Updated: Shows env vars
```

All files are created/updated. Just push to GitHub!

---

## 🚀 Step 1: Deploy Backend (2 minutes)

### 1.1 Go to https://render.com
- Sign up with GitHub (authorize Render)

### 1.2 Create Web Service
```
Click: New + → Web Service
```

### 1.3 Select Repository
```
Repository: shivangi71/SmartDox
Branch: main
```

### 1.4 Configure Service
```
Name:            smartdox-backend
Environment:     Python 3.10
Build Command:   pip install -r backend/requirements.txt
Start Command:   cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
Plan:            Free (or Starter if you want always-on)
```

### 1.5 Add Environment Variables
```
Settings → Environment
Add: GROQ_API_KEY = your_groq_api_key_here
```

### 1.6 Deploy
```
Click: Create Web Service
⏳ Wait 2-3 minutes...
✅ Copy the URL when done
   Example: https://smartdox-backend.onrender.com
```

---

## 🚀 Step 2: Deploy Frontend (2 minutes)

### 2.1 Go to https://streamlit.io/cloud

### 2.2 Create New App
```
Click: New app
Repository:  shivangi71/SmartDox
Branch:      main
File:        app.py
```

### 2.3 Deploy
```
Click: Deploy
⏳ Wait 1-2 minutes...
```

### 2.4 Add Secrets
```
Settings (⚙️) → Secrets

Paste this exactly:
API_BASE_URL = "https://smartdox-backend.onrender.com"

(Replace with YOUR Render URL from Step 1.6)
```

### 2.5 Done! ✅
```
✅ Frontend reloads automatically
✅ You get a public URL like:
   https://your-username-smartdox.streamlit.app
```

---

## 🔗 Share Your App

Send this URL to your team:
```
https://your-username-smartdox.streamlit.app
```

---

## 📝 Environment Variables Reference

### For Render (Backend)
```
GROQ_API_KEY        = your-groq-api-key
DATABASE_URL        = sqlite:///./smartdox.db  (auto)
```

### For Streamlit Cloud (Frontend)
```
API_BASE_URL        = https://smartdox-backend.onrender.com
```

---

## ⏰ First Request Takes Time?

Render free tier **spins down** after 15 minutes of inactivity.

**First request after idle:**
- Takes 30 seconds (normal)
- Subsequent requests are instant

**Solutions:**
- Use paid tier ($7/month) for always-on
- Keep-alive service (searches for "Render free tier uptime")

---

## 🐛 Troubleshooting

### "Cannot connect to backend"
```
✅ Check Render backend URL in Streamlit Secrets
✅ Verify Render service is running (check Render dashboard)
✅ Wait 30 seconds if Render is spinning up
```

### "GROQ_API_KEY error"
```
✅ Add GROQ_API_KEY in Render Environment Variables
✅ Click "Deploy" again
```

### "Render spins down my service"
```
✅ This is normal on free tier
✅ Upgrade to Starter ($7/month) for always-on
✅ Or accept 30-second startup delay
```

### Backend URL not updating in Streamlit
```
✅ Check Secrets are saved correctly
✅ Manual redeploy: Settings → Manual Deploy
```

---

## 📊 What's Included?

### Backend (Render)
- ✅ FastAPI server
- ✅ User authentication
- ✅ Document processing
- ✅ AI evaluation engine
- ✅ SQLite database
- ✅ Chatbot endpoint

### Frontend (Streamlit)
- ✅ Web interface
- ✅ File upload
- ✅ Results display
- ✅ History tracking
- ✅ Chatbot chat interface
- ✅ Multi-language support

---

## 🎯 Next Steps After Deployment

1. **Test the app**
   - Sign up with test account
   - Upload a test PDF
   - Verify evaluation works

2. **Monitor backend logs**
   - Render dashboard → Logs
   - Check for any errors

3. **Share with team**
   - Send Streamlit Cloud URL
   - They can sign up and use!

4. **Consider upgrades** (optional)
   - Render Starter ($7/mo) for always-on
   - Streamlit Community Cloud (free)
   - Or PostgreSQL for better data

---

## 💰 Cost Breakdown

| Service | Free | Paid |
|---------|------|------|
| **Render (Backend)** | Limited | $7/mo+ |
| **Streamlit (Frontend)** | Free | $20/mo |
| **Total Monthly** | Limited | ~$27+/mo |

**Best value:** Free tier for testing, $7/mo for production backend

---

## 🔐 Security Notes

1. **GROQ_API_KEY** - Keep secret, only in Render env vars
2. **API_BASE_URL** - Public, safe to share in Streamlit Secrets
3. **Database** - SQLite is local, consider PostgreSQL for production
4. **SSL/TLS** - Automatic on both platforms

---

## 📞 Still Need Help?

### Resources:
- **Render Docs:** https://render.com/docs
- **Streamlit Docs:** https://docs.streamlit.io/deploy
- **This Project:** Check DEPLOY_RENDER.md for detailed guide

### Quick Links:
- **Sign up Render:** https://render.com
- **Sign up Streamlit:** https://streamlit.io/cloud
- **Your GitHub:** https://github.com/shivangi71/SmartDox

---

## ✨ Success Indicators

You'll know it's working when:

✅ Backend URL works: `https://smartdox-backend.onrender.com/`  
✅ Frontend loads at Streamlit Cloud URL  
✅ Can sign up and login  
✅ Can upload documents  
✅ Can see evaluation results  
✅ Chatbot responds  

**If all 6 ✅, you're done!** 🎉

---

## 🚀 You're Live!

Your SmartDOX platform is now:
- Running on Render (backend)
- Served by Streamlit Cloud (frontend)
- Accessible from anywhere
- Auto-deploying from GitHub

**Congratulations!** 🎊

---

**Need custom deployment? See DEPLOYMENT_GUIDE.md for more options.**
