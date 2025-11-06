# FitArena - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup Environment (2 minutes)

```bash
# Clone the repository
cd "FitArena - Sports Performance Analytics Platform/FitArena-Sports-Performance-Analytics"

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Application (1 minute)

```bash
# Copy environment template
copy .env.example .env

# Edit .env with your settings (optional for local development)
notepad .env
```

### Step 3: Run Setup Script (1 minute)

```bash
python setup.py
```

This will:
- Create necessary directories
- Set up environment variables
- Install dependencies
- Verify installation

### Step 4: Explore the Data (1 minute)

```bash
# Start Jupyter Notebook
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

Run the cells to explore the Fitbit data!

---

## 📊 Main Workflows

### Workflow 1: Data Analysis

```bash
# 1. Open Jupyter
jupyter notebook

# 2. Navigate to notebooks/
# 3. Open 01_exploratory_data_analysis.ipynb
# 4. Run all cells (Cell > Run All)
```

### Workflow 2: Train ML Models

```bash
# Run training script
python train_models.py

# Output:
# - Trained models saved to models/saved_models/
# - Training logs in logs/
# - Training report in reports/
```

### Workflow 3: Start API Server

```bash
# Start FastAPI server
cd src/api
python main.py

# API available at:
# http://localhost:8000

# Interactive API docs:
# http://localhost:8000/api/docs
```

### Workflow 4: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_data_processing.py -v
```

---

## 🐳 Docker Quick Start

```bash
# Start all services
docker-compose up -d

# Access services:
# API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
# Jupyter: http://localhost:8888
# PostgreSQL: localhost:5432

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 💡 Common Tasks

### Load and Process Data

```python
from src.data_processing.data_loader import DataLoader
from src.data_processing.feature_engineering import FeatureEngineer

# Load data
loader = DataLoader(data_dir='./data')
data = loader.load_daily_activity()

# Engineer features
engineer = FeatureEngineer()
featured_data = engineer.create_all_features(data)
```

### Train a Model

```python
from src.models.predictive_models import ActivityClassifier

# Initialize and train
classifier = ActivityClassifier()
metrics = classifier.train(featured_data)

# Save model
classifier.save_model('./models/saved_models/my_model.pkl')
```

### Generate Recommendations

```python
from src.models.recommendation_engine import RecommendationEngine

# Create engine
engine = RecommendationEngine()

# Generate recommendations
recommendations = engine.generate_comprehensive_recommendations(
    df=data,
    athlete_id='1234567890'
)

print(f"Generated {len(recommendations['recommendations'])} recommendations")
```

### Create Visualizations

```python
from src.analytics.visualizations import PerformanceVisualizer

# Initialize visualizer
viz = PerformanceVisualizer()

# Create dashboard
dashboard = viz.create_dashboard(data, athlete_id='1234567890')
dashboard.show()
```

### Make API Calls

```bash
# Register user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"testuser","password":"password123","role":"athlete"}'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Get analytics (with token)
curl -X GET "http://localhost:8000/api/v1/analytics/summary?athlete_id=1234" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `setup.py` | Initial setup script |
| `train_models.py` | Train all ML models |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment template |
| `docker-compose.yml` | Docker orchestration |
| `README_PROJECT.md` | Full documentation |
| `PROJECT_SUMMARY.md` | Project overview |

---

## 🎯 Next Steps

1. **Explore the Data**
   - Open `notebooks/01_exploratory_data_analysis.ipynb`
   - Understand the dataset structure
   - Analyze key patterns

2. **Train Models**
   - Run `python train_models.py`
   - Review training logs
   - Test model predictions

3. **Try the API**
   - Start API server: `python src/api/main.py`
   - Visit http://localhost:8000/api/docs
   - Test endpoints

4. **Customize**
   - Modify models in `src/models/`
   - Add new features in `src/data_processing/`
   - Create custom analytics in `src/analytics/`

---

## ❓ Troubleshooting

### Issue: Import errors
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: Database connection error
```bash
# Solution: Update .env with correct DATABASE_URL
# Or use SQLite for development:
DATABASE_URL=sqlite:///./fitarena.db
```

### Issue: Port already in use
```bash
# Solution: Change port in .env or command
uvicorn src.api.main:app --port 8001
```

### Issue: Module not found
```bash
# Solution: Add project to PYTHONPATH
$env:PYTHONPATH = "G:\Projects\Euron\FitArena - Sports Performance Analytics Platform\FitArena-Sports-Performance-Analytics"  # Windows PowerShell
```

---

## 📚 Learning Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pandas Guide**: https://pandas.pydata.org/docs/
- **Scikit-learn**: https://scikit-learn.org/stable/
- **Plotly**: https://plotly.com/python/
- **SQLAlchemy**: https://www.sqlalchemy.org/

---

## 🆘 Get Help

1. Check `README_PROJECT.md` for detailed documentation
2. Review inline code comments
3. Explore example notebooks
4. Check error logs in `logs/` directory

---

**Ready to build amazing sports analytics! 🏃‍♂️📊**
