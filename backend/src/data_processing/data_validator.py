"""
Data validation module for FitArena
Validates data quality and consistency
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """Validate data quality and consistency"""
    
    def __init__(self):
        self.validation_results = {}
    
    def validate_missing_values(self, df: pd.DataFrame, dataset_name: str) -> Dict:
        """
        Check for missing values in dataset
        
        Args:
            df: DataFrame to validate
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary with validation results
        """
        missing_info = df.isnull().sum()
        missing_pct = (missing_info / len(df) * 100).round(2)
        
        result = {
            'dataset': dataset_name,
            'total_rows': len(df),
            'columns_with_missing': missing_info[missing_info > 0].to_dict(),
            'missing_percentage': missing_pct[missing_pct > 0].to_dict()
        }
        
        logger.info(f"{dataset_name}: {len(result['columns_with_missing'])} columns have missing values")
        return result
    
    def validate_duplicates(self, df: pd.DataFrame, dataset_name: str, 
                          subset: List[str] = None) -> Dict:
        """
        Check for duplicate records
        
        Args:
            df: DataFrame to validate
            dataset_name: Name of the dataset
            subset: Columns to consider for identifying duplicates
            
        Returns:
            Dictionary with validation results
        """
        duplicate_count = df.duplicated(subset=subset).sum()
        duplicate_pct = (duplicate_count / len(df) * 100).round(2)
        
        result = {
            'dataset': dataset_name,
            'total_duplicates': int(duplicate_count),
            'duplicate_percentage': float(duplicate_pct)
        }
        
        logger.info(f"{dataset_name}: {duplicate_count} duplicate records found ({duplicate_pct}%)")
        return result
    
    def validate_data_types(self, df: pd.DataFrame, dataset_name: str) -> Dict:
        """
        Validate data types and detect potential issues
        
        Args:
            df: DataFrame to validate
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary with validation results
        """
        dtype_info = df.dtypes.astype(str).to_dict()
        
        # Check for numeric columns with potential issues
        numeric_issues = {}
        for col in df.select_dtypes(include=[np.number]).columns:
            if df[col].isnull().any():
                numeric_issues[col] = f"Contains {df[col].isnull().sum()} null values"
            elif (df[col] < 0).any():
                numeric_issues[col] = f"Contains {(df[col] < 0).sum()} negative values"
        
        result = {
            'dataset': dataset_name,
            'data_types': dtype_info,
            'numeric_issues': numeric_issues
        }
        
        logger.info(f"{dataset_name}: Data types validated")
        return result
    
    def validate_ranges(self, df: pd.DataFrame, dataset_name: str, 
                       range_rules: Dict[str, Tuple[float, float]]) -> Dict:
        """
        Validate numeric values are within expected ranges
        
        Args:
            df: DataFrame to validate
            dataset_name: Name of the dataset
            range_rules: Dictionary mapping column names to (min, max) tuples
            
        Returns:
            Dictionary with validation results
        """
        violations = {}
        
        for col, (min_val, max_val) in range_rules.items():
            if col in df.columns:
                out_of_range = ((df[col] < min_val) | (df[col] > max_val)).sum()
                if out_of_range > 0:
                    violations[col] = {
                        'count': int(out_of_range),
                        'percentage': round(out_of_range / len(df) * 100, 2),
                        'expected_range': (min_val, max_val),
                        'actual_range': (df[col].min(), df[col].max())
                    }
        
        result = {
            'dataset': dataset_name,
            'range_violations': violations
        }
        
        logger.info(f"{dataset_name}: {len(violations)} columns have range violations")
        return result
    
    def validate_consistency(self, df: pd.DataFrame, dataset_name: str) -> Dict:
        """
        Check for logical consistency in data
        
        Args:
            df: DataFrame to validate
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary with validation results
        """
        inconsistencies = []
        
        # Example consistency checks for activity data
        if 'TotalSteps' in df.columns and 'TotalDistance' in df.columns:
            # Check if distance is 0 but steps > 0
            invalid_distance = ((df['TotalSteps'] > 0) & (df['TotalDistance'] == 0)).sum()
            if invalid_distance > 0:
                inconsistencies.append({
                    'check': 'Steps without distance',
                    'count': int(invalid_distance)
                })
        
        if 'Calories' in df.columns:
            # Check for unrealistic calorie values
            high_calories = (df['Calories'] > 10000).sum()
            low_calories = (df['Calories'] < 0).sum()
            if high_calories > 0 or low_calories > 0:
                inconsistencies.append({
                    'check': 'Unrealistic calorie values',
                    'high_count': int(high_calories),
                    'low_count': int(low_calories)
                })
        
        result = {
            'dataset': dataset_name,
            'inconsistencies': inconsistencies
        }
        
        logger.info(f"{dataset_name}: {len(inconsistencies)} consistency issues found")
        return result
    
    def generate_validation_report(self, df: pd.DataFrame, dataset_name: str, 
                                  range_rules: Dict[str, Tuple[float, float]] = None) -> Dict:
        """
        Generate comprehensive validation report
        
        Args:
            df: DataFrame to validate
            dataset_name: Name of the dataset
            range_rules: Optional range validation rules
            
        Returns:
            Complete validation report
        """
        logger.info(f"Generating validation report for {dataset_name}")
        
        report = {
            'missing_values': self.validate_missing_values(df, dataset_name),
            'duplicates': self.validate_duplicates(df, dataset_name),
            'data_types': self.validate_data_types(df, dataset_name),
            'consistency': self.validate_consistency(df, dataset_name)
        }
        
        if range_rules:
            report['ranges'] = self.validate_ranges(df, dataset_name, range_rules)
        
        # Calculate overall quality score
        quality_score = self._calculate_quality_score(df, report)
        report['quality_score'] = quality_score
        
        return report
    
    def _calculate_quality_score(self, df: pd.DataFrame, report: Dict) -> float:
        """
        Calculate overall data quality score (0-100)
        
        Args:
            df: DataFrame
            report: Validation report
            
        Returns:
            Quality score
        """
        score = 100.0
        
        # Deduct for missing values
        missing_pct = report['missing_values']['missing_percentage']
        if missing_pct:
            avg_missing = sum(missing_pct.values()) / len(missing_pct)
            score -= min(avg_missing, 20)
        
        # Deduct for duplicates
        dup_pct = report['duplicates']['duplicate_percentage']
        score -= min(dup_pct, 10)
        
        # Deduct for inconsistencies
        inconsistency_count = len(report['consistency']['inconsistencies'])
        score -= min(inconsistency_count * 5, 20)
        
        return max(0, round(score, 2))


class DataCleaner:
    """Clean and preprocess data"""
    
    def __init__(self):
        pass
    
    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None, 
                         keep: str = 'first') -> pd.DataFrame:
        """
        Remove duplicate records
        
        Args:
            df: DataFrame to clean
            subset: Columns to consider for identifying duplicates
            keep: Which duplicate to keep ('first', 'last', False)
            
        Returns:
            Cleaned DataFrame
        """
        initial_count = len(df)
        df_clean = df.drop_duplicates(subset=subset, keep=keep)
        removed_count = initial_count - len(df_clean)
        
        logger.info(f"Removed {removed_count} duplicate records")
        return df_clean
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: Dict[str, str] = None) -> pd.DataFrame:
        """
        Handle missing values using specified strategies
        
        Args:
            df: DataFrame to clean
            strategy: Dictionary mapping column names to strategies
                     ('drop', 'mean', 'median', 'mode', 'forward_fill', 'backward_fill', value)
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        
        if strategy is None:
            # Default strategy: drop rows with any missing values
            return df_clean.dropna()
        
        for col, method in strategy.items():
            if col not in df_clean.columns:
                continue
            
            if method == 'drop':
                df_clean = df_clean.dropna(subset=[col])
            elif method == 'mean':
                df_clean[col].fillna(df_clean[col].mean(), inplace=True)
            elif method == 'median':
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
            elif method == 'mode':
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
            elif method == 'forward_fill':
                df_clean[col].fillna(method='ffill', inplace=True)
            elif method == 'backward_fill':
                df_clean[col].fillna(method='bfill', inplace=True)
            else:
                # Assume it's a constant value
                df_clean[col].fillna(method, inplace=True)
        
        logger.info("Missing values handled")
        return df_clean
    
    def remove_outliers(self, df: pd.DataFrame, columns: List[str], 
                       method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Remove outliers from specified columns
        
        Args:
            df: DataFrame to clean
            columns: Columns to check for outliers
            method: 'iqr' or 'zscore'
            threshold: Threshold for outlier detection (IQR multiplier or Z-score)
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        initial_count = len(df_clean)
        
        for col in columns:
            if col not in df_clean.columns:
                continue
            
            if method == 'iqr':
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
            
            elif method == 'zscore':
                z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
                df_clean = df_clean[z_scores < threshold]
        
        removed_count = initial_count - len(df_clean)
        logger.info(f"Removed {removed_count} outlier records")
        
        return df_clean
    
    def normalize_data(self, df: pd.DataFrame, columns: List[str], 
                      method: str = 'minmax') -> pd.DataFrame:
        """
        Normalize numeric columns
        
        Args:
            df: DataFrame to normalize
            columns: Columns to normalize
            method: 'minmax' or 'standard'
            
        Returns:
            DataFrame with normalized columns
        """
        df_norm = df.copy()
        
        for col in columns:
            if col not in df_norm.columns:
                continue
            
            if method == 'minmax':
                min_val = df_norm[col].min()
                max_val = df_norm[col].max()
                df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
            
            elif method == 'standard':
                mean_val = df_norm[col].mean()
                std_val = df_norm[col].std()
                df_norm[col] = (df_norm[col] - mean_val) / std_val
        
        logger.info(f"Normalized {len(columns)} columns using {method} method")
        return df_norm


if __name__ == "__main__":
    # Test validation
    print("Data validation module loaded successfully!")
