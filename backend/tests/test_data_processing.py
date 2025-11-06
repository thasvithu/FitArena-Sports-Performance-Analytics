"""
Unit tests for FitArena data processing modules
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.data_processing.data_loader import DataLoader
from src.data_processing.data_validator import DataValidator, DataCleaner
from src.data_processing.feature_engineering import FeatureEngineer


class TestDataLoader:
    """Test DataLoader class"""
    
    def test_data_loader_initialization(self):
        """Test DataLoader initialization"""
        loader = DataLoader(data_dir='./data')
        assert loader.data_dir.exists()
    
    def test_load_daily_activity(self):
        """Test loading daily activity data"""
        loader = DataLoader(data_dir='./data')
        df = loader.load_daily_activity(folder='Fitabase Data 4.12.16-5.12.16')
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'Id' in df.columns
        assert 'ActivityDate' in df.columns
        assert 'TotalSteps' in df.columns


class TestDataValidator:
    """Test DataValidator class"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        return pd.DataFrame({
            'Id': ['1', '2', '3', '4', '5'],
            'TotalSteps': [10000, 15000, 8000, 12000, 9000],
            'Calories': [2500, 3000, 2000, 2700, 2300],
            'TotalDistance': [7.5, 10.0, 6.0, 8.5, 7.0]
        })
    
    def test_validate_missing_values(self, sample_data):
        """Test missing value validation"""
        validator = DataValidator()
        result = validator.validate_missing_values(sample_data, 'test_data')
        
        assert 'dataset' in result
        assert 'total_rows' in result
        assert result['total_rows'] == 5
    
    def test_validate_duplicates(self, sample_data):
        """Test duplicate validation"""
        validator = DataValidator()
        result = validator.validate_duplicates(sample_data, 'test_data')
        
        assert 'total_duplicates' in result
        assert result['total_duplicates'] == 0
    
    def test_quality_score_calculation(self, sample_data):
        """Test quality score calculation"""
        validator = DataValidator()
        report = validator.generate_validation_report(sample_data, 'test_data')
        
        assert 'quality_score' in report
        assert 0 <= report['quality_score'] <= 100


class TestDataCleaner:
    """Test DataCleaner class"""
    
    @pytest.fixture
    def dirty_data(self):
        """Create dirty data for testing"""
        return pd.DataFrame({
            'Id': ['1', '1', '2', '3', '4'],
            'Value': [100, 100, 200, None, 400]
        })
    
    def test_remove_duplicates(self, dirty_data):
        """Test duplicate removal"""
        cleaner = DataCleaner()
        cleaned = cleaner.remove_duplicates(dirty_data)
        
        assert len(cleaned) < len(dirty_data)
        assert cleaned.duplicated().sum() == 0
    
    def test_handle_missing_values(self, dirty_data):
        """Test missing value handling"""
        cleaner = DataCleaner()
        cleaned = cleaner.handle_missing_values(
            dirty_data, 
            strategy={'Value': 'mean'}
        )
        
        assert cleaned['Value'].isnull().sum() == 0


class TestFeatureEngineer:
    """Test FeatureEngineer class"""
    
    @pytest.fixture
    def activity_data(self):
        """Create sample activity data"""
        dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
        return pd.DataFrame({
            'Id': ['1'] * 10,
            'ActivityDate': dates,
            'TotalSteps': np.random.randint(5000, 15000, 10),
            'Calories': np.random.randint(2000, 3500, 10),
            'TotalDistance': np.random.uniform(5, 12, 10),
            'VeryActiveMinutes': np.random.randint(10, 60, 10),
            'FairlyActiveMinutes': np.random.randint(20, 80, 10),
            'LightlyActiveMinutes': np.random.randint(50, 150, 10),
            'SedentaryMinutes': np.random.randint(400, 800, 10)
        })
    
    def test_create_temporal_features(self, activity_data):
        """Test temporal feature creation"""
        engineer = FeatureEngineer()
        featured = engineer.create_temporal_features(activity_data, 'ActivityDate')
        
        assert 'day_of_week' in featured.columns
        assert 'is_weekend' in featured.columns
        assert 'month' in featured.columns
    
    def test_create_activity_features(self, activity_data):
        """Test activity feature creation"""
        engineer = FeatureEngineer()
        featured = engineer.create_activity_features(activity_data)
        
        assert 'total_active_minutes' in featured.columns
        assert 'high_intensity_ratio' in featured.columns
    
    def test_create_rolling_features(self, activity_data):
        """Test rolling feature creation"""
        engineer = FeatureEngineer()
        featured = engineer.create_rolling_features(
            activity_data, 
            'Id', 
            ['TotalSteps'], 
            windows=[3]
        )
        
        assert 'TotalSteps_rolling_mean_3d' in featured.columns
        assert 'TotalSteps_rolling_std_3d' in featured.columns


def test_integration_pipeline():
    """Test complete data processing pipeline"""
    # Load data
    loader = DataLoader(data_dir='./data')
    data = loader.load_daily_activity(folder='Fitabase Data 4.12.16-5.12.16')
    
    # Validate
    validator = DataValidator()
    report = validator.generate_validation_report(data, 'test')
    assert report['quality_score'] > 0
    
    # Clean
    cleaner = DataCleaner()
    cleaned = cleaner.remove_duplicates(data, subset=['Id', 'ActivityDate'])
    assert len(cleaned) <= len(data)
    
    # Engineer features
    engineer = FeatureEngineer()
    featured = engineer.create_temporal_features(cleaned, 'ActivityDate')
    assert len(featured.columns) > len(cleaned.columns)


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
