from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Prediction(str, Enum):
    NORMAL = "NORMAL"
    WARNING_ANOMALY = "WARNING_ANOMALY"
    CRITICAL_RISK = "CRITICAL_RISK"


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(min_length=1, max_length=128)
    temperature: float = Field(ge=-50.0, le=250.0)
    vibration_amplitude: float = Field(ge=0.0, le=100.0)
    operating_hours: int = Field(ge=0)
    error_code_last_24h: int = Field(default=0, ge=0, le=999)


class PredictionResult(BaseModel):
    item_id: str
    prediction: Prediction
    probability: float = Field(ge=0.0, le=1.0)
    model_version: str
    manual_review_required: bool
