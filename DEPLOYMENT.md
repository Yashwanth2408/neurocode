# 🚀 NeuroCode Production Deployment Guide

Complete guide for deploying NeuroCode to production servers.

## 📋 Prerequisites

- Ubuntu 20.04+ / Debian 11+ server
- 8GB+ RAM (16GB recommended)
- 20GB+ disk space
- Docker & Docker Compose installed
- Public IP or domain name (for webhook access)
- GitHub/GitLab account with repository access

---

## 🐳 Option 1: Docker Deployment (Recommended)

### Step 1: Clone Repository

git clone https://github.com/your-username/neurocode.git
cd neurocode

### Step 2: Configure Environment

cp .env.example .env
nano .env

**Required settings:**
GITHUB_TOKEN=ghp_your_token_here
GITHUB_WEBHOOK_SECRET=your_random_secret_here

### Step 3: Build & Start Container

Build image
docker-compose build

Start service
docker-compose up -d

Check logs
docker-compose logs -f

### Step 4: Verify Service

Health check
curl http://localhost:8000/health

Expected output:
{"status":"healthy","ollama_model":"codellama:7b-instruct",...}

### Step 5: Setup Reverse Proxy (Nginx)

**Install Nginx:**
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx

**Configure Nginx (`/etc/nginx/sites-available/neurocode`):**
server {
listen 80;
server_name neurocode.yourdomain.com;
location / {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
}


**Enable site:**
sudo ln -s /etc/nginx/sites-available/neurocode /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

**Setup SSL (Let's Encrypt):**
sudo certbot --nginx -d neurocode.yourdomain.com

---

## 💻 Option 2: Manual Deployment (Bare Metal)

### Step 1: Install System Dependencies

Update system
sudo apt update && sudo apt upgrade -y

Install Python
sudo apt install python3.10 python3-pip python3-venv -y

Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

### Step 2: Setup Application

Create app directory
sudo mkdir -p /opt/neurocode
sudo chown $USER:$USER /opt/neurocode
cd /opt/neurocode

Clone repository
git clone https://github.com/your-username/neurocode.git .

Create virtual environment
python3 -m venv venv
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

### Step 3: Configure Environment

cp .env.example .env
nano .env

### Step 4: Pull Ollama Model

ollama pull codellama:7b-instruct

### Step 5: Create Systemd Services

**Ollama service (`/etc/systemd/system/ollama.service`):**
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=ollama
ExecStart=/usr/local/bin/ollama serve
Restart=always

[Install]
WantedBy=multi-user.target

**NeuroCode service (`/etc/systemd/system/neurocode.service`):**
[Unit]
Description=NeuroCode Security Scanner
After=network.target ollama.service
Requires=ollama.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/neurocode
Environment="PATH=/opt/neurocode/venv/bin"
ExecStart=/opt/neurocode/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target

**Enable & start services:**
sudo systemctl daemon-reload
sudo systemctl enable ollama neurocode
sudo systemctl start ollama
sleep 5
sudo systemctl start neurocode

Check status
sudo systemctl status neurocode

---

## 🔗 GitHub Webhook Configuration

### Step 1: Generate Webhook Secret

python3 -c "import secrets; print(secrets.token_hex(32))"

Add this to `.env`:

GITHUB_WEBHOOK_SECRET=your_generated_secret

### Step 2: Configure GitHub Webhook

1. Go to your repository: `https://github.com/username/repo/settings/hooks`
2. Click **Add webhook**
3. Configure:
   - **Payload URL:** `https://neurocode.yourdomain.com/webhook/github`
   - **Content type:** `application/json`
   - **Secret:** (paste your GITHUB_WEBHOOK_SECRET)
   - **Events:** Select `Pull requests`
4. Click **Add webhook**

### Step 3: Test Webhook

Create a test PR and check:
Docker logs
docker-compose logs -f

Or systemd logs
sudo journalctl -u neurocode -f

---

## 🔑 GitHub Token Setup

### Create Personal Access Token

1. Go to: `https://github.com/settings/tokens`
2. Click **Generate new token (classic)**
3. Name: `NeuroCode Scanner`
4. Scopes required:
   - ✅ `repo` (all)
   - ✅ `read:org`
5. Click **Generate token**
6. Copy token immediately (won't be shown again)

Add to `.env`:
GITHUB_TOKEN=ghp_your_token_here

---

## 📊 Monitoring & Maintenance

### Check Service Health

Docker
docker-compose ps
docker-compose logs --tail=100

Manual
systemctl status neurocode ollama
journalctl -u neurocode --since "1 hour ago"

### Monitor Resources

CPU/Memory
htop

Disk space
df -h
du -sh /root/.ollama # Ollama models

Docker stats
docker stats neurocode-scanner

### Update Application

Docker
cd /path/to/neurocode
git pull
docker-compose down
docker-compose build
docker-compose up -d

Manual
cd /opt/neurocode
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart neurocode

---

## 🛡️ Security Best Practices

1. **Firewall Configuration:**
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable


2. **Regular Updates:**
sudo apt update && sudo apt upgrade -y
pip install --upgrade -r requirements.txt

3. **Secure Environment Variables:**
- Never commit `.env` to git
- Use strong webhook secrets
- Rotate tokens periodically

4. **Backup Ollama Models:**
tar -czf ollama-backup.tar.gz /root/.ollama

---

## 🐛 Troubleshooting

### API Not Starting

Check if port is already in use
sudo lsof -i :8000

Check Python errors
python main.py # Run in foreground to see errors

### Ollama Connection Issues

Test Ollama
curl http://localhost:11434/api/version

Restart Ollama
sudo systemctl restart ollama

### Webhook Not Triggering

1. Check GitHub webhook delivery logs
2. Verify firewall allows incoming traffic
3. Check webhook secret matches
4. Review application logs

---

## 📈 Performance Optimization

### For High-Load Deployments

1. **Increase worker processes** (edit `main.py`):
uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)

2. **Use Gunicorn** (more production-ready):
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

3. **Add Redis for task queue** (for parallel scanning):
docker-compose.yml:
services:
redis:
image: redis:alpine

---

## 🎯 Next Steps

- ✅ Deploy to production server
- ✅ Configure GitHub webhooks
- ✅ Test with real PRs
- ⬜ Add more language support
- ⬜ Implement caching for faster scans
- ⬜ Add dashboard for scan history

---

**🎉 You're now ready for production deployment!**
