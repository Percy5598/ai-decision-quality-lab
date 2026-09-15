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

    # Initial human decision
    initial_decision: str
    initial_confidence: int

    # AI information
    ai_recommendation: Optional[str]
    ai_confidence: Optional[int]
    ai_correct: Optional[bool]

    # Final human decision
    final_decision: str
    final_confidence: int

    # Economic benchmark
    optimal_decision: str
    expected_value: float

    # Basic outcome
    decision_quality: int

    # Behavioral measures
    decision_changed: bool
    initial_correct: bool
    final_correct: bool
    followed_ai: bool
    confidence_change: int
    over_reliance: bool


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

    These measures describe how the participant
    responded to the AI recommendation.
    """

    # Did the participant change their decision?
    decision_changed = (
        initial_decision != final_decision
    )

    # Was the initial decision correct
    # according to the economic benchmark?
    initial_correct = (
        initial_decision == optimal_decision
    )

    # Was the final decision correct?
    final_correct = (
        final_decision == optimal_decision
    )

    # Did the participant's final decision
    # match the AI recommendation?
    followed_ai = (
        ai_recommendation is not None
        and final_decision == ai_recommendation
    )

    # Change in confidence after AI exposure.
    confidence_change = (
        final_confidence - initial_confidence
    )

    # Over-reliance:
    #
    # 1. AI was wrong
    # 2. Human was initially correct
    # 3. Human changed to follow the AI
    #
    over_reliance = (
        ai_correct is False
        and initial_correct
        and followed_ai
    )

    return {
        "decision_changed": decision_changed,
        "initial_correct": initial_correct,
        "final_correct": final_correct,
        "followed_ai": followed_ai,
        "confidence_change": confidence_change,
        "over_reliance": over_reliance,
    }