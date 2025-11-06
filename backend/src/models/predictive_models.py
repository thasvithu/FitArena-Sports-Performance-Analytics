"""
Predictive models for FitArena
Includes activity prediction, performance forecasting, and anomaly detection
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_absolute_error, mean_squared_error, r2_score,
    classification_report, confusion_matrix
)
import joblib
from typing import Dict, Tuple, List, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ActivityClassifier:
    """Classify activity levels and fitness categories"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize activity classifier
        
        Args:
            model_path: Path to save/load model
        """
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = None
        self.model_path = model_path
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare features for classification
        
        Args:
            df: DataFrame with features and target
            
        Returns:
            X (features), y (target)
        """
        # Select relevant features
        feature_cols = [
            'TotalSteps', 'TotalDistance', 'Calories',
            'VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes',
            'SedentaryMinutes', 'total_active_minutes', 'high_intensity_ratio',
            'sedentary_ratio', 'performance_score'
        ]
        
        # Filter available features
        available_features = [col for col in feature_cols if col in df.columns]
        self.feature_names = available_features
        
        X = df[available_features].copy()
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Get target variable (fitness_level)
        if 'fitness_level' in df.columns:
            y = df['fitness_level'].astype(str)
        else:
            raise ValueError("Target variable 'fitness_level' not found in DataFrame")
        
        return X, y
    
    def train(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict[str, Any]:
        """
        Train activity classifier
        
        Args:
            df: Training data
            test_size: Proportion of data for testing
            
        Returns:
            Dictionary with training metrics
        """
        logger.info("Training activity classifier...")
        
        # Prepare features
        X, y = self.prepare_features(df)
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=test_size, random_state=42, stratify=y_encoded
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = self.model.predict(X_test_scaled)
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1_score': f1_score(y_test, y_pred, average='weighted'),
            'classification_report': classification_report(
                y_test, y_pred, 
                target_names=self.label_encoder.classes_
            ),
            'feature_importance': dict(zip(
                self.feature_names,
                self.model.feature_importances_
            ))
        }
        
        logger.info(f"Training completed! Accuracy: {metrics['accuracy']:.4f}")
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict activity levels
        
        Args:
            X: Features for prediction
            
        Returns:
            Predicted labels
        """
        X_scaled = self.scaler.transform(X[self.feature_names])
        predictions = self.model.predict(X_scaled)
        return self.label_encoder.inverse_transform(predictions)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict probabilities for each class
        
        Args:
            X: Features for prediction
            
        Returns:
            Prediction probabilities
        """
        X_scaled = self.scaler.transform(X[self.feature_names])
        return self.model.predict_proba(X_scaled)
    
    def save_model(self, path: str = None):
        """Save trained model"""
        save_path = path or self.model_path
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'label_encoder': self.label_encoder,
                'feature_names': self.feature_names
            }, save_path)
            logger.info(f"Model saved to {save_path}")
    
    def load_model(self, path: str = None):
        """Load trained model"""
        load_path = path or self.model_path
        if load_path and Path(load_path).exists():
            data = joblib.load(load_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.label_encoder = data['label_encoder']
            self.feature_names = data['feature_names']
            logger.info(f"Model loaded from {load_path}")


class PerformancePredictor:
    """Predict future performance metrics"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize performance predictor
        
        Args:
            model_path: Path to save/load model
        """
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_names = None
        self.model_path = model_path
    
    def prepare_features(self, df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare features for regression
        
        Args:
            df: DataFrame with features and target
            target_col: Target column name
            
        Returns:
            X (features), y (target)
        """
        # Select relevant features (including lag and rolling features)
        feature_cols = [
            col for col in df.columns 
            if any(keyword in col for keyword in [
                'lag_', 'rolling_', 'user_', 'change', 'ratio',
                'Minutes', 'Steps', 'Distance', 'Calories'
            ]) and col != target_col
        ]
        
        # Add important base features
        base_features = ['day_of_week', 'is_weekend', 'month']
        feature_cols.extend([col for col in base_features if col in df.columns])
        
        # Remove duplicates
        feature_cols = list(set(feature_cols))
        
        self.feature_names = feature_cols
        
        X = df[feature_cols].copy()
        y = df[target_col].copy()
        
        # Handle missing values
        X = X.fillna(X.mean())
        y = y.fillna(y.mean())
        
        return X, y
    
    def train(self, df: pd.DataFrame, target_col: str, test_size: float = 0.2) -> Dict[str, Any]:
        """
        Train performance predictor
        
        Args:
            df: Training data
            target_col: Target column to predict
            test_size: Proportion of data for testing
            
        Returns:
            Dictionary with training metrics
        """
        logger.info(f"Training performance predictor for {target_col}...")
        
        # Prepare features
        X, y = self.prepare_features(df, target_col)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = self.model.predict(X_test_scaled)
        
        # Calculate metrics
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2_score': r2_score(y_test, y_pred),
            'mape': np.mean(np.abs((y_test - y_pred) / (y_test + 1))) * 100,
            'feature_importance': dict(zip(
                self.feature_names,
                self.model.feature_importances_
            ))
        }
        
        logger.info(f"Training completed! R² Score: {metrics['r2_score']:.4f}")
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict performance metrics
        
        Args:
            X: Features for prediction
            
        Returns:
            Predicted values
        """
        X_scaled = self.scaler.transform(X[self.feature_names])
        return self.model.predict(X_scaled)
    
    def save_model(self, path: str = None):
        """Save trained model"""
        save_path = path or self.model_path
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names
            }, save_path)
            logger.info(f"Model saved to {save_path}")
    
    def load_model(self, path: str = None):
        """Load trained model"""
        load_path = path or self.model_path
        if load_path and Path(load_path).exists():
            data = joblib.load(load_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_names = data['feature_names']
            logger.info(f"Model loaded from {load_path}")


class AnomalyDetector:
    """Detect anomalies in athlete performance"""
    
    def __init__(self, threshold: float = 2.5):
        """
        Initialize anomaly detector
        
        Args:
            threshold: Z-score threshold for anomaly detection
        """
        self.threshold = threshold
        self.statistics = {}
    
    def fit(self, df: pd.DataFrame, metrics: List[str]):
        """
        Fit anomaly detector by calculating statistics
        
        Args:
            df: Training data
            metrics: Metrics to monitor for anomalies
        """
        logger.info("Fitting anomaly detector...")
        
        for metric in metrics:
            if metric in df.columns:
                self.statistics[metric] = {
                    'mean': df[metric].mean(),
                    'std': df[metric].std(),
                    'q1': df[metric].quantile(0.25),
                    'q3': df[metric].quantile(0.75),
                    'iqr': df[metric].quantile(0.75) - df[metric].quantile(0.25)
                }
        
        logger.info(f"Anomaly detector fitted for {len(self.statistics)} metrics")
    
    def detect(self, df: pd.DataFrame, method: str = 'zscore') -> pd.DataFrame:
        """
        Detect anomalies
        
        Args:
            df: Data to check for anomalies
            method: 'zscore' or 'iqr'
            
        Returns:
            DataFrame with anomaly flags
        """
        df_result = df.copy()
        anomaly_flags = []
        
        for metric, stats in self.statistics.items():
            if metric not in df.columns:
                continue
            
            if method == 'zscore':
                z_scores = np.abs((df[metric] - stats['mean']) / (stats['std'] + 1e-6))
                df_result[f'{metric}_anomaly'] = (z_scores > self.threshold).astype(int)
            
            elif method == 'iqr':
                lower_bound = stats['q1'] - 1.5 * stats['iqr']
                upper_bound = stats['q3'] + 1.5 * stats['iqr']
                df_result[f'{metric}_anomaly'] = (
                    (df[metric] < lower_bound) | (df[metric] > upper_bound)
                ).astype(int)
            
            anomaly_flags.append(f'{metric}_anomaly')
        
        # Overall anomaly flag
        if anomaly_flags:
            df_result['is_anomaly'] = df_result[anomaly_flags].max(axis=1)
        
        logger.info(f"Detected {df_result['is_anomaly'].sum() if 'is_anomaly' in df_result else 0} anomalies")
        
        return df_result


if __name__ == "__main__":
    print("Predictive models module loaded successfully!")
