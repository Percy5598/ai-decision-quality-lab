"""
Data models for the AI Decision Quality Lab.

These models represent the experimental design independently
from Streamlit.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class DecisionScenario:
    """
    A single decision problem.

    true_probability is researcher-side ground truth and is never
    shown to participants.
    """

    question_id: str
    domain: str
    title: str
    scenario_text: str

    option_a: str
    option_b: str

    true_probability: float
    decision_threshold: float

    ai_estimate: float
    ai_lower_bound: float
    ai_upper_bound: float

@dataclass(frozen=True)
class TrialAssignment:
    """
    Assignment of one scenario to one participant trial.
    """

    trial_id: str
    trial_number: int
    question_id: str
    condition: str


@dataclass
class TrialResponse:
    """
    Trial-level research observation.

    One participant produces one record for every completed trial.
    """

    participant_id: str
    trial_id: str
    question_id: str
    condition: str
    question_domain: str

    true_probability: float

    human_initial_estimate: float

    ai_estimate: Optional[float]
    ai_lower_bound: Optional[float]
    ai_upper_bound: Optional[float]

    human_final_estimate: float

    initial_decision: str
    final_decision: str

    initial_confidence: float
    final_confidence: float

    followed_ai: Optional[bool]
    changed_estimate: bool

    absolute_update: float
    signed_update: float

    ai_influence: Optional[float]

    initial_decision_correct: bool
    final_decision_correct: bool
    decision_correct: bool

    response_time: float
    timestamp: str
