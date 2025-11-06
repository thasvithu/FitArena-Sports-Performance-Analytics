"""
Visualization module for FitArena
Creates charts and visualizations for performance data
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class PerformanceVisualizer:
    """Create visualizations for performance analytics"""
    
    def __init__(self, style: str = 'plotly'):
        """
        Initialize visualizer
        
        Args:
            style: 'plotly' or 'matplotlib'
        """
        self.style = style
    
    def plot_activity_trends(self, df: pd.DataFrame, athlete_id: str, 
                            metrics: List[str] = None) -> go.Figure:
        """
        Plot activity trends over time
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID
            metrics: Metrics to plot
            
        Returns:
            Plotly figure
        """
        athlete_data = df[df['Id'] == athlete_id].copy()
        athlete_data = athlete_data.sort_values('ActivityDate')
        
        if metrics is None:
            metrics = ['TotalSteps', 'Calories', 'TotalDistance']
        
        # Create subplots
        fig = make_subplots(
            rows=len(metrics), cols=1,
            subplot_titles=metrics,
            vertical_spacing=0.1
        )
        
        for idx, metric in enumerate(metrics, 1):
            if metric in athlete_data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=athlete_data['ActivityDate'],
                        y=athlete_data[metric],
                        mode='lines+markers',
                        name=metric,
                        line=dict(width=2),
                        marker=dict(size=6)
                    ),
                    row=idx, col=1
                )
        
        fig.update_layout(
            height=300 * len(metrics),
            title_text=f"Activity Trends for Athlete {athlete_id}",
            showlegend=False,
            hovermode='x unified'
        )
        
        return fig
    
    def plot_weekly_patterns(self, df: pd.DataFrame, athlete_id: str = None) -> go.Figure:
        """
        Plot weekly activity patterns
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID (None for all athletes)
            
        Returns:
            Plotly figure
        """
        if athlete_id:
            data = df[df['Id'] == athlete_id].copy()
        else:
            data = df.copy()
        
        # Ensure day_of_week exists
        if 'day_of_week' not in data.columns:
            data['day_of_week'] = pd.to_datetime(data['ActivityDate']).dt.dayofweek
        
        # Calculate averages by day
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_avg = data.groupby('day_of_week').agg({
            'TotalSteps': 'mean',
            'Calories': 'mean',
            'TotalDistance': 'mean'
        }).reset_index()
        
        weekly_avg['day_name'] = weekly_avg['day_of_week'].apply(lambda x: day_names[x])
        
        # Create figure
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=weekly_avg['day_name'],
            y=weekly_avg['TotalSteps'],
            name='Steps',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title="Weekly Activity Patterns",
            xaxis_title="Day of Week",
            yaxis_title="Average Steps",
            hovermode='x'
        )
        
        return fig
    
    def plot_performance_distribution(self, df: pd.DataFrame) -> go.Figure:
        """
        Plot performance score distribution
        
        Args:
            df: DataFrame with performance scores
            
        Returns:
            Plotly figure
        """
        if 'performance_score' not in df.columns:
            return go.Figure()
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=df['performance_score'],
            nbinsx=20,
            marker_color='lightgreen',
            name='Performance Score'
        ))
        
        fig.update_layout(
            title="Performance Score Distribution",
            xaxis_title="Performance Score",
            yaxis_title="Count",
            showlegend=False
        )
        
        return fig
    
    def plot_athlete_comparison(self, df: pd.DataFrame, athlete_ids: List[str], 
                               metric: str = 'TotalSteps') -> go.Figure:
        """
        Compare multiple athletes
        
        Args:
            df: DataFrame with activity data
            athlete_ids: List of athlete IDs to compare
            metric: Metric to compare
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        for athlete_id in athlete_ids:
            athlete_data = df[df['Id'] == athlete_id].sort_values('ActivityDate')
            
            if len(athlete_data) > 0:
                fig.add_trace(go.Scatter(
                    x=athlete_data['ActivityDate'],
                    y=athlete_data[metric],
                    mode='lines',
                    name=f'Athlete {athlete_id}',
                    line=dict(width=2)
                ))
        
        fig.update_layout(
            title=f"{metric} Comparison Across Athletes",
            xaxis_title="Date",
            yaxis_title=metric,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def plot_correlation_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """
        Plot correlation heatmap of metrics
        
        Args:
            df: DataFrame with metrics
            
        Returns:
            Plotly figure
        """
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Calculate correlation
        corr_matrix = df[numeric_cols].corr()
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Correlation Heatmap of Performance Metrics",
            width=800,
            height=800
        )
        
        return fig
    
    def plot_goal_progress(self, df: pd.DataFrame, athlete_id: str, 
                          goal_metric: str, goal_value: float) -> go.Figure:
        """
        Plot progress towards a goal
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID
            goal_metric: Metric to track
            goal_value: Goal value
            
        Returns:
            Plotly figure
        """
        athlete_data = df[df['Id'] == athlete_id].sort_values('ActivityDate')
        
        if goal_metric not in athlete_data.columns:
            return go.Figure()
        
        fig = go.Figure()
        
        # Actual values
        fig.add_trace(go.Scatter(
            x=athlete_data['ActivityDate'],
            y=athlete_data[goal_metric],
            mode='lines+markers',
            name='Actual',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ))
        
        # Goal line
        fig.add_trace(go.Scatter(
            x=athlete_data['ActivityDate'],
            y=[goal_value] * len(athlete_data),
            mode='lines',
            name='Goal',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # 7-day moving average
        if len(athlete_data) >= 7:
            ma_7 = athlete_data[goal_metric].rolling(window=7, min_periods=1).mean()
            fig.add_trace(go.Scatter(
                x=athlete_data['ActivityDate'],
                y=ma_7,
                mode='lines',
                name='7-day Average',
                line=dict(color='green', width=2)
            ))
        
        fig.update_layout(
            title=f"Progress Towards {goal_metric} Goal",
            xaxis_title="Date",
            yaxis_title=goal_metric,
            hovermode='x unified'
        )
        
        return fig
    
    def plot_activity_heatmap(self, df: pd.DataFrame, athlete_id: str) -> go.Figure:
        """
        Create activity heatmap (calendar style)
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID
            
        Returns:
            Plotly figure
        """
        athlete_data = df[df['Id'] == athlete_id].copy()
        
        # Add temporal features if not present
        if 'day_of_week' not in athlete_data.columns:
            athlete_data['day_of_week'] = pd.to_datetime(athlete_data['ActivityDate']).dt.dayofweek
        if 'week_of_year' not in athlete_data.columns:
            athlete_data['week_of_year'] = pd.to_datetime(athlete_data['ActivityDate']).dt.isocalendar().week
        
        # Create pivot table
        pivot_data = athlete_data.pivot_table(
            values='TotalSteps',
            index='day_of_week',
            columns='week_of_year',
            aggfunc='mean'
        )
        
        # Day names
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=[day_names[i] for i in pivot_data.index],
            colorscale='Viridis',
            colorbar=dict(title="Steps")
        ))
        
        fig.update_layout(
            title=f"Activity Heatmap for Athlete {athlete_id}",
            xaxis_title="Week of Year",
            yaxis_title="Day of Week"
        )
        
        return fig
    
    def create_dashboard(self, df: pd.DataFrame, athlete_id: str) -> go.Figure:
        """
        Create comprehensive dashboard
        
        Args:
            df: DataFrame with activity data
            athlete_id: Athlete ID
            
        Returns:
            Plotly figure with multiple subplots
        """
        athlete_data = df[df['Id'] == athlete_id].sort_values('ActivityDate')
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Daily Steps Trend',
                'Activity Distribution',
                'Calories vs Distance',
                'Performance Score'
            ),
            specs=[
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "scatter"}]
            ]
        )
        
        # 1. Steps trend
        fig.add_trace(
            go.Scatter(
                x=athlete_data['ActivityDate'],
                y=athlete_data['TotalSteps'],
                mode='lines',
                name='Steps',
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        
        # 2. Activity minutes distribution
        if all(col in athlete_data.columns for col in ['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes']):
            activity_avg = {
                'Very Active': athlete_data['VeryActiveMinutes'].mean(),
                'Fairly Active': athlete_data['FairlyActiveMinutes'].mean(),
                'Lightly Active': athlete_data['LightlyActiveMinutes'].mean()
            }
            fig.add_trace(
                go.Bar(
                    x=list(activity_avg.keys()),
                    y=list(activity_avg.values()),
                    marker_color=['red', 'orange', 'lightblue']
                ),
                row=1, col=2
            )
        
        # 3. Calories vs Distance
        fig.add_trace(
            go.Scatter(
                x=athlete_data['TotalDistance'],
                y=athlete_data['Calories'],
                mode='markers',
                name='Calories vs Distance',
                marker=dict(color='green', size=8)
            ),
            row=2, col=1
        )
        
        # 4. Performance score
        if 'performance_score' in athlete_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=athlete_data['ActivityDate'],
                    y=athlete_data['performance_score'],
                    mode='lines+markers',
                    name='Performance',
                    line=dict(color='purple')
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            height=800,
            showlegend=False,
            title_text=f"Performance Dashboard - Athlete {athlete_id}"
        )
        
        return fig


if __name__ == "__main__":
    print("Visualization module loaded successfully!")
