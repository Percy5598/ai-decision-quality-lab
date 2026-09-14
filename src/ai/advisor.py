from dataclasses import dataclass

from src.decisions.scenarios import DecisionScenario
from src.experiment.experiment import ExperimentCondition


@dataclass
class AIAdvice:
    recommendation: str
    probability: float
    confidence: int
    correct: bool
    uncertainty_lower: float | None = None
    uncertainty_upper: float | None = None


def generate_advice(
    scenario: DecisionScenario,
    condition: ExperimentCondition,
    ai_correct: bool = True,
) -> AIAdvice | None:
    """
    Generate deterministic AI advice.

    Parameters
    ----------
    scenario:
        The decision scenario.

    condition:
        Experimental condition.

    ai_correct:
        Controls whether the AI recommendation agrees with
        the model-optimal benchmark.

    Returns
    -------
    AIAdvice | None
        AI advice for AI conditions, otherwise None.
    """

    # Human-only condition receives no AI advice.
    if condition == ExperimentCondition.HUMAN_ONLY:
        return None

    # --------------------------------------------------
    # Determine AI recommendation
    # --------------------------------------------------

    if ai_correct:
        recommendation = scenario.optimal_decision
    else:
        if scenario.optimal_decision == "Invest":
            recommendation = "Do not invest"
        else:
            recommendation = "Invest"

    # --------------------------------------------------
    # AI probability estimate
    # --------------------------------------------------

    if recommendation == "Invest":
        probability = 0.72
    else:
        probability = 0.38

    # Fixed confidence for the prototype.
    confidence = 61

    # --------------------------------------------------
    # Point estimate condition
    # --------------------------------------------------

    if condition == ExperimentCondition.AI_POINT_ESTIMATE:

        return AIAdvice(
            recommendation=recommendation,
            probability=probability,
            confidence=confidence,
            correct=ai_correct,
        )

    # --------------------------------------------------
    # Uncertainty condition
    # --------------------------------------------------

    if condition == ExperimentCondition.AI_UNCERTAINTY:

        uncertainty_width = 0.05

        lower = max(
            0,
            probability - uncertainty_width,
        )

        upper = min(
            1,
            probability + uncertainty_width,
        )

        return AIAdvice(
            recommendation=recommendation,
            probability=probability,
            confidence=confidence,
            correct=ai_correct,
            uncertainty_lower=lower,
            uncertainty_upper=upper,
        )

    raise ValueError(
        f"Unsupported experiment condition: {condition}"
    )

