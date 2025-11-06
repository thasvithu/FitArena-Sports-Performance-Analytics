"""
Training script for FitArena ML models
Run this script to train all models on the dataset
"""
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import modules
from src.data_processing.data_loader import DataLoader
from src.data_processing.data_validator import DataValidator, DataCleaner
from src.data_processing.feature_engineering import FeatureEngineer
from src.models.predictive_models import ActivityClassifier, PerformancePredictor, AnomalyDetector
from src.models.recommendation_engine import RecommendationEngine


def main():
    """Main training pipeline"""
    
    logger.info("="*80)
    logger.info("FitArena ML Model Training Pipeline")
    logger.info("="*80)
    
    # 1. Load Data
    logger.info("\n1. Loading data...")
    loader = DataLoader(data_dir='./data')
    data = loader.load_all_data(folder='Fitabase Data 4.12.16-5.12.16')
    daily_activity = data['daily_activity']
    logger.info(f"Loaded {len(daily_activity)} records with {daily_activity['Id'].nunique()} unique users")
    
    # 2. Validate Data
    logger.info("\n2. Validating data quality...")
    validator = DataValidator()
    validation_report = validator.generate_validation_report(daily_activity, 'daily_activity')
    logger.info(f"Data Quality Score: {validation_report['quality_score']}/100")
    
    # 3. Clean Data
    logger.info("\n3. Cleaning data...")
    cleaner = DataCleaner()
    daily_activity_clean = cleaner.remove_duplicates(daily_activity, subset=['Id', 'ActivityDate'])
    logger.info(f"Cleaned data: {len(daily_activity_clean)} records")
    
    # 4. Feature Engineering
    logger.info("\n4. Engineering features...")
    engineer = FeatureEngineer()
    featured_data = engineer.create_all_features(daily_activity_clean, date_column='ActivityDate')
    logger.info(f"Created {len(featured_data.columns)} features")
    
    # Save featured data
    featured_data.to_csv('./data/featured_data.csv', index=False)
    logger.info("Featured data saved to './data/featured_data.csv'")
    
    # 5. Train Activity Classifier
    logger.info("\n5. Training Activity Classifier...")
    try:
        classifier = ActivityClassifier(model_path='./models/saved_models/activity_classifier.pkl')
        
        # Filter data with valid fitness levels
        classifier_data = featured_data.dropna(subset=['fitness_level'])
        
        if len(classifier_data) > 0:
            metrics = classifier.train(classifier_data, test_size=0.2)
            logger.info(f"Classifier Accuracy: {metrics['accuracy']:.4f}")
            logger.info(f"Classifier F1-Score: {metrics['f1_score']:.4f}")
            
            # Save model
            classifier.save_model()
            logger.info("Activity Classifier saved!")
        else:
            logger.warning("Insufficient data for training Activity Classifier")
    except Exception as e:
        logger.error(f"Error training Activity Classifier: {e}")
    
    # 6. Train Performance Predictor
    logger.info("\n6. Training Performance Predictor...")
    try:
        predictor = PerformancePredictor(model_path='./models/saved_models/performance_predictor.pkl')
        
        # Filter data with necessary features
        predictor_data = featured_data.dropna(subset=['TotalSteps'])
        
        if len(predictor_data) > 100:  # Need sufficient data
            metrics = predictor.train(predictor_data, target_col='TotalSteps', test_size=0.2)
            logger.info(f"Predictor R² Score: {metrics['r2_score']:.4f}")
            logger.info(f"Predictor RMSE: {metrics['rmse']:.2f}")
            
            # Save model
            predictor.save_model()
            logger.info("Performance Predictor saved!")
        else:
            logger.warning("Insufficient data for training Performance Predictor")
    except Exception as e:
        logger.error(f"Error training Performance Predictor: {e}")
    
    # 7. Fit Anomaly Detector
    logger.info("\n7. Fitting Anomaly Detector...")
    try:
        detector = AnomalyDetector(threshold=2.5)
        metrics_to_monitor = ['TotalSteps', 'Calories', 'TotalDistance']
        detector.fit(featured_data, metrics_to_monitor)
        logger.info("Anomaly Detector fitted successfully!")
        
        # Test detection
        anomalies = detector.detect(featured_data, method='zscore')
        anomaly_count = anomalies['is_anomaly'].sum() if 'is_anomaly' in anomalies else 0
        logger.info(f"Detected {anomaly_count} anomalies in dataset")
    except Exception as e:
        logger.error(f"Error fitting Anomaly Detector: {e}")
    
    # 8. Test Recommendation Engine
    logger.info("\n8. Testing Recommendation Engine...")
    try:
        engine = RecommendationEngine()
        
        # Generate recommendations for first 3 users
        sample_users = featured_data['Id'].unique()[:3]
        
        for user_id in sample_users:
            recommendations = engine.generate_comprehensive_recommendations(
                featured_data, 
                str(user_id)
            )
            logger.info(f"Generated {recommendations['total_recommendations']} recommendations for user {user_id}")
    except Exception as e:
        logger.error(f"Error testing Recommendation Engine: {e}")
    
    # 9. Generate Training Report
    logger.info("\n9. Generating training report...")
    report = {
        'training_date': datetime.now().isoformat(),
        'total_records': len(featured_data),
        'total_users': featured_data['Id'].nunique(),
        'total_features': len(featured_data.columns),
        'data_quality_score': validation_report['quality_score'],
        'models_trained': [
            'Activity Classifier',
            'Performance Predictor',
            'Anomaly Detector',
            'Recommendation Engine'
        ]
    }
    
    # Save report
    report_df = pd.DataFrame([report])
    report_df.to_csv('./reports/training_report.csv', index=False)
    logger.info("Training report saved to './reports/training_report.csv'")
    
    logger.info("\n" + "="*80)
    logger.info("Training Pipeline Completed Successfully!")
    logger.info("="*80)
    logger.info("\nNext Steps:")
    logger.info("1. Review training logs in './logs' directory")
    logger.info("2. Test models using notebooks in './notebooks' directory")
    logger.info("3. Start API server: python src/api/main.py")
    logger.info("4. Access API docs: http://localhost:8000/api/docs")


if __name__ == "__main__":
    main()
