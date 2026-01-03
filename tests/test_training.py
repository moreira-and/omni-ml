# tests/

import numpy as np
import pytest
from unittest.mock import patch, MagicMock

from src.app import (
    load_data,
    train_model,
    evaluate_model,
    train,
)


def test_load_data_shapes():
    X_train, X_test, y_train, y_test = load_data()

    assert X_train.shape[0] > 0
    assert X_test.shape[0] > 0
    assert X_train.shape[1] == X_test.shape[1]
    assert y_train.ndim == 1
    assert y_test.ndim == 1


def test_train_model_fits():
    X_train, _, y_train, _ = load_data()

    model = train_model(X_train, y_train)

    assert hasattr(model, "predict")
    assert hasattr(model, "feature_importances_")


def test_evaluate_model_returns_valid_accuracy():
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)

    accuracy = evaluate_model(model, X_test, y_test)

    assert isinstance(accuracy, float)
    assert 0.0 <= accuracy <= 1.0


@patch("src.app.mlflow")
def test_train_endpoint_executes_training(mock_mlflow):
    # --- mock MLflow behavior ---
    mock_run = MagicMock()
    mock_mlflow.start_run.return_value.__enter__.return_value = mock_run

    # --- call train() directly (no HTTP) ---
    result = train()

    # --- assertions ---
    assert "accuracy" in result
    assert isinstance(result["accuracy"], float)
    assert 0.0 <= result["accuracy"] <= 1.0

    mock_mlflow.set_experiment.assert_called_once()
    mock_mlflow.log_metric.assert_called_once()
    mock_mlflow.sklearn.log_model.assert_called_once()
