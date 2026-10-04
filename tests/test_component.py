import pytest
from pydantic import ValidationError

from app.inference import RiskBaselineModel
from app.schemas import Prediction, PredictionRequest
from app.service import PredictionService


def test_normal_equipment_returns_typed_result() -> None:
    service = PredictionService(RiskBaselineModel())

    result = service.predict(
        PredictionRequest(
            item_id="PUMP-01",
            temperature=55.0,
            vibration_amplitude=1.0,
            operating_hours=1000,
            error_code_last_24h=0,
        )
    )

    assert result.prediction == Prediction.NORMAL
    assert 0.0 <= result.probability <= 1.0
    assert result.model_version == "baseline-1.0.0"


def test_high_risk_input_changes_prediction_and_requires_no_manual_review() -> None:
    service = PredictionService(RiskBaselineModel())

    result = service.predict(
        PredictionRequest(
            item_id="PUMP-02",
            temperature=110.0,
            vibration_amplitude=8.0,
            operating_hours=5000,
            error_code_last_24h=30,
        )
    )

    assert result.prediction == Prediction.CRITICAL_RISK
    assert result.probability >= 0.75
    assert result.manual_review_required is False


def test_invalid_boundary_value_is_rejected() -> None:
    with pytest.raises(ValidationError):
        PredictionRequest(
            item_id="PUMP-03",
            temperature=300.0,
            vibration_amplitude=1.0,
            operating_hours=100,
            error_code_last_24h=0,
        )


def test_unavailable_model_does_not_return_false_success() -> None:
    service = PredictionService(RiskBaselineModel(available=False))
    request = PredictionRequest(
        item_id="PUMP-04",
        temperature=70.0,
        vibration_amplitude=1.0,
        operating_hours=100,
        error_code_last_24h=0,
    )

    with pytest.raises(RuntimeError, match="model unavailable"):
        service.predict(request)


def test_borderline_result_is_marked_for_manual_review() -> None:
    service = PredictionService(RiskBaselineModel(), review_threshold=0.8)
    result = service.predict(
        PredictionRequest(
            item_id="PUMP-05",
            temperature=90.0,
            vibration_amplitude=5.0,
            operating_hours=2000,
            error_code_last_24h=10,
        )
    )

    assert result.probability < 0.8
    assert result.manual_review_required is True
