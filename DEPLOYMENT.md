# 🚀 Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the AI Medical Record Extractor to various platforms.

## Table of Contents

- [Quick Start](#quick-start)
- [Deployment Options](#deployment-options)
- [Environment Setup](#environment-setup)
- [Production Configuration](#production-configuration)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring](#monitoring)

---

## Quick Start

### Prerequisites

- Docker (recommended) or Python 3.8+ and Node.js 16+
- Git
- SSL certificate (for production)

### Fastest Deployment (Docker)

```bash
# Clone repository
git clone <your-repo-url>
cd ai-medical-record-extractor

# Deploy with Docker Compose
docker-compose up -d

# Access application
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## Deployment Options

### Option 1: Docker Compose (Recommended)

**Best for**: Production deployments, easy scaling, consistent environments

#### Steps:

1. **Create `docker-compose.yml`** (if not exists):
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_PATH=/app/data/medical_records.db
      - UPLOAD_DIR=/app/uploads
    volumes:
      - ./data:/app/data
      - ./uploads:/app/uploads
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  data:
  uploads:
```

2. **Create `Dockerfile`** in root:
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY .env.example .env

# Create directories
RUN mkdir -p uploads data

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. **Create `frontend/Dockerfile`**:
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

4. **Create `frontend/nginx.conf`**:
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Deploy**:
```bash
docker-compose up -d
```

---

### Option 2: Manual Deployment

**Best for**: Custom configurations, learning purposes

#### Backend Deployment

1. **Server Setup** (Ubuntu/Debian):
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip tesseract-ocr

# Install Nginx
sudo apt install -y nginx

# Install Supervisor (for process management)
sudo apt install -y supervisor
```

2. **Application Setup**:
```bash
# Create application directory
sudo mkdir -p /opt/medical-extractor
sudo chown $USER:$USER /opt/medical-extractor

# Clone repository
git clone <your-repo-url> /opt/medical-extractor
cd /opt/medical-extractor

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p uploads data logs

# Create environment file
cp .env.example .env
# Edit .env with production settings
```

3. **Create Supervisor Config** (`/etc/supervisor/conf.d/medical-extractor.conf`):
```ini
[program:medical-extractor]
directory=/opt/medical-extractor
command=/opt/medical-extractor/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
environment=PYTHONPATH="/opt/medical-extractor"
stdout_logfile=/opt/medical-extractor/logs/backend.log
stderr_logfile=/opt/medical-extractor/logs/backend-error.log
```

4. **Create Nginx Config** (`/etc/nginx/sites-available/medical-extractor`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /opt/medical-extractor/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # File uploads
    location /uploads {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

5. **Enable and Start Services**:
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/medical-extractor /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Start backend
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start medical-extractor
```

#### Frontend Deployment

1. **Build Frontend**:
```bash
cd /opt/medical-extractor/frontend

# Install dependencies
npm ci --only=production

# Build for production
npm run build

# Copy to Nginx directory
sudo cp -r dist/* /opt/medical-extractor/frontend/dist/
```

---

### Option 3: Cloud Platforms

#### Vercel (Frontend)

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Deploy**:
```bash
cd frontend
vercel --prod
```

3. **Configure** (`vercel.json`):
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-backend-url.com/$1"
    }
  ]
}
```

#### Railway (Backend)

1. **Create `railway.toml`**:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn src.api.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10
```

2. **Deploy**:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### Render

1. **Create `render.yaml`**:
```yaml
services:
  - type: web
    name: medical-extractor-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: DATABASE_PATH
        value: /opt/render/project/src/data/medical_records.db
      - key: UPLOAD_DIR
        value: /opt/render/project/src/uploads

  - type: web
    name: medical-extractor-frontend
    env: static
    buildCommand: npm install && npm run build
    staticPublishPath: ./dist
    routes:
      - type: rewrite
        source: /api/*
        destination: https://medical-extractor-backend.onrender.com/*
```

---

## Environment Setup

### Production Environment Variables

Create `.env` for production:

```env
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_RELOAD=false
LOG_LEVEL=INFO

# Database
DATABASE_PATH=/app/data/medical_records.db
DB_POOL_SIZE=5

# File Upload
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=.pdf,.txt,.png,.jpg,.jpeg,.bmp,.tiff

# CORS (Update with your frontend URL)
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com

# OCR (Optional)
TESSERACT_CMD=/usr/bin/tesseract

# Security
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32
```

### Frontend Environment Variables

Create `frontend/.env.production`:

```env
VITE_API_URL=https://your-backend-url.com
VITE_APP_TITLE=AI Medical Record Extractor
```

---

## Production Configuration

### Backend Configuration

1. **Update `src/api/main.py`** for production:
```python
# Add production middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["your-domain.com", "www.your-domain.com"]
)

# Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate limiting (optional)
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

2. **Create Production Startup Script** (`start_prod.sh`):
```bash
#!/bin/bash
# Production startup script

echo "Starting AI Medical Record Extractor..."

# Create directories
mkdir -p uploads data logs

# Activate virtual environment
source venv/bin/activate

# Start backend with Gunicorn
gunicorn src.api.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --capture-output \
    --log-level info
```

3. **Make executable**:
```bash
chmod +x start_prod.sh
```

### Frontend PWA Configuration

1. **Install PWA plugin**:
```bash
cd frontend
npm install -D vite-plugin-pwa
```

2. **Update `vite.config.js`**:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
      manifest: {
        name: 'AI Medical Record Extractor',
        short_name: 'MedExtractor',
        description: 'Offline-first medical record extraction',
        theme_color: '#6366f1',
        background_color: '#ffffff',
        display: 'standalone',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'google-fonts-cache',
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
              }
            }
          }
        ]
      }
    })
  ]
})
```

3. **Create PWA icons**:
   - `pwa-192x192.png` (192x192 pixels)
   - `pwa-512x512.png` (512x512 pixels)
   - Place in `frontend/public/`

---

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio
          
      - name: Run tests
        run: pytest tests/ -v

  build-and-deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t medical-extractor-backend .
        
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker tag medical-extractor-backend ${{ secrets.DOCKER_USERNAME }}/medical-extractor-backend:latest
          docker push ${{ secrets.DOCKER_USERNAME }}/medical-extractor-backend:latest

  build-and-deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci
        
      - name: Build
        working-directory: ./frontend
        run: npm run build
        
      - name: Deploy to Vercel
        working-directory: ./frontend
        run: |
          npm install -g vercel
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

### GitLab CI/CD

Create `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

test:
  stage: test
  image: python:3.11
  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-asyncio
  script:
    - pytest tests/ -v
  cache:
    paths:
      - .pytest_cache

build-backend:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE/backend .
    - docker push $CI_REGISTRY_IMAGE/backend
  only:
    - main

build-frontend:
  stage: build
  image: node:18
  cache:
    paths:
      - frontend/node_modules/
  script:
    - cd frontend
    - npm ci
    - npm run build
  artifacts:
    paths:
      - frontend/dist/
    expire_in: 1 week
  only:
    - main

deploy-production:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - chmod 700 ~/.ssh
  script:
    - ssh -o StrictHostKeyChecking=no $SSH_USER@$SSH_HOST "cd /opt/medical-extractor && git pull"
    - ssh -o StrictHostKeyChecking=no $SSH_USER@$SSH_HOST "cd /opt/medical-extractor && docker-compose up -d --build"
  environment:
    name: production
    url: https://your-domain.com
  only:
    - main
```

---

## Monitoring

### Health Checks

The application includes built-in health endpoints:

- `GET /` - Basic health status
- `GET /health` - Detailed health check

### Monitoring Setup

1. **Uptime Monitoring** (UptimeRobot, Pingdom):
   - Monitor `https://your-domain.com/health`
   - Alert on downtime

2. **Log Aggregation** (optional):
```bash
# Install Filebeat for log shipping
# Configure to send logs to ELK stack or similar
```

3. **Metrics** (optional):
```python
# Add to src/api/main.py
from prometheus_client import Counter, Histogram
import time

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    request_count.inc()
    request_duration.observe(time.time() - start_time)
    return response
```

---

## Post-Deployment Checklist

- [ ] Application is accessible via domain
- [ ] HTTPS is configured (SSL certificate)
- [ ] Backend API is responding
- [ ] Frontend loads correctly
- [ ] File upload works
- [ ] Text extraction works
- [ ] Database is persisting data
- [ ] Logs are being generated
- [ ] Health checks pass
- [ ] Error monitoring is active
- [ ] Backup strategy is in place
- [ ] Environment variables are set
- [ ] CORS is configured correctly
- [ ] Rate limiting is enabled (if needed)

---

## Troubleshooting

### Common Issues

1. **Port already in use**:
```bash
# Find process using port
sudo lsof -i :8000
# Kill process
sudo kill -9 <PID>
```

2. **Permission errors**:
```bash
# Fix directory permissions
sudo chown -R www-data:www-data /opt/medical-extractor
```

3. **Database locked**:
```bash
# Ensure only one process accesses SQLite
# Consider using WAL mode
```

---

## Support

For deployment issues:
- Check logs: `/opt/medical-extractor/logs/`
- Review Nginx logs: `/var/log/nginx/`
- Check Supervisor status: `sudo supervisorctl status`

---

## License

Same as main project - GNU General Public License v3.0