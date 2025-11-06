# FitArena - Complete Setup Guide

## 🚀 Complete Platform Setup (Backend + Frontend)

This guide will help you set up the entire FitArena platform including backend API, database, and frontend UI.

## 📋 Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- PostgreSQL 12+ installed (or use Docker)
- Git installed

## 🎯 Quick Start (5 Minutes)

### Option 1: Using Docker (Easiest) 🐳

```powershell
# Clone repository
cd "g:\Projects\Euron\FitArena - Sports Performance Analytics Platform\FitArena-Sports-Performance-Analytics"

# Start all services
docker-compose up -d

# Wait for services to start (30-60 seconds)
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Jupyter: http://localhost:8888
- Database: localhost:5432

### Option 2: Manual Setup (More Control)

#### Step 1: Backend Setup

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env with your settings

# Initialize database
python setup.py

# Start backend
cd src/api
python main.py
```

Backend will be at: http://localhost:8000

#### Step 2: Frontend Setup

```powershell
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start frontend
npm run serve
```

Frontend will be at: http://localhost:3000

---

## 📁 Project Structure Overview

```
FitArena-Sports-Performance-Analytics/
├── backend/
│   ├── src/
│   │   ├── api/              # FastAPI application
│   │   ├── models/           # ML models
│   │   ├── data_processing/  # Data pipelines
│   │   ├── analytics/        # Analytics engine
│   │   └── database/         # Database models
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile           # Backend container
│
├── frontend/
│   ├── src/
│   │   ├── views/           # Page components
│   │   ├── components/      # Reusable components
│   │   ├── store/           # Vuex state management
│   │   ├── router/          # Vue Router
│   │   └── services/        # API services
│   ├── package.json         # Node dependencies
│   └── Dockerfile          # Frontend container
│
├── data/                    # Training datasets
├── notebooks/               # Jupyter notebooks
├── models/                  # Saved ML models
├── docker-compose.yml       # Multi-container orchestration
└── README.md               # Main documentation
```

---

## 🔧 Detailed Configuration

### Backend Configuration

Edit `.env` file:

```env
# Application
APP_NAME=FitArena
ENVIRONMENT=development

# API
API_V1_PREFIX=/api/v1
API_HOST=0.0.0.0
API_PORT=8000

# Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://fitarena_user:fitarena_pass@localhost:5432/fitarena_db

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# File Upload
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=[".csv",".xlsx",".xls"]
```

### Frontend Configuration

Edit `frontend/.env.development`:

```env
VUE_APP_API_BASE_URL=http://localhost:8000/api/v1
VUE_APP_TITLE=FitArena - Development
VUE_APP_ENV=development
```

---

## 🗄️ Database Setup

### Using PostgreSQL Locally

```powershell
# Create database
psql -U postgres
CREATE DATABASE fitarena_db;
CREATE USER fitarena_user WITH PASSWORD 'fitarena_pass';
GRANT ALL PRIVILEGES ON DATABASE fitarena_db TO fitarena_user;
\q

# Initialize tables (automatic when starting backend)
python setup.py
```

### Using Docker

```powershell
# PostgreSQL included in docker-compose
docker-compose up -d db
```

---

## 🎓 First Time Usage

### 1. Register a User

Visit http://localhost:3000/register

- Username: `admin`
- Email: `admin@fitarena.com`
- Password: `SecurePass123!`
- Role: `Coach` (for full access)

### 2. Login

Visit http://localhost:3000/login

Use the credentials you just created.

### 3. Upload Data

Navigate to **Data Upload** page:

- Upload CSV files from `data/Fitabase Data 3.12.16-4.11.16/`
- Supported files:
  - `dailyActivity_merged.csv`
  - `heartrate_seconds_merged.csv`
  - `hourlyCalories_merged.csv`

### 4. Explore Features

- **Dashboard**: View KPIs and charts
- **Analytics**: Deep dive into metrics
- **Recommendations**: Get AI suggestions
- **Predictions**: See future performance
- **Teams**: Manage athletes (Coach/Admin only)

---

## 🧪 Running Tests

### Backend Tests

```powershell
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_data_processing.py -v
```

### Frontend Tests

```powershell
cd frontend

# Run unit tests
npm run test:unit

# Run with coverage
npm run test:unit -- --coverage
```

---

## 📊 Training ML Models

```powershell
# Train all models
python train_models.py

# Output:
# - models/saved_models/*.pkl (trained models)
# - logs/training.log (training logs)
# - reports/training_report.txt (summary)
```

---

## 🐳 Docker Commands

### Start Services

```powershell
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d api
docker-compose up -d frontend
```

### View Logs

```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f frontend
```

### Stop Services

```powershell
# Stop all
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Rebuild

```powershell
# Rebuild all images
docker-compose build

# Rebuild specific service
docker-compose build api
docker-compose build frontend
```

---

## 🌐 Production Deployment

### Backend Deployment

```powershell
# Build production image
docker build -t fitarena-api:latest .

# Run container
docker run -d -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=production-secret-key \
  fitarena-api:latest
```

### Frontend Deployment

```powershell
cd frontend

# Build production files
npm run build

# Deploy dist/ folder to:
# - Netlify
# - Vercel
# - AWS S3 + CloudFront
# - Nginx server
```

### Using Docker Compose

```powershell
# Set production environment
$env:ENVIRONMENT="production"

# Start with production config
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 🔐 Security Checklist

- [ ] Change default SECRET_KEY in production
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable authentication on all endpoints
- [ ] Regular security updates
- [ ] Backup database regularly

---

## 📈 Monitoring & Logging

### Application Logs

```powershell
# Backend logs
tail -f logs/app.log

# Frontend logs (browser console)
Open DevTools > Console
```

### Database Monitoring

```powershell
# Connect to database
docker exec -it fitarena_db psql -U fitarena_user -d fitarena_db

# Check active connections
SELECT * FROM pg_stat_activity;
```

---

## 🐛 Common Issues & Solutions

### Issue: Port already in use

```powershell
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill the process or change port in config
```

### Issue: Database connection failed

```powershell
# Check if PostgreSQL is running
docker ps | grep postgres

# Verify connection string in .env
DATABASE_URL=postgresql://user:pass@host:port/db
```

### Issue: Frontend can't reach backend

```powershell
# Check CORS settings in backend
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Verify proxy in frontend/vue.config.js
proxy: {
  '/api': {
    target: 'http://localhost:8000'
  }
}
```

### Issue: npm install fails

```powershell
# Clear cache and reinstall
cd frontend
rm -r node_modules
rm package-lock.json
npm cache clean --force
npm install
```

---

## 🔄 Development Workflow

### 1. Make Changes

```powershell
# Backend changes
Edit files in src/

# Frontend changes
cd frontend
Edit files in src/
```

### 2. Test Locally

```powershell
# Backend
python -m pytest tests/

# Frontend
cd frontend
npm run serve
```

### 3. Commit Changes

```powershell
git add .
git commit -m "Description of changes"
git push origin main
```

### 4. Deploy

```powershell
# Using Docker
docker-compose up -d --build
```

---

## 📚 Additional Resources

### Documentation
- Backend API Docs: http://localhost:8000/api/docs
- Frontend README: `frontend/README.md`
- Quick Start: `QUICKSTART.md` / `frontend/QUICKSTART.md`

### Technologies
- FastAPI: https://fastapi.tiangolo.com/
- Vue.js 3: https://vuejs.org/
- Vuetify 3: https://vuetifyjs.com/
- PostgreSQL: https://www.postgresql.org/docs/
- Docker: https://docs.docker.com/

---

## 💡 Tips for Success

1. **Start with Docker** - Easiest way to get everything running
2. **Use sample data** - Test with provided Fitbit datasets
3. **Check logs** - Most issues are visible in logs
4. **Read the docs** - API documentation is auto-generated
5. **Explore the code** - Well-commented and structured
6. **Ask for help** - Check issues or create new ones

---

## 🎉 You're Ready!

Your complete FitArena Sports Performance Analytics Platform is now set up!

**Next Steps:**
1. Register your first user
2. Upload some training data
3. Explore the dashboard
4. Generate recommendations
5. Create custom reports

**Happy Analyzing! 🏃‍♂️📊**
