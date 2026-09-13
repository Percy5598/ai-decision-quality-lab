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

    initial_decision: Optional[str]
    initial_confidence: Optional[int]

    ai_recommendation: Optional[str]
    ai_confidence: Optional[int]

    final_decision: str
    final_confidence: int


def assign_condition() -> ExperimentCondition:
    """Randomly assign a participant to an experimental condition."""

    return random.choice(
        list(ExperimentCondition)
    )