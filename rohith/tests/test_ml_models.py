import pytest
import numpy as np
import os
from src.models.ml_predictor import MLPredictor

@pytest.fixture
def predictor():
    # Use test model path
    model = MLPredictor(model_path="models/test_predictor.joblib")
    yield model
    # Cleanup
    if os.path.exists("models/test_predictor.joblib"):
        os.remove("models/test_predictor.joblib")

def test_model_training_and_persistence(predictor):
    predictor.train_synthetic()
    assert os.path.exists(predictor.model_path)
    assert hasattr(predictor.model, "estimators_")

def test_prediction_output(predictor):
    predictor.train_synthetic()
    
    # Dummy features [volatility, prev_return, macro]
    features = np.array([[0.15, 0.05, 0.02]])
    result = predictor.predict_returns(features)
    
    assert "expected_return" in result
    assert "lower_bound_95" in result
    assert "upper_bound_95" in result
    
def test_feature_importance(predictor):
    predictor.train_synthetic()
    importance = predictor.get_feature_importance()
    assert "Volatility" in importance
    assert "Trailing Return" in importance
