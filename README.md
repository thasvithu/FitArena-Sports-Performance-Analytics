# FitArena - Sports Performance Analytics Platform

## 🏃‍♂️ Complete Full-Stack Data Science Platform

A production-ready, enterprise-grade sports performance analytics platform with AI-powered insights, real-time dashboards, and comprehensive team management.

## ✨ What's Inside

### 🎨 **Modern Frontend** (Vue.js 3 + Vuetify 3)
- 12+ responsive pages with Material Design
- Real-time interactive dashboards
- Advanced analytics visualizations
- AI recommendations display
- Performance predictions
- Team management interface
- Dark mode support
- Mobile-optimized layouts

### 🚀 **Powerful Backend** (FastAPI + Python)
- RESTful API with 15+ endpoints
- JWT authentication & authorization
- Role-based access control
- File upload & processing
- Real-time data analytics

### 🤖 **Machine Learning Models**
- Activity classification (Random Forest)
- Performance prediction (Gradient Boosting)
- Anomaly detection (Statistical methods)
- AI-powered recommendation engine

### 📊 **Data Science Pipeline**
- Automated data loading & validation
- Feature engineering (50+ features)
- Data quality assessment
- Statistical analysis
- Trend detection

### 🗄️ **Database Architecture**
- PostgreSQL with SQLAlchemy ORM
- 8 optimized data models
- Relationship management
- Connection pooling

### 🐳 **Docker Deployment**
- Multi-container orchestration
- One-command deployment
- Production-ready configuration
- Scalable architecture

---

## 🚀 Quick Start (5 Minutes)

### Option 1: Docker (Recommended)

```powershell
# Navigate to deployment folder
cd deployment

# Start all services
docker-compose up -d

# Access the platform
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Option 2: Manual Setup

**Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python setup.py
cd src/api && python main.py
```

**Frontend:**
```powershell
cd frontend
npm install
npm run serve
```

---

## 📁 Project Structure

```
FitArena-Sports-Performance-Analytics/
│
├── frontend/                    # Vue.js 3 Frontend
│   ├── src/
│   │   ├── views/              # 12 complete pages
│   │   ├── components/         # Reusable components
│   │   ├── store/              # Vuex state management
│   │   ├── router/             # Vue Router
│   │   └── services/           # API integration
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
│
├── src/                        # Backend Source Code
│   ├── api/                    # FastAPI application
│   ├── models/                 # ML models
│   ├── data_processing/        # Data pipelines
│   ├── analytics/              # Analytics engine
│   └── database/               # Database models
│
├── data/                       # Training datasets (Fitbit data)
├── notebooks/                  # Jupyter notebooks (EDA)
├── models/                     # Saved ML models
├── tests/                      # Test suite
├── config/                     # Configuration files
├── logs/                       # Application logs
├── reports/                    # Generated reports
│
├── docker-compose.yml          # Multi-container setup
├── Dockerfile                  # Backend container
├── requirements.txt            # Python dependencies
├── setup.py                    # Setup automation
├── train_models.py            # ML training pipeline
│
├── README.md                   # This file
├── SETUP_GUIDE.md             # Complete setup guide
├── QUICKSTART.md              # Quick start guide
├── FRONTEND_SUMMARY.md        # Frontend documentation
└── PROJECT_SUMMARY.md         # Project overview
```

---

## 🎯 Features

### Frontend Features ✅
- ✅ User authentication & registration
- ✅ Performance dashboard with KPIs
- ✅ Advanced analytics with 10+ chart types
- ✅ Team management (CRUD operations)
- ✅ AI-powered recommendations
- ✅ ML performance predictions
- ✅ CSV/Excel data upload
- ✅ Custom report generation
- ✅ User profile management
- ✅ Dark mode support
- ✅ Responsive design (mobile + desktop)
- ✅ Real-time data visualization

### Backend Features ✅
- ✅ JWT authentication with bcrypt
- ✅ Role-based access (athlete/coach/admin)
- ✅ RESTful API with auto-generated docs
- ✅ Data validation & cleaning
- ✅ Feature engineering pipeline
- ✅ 4 ML model implementations
- ✅ Statistical analytics
- ✅ File upload processing
- ✅ Report generation
- ✅ CORS & security middleware
- ✅ Database migrations
- ✅ Error handling & logging

### Data Science Features ✅
- ✅ Exploratory Data Analysis (EDA)
- ✅ Data quality assessment
- ✅ 50+ engineered features
- ✅ Activity classification
- ✅ Performance prediction
- ✅ Anomaly detection
- ✅ Recommendation engine
- ✅ Trend analysis
- ✅ Correlation analysis
- ✅ Statistical summaries

---

## 🖥️ Screenshots & Pages

### 1. **Login & Registration**
- Material Design forms
- Form validation
- Role selection

### 2. **Dashboard**
- 4 KPI cards (Steps, Calories, Minutes, Score)
- Activity trends chart (30 days)
- Activity distribution donut chart
- Weekly performance bar chart
- Calories area chart
- Recent activity table

### 3. **Analytics**
- Performance comparison charts
- Correlation heatmaps
- Distribution box plots
- Statistical summary tables
- Export to PDF/Excel

### 4. **Teams** (Coach/Admin)
- Team cards with metrics
- Create/edit/delete teams
- Team member management
- Performance tracking

### 5. **Recommendations**
- AI-powered suggestions
- Priority indicators (High/Medium/Low)
- Action item checklists
- Expected impact predictions
- Confidence scores

### 6. **Predictions**
- Historical vs predicted charts
- Confidence intervals
- Model accuracy metrics
- Goal predictions with probability

### 7. **Data Upload** (Coach/Admin)
- Drag & drop file upload
- CSV/Excel support
- Upload history
- Data validation

### 8. **Reports**
- Custom report generation
- Multiple formats (PDF/Excel/CSV)
- Report history
- Download functionality

### 9. **Profile**
- User information editing
- Password change
- Role display

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: Vue.js 3.3.4
- **UI Library**: Vuetify 3.3.15
- **State Management**: Vuex 4.1.0
- **Routing**: Vue Router 4.2.4
- **Charts**: ApexCharts 3.44.0
- **HTTP Client**: Axios 1.5.0
- **Icons**: Material Design Icons

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL 12+ with SQLAlchemy 2.0.25
- **Authentication**: JWT with python-jose 3.3.0
- **Password Hashing**: Passlib 1.7.4 with bcrypt
- **Validation**: Pydantic 2.5.3
- **CORS**: FastAPI middleware

### Data Science
- **Data Processing**: Pandas 2.1.4, NumPy 1.26.2
- **Machine Learning**: Scikit-learn 1.3.2, XGBoost 2.0.3
- **Visualization**: Matplotlib 3.8.2, Seaborn 0.13.0, Plotly 5.18.0
- **Statistics**: SciPy 1.11.4

### DevOps
- **Containerization**: Docker, Docker Compose
- **Web Server**: Nginx (frontend), Uvicorn (backend)
- **Testing**: Pytest 7.4.3
- **Linting**: ESLint (frontend), Black (backend)

---

## 📚 Documentation

- **[SETUP_GUIDE.md](./docs/SETUP_GUIDE.md)** - Complete setup instructions
- **[QUICKSTART.md](./docs/QUICKSTART.md)** - Backend quick start
- **[frontend/QUICKSTART.md](./frontend/QUICKSTART.md)** - Frontend quick start
- **[frontend/README.md](./frontend/README.md)** - Frontend documentation
- **[FRONTEND_SUMMARY.md](./docs/FRONTEND_SUMMARY.md)** - Frontend implementation details
- **[PROJECT_SUMMARY.md](./docs/PROJECT_SUMMARY.md)** - Project architecture overview
- **[REORGANIZATION_GUIDE.md](./REORGANIZATION_GUIDE.md)** - Project structure guide
- **[deployment/deployment-guide.md](./deployment/deployment-guide.md)** - Deployment guide

---

## 🧪 Testing

### Backend Tests
```powershell
pytest tests/ -v
pytest --cov=src tests/
```

### Frontend Tests
```powershell
cd frontend
npm run test:unit
npm run test:unit -- --coverage
```

---

## 🎓 Getting Started

### 1. Clone Repository
```powershell
git clone https://github.com/thasvithu/FitArena-Sports-Performance-Analytics.git
cd FitArena-Sports-Performance-Analytics
```

### 2. Choose Setup Method

**Docker (Easiest):**
```powershell
docker-compose up -d
```

**Manual Setup:**
See [SETUP_GUIDE.md](./SETUP_GUIDE.md)

### 3. Access Platform
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

### 4. Register & Login
1. Visit http://localhost:3000/register
2. Create account (choose "Coach" for full access)
3. Login with credentials
4. Explore the platform!

---

## 📊 Sample Data

The project includes Fitbit activity tracking data:
- **29 CSV files** across 2 time periods
- Daily activity, heart rate, calories, steps
- Hourly and minute-level data
- Sleep and weight tracking

Located in: `data/Fitabase Data 3.12.16-4.11.16/` and `data/Fitabase Data 4.12.16-5.12.16/`

---

## 🚀 Deployment

### Production Deployment

**Using Docker:**
```powershell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Manual Deployment:**
1. Build frontend: `cd frontend && npm run build`
2. Deploy dist/ to web server
3. Configure Nginx as reverse proxy
4. Set production environment variables
5. Start backend with production settings

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed deployment instructions.

---

## 🔒 Security

- ✅ JWT authentication with secure tokens
- ✅ Password hashing with bcrypt
- ✅ Role-based access control
- ✅ CORS protection
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ XSS protection headers
- ✅ Input validation (Pydantic)
- ✅ Rate limiting ready
- ✅ HTTPS/SSL ready

---

## 📈 Performance

- **Frontend**: Optimized with lazy loading, code splitting
- **Backend**: Async operations, connection pooling
- **Database**: Indexed queries, efficient ORM
- **API**: Response caching ready
- **Docker**: Multi-stage builds, minimal images

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👥 Team

**Developer**: FitArena Development Team  
**Repository**: [FitArena-Sports-Performance-Analytics](https://github.com/thasvithu/FitArena-Sports-Performance-Analytics)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/thasvithu/FitArena-Sports-Performance-Analytics/issues)
- **Documentation**: See docs above
- **API Docs**: http://localhost:8000/api/docs

---

## 🎉 Achievements

✅ **Complete Full-Stack Platform**  
✅ **Production-Ready Code**  
✅ **Comprehensive Documentation**  
✅ **Docker Support**  
✅ **ML Models Integrated**  
✅ **Modern UI/UX**  
✅ **Responsive Design**  
✅ **Security Implemented**  
✅ **Testing Framework**  
✅ **API Documentation**  

---

## 🔮 Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Mobile app (React Native)
- [ ] Wearable device integration
- [ ] Video analysis with computer vision
- [ ] Social features (sharing, leaderboards)
- [ ] Advanced ML models (LSTM, Transformers)
- [ ] Multi-sport support
- [ ] Offline mode (PWA)

---

**Built with ❤️ for Athletes and Coaches**

**Ready to revolutionize sports performance analytics! 🏃‍♂️📊🚀**