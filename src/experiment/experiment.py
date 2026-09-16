from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DecisionRecord:
    participant_id: str
    scenario_id: int
    condition: str

    initial_decision: str
    initial_confidence: int

    ai_recommendation: Optional[str]
    ai_confidence: Optional[float]
    ai_reasoning: Optional[str]

    final_decision: str
    final_confidence: int

    correct_option: str

    initial_correct: bool
    final_correct: bool

    decision_changed: bool
    followed_ai: Optional[bool]

    confidence_change: int

    created_at: str


def calculate_decision_metrics(
    initial_decision: str,
    final_decision: str,
    correct_option: str,
    ai_recommendation: Optional[str],
    initial_confidence: int,
    final_confidence: int,
):
    initial_correct = initial_decision == correct_option
    final_correct = final_decision == correct_option

    decision_changed = initial_decision != final_decision

    followed_ai = None

    if ai_recommendation is not None:
        followed_ai = final_decision == ai_recommendation

    confidence_change = final_confidence - initial_confidence

    return {
        "initial_correct": initial_correct,
        "final_correct": final_correct,
        "decision_changed": decision_changed,
        "followed_ai": followed_ai,
        "confidence_change": confidence_change,
    }


def create_decision_record(
    participant_id: str,
    scenario_id: int,
    condition: str,
    initial_decision: str,
    initial_confidence: int,
    ai_recommendation: Optional[str],
    ai_confidence: Optional[float],
    ai_reasoning: Optional[str],
    final_decision: str,
    final_confidence: int,
    correct_option: str,
) -> DecisionRecord:

    metrics = calculate_decision_metrics(
        initial_decision=initial_decision,
        final_decision=final_decision,
        correct_option=correct_option,
        ai_recommendation=ai_recommendation,
        initial_confidence=initial_confidence,
        final_confidence=final_confidence,
    )

    return DecisionRecord(
        participant_id=participant_id,
        scenario_id=scenario_id,
        condition=condition,
        initial_decision=initial_decision,
        initial_confidence=initial_confidence,
        ai_recommendation=ai_recommendation,
        ai_confidence=ai_confidence,
        ai_reasoning=ai_reasoning,
        final_decision=final_decision,
        final_confidence=final_confidence,
        correct_option=correct_option,
        initial_correct=metrics["initial_correct"],
        final_correct=metrics["final_correct"],
        decision_changed=metrics["decision_changed"],
        followed_ai=metrics["followed_ai"],
        confidence_change=metrics["confidence_change"],
        created_at=datetime.utcnow().isoformat(),
    )