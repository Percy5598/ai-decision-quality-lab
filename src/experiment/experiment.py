from dataclasses import dataclass
from enum import Enum
from typing import Optional

import random


class ExperimentCondition(Enum):
    HUMAN_ONLY = "human_only"
    AI_POINT_ESTIMATE = "ai_point_estimate"
    AI_UNCERTAINTY = "ai_uncertainty"


@dataclass
class DecisionRecord:
    # -------------------------
    # EXPERIMENT IDENTIFICATION
    # -------------------------

    participant_id: str
    trial_number: int
    scenario_id: str
    condition: ExperimentCondition

    # -------------------------
    # BEFORE AI
    # -------------------------

    initial_decision: str
    initial_confidence: int
    perceived_risk_initial: int
    financial_attractiveness_initial: int
    perceived_uncertainty_initial: int
    decision_difficulty: int

    # -------------------------
    # AI INFORMATION
    # -------------------------

    ai_recommendation: Optional[str]
    ai_probability: Optional[float]
    ai_confidence: Optional[int]
    ai_uncertainty_lower: Optional[float]
    ai_uncertainty_upper: Optional[float]
    ai_correct: Optional[bool]

    # -------------------------
    # AFTER AI
    # -------------------------

    final_decision: str
    final_confidence: int
    perceived_risk_final: int
    perceived_uncertainty_final: int

    # -------------------------
    # AI EVALUATION
    # -------------------------

    trust_in_ai: Optional[int]
    perceived_ai_reliability: Optional[int]
    ai_clarity: Optional[int]
    ai_agreement: Optional[int]
    ai_influence: Optional[int]

    decision_reason: str

    # -------------------------
    # ECONOMIC BENCHMARK
    # -------------------------

    optimal_decision: str
    expected_value: float

    # -------------------------
    # BEHAVIORAL OUTCOMES
    # -------------------------

    decision_quality: int

    decision_changed: bool
    initial_correct: bool
    final_correct: bool
    followed_ai: bool

    confidence_change: int
    risk_change: int
    uncertainty_change: int

    # -------------------------
    # RELIANCE
    # -------------------------

    over_reliance: bool
    under_reliance: bool


def assign_condition() -> ExperimentCondition:
    """
    Randomly assign a participant to one experimental condition.

    The condition remains the same across all trials for
    this participant.
    """

    return random.choice(
        list(ExperimentCondition)
    )


def calculate_behavioral_measures(
    initial_decision: str,
    final_decision: str,
    initial_confidence: int,
    final_confidence: int,
    perceived_risk_initial: int,
    perceived_risk_final: int,
    perceived_uncertainty_initial: int,
    perceived_uncertainty_final: int,
    ai_recommendation: Optional[str],
    ai_correct: Optional[bool],
    optimal_decision: str,
) -> dict:
    """
    Calculate behavioral outcomes for one trial.
    """

    decision_changed = (
        initial_decision != final_decision
    )

    initial_correct = (
        initial_decision == optimal_decision
    )

    final_correct = (
        final_decision == optimal_decision
    )

    followed_ai = (
        ai_recommendation is not None
        and final_decision == ai_recommendation
    )

    confidence_change = (
        final_confidence - initial_confidence
    )

    risk_change = (
        perceived_risk_final
        - perceived_risk_initial
    )

    uncertainty_change = (
        perceived_uncertainty_final
        - perceived_uncertainty_initial
    )

    over_reliance = (
        ai_correct is False
        and initial_correct
        and followed_ai
        and not final_correct
    )

    under_reliance = (
        ai_correct is True
        and not followed_ai
        and not final_correct
    )

    decision_quality = int(final_correct)

    return {
        "decision_changed": decision_changed,
        "initial_correct": initial_correct,
        "final_correct": final_correct,
        "followed_ai": followed_ai,
        "confidence_change": confidence_change,
        "risk_change": risk_change,
        "uncertainty_change": uncertainty_change,
        "over_reliance": over_reliance,
        "under_reliance": under_reliance,
        "decision_quality": decision_quality,
    }