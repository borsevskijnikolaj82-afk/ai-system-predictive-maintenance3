from app.inference import ModelUnavailableError, RiskBaselineModel
from app.preprocessing import transform
from app.schemas import PredictionRequest, PredictionResult


class PredictionService:
    """Coordinates validation, preprocessing, inference and business rules."""

    def __init__(self, model: RiskBaselineModel, review_threshold: float = 0.8) -> None:
        self.model = model
        self.review_threshold = review_threshold

    def predict(self, request: PredictionRequest) -> PredictionResult:
        features = transform(request.model_dump())

        try:
            inference = self.model.predict(features)
        except ModelUnavailableError as exc:
            raise RuntimeError("Prediction cannot be produced: model unavailable") from exc

        return PredictionResult(
            item_id=request.item_id,
            prediction=inference.prediction,
            probability=inference.probability,
            model_version=self.model.version,
            manual_review_required=inference.probability < self.review_threshold,
        )
