from dataclasses import dataclass

from src.decisions.scenarios import DecisionScenario
from src.experiment.experiment import ExperimentCondition


@dataclass
class AIAdvice:
    recommendation: str
    probability: float
    confidence: int
    uncertainty_lower: float | None = None
    uncertainty_upper: float | None = None


def generate_advice(
    scenario: DecisionScenario,
    condition: ExperimentCondition,
) -> AIAdvice | None:
    """
    Generate deterministic AI advice for an experimental condition.

    The underlying recommendation is identical across AI conditions.
    Only the presentation of uncertainty changes.
    """

    if condition == ExperimentCondition.HUMAN_ONLY:
        return None

    # Fixed model estimate for the prototype.
    probability = 0.72
    confidence = 61

    recommendation = (
        "Invest"
        if probability >= 0.50
        else "Do not invest"
    )

    if condition == ExperimentCondition.AI_POINT_ESTIMATE:
        return AIAdvice(
            recommendation=recommendation,
            probability=probability,
            confidence=confidence,
        )

    if condition == ExperimentCondition.AI_UNCERTAINTY:
        return AIAdvice(
            recommendation=recommendation,
            probability=probability,
            confidence=confidence,
            uncertainty_lower=0.65,
            uncertainty_upper=0.75,
        )

    raise ValueError(
        f"Unsupported experiment condition: {condition}"
    )
