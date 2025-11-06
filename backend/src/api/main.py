"""
FitArena API - Main Application
FastAPI application for Sports Performance Analytics Platform
"""
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
import logging

from src.database.connection import get_db, init_db
from src.database.models import User, Team, AthleteData, Recommendation
from src.api.schemas import (
    UserCreate, UserResponse, LoginRequest, Token,
    TeamCreate, TeamResponse, MessageResponse,
    RecommendationResponse, AnalyticsSummary
)
from src.api.auth import (
    authenticate_user, create_access_token, get_current_user,
    get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="FitArena API",
    description="Sports Performance Analytics Platform API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Starting FitArena API...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down FitArena API...")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "FitArena API"}


# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.post("/api/v1/auth/register", response_model=UserResponse, tags=["Authentication"])
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        password_hash=hashed_password,
        role=user.role,
        team_id=user.team_id,
        profile=user.profile
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"New user registered: {user.username}")
    return db_user


@app.post("/api/v1/auth/login", response_model=Token, tags=["Authentication"])
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login and get access token
    """
    user = authenticate_user(db, login_request.username, login_request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/v1/auth/me", response_model=UserResponse, tags=["Authentication"])
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return current_user


# ============================================================================
# User Management Endpoints
# ============================================================================

@app.get("/api/v1/users", response_model=List[UserResponse], tags=["Users"])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all users (requires authentication)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/api/v1/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


# ============================================================================
# Team Management Endpoints
# ============================================================================

@app.post("/api/v1/teams", response_model=TeamResponse, tags=["Teams"])
async def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new team
    """
    db_team = Team(name=team.name, description=team.description)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    
    logger.info(f"Team created: {team.name}")
    return db_team


@app.get("/api/v1/teams", response_model=List[TeamResponse], tags=["Teams"])
async def list_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all teams
    """
    teams = db.query(Team).offset(skip).limit(limit).all()
    return teams


@app.get("/api/v1/teams/{team_id}", response_model=TeamResponse, tags=["Teams"])
async def get_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get team by ID
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    return team


# ============================================================================
# Data Upload Endpoints
# ============================================================================

@app.post("/api/v1/data/upload", tags=["Data"])
async def upload_data(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload athlete performance data (CSV/Excel)
    """
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only CSV and Excel files are allowed."
        )
    
    # TODO: Implement data processing and storage
    logger.info(f"File uploaded: {file.filename} by user {current_user.username}")
    
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "success": True
    }


# ============================================================================
# Analytics Endpoints
# ============================================================================

@app.get("/api/v1/analytics/summary", tags=["Analytics"])
async def get_analytics_summary(
    athlete_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get analytics summary for an athlete
    """
    # TODO: Implement analytics calculation
    return {
        "athlete_id": athlete_id,
        "message": "Analytics summary endpoint - implementation pending"
    }


@app.get("/api/v1/analytics/team/{team_id}", tags=["Analytics"])
async def get_team_analytics(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get analytics for entire team
    """
    # TODO: Implement team analytics
    return {
        "team_id": team_id,
        "message": "Team analytics endpoint - implementation pending"
    }


# ============================================================================
# Recommendation Endpoints
# ============================================================================

@app.get("/api/v1/recommendations/{athlete_id}", response_model=List[RecommendationResponse], tags=["Recommendations"])
async def get_recommendations(
    athlete_id: int,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get recommendations for an athlete
    """
    recommendations = db.query(Recommendation).filter(
        Recommendation.athlete_id == athlete_id
    ).offset(skip).limit(limit).all()
    
    return recommendations


@app.post("/api/v1/recommendations/generate/{athlete_id}", tags=["Recommendations"])
async def generate_recommendations(
    athlete_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate new recommendations for an athlete
    """
    # TODO: Implement recommendation generation
    logger.info(f"Generating recommendations for athlete {athlete_id}")
    
    return {
        "message": "Recommendations generated successfully",
        "athlete_id": athlete_id
    }


# ============================================================================
# Prediction Endpoints
# ============================================================================

@app.get("/api/v1/predictions/{athlete_id}/{metric}", tags=["Predictions"])
async def get_predictions(
    athlete_id: str,
    metric: str,
    days_ahead: int = 7,
    current_user: User = Depends(get_current_user)
):
    """
    Get performance predictions for an athlete
    """
    # TODO: Implement prediction model
    return {
        "athlete_id": athlete_id,
        "metric": metric,
        "days_ahead": days_ahead,
        "message": "Prediction endpoint - implementation pending"
    }


# Run application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
