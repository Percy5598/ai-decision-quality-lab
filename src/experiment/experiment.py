from enum import Enum


class ExperimentCondition(Enum):
    HUMAN_ONLY = "human_only"
    AI_POINT_ESTIMATE = "ai_point_estimate"
    AI_UNCERTAINTY = "ai_uncertainty"

from dataclasses import dataclass
from typing import Optional


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