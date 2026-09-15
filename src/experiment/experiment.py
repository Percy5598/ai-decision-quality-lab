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
    participant_id: str
    scenario_id: str
    condition: ExperimentCondition

    # -----------------------------------------------------
    # Initial human decision
    # -----------------------------------------------------

    initial_decision: str
    initial_confidence: int
    perceived_risk_initial: int

    # -----------------------------------------------------
    # AI information
    # -----------------------------------------------------

    ai_recommendation: Optional[str]
    ai_confidence: Optional[int]
    ai_correct: Optional[bool]

    # -----------------------------------------------------
    # Participant's evaluation of AI
    # -----------------------------------------------------

    trust_in_ai: Optional[int]
    perceived_ai_reliability: Optional[int]
    ai_influence: Optional[int]

    # -----------------------------------------------------
    # Final human decision
    # -----------------------------------------------------

    final_decision: str
    final_confidence: int
    perceived_risk_final: int

    # -----------------------------------------------------
    # Participant's reason for final decision
    # -----------------------------------------------------

    decision_reason: str

    # -----------------------------------------------------
    # Economic benchmark
    # -----------------------------------------------------

    optimal_decision: str
    expected_value: float

    # -----------------------------------------------------
    # Basic outcome
    # -----------------------------------------------------

    decision_quality: int

    # -----------------------------------------------------
    # Behavioral measures
    # -----------------------------------------------------

    decision_changed: bool
    initial_correct: bool
    final_correct: bool
    followed_ai: bool
    confidence_change: int

    # -----------------------------------------------------
    # Reliance measures
    # -----------------------------------------------------

    over_reliance: bool
    under_reliance: bool


def assign_condition() -> ExperimentCondition:
    """
    Randomly assign a participant to an experimental condition.
    """

    return random.choice(
        list(ExperimentCondition)
    )


def calculate_behavioral_measures(
    initial_decision: str,
    final_decision: str,
    initial_confidence: int,
    final_confidence: int,
    ai_recommendation: Optional[str],
    ai_correct: Optional[bool],
    optimal_decision: str,
) -> dict:
    """
    Calculate behavioral measures for one experiment.

    These measures describe whether the participant changed
    their decision, followed the AI, and made an appropriate
    or inappropriate reliance decision.
    """

    # -----------------------------------------------------
    # Decision change
    # -----------------------------------------------------

    decision_changed = (
        initial_decision != final_decision
    )

    # -----------------------------------------------------
    # Decision correctness
    # -----------------------------------------------------

    initial_correct = (
        initial_decision == optimal_decision
    )

    final_correct = (
        final_decision == optimal_decision
    )

    # -----------------------------------------------------
    # AI following
    # -----------------------------------------------------

    followed_ai = (
        ai_recommendation is not None
        and final_decision == ai_recommendation
    )

    # -----------------------------------------------------
    # Confidence change
    # -----------------------------------------------------

    confidence_change = (
        final_confidence - initial_confidence
    )

    # -----------------------------------------------------
    # Over-reliance
    # -----------------------------------------------------

    # Participant was initially correct,
    # AI was incorrect,
    # participant followed the AI,
    # and therefore became incorrect.

    over_reliance = (
        ai_correct is False
        and initial_correct
        and followed_ai
        and not final_correct
    )

    # -----------------------------------------------------
    # Under-reliance
    # -----------------------------------------------------

    # AI was correct, participant did not follow it,
    # and the final decision was incorrect.

    under_reliance = (
        ai_correct is True
        and not followed_ai
        and not final_correct
    )

    return {
        "decision_changed": decision_changed,
        "initial_correct": initial_correct,
        "final_correct": final_correct,
        "followed_ai": followed_ai,
        "confidence_change": confidence_change,
        "over_reliance": over_reliance,
        "under_reliance": under_reliance,
    }