from dataclasses import dataclass


class ModelUnavailableError(RuntimeError):
    """Raised when the intellectual dependency cannot perform inference."""


@dataclass(frozen=True)
class InferenceResult:
    prediction: str
    probability: float


class RiskBaselineModel:
    """Compact deterministic baseline for equipment risk scoring."""

    def __init__(self, version: str = "baseline-1.0.0", available: bool = True) -> None:
        self.version = version
        self.available = available

    def predict(self, features: tuple[float, float, int, int]) -> InferenceResult:
        if not self.available:
            raise ModelUnavailableError("AI model is unavailable")

        temperature, vibration, operating_hours, error_code = features
        risk_score = min(
            1.0,
            max(
                0.0,
                0.003 * max(temperature - 70.0, 0.0)
                + 0.05 * vibration
                + 0.00005 * operating_hours
                + 0.01 * error_code,
            ),
        )

        if risk_score >= 0.75:
            label = "CRITICAL_RISK"
        elif risk_score >= 0.45:
            label = "WARNING_ANOMALY"
        else:
            label = "NORMAL"

        return InferenceResult(label, round(risk_score, 4))
