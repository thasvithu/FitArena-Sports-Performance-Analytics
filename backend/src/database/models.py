"""
Database models for FitArena platform
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # admin, coach, athlete, analyst
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    profile = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    team = relationship("Team", back_populates="members")
    athlete_data = relationship("AthleteData", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="athlete")


class Team(Base):
    """Team model for organizing users"""
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    members = relationship("User", back_populates="team")
    athlete_data = relationship("AthleteData", back_populates="team")


class AthleteData(Base):
    """Athlete performance data model"""
    __tablename__ = "athlete_data"
    
    id = Column(Integer, primary_key=True, index=True)
    athlete_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    data_date = Column(DateTime, nullable=False)
    
    # Activity Metrics
    total_steps = Column(Integer, nullable=True)
    total_distance = Column(Float, nullable=True)
    calories_burned = Column(Float, nullable=True)
    active_minutes = Column(Integer, nullable=True)
    sedentary_minutes = Column(Integer, nullable=True)
    
    # Intensity Metrics
    very_active_minutes = Column(Integer, nullable=True)
    fairly_active_minutes = Column(Integer, nullable=True)
    lightly_active_minutes = Column(Integer, nullable=True)
    
    # Heart Rate Metrics
    avg_heart_rate = Column(Float, nullable=True)
    max_heart_rate = Column(Float, nullable=True)
    min_heart_rate = Column(Float, nullable=True)
    resting_heart_rate = Column(Float, nullable=True)
    
    # Sleep Metrics
    total_sleep_minutes = Column(Integer, nullable=True)
    sleep_efficiency = Column(Float, nullable=True)
    
    # Weight Metrics
    weight_kg = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    
    # Additional Metrics (JSON for flexibility)
    additional_metrics = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="athlete_data")
    team = relationship("Team", back_populates="athlete_data")


class Recommendation(Base):
    """AI-generated recommendations model"""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    athlete_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recommendation_type = Column(String(100), nullable=False)  # training, recovery, nutrition, etc.
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(50), nullable=False)  # low, medium, high, critical
    plan_details = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    is_read = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    athlete = relationship("User", back_populates="recommendations")


class Report(Base):
    """Generated reports model"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_type = Column(String(100), nullable=False)  # performance, team, individual, etc.
    title = Column(String(255), nullable=False)
    metrics = Column(JSON, nullable=False)
    format = Column(String(50), nullable=False)  # pdf, csv, json
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Note(Base):
    """Collaboration notes model"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Alert(Base):
    """System alerts and notifications"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    alert_type = Column(String(100), nullable=False)  # anomaly, milestone, warning, etc.
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False)  # info, warning, critical
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
