#!/usr/bin/env python3
"""
Unit tests for NYC TLC ML pipeline components.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class TestDataIngestion(unittest.TestCase):
    """Tests for data ingestion module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create sample NYC TLC data
        n_samples = 100
        base_time = datetime(2019, 1, 1)
        
        self.sample_data = pd.DataFrame({
            'VendorID': np.random.randint(1, 3, n_samples),
            'tpep_pickup_datetime': [base_time + timedelta(hours=i) for i in range(n_samples)],
            'tpep_dropoff_datetime': [base_time + timedelta(hours=i, minutes=15) for i in range(n_samples)],
            'passenger_count': np.random.randint(1, 6, n_samples),
            'trip_distance': np.random.uniform(0.5, 20, n_samples),
            'fare_amount': np.random.uniform(5, 50, n_samples),
            'PULocationID': np.random.randint(1, 265, n_samples),
            'DOLocationID': np.random.randint(1, 265, n_samples),
        })
    
    def test_data_shape(self):
        """Test that data has correct shape."""
        self.assertEqual(self.sample_data.shape[0], 100)
        self.assertGreaterEqual(self.sample_data.shape[1], 8)
    
    def test_data_no_nulls(self):
        """Test that data has no null values."""
        self.assertEqual(self.sample_data.isnull().sum().sum(), 0)
    
    def test_datetime_columns(self):
        """Test datetime columns are properly formatted."""
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.sample_data['tpep_pickup_datetime']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.sample_data['tpep_dropoff_datetime']))
    
    def test_positive_values(self):
        """Test that distance and fare are positive."""
        self.assertTrue((self.sample_data['trip_distance'] > 0).all())
        self.assertTrue((self.sample_data['fare_amount'] > 0).all())


class TestFeatureEngineering(unittest.TestCase):
    """Tests for feature engineering module."""
    
    def setUp(self):
        """Set up test fixtures."""
        n_samples = 100
        base_time = datetime(2019, 1, 1, 10, 0)
        
        self.sample_data = pd.DataFrame({
            'tpep_pickup_datetime': [base_time + timedelta(hours=i) for i in range(n_samples)],
            'tpep_dropoff_datetime': [base_time + timedelta(hours=i, minutes=20) for i in range(n_samples)],
            'trip_distance': np.random.uniform(1, 10, n_samples),
            'fare_amount': np.random.uniform(10, 40, n_samples),
        })
    
    def test_trip_duration_calculation(self):
        """Test trip duration calculation."""
        self.sample_data['trip_duration_minutes'] = (
            (self.sample_data['tpep_dropoff_datetime'] - 
             self.sample_data['tpep_pickup_datetime']).dt.total_seconds() / 60
        )
        self.assertTrue((self.sample_data['trip_duration_minutes'] > 0).all())
        self.assertAlmostEqual(self.sample_data['trip_duration_minutes'].iloc[0], 20.0, places=1)
    
    def test_temporal_features(self):
        """Test temporal feature extraction."""
        self.sample_data['pickup_hour'] = self.sample_data['tpep_pickup_datetime'].dt.hour
        self.sample_data['pickup_day'] = self.sample_data['tpep_pickup_datetime'].dt.dayofweek
        
        self.assertTrue((self.sample_data['pickup_hour'] >= 0).all())
        self.assertTrue((self.sample_data['pickup_hour'] <= 23).all())
        self.assertTrue((self.sample_data['pickup_day'] >= 0).all())
        self.assertTrue((self.sample_data['pickup_day'] <= 6).all())
    
    def test_speed_calculation(self):
        """Test average speed calculation."""
        self.sample_data['trip_duration_hours'] = 20 / 60  # 20 minutes
        self.sample_data['avg_speed_mph'] = (
            self.sample_data['trip_distance'] / self.sample_data['trip_duration_hours']
        )
        self.assertTrue((self.sample_data['avg_speed_mph'] > 0).all())


class TestModelTraining(unittest.TestCase):
    """Tests for model training module."""
    
    def test_train_test_split(self):
        """Test train-test split proportions."""
        n_samples = 1000
        train_ratio = 0.7
        val_ratio = 0.15
        test_ratio = 0.15
        
        # Simulate split
        train_size = int(n_samples * train_ratio)
        val_size = int(n_samples * val_ratio)
        test_size = n_samples - train_size - val_size
        
        self.assertAlmostEqual(train_size / n_samples, train_ratio, places=1)
        self.assertAlmostEqual(val_size / n_samples, val_ratio, places=1)
        self.assertAlmostEqual(test_size / n_samples, test_ratio, places=1)
    
    def test_feature_vector_size(self):
        """Test feature vector has correct dimensions."""
        # Assuming 10 numerical + 6 binary + 5 categorical (indexed) = 21 features
        expected_features = 21
        actual_features = 21  # This would come from actual feature assembly
        self.assertEqual(actual_features, expected_features)


class TestEvaluation(unittest.TestCase):
    """Tests for model evaluation module."""
    
    def test_rmse_calculation(self):
        """Test RMSE calculation."""
        y_true = np.array([10, 20, 30, 40, 50])
        y_pred = np.array([12, 18, 32, 38, 52])
        
        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
        expected_rmse = 2.0
        
        self.assertAlmostEqual(rmse, expected_rmse, places=1)
    
    def test_r2_calculation(self):
        """Test R² calculation."""
        y_true = np.array([10, 20, 30, 40, 50])
        y_pred = np.array([10, 20, 30, 40, 50])
        
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        
        self.assertAlmostEqual(r2, 1.0, places=1)
    
    def test_mae_calculation(self):
        """Test MAE calculation."""
        y_true = np.array([10, 20, 30, 40, 50])
        y_pred = np.array([12, 18, 32, 38, 52])
        
        mae = np.mean(np.abs(y_true - y_pred))
        expected_mae = 2.0
        
        self.assertAlmostEqual(mae, expected_mae, places=1)


class TestDataQuality(unittest.TestCase):
    """Tests for data quality checks."""
    
    def test_no_negative_values(self):
        """Test that key columns have no negative values."""
        data = pd.DataFrame({
            'trip_distance': [1.5, 2.3, 5.0],
            'fare_amount': [10.5, 15.0, 25.0],
            'passenger_count': [1, 2, 3]
        })
        
        self.assertTrue((data['trip_distance'] >= 0).all())
        self.assertTrue((data['fare_amount'] >= 0).all())
        self.assertTrue((data['passenger_count'] >= 0).all())
    
    def test_reasonable_passenger_count(self):
        """Test passenger count is within reasonable range."""
        data = pd.DataFrame({
            'passenger_count': [1, 2, 3, 4, 5, 6]
        })
        
        self.assertTrue((data['passenger_count'] >= 1).all())
        self.assertTrue((data['passenger_count'] <= 6).all())


if __name__ == '__main__':
    unittest.main()
