"""
Pydantic schemas for FitArena API
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class UserRole(str, Enum):
    """User roles"""
    ADMIN = "admin"
    COACH = "coach"
    ATHLETE = "athlete"
    ANALYST = "analyst"


class FitnessLevel(str, Enum):
    """Fitness levels"""
    LOW = "Low"
    MODERATE = "Moderate"
    GOOD = "Good"
    EXCELLENT = "Excellent"


class Priority(str, Enum):
    """Priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str
    role: UserRole


class UserCreate(UserBase):
    """Schema for creating user"""
    password: str
    team_id: Optional[int] = None
    profile: Optional[Dict[str, Any]] = None


class UserUpdate(BaseModel):
    """Schema for updating user"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    role: Optional[UserRole] = None
    team_id: Optional[int] = None
    profile: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    team_id: Optional[int] = None
    profile: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    """JWT token schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


# Team Schemas
class TeamBase(BaseModel):
    """Base team schema"""
    name: str
    description: Optional[str] = None


class TeamCreate(TeamBase):
    """Schema for creating team"""
    pass


class TeamResponse(TeamBase):
    """Schema for team response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Athlete Data Schemas
class AthleteDataBase(BaseModel):
    """Base athlete data schema"""
    data_date: datetime
    total_steps: Optional[int] = None
    total_distance: Optional[float] = None
    calories_burned: Optional[float] = None
    active_minutes: Optional[int] = None
    sedentary_minutes: Optional[int] = None
    very_active_minutes: Optional[int] = None
    fairly_active_minutes: Optional[int] = None
    lightly_active_minutes: Optional[int] = None


class AthleteDataCreate(AthleteDataBase):
    """Schema for creating athlete data"""
    athlete_id: int
    team_id: Optional[int] = None
    avg_heart_rate: Optional[float] = None
    max_heart_rate: Optional[float] = None
    min_heart_rate: Optional[float] = None
    total_sleep_minutes: Optional[int] = None
    sleep_efficiency: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    additional_metrics: Optional[Dict[str, Any]] = None


class AthleteDataResponse(AthleteDataBase):
    """Schema for athlete data response"""
    id: int
    athlete_id: int
    team_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Recommendation Schemas
class RecommendationBase(BaseModel):
    """Base recommendation schema"""
    recommendation_type: str
    title: str
    description: str
    priority: Priority


class RecommendationCreate(RecommendationBase):
    """Schema for creating recommendation"""
    athlete_id: int
    plan_details: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    expires_at: Optional[datetime] = None


class RecommendationResponse(RecommendationBase):
    """Schema for recommendation response"""
    id: int
    athlete_id: int
    plan_details: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    is_read: bool
    is_completed: bool
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Analytics Schemas
class PerformanceMetrics(BaseModel):
    """Performance metrics schema"""
    avg_steps: float
    avg_distance: float
    avg_calories: float
    avg_active_minutes: float
    performance_score: Optional[float] = None
    consistency_score: Optional[float] = None


class AnalyticsSummary(BaseModel):
    """Analytics summary schema"""
    athlete_id: str
    total_days: int
    date_range: Dict[str, str]
    metrics: PerformanceMetrics
    trends: Optional[Dict[str, str]] = None


class TeamSummary(BaseModel):
    """Team summary schema"""
    total_athletes: int
    total_records: int
    team_averages: Dict[str, float]
    team_totals: Dict[str, float]
    date_range: Dict[str, str]


# File Upload Schemas
class FileUploadResponse(BaseModel):
    """File upload response schema"""
    filename: str
    file_size: int
    records_processed: int
    success: bool
    message: str
    errors: Optional[List[str]] = None


# Report Schemas
class ReportRequest(BaseModel):
    """Report generation request schema"""
    report_type: str
    athlete_ids: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metrics: Optional[List[str]] = None
    format: str = "pdf"


class ReportResponse(BaseModel):
    """Report response schema"""
    report_id: int
    report_type: str
    file_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Prediction Schemas
class PredictionRequest(BaseModel):
    """Prediction request schema"""
    athlete_id: str
    metric: str
    days_ahead: int = Field(default=7, ge=1, le=30)


class PredictionResponse(BaseModel):
    """Prediction response schema"""
    athlete_id: str
    metric: str
    predictions: List[Dict[str, Any]]
    confidence: float
    model_used: str


# Alert Schemas
class AlertBase(BaseModel):
    """Base alert schema"""
    alert_type: str
    title: str
    message: str
    severity: str


class AlertCreate(AlertBase):
    """Schema for creating alert"""
    user_id: int


class AlertResponse(AlertBase):
    """Schema for alert response"""
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Generic Response Schemas
class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: Optional[str] = None
    status_code: int
