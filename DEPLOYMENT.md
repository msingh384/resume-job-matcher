# 🚀 Production Deployment Guide

Complete guide for deploying Resume-Job Matcher to production.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you've completed:

- ✅ All tests pass (see [TESTING.md](TESTING.md))
- ✅ Application runs successfully in Docker
- ✅ Data persistence verified
- ✅ Environment variables configured
- ✅ Documentation reviewed and updated
- ✅ Security best practices followed

---

## 🐳 Docker Deployment (Recommended)

### Quick Start

```bash
# Build and start
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Access application
open http://localhost:5000
```

### Production Configuration

1. **Create environment file:**

```bash
cat > .env << EOF
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=0

# Database
DATABASE_PATH=/app/data/jobs.db

# File Upload
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=/tmp

# Optional: ML Mode
USE_ML_MODE=false
EOF
```

2. **Update docker-compose.yml for production:**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/status"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

3. **Start in production mode:**

```bash
docker-compose up -d
```

### Docker Management Commands

```bash
# Stop containers
docker-compose down

# Stop and remove volumes (WARNING: Deletes data!)
docker-compose down -v

# Restart
docker-compose restart

# View logs
docker-compose logs -f

# Execute commands in container
docker-compose exec app bash

# Update to latest
git pull
docker-compose up -d --build
```

---

## ☁️ Cloud Deployment Options

### Option 1: AWS ECS (Elastic Container Service)

1. **Build and push Docker image:**

```bash
# Login to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_URL

# Build image
docker build -t resume-job-matcher .

# Tag image
docker tag resume-job-matcher:latest YOUR_ECR_URL/resume-job-matcher:latest

# Push image
docker push YOUR_ECR_URL/resume-job-matcher:latest
```

2. **Create ECS Task Definition:**

```json
{
  "family": "resume-job-matcher",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "YOUR_ECR_URL/resume-job-matcher:latest",
      "memory": 512,
      "cpu": 256,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000
        }
      ],
      "environment": [
        {"name": "FLASK_ENV", "value": "production"}
      ],
      "mountPoints": [
        {
          "sourceVolume": "data",
          "containerPath": "/app/data"
        }
      ]
    }
  ],
  "volumes": [
    {
      "name": "data",
      "efsVolumeConfiguration": {
        "fileSystemId": "YOUR_EFS_ID"
      }
    }
  ]
}
```

### Option 2: Google Cloud Run

```bash
# Build and submit
gcloud builds submit --tag gcr.io/YOUR_PROJECT/resume-job-matcher

# Deploy
gcloud run deploy resume-job-matcher \
  --image gcr.io/YOUR_PROJECT/resume-job-matcher \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000 \
  --memory 1Gi
```

### Option 3: Heroku

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Add container registry
heroku container:login

# Build and push
heroku container:push web

# Release
heroku container:release web

# Open
heroku open
```

### Option 4: DigitalOcean App Platform

1. Connect your GitHub repository
2. Select "Docker" as runtime
3. Set port to 5000
4. Add environment variables
5. Deploy!

### Option 5: Railway.app

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

---

## 🖥️ VPS/Bare Metal Deployment

### Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Root or sudo access
- Domain name (optional but recommended)

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

### Step 2: Deploy Application

```bash
# Clone repository
git clone YOUR_REPO_URL
cd resume-job-matcher

# Create data directory
mkdir -p data

# Start application
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs
```

### Step 3: Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/resume-matcher
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Increase upload size limit
    client_max_body_size 20M;
}
```

Enable and start:

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/resume-matcher /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### Step 4: Setup SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

### Step 5: Setup Firewall

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

---

## 🔒 Security Hardening

### 1. Environment Variables

Never commit sensitive data. Use environment variables:

```bash
# Create .env file (not committed to git)
cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_PATH=/app/data/jobs.db
MAX_CONTENT_LENGTH=16777216
EOF
```

### 2. Update .gitignore

Ensure these are ignored:

```
.env
*.db
data/
__pycache__/
*.pyc
venv/
node_modules/
.DS_Store
```

### 3. Rate Limiting (Optional)

Add Flask-Limiter for API rate limiting:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)
```

### 4. HTTPS Only

Force HTTPS in production:

```python
from flask_talisman import Talisman

if not app.debug:
    Talisman(app)
```

### 5. Database Backups

Setup automatic backups:

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp data/jobs.db $BACKUP_DIR/jobs_$DATE.db
# Keep only last 30 days
find $BACKUP_DIR -name "jobs_*.db" -mtime +30 -delete
EOF

chmod +x backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

---

## 📊 Monitoring & Logging

### Docker Logs

```bash
# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f app

# Save logs to file
docker-compose logs > logs.txt
```

### Application Logs

Add logging to Flask app:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/data/app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Monitoring

Setup monitoring with UptimeRobot, Pingdom, or similar:
- Monitor: `https://your-domain.com/api/status`
- Check interval: 5 minutes
- Alert on failures

---

## 🔄 Updates & Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build

# Clean old images
docker image prune -a
```

### Database Migration

If database schema changes:

```bash
# Backup first!
cp data/jobs.db data/jobs.db.backup

# Run migration (if needed)
# docker-compose exec app python migrate.py
```

---

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs

# Check container status
docker-compose ps

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Out of Memory

```bash
# Check memory usage
docker stats

# Increase container memory in docker-compose.yml:
services:
  app:
    mem_limit: 1g
```

### Data Not Persisting

```bash
# Check volume mount
docker-compose config

# Verify data directory
ls -la data/

# Check permissions
sudo chown -R 1000:1000 data/
```

---

## 📈 Scaling

### Horizontal Scaling

For high traffic, run multiple instances:

```yaml
version: '3.8'

services:
  app:
    build: .
    deploy:
      replicas: 3
    ports:
      - "5000-5002:5000"
```

### Database Optimization

- Switch to PostgreSQL for better concurrency
- Add database connection pooling
- Implement caching (Redis)

---

## ✅ Post-Deployment Checklist

- [ ] Application accessible via domain
- [ ] HTTPS enabled and working
- [ ] Health check endpoint responding
- [ ] Data persisting after restart
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Logs accessible
- [ ] Firewall configured
- [ ] Documentation updated
- [ ] Team notified

---

## 🆘 Support

If you encounter issues:

1. Check logs: `docker-compose logs`
2. Review [TESTING.md](TESTING.md)
3. Search GitHub issues
4. Open new issue with details

---

**Congratulations! Your application is now in production! 🎉**

