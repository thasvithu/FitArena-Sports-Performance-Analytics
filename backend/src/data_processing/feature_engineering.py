"""
Feature engineering module for FitArena
Creates features for machine learning models
"""
import pandas as pd
import numpy as np
from typing import List, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Feature engineering for athlete performance data"""
    
    def __init__(self):
        pass
    
    def create_temporal_features(self, df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """
        Create temporal features from date column
        
        Args:
            df: DataFrame with date column
            date_column: Name of the date column
            
        Returns:
            DataFrame with added temporal features
        """
        df = df.copy()
        
        # Ensure datetime type
        if df[date_column].dtype != 'datetime64[ns]':
            df[date_column] = pd.to_datetime(df[date_column])
        
        # Extract temporal features
        df['day_of_week'] = df[date_column].dt.dayofweek
        df['day_of_month'] = df[date_column].dt.day
        df['week_of_year'] = df[date_column].dt.isocalendar().week
        df['month'] = df[date_column].dt.month
        df['quarter'] = df[date_column].dt.quarter
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_month_start'] = df[date_column].dt.is_month_start.astype(int)
        df['is_month_end'] = df[date_column].dt.is_month_end.astype(int)
        
        logger.info("Created temporal features")
        return df
    
    def create_activity_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create derived features from activity data
        
        Args:
            df: DataFrame with activity metrics
            
        Returns:
            DataFrame with added activity features
        """
        df = df.copy()
        
        # Calculate total active minutes
        if all(col in df.columns for col in ['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes']):
            df['total_active_minutes'] = (
                df['VeryActiveMinutes'] + 
                df['FairlyActiveMinutes'] + 
                df['LightlyActiveMinutes']
            )
        
        # Activity intensity ratio
        if 'VeryActiveMinutes' in df.columns and 'total_active_minutes' in df.columns:
            df['high_intensity_ratio'] = df['VeryActiveMinutes'] / (df['total_active_minutes'] + 1)
        
        # Steps per kilometer (assuming TotalDistance is in km)
        if 'TotalSteps' in df.columns and 'TotalDistance' in df.columns:
            df['steps_per_km'] = df['TotalSteps'] / (df['TotalDistance'] + 0.001)
        
        # Calories per step
        if 'Calories' in df.columns and 'TotalSteps' in df.columns:
            df['calories_per_step'] = df['Calories'] / (df['TotalSteps'] + 1)
        
        # Calories per active minute
        if 'Calories' in df.columns and 'total_active_minutes' in df.columns:
            df['calories_per_active_minute'] = df['Calories'] / (df['total_active_minutes'] + 1)
        
        # Sedentary ratio
        if 'SedentaryMinutes' in df.columns:
            total_minutes = 24 * 60  # Minutes in a day
            df['sedentary_ratio'] = df['SedentaryMinutes'] / total_minutes
        
        # Activity diversity score
        if all(col in df.columns for col in ['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes']):
            df['activity_diversity'] = (
                (df['VeryActiveMinutes'] > 0).astype(int) +
                (df['FairlyActiveMinutes'] > 0).astype(int) +
                (df['LightlyActiveMinutes'] > 0).astype(int)
            )
        
        logger.info("Created activity features")
        return df
    
    def create_rolling_features(self, df: pd.DataFrame, group_col: str, 
                               value_cols: List[str], windows: List[int] = [3, 7, 14, 30]) -> pd.DataFrame:
        """
        Create rolling window features for trend analysis
        
        Args:
            df: DataFrame with time-series data
            group_col: Column to group by (e.g., 'Id')
            value_cols: Columns to calculate rolling statistics for
            windows: Window sizes for rolling calculations
            
        Returns:
            DataFrame with added rolling features
        """
        df = df.copy()
        df = df.sort_values(['Id', 'ActivityDate'])
        
        for col in value_cols:
            if col not in df.columns:
                continue
            
            for window in windows:
                # Rolling mean
                df[f'{col}_rolling_mean_{window}d'] = df.groupby(group_col)[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).mean()
                )
                
                # Rolling std
                df[f'{col}_rolling_std_{window}d'] = df.groupby(group_col)[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).std()
                )
                
                # Rolling max
                df[f'{col}_rolling_max_{window}d'] = df.groupby(group_col)[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).max()
                )
                
                # Rolling min
                df[f'{col}_rolling_min_{window}d'] = df.groupby(group_col)[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).min()
                )
        
        logger.info(f"Created rolling features for windows: {windows}")
        return df
    
    def create_lag_features(self, df: pd.DataFrame, group_col: str, 
                           value_cols: List[str], lags: List[int] = [1, 3, 7]) -> pd.DataFrame:
        """
        Create lag features for time-series prediction
        
        Args:
            df: DataFrame with time-series data
            group_col: Column to group by
            value_cols: Columns to create lags for
            lags: Lag periods
            
        Returns:
            DataFrame with added lag features
        """
        df = df.copy()
        df = df.sort_values([group_col, 'ActivityDate'])
        
        for col in value_cols:
            if col not in df.columns:
                continue
            
            for lag in lags:
                df[f'{col}_lag_{lag}'] = df.groupby(group_col)[col].shift(lag)
        
        logger.info(f"Created lag features for lags: {lags}")
        return df
    
    def create_change_features(self, df: pd.DataFrame, group_col: str, 
                              value_cols: List[str]) -> pd.DataFrame:
        """
        Create features showing change from previous values
        
        Args:
            df: DataFrame with time-series data
            group_col: Column to group by
            value_cols: Columns to calculate changes for
            
        Returns:
            DataFrame with added change features
        """
        df = df.copy()
        df = df.sort_values([group_col, 'ActivityDate'])
        
        for col in value_cols:
            if col not in df.columns:
                continue
            
            # Absolute change
            df[f'{col}_change'] = df.groupby(group_col)[col].diff()
            
            # Percentage change
            df[f'{col}_pct_change'] = df.groupby(group_col)[col].pct_change() * 100
        
        logger.info("Created change features")
        return df
    
    def create_aggregate_features(self, df: pd.DataFrame, group_col: str, 
                                 value_cols: List[str]) -> pd.DataFrame:
        """
        Create aggregate features per user/group
        
        Args:
            df: DataFrame with data
            group_col: Column to group by
            value_cols: Columns to aggregate
            
        Returns:
            DataFrame with added aggregate features
        """
        df = df.copy()
        
        for col in value_cols:
            if col not in df.columns:
                continue
            
            # Mean per user
            df[f'{col}_user_mean'] = df.groupby(group_col)[col].transform('mean')
            
            # Std per user
            df[f'{col}_user_std'] = df.groupby(group_col)[col].transform('std')
            
            # Max per user
            df[f'{col}_user_max'] = df.groupby(group_col)[col].transform('max')
            
            # Min per user
            df[f'{col}_user_min'] = df.groupby(group_col)[col].transform('min')
            
            # Deviation from user mean
            df[f'{col}_deviation_from_mean'] = df[col] - df[f'{col}_user_mean']
        
        logger.info("Created aggregate features")
        return df
    
    def create_performance_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create high-level performance indicators
        
        Args:
            df: DataFrame with activity data
            
        Returns:
            DataFrame with performance indicators
        """
        df = df.copy()
        
        # Performance score (0-100)
        if all(col in df.columns for col in ['TotalSteps', 'VeryActiveMinutes', 'Calories']):
            # Normalize each metric to 0-1 scale
            steps_score = np.clip(df['TotalSteps'] / 15000, 0, 1) * 40  # 40% weight
            activity_score = np.clip(df['VeryActiveMinutes'] / 60, 0, 1) * 30  # 30% weight
            calorie_score = np.clip(df['Calories'] / 3000, 0, 1) * 30  # 30% weight
            
            df['performance_score'] = (steps_score + activity_score + calorie_score)
        
        # Fitness level category
        if 'performance_score' in df.columns:
            df['fitness_level'] = pd.cut(
                df['performance_score'],
                bins=[0, 30, 50, 70, 100],
                labels=['Low', 'Moderate', 'Good', 'Excellent']
            )
        
        # Activity consistency (coefficient of variation)
        if 'TotalSteps' in df.columns:
            df['steps_consistency'] = df.groupby('Id')['TotalSteps'].transform(
                lambda x: x.std() / (x.mean() + 1)
            )
        
        # Recovery indicator (based on sedentary time and sleep)
        if 'SedentaryMinutes' in df.columns:
            df['recovery_indicator'] = np.clip(df['SedentaryMinutes'] / 720, 0, 1)  # Normalized to 12 hours
        
        logger.info("Created performance indicators")
        return df
    
    def create_all_features(self, df: pd.DataFrame, date_column: str = 'ActivityDate') -> pd.DataFrame:
        """
        Create all features in one pipeline
        
        Args:
            df: DataFrame with raw data
            date_column: Name of the date column
            
        Returns:
            DataFrame with all engineered features
        """
        logger.info("Starting comprehensive feature engineering...")
        
        # Temporal features
        df = self.create_temporal_features(df, date_column)
        
        # Activity features
        df = self.create_activity_features(df)
        
        # Performance indicators
        df = self.create_performance_indicators(df)
        
        # Time-series features
        value_cols = ['TotalSteps', 'Calories', 'TotalDistance']
        value_cols = [col for col in value_cols if col in df.columns]
        
        if value_cols:
            df = self.create_rolling_features(df, 'Id', value_cols, windows=[3, 7, 14])
            df = self.create_lag_features(df, 'Id', value_cols, lags=[1, 3, 7])
            df = self.create_change_features(df, 'Id', value_cols)
            df = self.create_aggregate_features(df, 'Id', value_cols)
        
        logger.info("Feature engineering completed!")
        return df


if __name__ == "__main__":
    print("Feature engineering module loaded successfully!")
