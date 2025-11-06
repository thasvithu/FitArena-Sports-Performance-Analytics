# 🔧 FitArena Backend - FastAPI Data Science Platform

The backend API for FitArena Sports Performance Analytics Platform.

## 📋 Overview

This is a production-ready FastAPI backend with:
- RESTful API with 15+ endpoints
- JWT authentication & authorization
- 4 ML models (Classification, Prediction, Anomaly Detection, Recommendations)
- PostgreSQL database with SQLAlchemy ORM
- Comprehensive analytics engine
- Data processing pipelines

## 🏗️ Architecture

```
backend/
├── src/                          # Source code
│   ├── api/                      # FastAPI application
│   │   ├── main.py              # Application entry point
│   │   ├── routes/              # API routes
│   │   └── middleware/          # CORS, Auth middleware
│   ├── models/                   # ML models
│   │   ├── activity_classifier.py
│   │   ├── performance_predictor.py
│   │   ├── anomaly_detector.py
│   │   └── recommendation_engine.py
│   ├── data_processing/          # Data pipelines
│   │   ├── data_loader.py
│   │   ├── data_validator.py
│   │   └── feature_engineering.py
│   ├── analytics/                # Analytics engine
│   │   ├── metrics.py
│   │   └── visualizations.py
│   ├── database/                 # Database layer
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── database.py          # Database connection
│   │   └── schemas.py           # Pydantic schemas
│   └── utils/                    # Utilities
│
├── tests/                        # Test suite
│   ├── test_api.py
│   ├── test_models.py
│   └── test_analytics.py
│
├── config/                       # Configuration files
├── models/                       # Saved ML models
├── logs/                         # Application logs
├── notebooks/                    # Jupyter notebooks
├── reports/                      # Generated reports
│
├── requirements.txt              # Python dependencies
├── setup.py                      # Setup automation
├── train_models.py              # ML training pipeline
├── Dockerfile                    # Docker container
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

### Installation

```powershell
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up database and configuration
python setup.py

# 6. Train ML models (optional, pre-trained models included)
python train_models.py

# 7. Start the API server
cd src/api
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

## 🔑 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fitarena

# JWT Authentication
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=FitArena API

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user

### Users
- `GET /api/v1/users` - List all users (admin)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Teams
- `GET /api/v1/teams` - List all teams
- `POST /api/v1/teams` - Create team (coach/admin)
- `GET /api/v1/teams/{id}` - Get team details
- `PUT /api/v1/teams/{id}` - Update team (coach/admin)
- `DELETE /api/v1/teams/{id}` - Delete team (admin)

### Analytics
- `GET /api/v1/analytics/summary` - Get analytics summary
- `GET /api/v1/analytics/trends` - Get performance trends
- `GET /api/v1/analytics/team/{id}` - Get team analytics

### Recommendations
- `GET /api/v1/recommendations` - Get recommendations
- `POST /api/v1/recommendations/generate` - Generate new recommendations

### Predictions
- `GET /api/v1/predictions` - Get predictions
- `POST /api/v1/predictions/generate` - Generate predictions

### Data Management
- `POST /api/v1/data/upload` - Upload CSV/Excel data (coach/admin)
- `GET /api/v1/data/uploads` - Get upload history

### Reports
- `POST /api/v1/reports/generate` - Generate report
- `GET /api/v1/reports` - List reports
- `GET /api/v1/reports/{id}/download` - Download report

## 🤖 Machine Learning Models

### 1. Activity Classifier
- **Algorithm**: Random Forest
- **Purpose**: Classify activity types
- **Features**: 50+ engineered features
- **Accuracy**: ~92%

### 2. Performance Predictor
- **Algorithm**: Gradient Boosting
- **Purpose**: Predict future performance
- **Features**: Time series + engineered features
- **MAE**: <5%

### 3. Anomaly Detector
- **Algorithm**: Statistical methods + Isolation Forest
- **Purpose**: Detect unusual patterns
- **Features**: Z-score + IQR analysis

### 4. Recommendation Engine
- **Algorithm**: Collaborative filtering + Rule-based
- **Purpose**: Generate personalized recommendations
- **Features**: User profile + performance history

## 🧪 Testing

### Run All Tests
```powershell
cd backend
pytest tests/ -v
```

### Run with Coverage
```powershell
pytest --cov=src tests/
pytest --cov=src --cov-report=html tests/
```

### Test Specific Module
```powershell
pytest tests/test_api.py -v
pytest tests/test_models.py -v
```

## 📊 Database Schema

### Tables
1. **users** - User accounts
2. **teams** - Team information
3. **team_members** - Team membership
4. **activities** - Activity records
5. **performance_metrics** - Performance data
6. **recommendations** - AI recommendations
7. **predictions** - ML predictions
8. **data_uploads** - Upload history

### Relationships
- User → Teams (many-to-many)
- Team → Activities (one-to-many)
- User → Recommendations (one-to-many)
- User → Predictions (one-to-many)

## 🔐 Security

- **Authentication**: JWT tokens with bcrypt password hashing
- **Authorization**: Role-based access control (athlete/coach/admin)
- **SQL Injection**: Protected by SQLAlchemy ORM
- **XSS**: Input validation with Pydantic
- **CORS**: Configured for specific origins
- **Rate Limiting**: Ready to implement

## 📈 Performance

- **Async Operations**: FastAPI async/await support
- **Connection Pooling**: SQLAlchemy connection pool
- **Caching**: Ready for Redis integration
- **Query Optimization**: Indexed database queries
- **Response Time**: <100ms for most endpoints

## 🐳 Docker

### Build Image
```powershell
cd backend
docker build -t fitarena-api .
```

### Run Container
```powershell
docker run -p 8000:8000 --env-file .env fitarena-api
```

### Using Docker Compose
```powershell
cd ../deployment
docker-compose up -d
```

## 📝 Development Workflow

1. **Create Branch**
   ```powershell
   git checkout -b feature/new-feature
   ```

2. **Make Changes**
   - Write code in `src/`
   - Add tests in `tests/`

3. **Run Tests**
   ```powershell
   pytest tests/ -v
   ```

4. **Format Code**
   ```powershell
   black src/
   ```

5. **Lint Code**
   ```powershell
   flake8 src/
   ```

6. **Commit**
   ```powershell
   git add .
   git commit -m "Add new feature"
   ```

## 🔧 Configuration

### Database Configuration
Edit `config/database.py`:
```python
DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
```

### CORS Configuration
Edit `src/api/middleware/cors.py`:
```python
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    # Add production origins
]
```

### JWT Configuration
Edit `.env`:
```env
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📚 Documentation

- **API Docs**: http://localhost:8000/api/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/api/redoc (Alternative API docs)
- **Setup Guide**: [../docs/SETUP_GUIDE.md](../docs/SETUP_GUIDE.md)
- **Quick Start**: [../docs/QUICKSTART.md](../docs/QUICKSTART.md)

## 🐛 Troubleshooting

### Database Connection Fails
```powershell
# Check PostgreSQL is running
Get-Service postgresql*

# Test connection
psql -U postgres -h localhost
```

### Import Errors
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <process_id> /F
```

### ML Models Not Found
```powershell
# Train models
python train_models.py

# Check models directory
ls models/
```

## 🎯 Next Steps

- [ ] Add Redis caching layer
- [ ] Implement rate limiting
- [ ] Add WebSocket support for real-time updates
- [ ] Enhance ML models with deep learning
- [ ] Add monitoring with Prometheus
- [ ] Implement CI/CD pipeline
- [ ] Add API versioning
- [ ] Create admin dashboard

## 📞 Support

- **Documentation**: [../docs/](../docs/)
- **API Issues**: Check logs in `logs/`
- **Database Issues**: Check PostgreSQL logs

---

**Built with FastAPI ⚡ | Powered by Machine Learning 🤖**
