"""
Data loader module for FitArena
Handles loading and initial processing of Fitbit data
"""
import pandas as pd
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load and manage Fitbit dataset"""
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize DataLoader
        
        Args:
            data_dir: Base directory containing Fitbit data folders
        """
        self.data_dir = Path(data_dir)
        self.datasets = {}
        
    def load_daily_activity(self, folder: str = "Fitabase Data 4.12.16-5.12.16") -> pd.DataFrame:
        """Load daily activity data"""
        file_path = self.data_dir / folder / "dailyActivity_merged.csv"
        logger.info(f"Loading daily activity from {file_path}")
        
        df = pd.read_csv(file_path)
        df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])
        df['Id'] = df['Id'].astype(str)
        
        logger.info(f"Loaded {len(df)} records from daily activity")
        return df
    
    def load_hourly_data(self, folder: str = "Fitabase Data 4.12.16-5.12.16") -> Dict[str, pd.DataFrame]:
        """Load all hourly data (calories, intensities, steps)"""
        hourly_data = {}
        
        files = {
            'calories': 'hourlyCalories_merged.csv',
            'intensities': 'hourlyIntensities_merged.csv',
            'steps': 'hourlySteps_merged.csv'
        }
        
        for key, filename in files.items():
            file_path = self.data_dir / folder / filename
            logger.info(f"Loading {key} from {file_path}")
            
            df = pd.read_csv(file_path)
            df['ActivityHour'] = pd.to_datetime(df['ActivityHour'])
            df['Id'] = df['Id'].astype(str)
            hourly_data[key] = df
            
            logger.info(f"Loaded {len(df)} records from hourly {key}")
        
        return hourly_data
    
    def load_minute_data(self, folder: str = "Fitabase Data 4.12.16-5.12.16", 
                        data_type: str = 'narrow') -> Dict[str, pd.DataFrame]:
        """
        Load minute-level data
        
        Args:
            folder: Data folder name
            data_type: 'narrow' or 'wide' format
        """
        minute_data = {}
        
        format_suffix = 'Narrow' if data_type == 'narrow' else 'Wide'
        
        files = {
            'calories': f'minuteCalories{format_suffix}_merged.csv',
            'intensities': f'minuteIntensities{format_suffix}_merged.csv',
            'steps': f'minuteSteps{format_suffix}_merged.csv',
            'mets': f'minuteMETs{format_suffix}_merged.csv'
        }
        
        for key, filename in files.items():
            file_path = self.data_dir / folder / filename
            
            if file_path.exists():
                logger.info(f"Loading minute {key} from {file_path}")
                df = pd.read_csv(file_path)
                
                # Parse datetime column
                time_col = 'ActivityMinute' if 'ActivityMinute' in df.columns else df.columns[1]
                df[time_col] = pd.to_datetime(df[time_col])
                df['Id'] = df['Id'].astype(str)
                
                minute_data[key] = df
                logger.info(f"Loaded {len(df)} records from minute {key}")
        
        return minute_data
    
    def load_heartrate_data(self, folder: str = "Fitabase Data 4.12.16-5.12.16") -> pd.DataFrame:
        """Load heart rate data (second-level)"""
        file_path = self.data_dir / folder / "heartrate_seconds_merged.csv"
        logger.info(f"Loading heart rate data from {file_path}")
        
        df = pd.read_csv(file_path)
        df['Time'] = pd.to_datetime(df['Time'])
        df['Id'] = df['Id'].astype(str)
        
        logger.info(f"Loaded {len(df)} records from heart rate data")
        return df
    
    def load_sleep_data(self, folder: str = "Fitabase Data 4.12.16-5.12.16") -> pd.DataFrame:
        """Load sleep data"""
        # Try sleepDay first, then minuteSleep
        sleep_day_path = self.data_dir / folder / "sleepDay_merged.csv"
        minute_sleep_path = self.data_dir / folder / "minuteSleep_merged.csv"
        
        if sleep_day_path.exists():
            logger.info(f"Loading sleep day data from {sleep_day_path}")
            df = pd.read_csv(sleep_day_path)
            df['SleepDay'] = pd.to_datetime(df['SleepDay'])
            df['Id'] = df['Id'].astype(str)
            logger.info(f"Loaded {len(df)} records from sleep day")
            return df
        elif minute_sleep_path.exists():
            logger.info(f"Loading minute sleep data from {minute_sleep_path}")
            df = pd.read_csv(minute_sleep_path)
            df['date'] = pd.to_datetime(df['date'])
            df['Id'] = df['Id'].astype(str)
            logger.info(f"Loaded {len(df)} records from minute sleep")
            return df
        else:
            logger.warning("No sleep data found")
            return pd.DataFrame()
    
    def load_weight_data(self, folder: str = "Fitabase Data 4.12.16-5.12.16") -> pd.DataFrame:
        """Load weight log data"""
        file_path = self.data_dir / folder / "weightLogInfo_merged.csv"
        logger.info(f"Loading weight data from {file_path}")
        
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Id'] = df['Id'].astype(str)
        
        logger.info(f"Loaded {len(df)} records from weight data")
        return df
    
    def load_all_data(self, folder: str = "Fitabase Data 4.12.16-5.12.16") -> Dict[str, pd.DataFrame]:
        """
        Load all available datasets
        
        Returns:
            Dictionary containing all loaded datasets
        """
        logger.info("Loading all datasets...")
        
        all_data = {
            'daily_activity': self.load_daily_activity(folder),
            'hourly_data': self.load_hourly_data(folder),
            'sleep': self.load_sleep_data(folder),
            'weight': self.load_weight_data(folder),
            'heartrate': self.load_heartrate_data(folder)
        }
        
        # Try to load minute data (may not exist for all folders)
        try:
            all_data['minute_data'] = self.load_minute_data(folder)
        except Exception as e:
            logger.warning(f"Could not load minute data: {e}")
        
        logger.info("All datasets loaded successfully!")
        return all_data
    
    def get_data_summary(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Get summary statistics for all loaded datasets
        
        Args:
            data: Dictionary of datasets
            
        Returns:
            DataFrame with summary statistics
        """
        summary_data = []
        
        for name, df in data.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                summary_data.append({
                    'Dataset': name,
                    'Rows': len(df),
                    'Columns': len(df.columns),
                    'Memory (MB)': round(df.memory_usage(deep=True).sum() / 1024**2, 2),
                    'Unique Users': df['Id'].nunique() if 'Id' in df.columns else 'N/A'
                })
            elif isinstance(df, dict):
                for sub_name, sub_df in df.items():
                    if isinstance(sub_df, pd.DataFrame) and not sub_df.empty:
                        summary_data.append({
                            'Dataset': f"{name}_{sub_name}",
                            'Rows': len(sub_df),
                            'Columns': len(sub_df.columns),
                            'Memory (MB)': round(sub_df.memory_usage(deep=True).sum() / 1024**2, 2),
                            'Unique Users': sub_df['Id'].nunique() if 'Id' in sub_df.columns else 'N/A'
                        })
        
        return pd.DataFrame(summary_data)


if __name__ == "__main__":
    # Test the data loader
    loader = DataLoader(data_dir="./data")
    data = loader.load_all_data()
    summary = loader.get_data_summary(data)
    print("\nData Summary:")
    print(summary)
