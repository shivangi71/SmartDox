@echo off
REM SmartDOX Render Deployment Script for Windows

echo =========================================
echo   SmartDOX Render Deployment Guide
echo =========================================
echo.
echo This script will guide you through deploying:
echo   - Backend API on Render
echo   - Frontend on Streamlit Cloud
echo.
echo Prerequisites:
echo   - GitHub account
echo   - Code pushed to GitHub (shivangi71/SmartDox)
echo   - Render.com account
echo   - Streamlit Community Cloud account
echo.

pause

echo.
echo STEP 1: Deploy Backend to Render
echo ================================
echo.
echo 1. Go to https://render.com
echo 2. Sign up/Login with GitHub
echo 3. Click "New +" then "Web Service"
echo 4. Select repository: shivangi71/SmartDox
echo 5. Fill in the form:
echo    - Name: smartdox-backend
echo    - Environment: Python 3.10
echo    - Build Command: pip install -r backend/requirements.txt
echo    - Start Command: cd backend ^&^& uvicorn main:app --host 0.0.0.0 --port $PORT
echo    - Plan: Free (or Starter for production)
echo 6. Click "Create Web Service"
echo 7. Go to Environment section and add:
echo    - GROQ_API_KEY = your_groq_api_key_here
echo 8. Wait for deployment (2-3 minutes)
echo 9. Copy the URL when done (e.g., https://smartdox-backend.onrender.com)
echo.

pause

echo.
echo STEP 2: Update Frontend with Backend URL
echo =========================================
echo.
echo The backend URL you copied will be used in Streamlit Cloud secrets.
echo.
echo STEP 3: Deploy Frontend to Streamlit Cloud
echo ============================================
echo.
echo 1. Go to https://streamlit.io/cloud
echo 2. Click "New app"
echo 3. Select:
echo    - Repository: shivangi71/SmartDox
echo    - Branch: main
echo    - File: app.py
echo 4. Click "Deploy"
echo 5. Once deployed, click Settings (gear icon)
echo 6. Go to "Secrets" and add:
echo    API_BASE_URL = https://smartdox-backend.onrender.com
echo    (Replace with your actual backend URL from Step 1)
echo 7. The app will automatically redeploy with the new secrets
echo.
echo DONE! Your app is now live! 🎉
echo.

echo.
echo Additional Notes:
echo ================
echo.
echo - Render free tier spins down after 15 min of inactivity
echo   (First request after inactivity takes 30 seconds)
echo - For production, upgrade to paid tier ($7+/month)
echo - Check deployment logs on Render dashboard for any errors
echo - Share your Streamlit Cloud URL with your team
echo.

pause
