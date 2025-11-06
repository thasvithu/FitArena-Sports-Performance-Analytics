# 🐳 FitArena Deployment Guide

Complete guide for deploying the FitArena Sports Performance Analytics Platform.

## 📋 Table of Contents

1. [Quick Start with Docker](#quick-start-with-docker)
2. [Manual Deployment](#manual-deployment)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [SSL/HTTPS Setup](#sslhttps-setup)
7. [Monitoring & Logging](#monitoring--logging)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start with Docker

The easiest way to deploy FitArena is using Docker Compose.

### Prerequisites
- Docker 20.10+
- Docker Compose 1.29+
- 4GB RAM minimum
- 10GB disk space

### Steps

```powershell
# 1. Navigate to deployment folder
cd deployment

# 2. Copy environment template
Copy-Item .env.example .env

# 3. Edit .env file with your settings
notepad .env

# 4. Start all services
docker-compose up -d

# 5. Check status
docker-compose ps

# 6. View logs
docker-compose logs -f

# 7. Access platform
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api/docs
```

### Docker Commands

```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f [service_name]

# Rebuild containers
docker-compose up -d --build

# Remove everything (including volumes)
docker-compose down -v
```

---

## 🔧 Manual Deployment

For more control, deploy each component manually.

### 1. Database Setup

**Install PostgreSQL:**
```powershell
# Download from: https://www.postgresql.org/download/
# Or use Chocolatey:
choco install postgresql

# Start PostgreSQL service
Start-Service postgresql-x64-13
```

**Create Database:**
```powershell
psql -U postgres
```
```sql
CREATE DATABASE fitarena;
CREATE USER fitarena_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fitarena TO fitarena_user;
\q
```

### 2. Backend Deployment

```powershell
# Navigate to backend
cd ../backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
Copy-Item .env.example .env
notepad .env

# Run setup
python setup.py

# Train ML models (optional)
python train_models.py

# Start API server
cd src/api
python main.py
```

**Backend will run on:** http://localhost:8000

### 3. Frontend Deployment

```powershell
# Navigate to frontend
cd ../../frontend

# Install dependencies
npm install

# Create .env file
Copy-Item .env.development .env.local
notepad .env.local

# Development mode
npm run serve

# Or build for production
npm run build
# Then serve dist/ with Nginx or any web server
```

**Frontend will run on:** http://localhost:3000 (dev) or port 80 (production)

---

## 🌐 Production Deployment

### Option 1: Docker Compose (Production Mode)

**Create `docker-compose.prod.yml`:**
```yaml
version: '3.8'

services:
  db:
    restart: always
    volumes:
      - postgres_data_prod:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}

  api:
    restart: always
    environment:
      - ENVIRONMENT=production
      - DEBUG=False
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

  frontend:
    restart: always
    environment:
      - NODE_ENV=production

volumes:
  postgres_data_prod:
```

**Deploy:**
```powershell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Option 2: Cloud Deployment (AWS)

#### A. AWS EC2 Deployment

**1. Launch EC2 Instance:**
- Instance type: t3.medium (2 vCPU, 4GB RAM)
- OS: Ubuntu 22.04 LTS
- Security groups: Open ports 80, 443, 22

**2. Connect and Setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Clone repository
git clone https://github.com/yourusername/FitArena-Sports-Performance-Analytics.git
cd FitArena-Sports-Performance-Analytics/deployment

# Configure environment
cp .env.example .env
nano .env

# Deploy
docker-compose up -d
```

**3. Setup Nginx Reverse Proxy:**
```bash
sudo apt install nginx -y

sudo nano /etc/nginx/sites-available/fitarena
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000/api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/fitarena /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### B. AWS RDS for Database

**1. Create RDS PostgreSQL Instance:**
- Engine: PostgreSQL 13+
- Instance class: db.t3.micro (dev) or db.t3.small (prod)
- Storage: 20GB SSD
- Enable automated backups

**2. Update `.env` file:**
```env
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/fitarena
```

#### C. AWS S3 for Static Files

**Frontend deployment to S3:**
```powershell
# Build frontend
cd frontend
npm run build

# Upload to S3
aws s3 sync dist/ s3://your-bucket-name --delete
```

**Configure CloudFront CDN for S3 bucket**

### Option 3: Kubernetes Deployment

**Create `k8s-deployment.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fitarena-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fitarena-backend
  template:
    metadata:
      labels:
        app: fitarena-backend
    spec:
      containers:
      - name: api
        image: your-registry/fitarena-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: fitarena-secrets
              key: database-url
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fitarena-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fitarena-frontend
  template:
    metadata:
      labels:
        app: fitarena-frontend
    spec:
      containers:
      - name: frontend
        image: your-registry/fitarena-frontend:latest
        ports:
        - containerPort: 80
```

**Deploy:**
```bash
kubectl apply -f k8s-deployment.yaml
kubectl get pods
kubectl get services
```

---

## ⚙️ Environment Configuration

### Backend `.env` File

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/fitarena
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=fitarena

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=FitArena API
ENVIRONMENT=production
DEBUG=False

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000","https://your-domain.com"]

# File Upload
MAX_UPLOAD_SIZE=10485760  # 10MB
UPLOAD_DIR=./uploads

# ML Models
MODEL_PATH=./models
```

### Frontend `.env` File

```env
# API Configuration
VUE_APP_API_BASE_URL=http://localhost:8000/api/v1
VUE_APP_API_TIMEOUT=30000

# Application
VUE_APP_NAME=FitArena
VUE_APP_VERSION=1.0.0

# Features
VUE_APP_ENABLE_DARK_MODE=true
VUE_APP_ENABLE_ANALYTICS=true
```

---

## 🗄️ Database Setup

### Initial Migration

```powershell
cd backend

# Run Alembic migrations
alembic upgrade head

# Or run setup script
python setup.py
```

### Backup Database

```powershell
# Using pg_dump
pg_dump -U postgres -h localhost fitarena > backup_$(date +%Y%m%d).sql

# Using Docker
docker exec fitarena_db pg_dump -U postgres fitarena > backup.sql
```

### Restore Database

```powershell
# Using psql
psql -U postgres -h localhost fitarena < backup.sql

# Using Docker
docker exec -i fitarena_db psql -U postgres fitarena < backup.sql
```

---

## 🔒 SSL/HTTPS Setup

### Using Let's Encrypt (Free SSL)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal (already setup by certbot)
sudo certbot renew --dry-run
```

### Update Nginx Configuration

Certbot will automatically update your Nginx configuration to use HTTPS.

Verify in `/etc/nginx/sites-available/fitarena`:
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 📊 Monitoring & Logging

### Docker Logs

```powershell
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f api
docker-compose logs -f frontend
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100 api
```

### Application Logs

Backend logs: `backend/logs/app.log`
Frontend logs: Browser console

### Monitoring with Prometheus & Grafana

**Add to `docker-compose.yml`:**
```yaml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## 🐛 Troubleshooting

### Services Won't Start

```powershell
# Check Docker status
docker-compose ps

# Check logs for errors
docker-compose logs

# Restart services
docker-compose restart

# Rebuild from scratch
docker-compose down -v
docker-compose up -d --build
```

### Database Connection Failed

```powershell
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker exec -it fitarena_db psql -U postgres
```

### Frontend Can't Connect to Backend

1. Check CORS settings in backend `.env`
2. Verify API_BASE_URL in frontend `.env`
3. Check if backend is running: http://localhost:8000/api/docs

### Port Already in Use

```powershell
# Find process using port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <process_id> /F

# Or change port in docker-compose.yml
```

### Out of Memory

```yaml
# Add memory limits to docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## 📋 Deployment Checklist

### Pre-Deployment

- [ ] ✅ Update all dependencies
- [ ] ✅ Run all tests
- [ ] ✅ Configure production environment variables
- [ ] ✅ Set strong passwords
- [ ] ✅ Backup existing data
- [ ] ✅ Review security settings
- [ ] ✅ Set up SSL certificates
- [ ] ✅ Configure domain DNS

### Deployment

- [ ] ✅ Deploy database
- [ ] ✅ Run migrations
- [ ] ✅ Deploy backend
- [ ] ✅ Deploy frontend
- [ ] ✅ Configure reverse proxy
- [ ] ✅ Set up SSL/HTTPS
- [ ] ✅ Configure monitoring

### Post-Deployment

- [ ] ✅ Test all endpoints
- [ ] ✅ Test frontend pages
- [ ] ✅ Verify authentication
- [ ] ✅ Test file uploads
- [ ] ✅ Check performance
- [ ] ✅ Set up automated backups
- [ ] ✅ Configure log rotation
- [ ] ✅ Document deployment

---

## 🎯 Performance Optimization

### Backend Optimization

1. **Enable Caching**
   - Add Redis for API response caching
   - Cache ML model predictions

2. **Database Optimization**
   - Add indexes to frequently queried fields
   - Use connection pooling
   - Enable query caching

3. **API Optimization**
   - Use async/await for I/O operations
   - Implement pagination
   - Add rate limiting

### Frontend Optimization

1. **Build Optimization**
   - Enable code splitting
   - Lazy load routes
   - Optimize images

2. **Runtime Optimization**
   - Use virtual scrolling for large lists
   - Debounce search inputs
   - Cache API responses

3. **CDN Integration**
   - Serve static assets from CDN
   - Use CloudFront or Cloudflare

---

## 📞 Support

- **Documentation**: [../docs/SETUP_GUIDE.md](../docs/SETUP_GUIDE.md)
- **Issues**: GitHub Issues
- **Email**: support@fitarena.com

---

**Deployment made easy! 🚀**
