"""
Analytics dashboard module for FitArena
Provides analytics and insights for performance data
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class PerformanceAnalytics:
    """Analytics for athlete performance data"""
    
    def __init__(self):
        pass
    
    def calculate_summary_statistics(self, df: pd.DataFrame, athlete_id: str = None) -> Dict:
        """
        Calculate summary statistics
        
        Args:
            df: DataFrame with activity data
            athlete_id: Specific athlete ID (None for all athletes)
            
        Returns:
            Dictionary with summary statistics
        """
        if athlete_id:
            data = df[df['Id'] == athlete_id].copy()
        else:
            data = df.copy()
        
        summary = {
            'total_records': len(data),
            'unique_athletes': data['Id'].nunique(),
            'date_range': {
                'start': data['ActivityDate'].min().strftime('%Y-%m-%d') if 'ActivityDate' in data.columns else None,
                'end': data['ActivityDate'].max().strftime('%Y-%m-%d') if 'ActivityDate' in data.columns else None,
                'days': (data['ActivityDate'].max() - data['ActivityDate'].min()).days if 'ActivityDate' in data.columns else 0
            },
            'averages': {
                'steps': round(data['TotalSteps'].mean(), 2) if 'TotalSteps' in data.columns else 0,
                'distance_km': round(data['TotalDistance'].mean(), 2) if 'TotalDistance' in data.columns else 0,
                'calories': round(data['Calories'].mean(), 2) if 'Calories' in data.columns else 0,
                'active_minutes': round(data['total_active_minutes'].mean(), 2) if 'total_active_minutes' in data.columns else 0,
                'sedentary_minutes': round(data['SedentaryMinutes'].mean(), 2) if 'SedentaryMinutes' in data.columns else 0
            },
            'totals': {
                'steps': int(data['TotalSteps'].sum()) if 'TotalSteps' in data.columns else 0,
                'distance_km': round(data['TotalDistance'].sum(), 2) if 'TotalDistance' in data.columns else 0,
                'calories': int(data['Calories'].sum()) if 'Calories' in data.columns else 0
            }
        }
        
        return summary
    
    def calculate_performance_trends(self, df: pd.DataFrame, athlete_id: str, 
                                    window: int = 7) -> pd.DataFrame:
        """
        Calculate performance trends over time
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID
            window: Rolling window size for trends
            
        Returns:
            DataFrame with trend data
        """
        athlete_data = df[df['Id'] == athlete_id].copy()
        athlete_data = athlete_data.sort_values('ActivityDate')
        
        # Calculate rolling averages
        metrics = ['TotalSteps', 'TotalDistance', 'Calories']
        
        for metric in metrics:
            if metric in athlete_data.columns:
                athlete_data[f'{metric}_trend'] = athlete_data[metric].rolling(
                    window=window, min_periods=1
                ).mean()
        
        return athlete_data
    
    def compare_athletes(self, df: pd.DataFrame, athlete_ids: List[str], 
                        metrics: List[str] = None) -> pd.DataFrame:
        """
        Compare performance metrics across athletes
        
        Args:
            df: DataFrame with activity data
            athlete_ids: List of athlete IDs to compare
            metrics: Metrics to compare
            
        Returns:
            DataFrame with comparison data
        """
        if metrics is None:
            metrics = ['TotalSteps', 'TotalDistance', 'Calories', 'total_active_minutes']
        
        comparison_data = []
        
        for athlete_id in athlete_ids:
            athlete_data = df[df['Id'] == athlete_id]
            
            if len(athlete_data) == 0:
                continue
            
            athlete_stats = {'athlete_id': athlete_id}
            
            for metric in metrics:
                if metric in athlete_data.columns:
                    athlete_stats[f'{metric}_avg'] = athlete_data[metric].mean()
                    athlete_stats[f'{metric}_total'] = athlete_data[metric].sum()
                    athlete_stats[f'{metric}_max'] = athlete_data[metric].max()
            
            comparison_data.append(athlete_stats)
        
        return pd.DataFrame(comparison_data)
    
    def calculate_consistency_metrics(self, df: pd.DataFrame, athlete_id: str) -> Dict:
        """
        Calculate consistency metrics for an athlete
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID
            
        Returns:
            Dictionary with consistency metrics
        """
        athlete_data = df[df['Id'] == athlete_id].copy()
        
        metrics = {
            'athlete_id': athlete_id,
            'total_days': len(athlete_data)
        }
        
        # Calculate coefficient of variation for key metrics
        for col in ['TotalSteps', 'Calories', 'TotalDistance']:
            if col in athlete_data.columns:
                mean_val = athlete_data[col].mean()
                std_val = athlete_data[col].std()
                cv = (std_val / mean_val) if mean_val > 0 else 0
                
                metrics[f'{col}_cv'] = round(cv, 4)
                metrics[f'{col}_consistency_score'] = round(max(0, min(100, 100 * (1 - cv))), 2)
        
        return metrics
    
    def identify_best_performance_days(self, df: pd.DataFrame, athlete_id: str, 
                                      top_n: int = 5) -> pd.DataFrame:
        """
        Identify best performance days
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID
            top_n: Number of top days to return
            
        Returns:
            DataFrame with best performance days
        """
        athlete_data = df[df['Id'] == athlete_id].copy()
        
        if 'performance_score' in athlete_data.columns:
            top_days = athlete_data.nlargest(top_n, 'performance_score')
        elif 'TotalSteps' in athlete_data.columns:
            top_days = athlete_data.nlargest(top_n, 'TotalSteps')
        else:
            return pd.DataFrame()
        
        return top_days[['ActivityDate', 'TotalSteps', 'TotalDistance', 'Calories', 
                        'VeryActiveMinutes', 'performance_score']].reset_index(drop=True)
    
    def analyze_weekly_patterns(self, df: pd.DataFrame, athlete_id: str = None) -> pd.DataFrame:
        """
        Analyze weekly activity patterns
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID (None for all athletes)
            
        Returns:
            DataFrame with weekly pattern analysis
        """
        if athlete_id:
            data = df[df['Id'] == athlete_id].copy()
        else:
            data = df.copy()
        
        # Group by day of week
        if 'day_of_week' not in data.columns and 'ActivityDate' in data.columns:
            data['day_of_week'] = pd.to_datetime(data['ActivityDate']).dt.dayofweek
        
        weekly_pattern = data.groupby('day_of_week').agg({
            'TotalSteps': ['mean', 'std'],
            'Calories': ['mean', 'std'],
            'TotalDistance': ['mean', 'std']
        }).round(2)
        
        # Add day names
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_pattern.index = [day_names[i] for i in weekly_pattern.index]
        
        return weekly_pattern
    
    def calculate_goal_achievement(self, df: pd.DataFrame, athlete_id: str, 
                                  goals: Dict[str, float]) -> Dict:
        """
        Calculate goal achievement rates
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID
            goals: Dictionary of goals (e.g., {'TotalSteps': 10000})
            
        Returns:
            Dictionary with achievement rates
        """
        athlete_data = df[df['Id'] == athlete_id].copy()
        
        achievement = {
            'athlete_id': athlete_id,
            'total_days': len(athlete_data),
            'goals': {}
        }
        
        for metric, target in goals.items():
            if metric in athlete_data.columns:
                days_achieved = (athlete_data[metric] >= target).sum()
                achievement_rate = (days_achieved / len(athlete_data)) * 100
                
                achievement['goals'][metric] = {
                    'target': target,
                    'days_achieved': int(days_achieved),
                    'achievement_rate': round(achievement_rate, 2),
                    'average_value': round(athlete_data[metric].mean(), 2)
                }
        
        return achievement
    
    def generate_performance_report(self, df: pd.DataFrame, athlete_id: str) -> Dict:
        """
        Generate comprehensive performance report
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID
            
        Returns:
            Dictionary with complete performance report
        """
        logger.info(f"Generating performance report for athlete {athlete_id}")
        
        report = {
            'athlete_id': athlete_id,
            'generated_at': datetime.now().isoformat(),
            'summary': self.calculate_summary_statistics(df, athlete_id),
            'consistency': self.calculate_consistency_metrics(df, athlete_id),
            'best_days': self.identify_best_performance_days(df, athlete_id).to_dict('records'),
            'weekly_patterns': self.analyze_weekly_patterns(df, athlete_id).to_dict(),
            'goal_achievement': self.calculate_goal_achievement(
                df, athlete_id, 
                {'TotalSteps': 10000, 'Calories': 2500}
            )
        }
        
        logger.info(f"Performance report generated for athlete {athlete_id}")
        
        return report


class TeamAnalytics:
    """Analytics for team-level insights"""
    
    def __init__(self):
        pass
    
    def calculate_team_summary(self, df: pd.DataFrame) -> Dict:
        """
        Calculate team-wide summary statistics
        
        Args:
            df: DataFrame with all team data
            
        Returns:
            Dictionary with team summary
        """
        summary = {
            'total_athletes': df['Id'].nunique(),
            'total_records': len(df),
            'date_range': {
                'start': df['ActivityDate'].min().strftime('%Y-%m-%d') if 'ActivityDate' in df.columns else None,
                'end': df['ActivityDate'].max().strftime('%Y-%m-%d') if 'ActivityDate' in df.columns else None
            },
            'team_averages': {
                'steps': round(df['TotalSteps'].mean(), 2) if 'TotalSteps' in df.columns else 0,
                'distance': round(df['TotalDistance'].mean(), 2) if 'TotalDistance' in df.columns else 0,
                'calories': round(df['Calories'].mean(), 2) if 'Calories' in df.columns else 0
            },
            'team_totals': {
                'steps': int(df['TotalSteps'].sum()) if 'TotalSteps' in df.columns else 0,
                'distance': round(df['TotalDistance'].sum(), 2) if 'TotalDistance' in df.columns else 0,
                'calories': int(df['Calories'].sum()) if 'Calories' in df.columns else 0
            }
        }
        
        return summary
    
    def identify_top_performers(self, df: pd.DataFrame, metric: str = 'TotalSteps', 
                               top_n: int = 10) -> pd.DataFrame:
        """
        Identify top performing athletes
        
        Args:
            df: DataFrame with activity data
            metric: Metric to rank by
            top_n: Number of top performers
            
        Returns:
            DataFrame with top performers
        """
        athlete_stats = df.groupby('Id').agg({
            metric: ['mean', 'sum', 'count']
        }).reset_index()
        
        athlete_stats.columns = ['athlete_id', f'{metric}_avg', f'{metric}_total', 'days_active']
        athlete_stats = athlete_stats.sort_values(f'{metric}_total', ascending=False).head(top_n)
        
        return athlete_stats
    
    def calculate_team_diversity(self, df: pd.DataFrame) -> Dict:
        """
        Calculate diversity metrics for the team
        
        Args:
            df: DataFrame with activity data
            
        Returns:
            Dictionary with diversity metrics
        """
        diversity = {
            'activity_level_distribution': {},
            'performance_distribution': {}
        }
        
        # Activity level distribution
        if 'fitness_level' in df.columns:
            dist = df.groupby('fitness_level')['Id'].nunique().to_dict()
            diversity['activity_level_distribution'] = dist
        
        # Performance score distribution
        if 'performance_score' in df.columns:
            diversity['performance_distribution'] = {
                'mean': round(df['performance_score'].mean(), 2),
                'median': round(df['performance_score'].median(), 2),
                'std': round(df['performance_score'].std(), 2),
                'min': round(df['performance_score'].min(), 2),
                'max': round(df['performance_score'].max(), 2)
            }
        
        return diversity


if __name__ == "__main__":
    print("Analytics module loaded successfully!")
