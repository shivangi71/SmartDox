# Setup on Ubuntu/Debian VPS

## 1. SSH into your server
ssh user@your-server-ip

## 2. Update system
sudo apt update && sudo apt upgrade -y

## 3. Install dependencies
sudo apt install -y python3.10 python3.10-venv python3-pip \
    tesseract-ocr libsm6 libxext6 libxrender-dev \
    nginx curl git

## 4. Create app directory
sudo mkdir -p /opt/smartdox
sudo chown $USER:$USER /opt/smartdox
cd /opt/smartdox

## 5. Clone repository
git clone https://github.com/shivangi71/SmartDox.git .

## 6. Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

## 7. Install dependencies
pip install -r requirements_streamlit.txt

## 8. Configure environment
cp .env.example .env
nano .env  # Edit and set API_BASE_URL

## 9. Create systemd service
sudo cp smartdox-streamlit.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable smartdox-streamlit
sudo systemctl start smartdox-streamlit

## 10. Configure Nginx reverse proxy
sudo nano /etc/nginx/sites-available/smartdox

# Add this config:
upstream streamlit {
    server localhost:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/smartdox /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

## 11. Setup SSL with Let's Encrypt
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

## 12. Check status
sudo systemctl status smartdox-streamlit
curl http://localhost:8501
