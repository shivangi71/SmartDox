# 🚀 SmartDOX Deployment Guide

Complete guide for deploying the SmartDOX Streamlit application to production.

## 📊 Deployment Options Comparison

| Option | Setup Time | Cost | Scalability | Best For |
|--------|-----------|------|-------------|----------|
| **Streamlit Cloud** | 5 min | Free/$9/mo | Low | Quick demos, MVPs |
| **Docker + VPS** | 30 min | $5-20/mo | High | Full control, production |
| **Google Cloud Run** | 15 min | $0.00001667/GB-sec | Auto | Serverless, no ops |
| **Azure Container** | 15 min | $0.0125/hour | Medium | Enterprise, Azure ecosystem |
| **Heroku** | 10 min | ~$5/mo | Medium | Quick deployment, free tier gone |
| **AWS ECS** | 30 min | $5-50/mo | Very High | Enterprise scale |
| **Self-hosted VPS** | 45 min | $3-10/mo | Manual | Maximum control |

---

## 🚀 RECOMMENDED: Docker + Google Cloud Run (Production)

**Why?** Free tier available, auto-scaling, minimal DevOps

### Step 1: Setup Google Cloud Project
```bash
# Install Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Create project
gcloud projects create smartdox-prod --set-as-default

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Configure Docker
gcloud auth configure-docker
```

### Step 2: Build & Push Image
```bash
# Set variables
PROJECT_ID=$(gcloud config get-value project)
REGION=us-central1
IMAGE_NAME=smartdox-streamlit

# Build image
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$IMAGE_NAME/$IMAGE_NAME:latest .

# Create Artifact Registry repository (first time only)
gcloud artifacts repositories create $IMAGE_NAME \
    --repository-format=docker \
    --location=$REGION

# Push image
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$IMAGE_NAME/$IMAGE_NAME:latest
```

### Step 3: Deploy to Cloud Run
```bash
gcloud run deploy smartdox-streamlit \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/$IMAGE_NAME/$IMAGE_NAME:latest \
  --platform managed \
  --region $REGION \
  --set-env-vars API_BASE_URL=https://your-backend-api.com \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --allow-unauthenticated \
  --port 8501
```

**Result:** Your app is live at the provided Cloud Run URL ✅

---

## ☁️ EASY: Streamlit Cloud (Free & Fastest)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add Streamlit app"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click "New App"
3. Select repository: `shivangi71/SmartDox`
4. Select branch: `main`
5. Select file: `app.py`
6. Click "Deploy"

### Step 3: Add Secrets
1. Go to app settings (gear icon)
2. Secrets section
3. Add:
```toml
[secrets]
API_BASE_URL = "https://your-backend-api.com"
```

**Done!** Share the public URL with your team 🎉

---

## 🐳 PROFESSIONAL: Docker + VPS (Full Control)

### Step 1: Prepare VPS
Follow [DEPLOYMENT_VPS.md](DEPLOYMENT_VPS.md) for detailed Ubuntu/Debian setup.

**Quick summary:**
```bash
# SSH into VPS
ssh user@your-vps-ip

# Quick setup
wget https://raw.githubusercontent.com/shivangi71/SmartDox/main/deploy.sh
bash deploy.sh
```

### Step 2: Manual Docker Deployment
```bash
# On your machine, push to Docker Hub
docker build -t your-username/smartdox-streamlit:latest .
docker push your-username/smartdox-streamlit:latest

# On VPS, pull and run
docker run -d \
  --name smartdox \
  -p 80:8501 \
  -e API_BASE_URL=http://backend:8000 \
  your-username/smartdox-streamlit:latest
```

### Step 3: Using Docker Compose (Recommended)
```bash
# On VPS
mkdir -p /opt/smartdox
cd /opt/smartdox
git clone https://github.com/shivangi71/SmartDox.git .

# Create backend Dockerfile if needed
# Deploy both services
docker-compose up -d

# Check logs
docker-compose logs -f streamlit
```

---

## ☁️ Azure Deployment

### Option A: Azure Container Instances
```bash
# Create resource group
az group create --name smartdox-rg --location eastus

# Create container registry
az acr create --resource-group smartdox-rg \
  --name smartdoxregistry --sku Basic

# Build and push
az acr build --registry smartdoxregistry \
  --image smartdox-streamlit:latest .

# Deploy container
az container create \
  --resource-group smartdox-rg \
  --name smartdox-streamlit \
  --image smartdoxregistry.azurecr.io/smartdox-streamlit:latest \
  --registry-login-server smartdoxregistry.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --ports 80 \
  --environment-variables API_BASE_URL=https://your-backend
```

### Option B: Azure App Service
```bash
# Create App Service Plan
az appservice plan create \
  --name smartdox-plan \
  --resource-group smartdox-rg \
  --sku B1 --is-linux

# Create Web App
az webapp create \
  --resource-group smartdox-rg \
  --plan smartdox-plan \
  --name smartdox-streamlit \
  --runtime "PYTHON:3.10"
```

---

## 🟨 AWS Deployment Options

### Option A: AWS ECS + Fargate (Recommended)
```bash
# Create ECR repository
aws ecr create-repository --repository-name smartdox-streamlit

# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <your-ecr-uri>

# Build and push
docker build -t smartdox-streamlit:latest .
docker tag smartdox-streamlit:latest <your-ecr-uri>/smartdox-streamlit:latest
docker push <your-ecr-uri>/smartdox-streamlit:latest

# Create ECS task definition and service
# (Use AWS Console for easier setup)
```

### Option B: AWS Lambda + Docker
```bash
# Package for Lambda
docker build --tag smartdox-lambda .

# Note: Streamlit requires specific setup for Lambda
# Alternative: Use EC2 instance or App Runner instead
```

### Option C: AWS App Runner (Easiest)
```bash
# Just connect your GitHub repo
# AWS will auto-build and deploy from Dockerfile
```

---

## 🟧 Google Cloud Options

### Option A: Cloud Run (Recommended)
See "RECOMMENDED" section above

### Option B: Google App Engine
```bash
# Create app.yaml
cat > app.yaml << EOF
runtime: python310
env: flex
entrypoint: streamlit run app.py --server.address=0.0.0.0 --server.port=8080
env_variables:
  API_BASE_URL: "https://your-backend-api.com"
EOF

# Deploy
gcloud app deploy
```

### Option C: Compute Engine (VM)
```bash
# Create VM
gcloud compute instances create smartdox-vm \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud

# SSH and setup manually
gcloud compute ssh smartdox-vm

# Then follow VPS deployment guide
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
```bash
# Never commit secrets!
echo ".env" >> .gitignore
echo "*.db" >> .gitignore

# Use platform-specific secret management:
# - Streamlit Secrets
# - AWS Secrets Manager
# - Azure Key Vault
# - Google Secret Manager
```

### 2. SSL/TLS Certificates
```bash
# For VPS with Nginx:
sudo certbot --nginx -d your-domain.com

# For cloud platforms: Usually automatic with HTTPS
```

### 3. API Authentication
```python
# Add authentication to API calls:
API_KEY = os.getenv("API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}
response = requests.post(url, headers=headers, json=data)
```

### 4. Database Backup
```bash
# Regular backups
sudo cp -r /opt/smartdox/backend/smartdox.db /backup/smartdox.db.backup

# For production: Use managed database (RDS, Cloud SQL)
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
      
      - name: Configure Docker
        run: gcloud auth configure-docker
      
      - name: Build & Push
        run: |
          docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/smartdox-streamlit:latest .
          docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/smartdox-streamlit:latest
      
      - name: Deploy
        run: |
          gcloud run deploy smartdox-streamlit \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/smartdox-streamlit:latest \
            --region us-central1 \
            --set-env-vars API_BASE_URL=${{ secrets.API_BASE_URL }}
```

---

## 📊 Performance Tuning

### For High Traffic
```dockerfile
# In Dockerfile, use production WSGI server:
RUN pip install gunicorn
CMD ["gunicorn", "--workers", "4", "--threads", "4", "--worker-class", "gthread", "--timeout", "60", "app:app"]
```

### Caching Strategy
```python
# In app.py
import streamlit as st

@st.cache_data
def load_model():
    # Load expensive model once
    return model

@st.cache_resource
def get_db_connection():
    # Connection reused across sessions
    return db_connection()
```

### Monitoring
```bash
# Google Cloud: Enable monitoring
gcloud logging sink create smartdox-logs \
  logging.googleapis.com/projects/$PROJECT_ID/logs

# Azure: Application Insights
# AWS: CloudWatch
```

---

## ✅ Pre-Deployment Checklist

- [ ] All secrets in `.env` (not in git)
- [ ] API_BASE_URL configured correctly
- [ ] Backend API is accessible from deployment
- [ ] Tesseract installed (for Docker image)
- [ ] All dependencies in requirements file
- [ ] `.gitignore` excludes sensitive files
- [ ] `docker-compose.yml` tested locally
- [ ] SSL/TLS certificates configured
- [ ] Monitoring/logging setup
- [ ] Backup strategy in place
- [ ] Domain name configured (if using custom domain)
- [ ] Health checks working

---

## 🆘 Troubleshooting

### App crashes on startup
```bash
# Check logs
docker logs smartdox

# Verify Python version
python3 --version  # Should be 3.8+

# Test locally first
streamlit run app.py
```

### API connection errors
```bash
# Verify backend is running
curl http://backend-api-url:8000

# Check .env file
cat .env | grep API_BASE_URL

# Update in deployment if needed
```

### Tesseract not found
```bash
# Already included in Dockerfile
# If using different base image, ensure:
RUN apt-get install -y tesseract-ocr
```

### Out of memory
```bash
# Increase container resources
# Google Cloud Run: --memory 2Gi --cpu 2
# Docker: -m 2g
# Azure: --memory 2.0
```

---

## 📞 Support Resources

- **Streamlit Docs**: https://docs.streamlit.io/deploy
- **Docker Docs**: https://docs.docker.com/
- **Cloud Platform Docs**:
  - Google Cloud: https://cloud.google.com/docs
  - Azure: https://docs.microsoft.com/azure
  - AWS: https://docs.aws.amazon.com

## 🎯 Next Steps

1. **Choose** your deployment platform
2. **Follow** the appropriate section above
3. **Test** thoroughly before production
4. **Monitor** logs and metrics
5. **Setup** alerts and backups
6. **Document** your deployment configuration

---

**Deployment Summary:**
- ⭐ **Recommended**: Docker + Google Cloud Run
- 🚀 **Fastest**: Streamlit Cloud
- 🔒 **Most Control**: VPS with Docker Compose
- 💰 **Most Affordable**: VPS ($3-10/mo)
- 🏢 **Enterprise**: AWS ECS or Azure AKS

Good luck with your deployment! 🎉
