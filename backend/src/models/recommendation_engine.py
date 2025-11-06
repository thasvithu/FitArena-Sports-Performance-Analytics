"""
AI-powered recommendation engine for FitArena
Provides personalized training and improvement recommendations
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Generate personalized recommendations for athletes"""
    
    def __init__(self):
        """Initialize recommendation engine"""
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> Dict:
        """Initialize recommendation rules"""
        return {
            'steps': {
                'low': {'threshold': 5000, 'target': 10000},
                'moderate': {'threshold': 10000, 'target': 15000},
                'high': {'threshold': 15000, 'target': 20000}
            },
            'activity_minutes': {
                'low': {'threshold': 30, 'target': 60},
                'moderate': {'threshold': 60, 'target': 90},
                'high': {'threshold': 90, 'target': 120}
            },
            'sedentary': {
                'high': {'threshold': 600, 'target': 480},
                'moderate': {'threshold': 480, 'target': 360}
            }
        }
    
    def analyze_activity_patterns(self, df: pd.DataFrame, athlete_id: str) -> Dict:
        """
        Analyze athlete's activity patterns
        
        Args:
            df: DataFrame with athlete data
            athlete_id: Athlete ID to analyze
            
        Returns:
            Dictionary with analysis results
        """
        athlete_data = df[df['Id'] == athlete_id].copy()
        
        if len(athlete_data) == 0:
            return {'error': 'No data found for athlete'}
        
        # Sort by date
        athlete_data = athlete_data.sort_values('ActivityDate')
        
        # Calculate statistics
        analysis = {
            'athlete_id': athlete_id,
            'total_days': len(athlete_data),
            'avg_steps': athlete_data['TotalSteps'].mean(),
            'avg_distance': athlete_data['TotalDistance'].mean(),
            'avg_calories': athlete_data['Calories'].mean(),
            'avg_active_minutes': athlete_data.get('total_active_minutes', pd.Series([0])).mean(),
            'avg_sedentary_minutes': athlete_data.get('SedentaryMinutes', pd.Series([0])).mean(),
            'steps_trend': self._calculate_trend(athlete_data['TotalSteps']),
            'consistency_score': self._calculate_consistency(athlete_data['TotalSteps']),
            'performance_score': athlete_data.get('performance_score', pd.Series([50])).mean()
        }
        
        return analysis
    
    def _calculate_trend(self, series: pd.Series) -> str:
        """Calculate trend direction"""
        if len(series) < 2:
            return 'stable'
        
        # Simple linear regression slope
        x = np.arange(len(series))
        y = series.values
        
        # Handle NaN values
        mask = ~np.isnan(y)
        if mask.sum() < 2:
            return 'stable'
        
        x_clean = x[mask]
        y_clean = y[mask]
        
        slope = np.polyfit(x_clean, y_clean, 1)[0]
        
        if slope > 100:
            return 'improving'
        elif slope < -100:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_consistency(self, series: pd.Series) -> float:
        """Calculate consistency score (0-100)"""
        if len(series) < 2:
            return 50.0
        
        # Coefficient of variation (lower is more consistent)
        cv = series.std() / (series.mean() + 1)
        
        # Convert to 0-100 score (lower CV = higher score)
        consistency = max(0, min(100, 100 * (1 - cv)))
        
        return round(consistency, 2)
    
    def generate_activity_recommendations(self, analysis: Dict) -> List[Dict]:
        """
        Generate activity-based recommendations
        
        Args:
            analysis: Analysis results
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        avg_steps = analysis.get('avg_steps', 0)
        avg_active_minutes = analysis.get('avg_active_minutes', 0)
        avg_sedentary = analysis.get('avg_sedentary_minutes', 0)
        trend = analysis.get('steps_trend', 'stable')
        
        # Steps recommendations
        if avg_steps < self.rules['steps']['low']['threshold']:
            recommendations.append({
                'type': 'activity',
                'priority': 'high',
                'title': 'Increase Daily Steps',
                'description': f"Your average daily steps ({int(avg_steps)}) is below the recommended level. "
                             f"Aim for {self.rules['steps']['low']['target']} steps per day.",
                'action_items': [
                    'Take short walking breaks every hour',
                    'Use stairs instead of elevators',
                    'Park further from your destination',
                    'Take a 15-minute walk after meals'
                ],
                'expected_benefit': 'Improved cardiovascular health and weight management',
                'confidence': 0.9
            })
        elif avg_steps < self.rules['steps']['moderate']['threshold']:
            recommendations.append({
                'type': 'activity',
                'priority': 'medium',
                'title': 'Enhance Activity Level',
                'description': f"Good progress! Increase from {int(avg_steps)} to {self.rules['steps']['moderate']['target']} steps daily.",
                'action_items': [
                    'Add a 20-minute morning walk',
                    'Join a walking group or find a walking partner',
                    'Explore new routes to keep it interesting'
                ],
                'expected_benefit': 'Enhanced endurance and stamina',
                'confidence': 0.85
            })
        
        # Active minutes recommendations
        if avg_active_minutes < self.rules['activity_minutes']['low']['threshold']:
            recommendations.append({
                'type': 'intensity',
                'priority': 'high',
                'title': 'Boost Active Minutes',
                'description': f"Increase your daily active minutes from {int(avg_active_minutes)} to at least "
                             f"{self.rules['activity_minutes']['low']['target']} minutes.",
                'action_items': [
                    'Schedule 30 minutes of moderate exercise daily',
                    'Try activities you enjoy (swimming, cycling, dancing)',
                    'Break it into 3x10-minute sessions if needed'
                ],
                'expected_benefit': 'Significant fitness improvement and energy boost',
                'confidence': 0.95
            })
        
        # Sedentary time recommendations
        if avg_sedentary > self.rules['sedentary']['high']['threshold']:
            recommendations.append({
                'type': 'behavior',
                'priority': 'high',
                'title': 'Reduce Sedentary Time',
                'description': f"Your sedentary time ({int(avg_sedentary)} min/day) is high. "
                             f"Target: {self.rules['sedentary']['high']['target']} minutes.",
                'action_items': [
                    'Set hourly movement reminders',
                    'Use a standing desk or desk converter',
                    'Take active breaks during work',
                    'Stand during phone calls'
                ],
                'expected_benefit': 'Reduced risk of metabolic issues and improved posture',
                'confidence': 0.88
            })
        
        # Trend-based recommendations
        if trend == 'declining':
            recommendations.append({
                'type': 'motivation',
                'priority': 'high',
                'title': 'Reverse Declining Trend',
                'description': 'Your activity level has been declining. Let\'s get back on track!',
                'action_items': [
                    'Set realistic, achievable daily goals',
                    'Find an accountability partner',
                    'Reward yourself for meeting weekly targets',
                    'Identify and address barriers to activity'
                ],
                'expected_benefit': 'Restored motivation and activity levels',
                'confidence': 0.80
            })
        elif trend == 'improving':
            recommendations.append({
                'type': 'motivation',
                'priority': 'low',
                'title': 'Maintain Positive Momentum',
                'description': 'Great job! Your activity is trending upward. Keep it up!',
                'action_items': [
                    'Continue current routine',
                    'Gradually increase intensity',
                    'Try new activities to prevent boredom',
                    'Share your success with others'
                ],
                'expected_benefit': 'Sustained improvement and goal achievement',
                'confidence': 0.92
            })
        
        return recommendations
    
    def generate_recovery_recommendations(self, analysis: Dict) -> List[Dict]:
        """
        Generate recovery-based recommendations
        
        Args:
            analysis: Analysis results
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        consistency = analysis.get('consistency_score', 50)
        
        if consistency < 40:
            recommendations.append({
                'type': 'recovery',
                'priority': 'medium',
                'title': 'Improve Activity Consistency',
                'description': 'Your activity pattern is inconsistent. Regular activity is key to progress.',
                'action_items': [
                    'Create a weekly activity schedule',
                    'Set consistent workout times',
                    'Start with manageable goals',
                    'Track your progress daily'
                ],
                'expected_benefit': 'Better results and habit formation',
                'confidence': 0.87
            })
        
        # Always include a recovery recommendation
        recommendations.append({
            'type': 'recovery',
            'priority': 'medium',
            'title': 'Optimize Recovery',
            'description': 'Recovery is essential for performance improvement.',
            'action_items': [
                'Ensure 7-9 hours of quality sleep',
                'Include rest days in your routine',
                'Stay hydrated throughout the day',
                'Practice stretching or yoga'
            ],
            'expected_benefit': 'Enhanced performance and injury prevention',
            'confidence': 0.90
        })
        
        return recommendations
    
    def generate_performance_recommendations(self, analysis: Dict) -> List[Dict]:
        """
        Generate performance optimization recommendations
        
        Args:
            analysis: Analysis results
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        performance_score = analysis.get('performance_score', 50)
        
        if performance_score < 50:
            recommendations.append({
                'type': 'training',
                'priority': 'high',
                'title': 'Structured Training Program',
                'description': 'Your performance score can be improved with a structured approach.',
                'action_items': [
                    'Work with a coach or follow a training plan',
                    'Set specific, measurable goals',
                    'Track progress weekly',
                    'Incorporate variety in your training'
                ],
                'expected_benefit': 'Systematic performance improvement',
                'confidence': 0.85
            })
        elif performance_score > 70:
            recommendations.append({
                'type': 'training',
                'priority': 'low',
                'title': 'Advanced Performance Optimization',
                'description': 'You\'re performing well! Consider these advanced strategies.',
                'action_items': [
                    'Experiment with periodization',
                    'Add high-intensity interval training',
                    'Focus on specific performance metrics',
                    'Consider nutrition optimization'
                ],
                'expected_benefit': 'Elite-level performance gains',
                'confidence': 0.82
            })
        
        return recommendations
    
    def generate_comprehensive_recommendations(self, df: pd.DataFrame, athlete_id: str) -> Dict:
        """
        Generate comprehensive recommendations for an athlete
        
        Args:
            df: DataFrame with athlete data
            athlete_id: Athlete ID
            
        Returns:
            Dictionary with all recommendations
        """
        logger.info(f"Generating recommendations for athlete {athlete_id}")
        
        # Analyze patterns
        analysis = self.analyze_activity_patterns(df, athlete_id)
        
        if 'error' in analysis:
            return analysis
        
        # Generate different types of recommendations
        activity_recs = self.generate_activity_recommendations(analysis)
        recovery_recs = self.generate_recovery_recommendations(analysis)
        performance_recs = self.generate_performance_recommendations(analysis)
        
        # Combine all recommendations
        all_recommendations = activity_recs + recovery_recs + performance_recs
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        all_recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        result = {
            'athlete_id': athlete_id,
            'analysis_date': datetime.now().isoformat(),
            'analysis_summary': analysis,
            'recommendations': all_recommendations,
            'total_recommendations': len(all_recommendations),
            'high_priority_count': sum(1 for r in all_recommendations if r['priority'] == 'high'),
            'medium_priority_count': sum(1 for r in all_recommendations if r['priority'] == 'medium'),
            'low_priority_count': sum(1 for r in all_recommendations if r['priority'] == 'low')
        }
        
        logger.info(f"Generated {len(all_recommendations)} recommendations for athlete {athlete_id}")
        
        return result
    
    def generate_team_recommendations(self, df: pd.DataFrame, athlete_ids: List[str] = None) -> List[Dict]:
        """
        Generate recommendations for multiple athletes
        
        Args:
            df: DataFrame with athlete data
            athlete_ids: List of athlete IDs (if None, process all)
            
        Returns:
            List of recommendation results
        """
        if athlete_ids is None:
            athlete_ids = df['Id'].unique().tolist()
        
        team_recommendations = []
        
        for athlete_id in athlete_ids:
            recs = self.generate_comprehensive_recommendations(df, athlete_id)
            team_recommendations.append(recs)
        
        logger.info(f"Generated recommendations for {len(team_recommendations)} athletes")
        
        return team_recommendations


if __name__ == "__main__":
    print("Recommendation engine module loaded successfully!")
