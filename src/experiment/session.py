from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import streamlit as st

from src.analysis.metrics import (
    absolute_update,
    ai_influence,
    decision_from_estimate,
    decision_from_probability,
    decision_is_correct,
    signed_update,
)
from src.config import (
    CONDITION_AI_POINT,
    CONDITION_AI_UNCERTAINTY,
    CONDITION_HUMAN_ONLY,
    TOTAL_TRIALS,
)
from src.data.models import DecisionScenario, TrialAssignment, TrialResponse
from src.data.storage import CSVStorage


def create_participant_id() -> str:
    """Create an anonymous participant identifier."""
    return f"participant_{uuid4().hex[:12]}"


def initialize_session() -> None:
    """Initialize Streamlit session state once."""

    if st.session_state.get("experiment_initialized", False):
        return

    st.session_state.participant_id = create_participant_id()

    st.session_state.current_trial = 0
    st.session_state.trial_order = []
    st.session_state.current_condition = None
    st.session_state.current_question = None

    st.session_state.experiment_started = False
    st.session_state.experiment_completed = False

    st.session_state.responses = []

    st.session_state.initial_estimate = None
    st.session_state.initial_decision = None
    st.session_state.initial_confidence = None

    st.session_state.ai_revealed = False

    st.session_state.final_estimate = None
    st.session_state.final_decision = None
    st.session_state.final_confidence = None

    st.session_state.trial_started_at = None

    st.session_state.initial_response_recorded = False
    st.session_state.final_response_recorded = False
    st.session_state.trial_saved = False

    st.session_state.experiment_initialized = True


def set_trial_assignments(
    assignments: list[TrialAssignment],
    scenarios: list[DecisionScenario],
) -> None:
    """Store randomized assignments and load the first trial."""

    scenario_map = {
        scenario.question_id: scenario
        for scenario in scenarios
    }

    if len(assignments) != TOTAL_TRIALS:
        raise ValueError(
            f"Expected {TOTAL_TRIALS} assignments, "
            f"got {len(assignments)}."
        )

    for assignment in assignments:
        if assignment.question_id not in scenario_map:
            raise ValueError(
                f"Unknown question ID: {assignment.question_id}"
            )

    st.session_state.trial_order = assignments
    st.session_state.current_trial = 0

    load_current_trial(scenarios)


def load_current_trial(
    scenarios: list[DecisionScenario],
) -> None:
    """Load the current trial into session state."""

    index = st.session_state.current_trial

    if index >= len(st.session_state.trial_order):
        st.session_state.experiment_completed = True
        return

    scenario_map = {
        scenario.question_id: scenario
        for scenario in scenarios
    }

    assignment = st.session_state.trial_order[index]

    st.session_state.current_condition = assignment.condition
    st.session_state.current_question = scenario_map[
        assignment.question_id
    ]

    reset_current_trial()

    st.session_state.trial_started_at = datetime.now(
        timezone.utc
    )


def reset_current_trial() -> None:
    """Reset all state belonging to the current trial."""

    st.session_state.initial_estimate = None
    st.session_state.initial_decision = None
    st.session_state.initial_confidence = None

    st.session_state.ai_revealed = False

    st.session_state.final_estimate = None
    st.session_state.final_decision = None
    st.session_state.final_confidence = None

    st.session_state.initial_response_recorded = False
    st.session_state.final_response_recorded = False
    st.session_state.trial_saved = False


def record_initial_response(
    estimate: float,
    decision: str,
    confidence: float,
) -> None:
    """Store the participant's initial response."""

    st.session_state.initial_estimate = float(estimate)
    st.session_state.initial_decision = decision
    st.session_state.initial_confidence = float(confidence)

    st.session_state.initial_response_recorded = True


def reveal_ai() -> None:
    """Reveal AI information for the current trial."""

    st.session_state.ai_revealed = True


def record_final_response(
    estimate: float,
    decision: str,
    confidence: float,
) -> None:
    """Store the participant's final response."""

    st.session_state.final_estimate = float(estimate)
    st.session_state.final_decision = decision
    st.session_state.final_confidence = float(confidence)

    st.session_state.final_response_recorded = True


def current_trial_ready_for_submission() -> bool:
    """Return whether the current trial contains all required responses."""

    if not st.session_state.initial_response_recorded:
        return False

    if not st.session_state.final_response_recorded:
        return False

    condition = st.session_state.current_condition

    if condition != CONDITION_HUMAN_ONLY:
        if not st.session_state.ai_revealed:
            return False

    return True


def build_trial_response() -> TrialResponse:
    """Convert the current trial state into a TrialResponse."""

    if not current_trial_ready_for_submission():
        raise ValueError(
            "Current trial is not ready for submission."
        )

    assignment = st.session_state.trial_order[
        st.session_state.current_trial
    ]

    scenario: DecisionScenario = (
        st.session_state.current_question
    )

    initial_estimate = st.session_state.initial_estimate
    final_estimate = st.session_state.final_estimate

    signed = signed_update(
        initial_estimate,
        final_estimate,
    )

    absolute = absolute_update(
        initial_estimate,
        final_estimate,
    )

    ai_estimate = None
    ai_lower_bound = None
    ai_upper_bound = None
    influence = None
    followed_ai_value = None

    if assignment.condition != CONDITION_HUMAN_ONLY:
        ai_estimate = scenario.ai_estimate
        influence = ai_influence(
            initial_estimate,
            final_estimate,
            scenario.ai_estimate,
        )

        ai_decision = decision_from_estimate(
            scenario.ai_estimate,
            scenario.decision_threshold,
        )

        followed_ai_value = (
            st.session_state.final_decision == ai_decision
        )

    if assignment.condition == CONDITION_AI_UNCERTAINTY:
        ai_lower_bound = scenario.ai_lower_bound
        ai_upper_bound = scenario.ai_upper_bound

    correct_decision = decision_from_probability(
    scenario.true_probability,
    scenario.decision_threshold,
    )

    initial_correct = decision_is_correct(
        st.session_state.initial_decision,
        correct_decision,
    )

    final_correct = decision_is_correct(
        st.session_state.final_decision,
        correct_decision,
    )
    
    response_time = 0.0

    if st.session_state.trial_started_at:
        response_time = (
            datetime.now(timezone.utc)
            - st.session_state.trial_started_at
        ).total_seconds()

    return TrialResponse(
        participant_id=st.session_state.participant_id,
        trial_id=assignment.trial_id,
        question_id=scenario.question_id,
        condition=assignment.condition,
        question_domain=scenario.domain,
        true_probability=scenario.true_probability,
        human_initial_estimate=initial_estimate,
        ai_estimate=ai_estimate,
        ai_lower_bound=ai_lower_bound,
        ai_upper_bound=ai_upper_bound,
        human_final_estimate=final_estimate,
        initial_decision=st.session_state.initial_decision,
        final_decision=st.session_state.final_decision,
        initial_confidence=st.session_state.initial_confidence,
        final_confidence=st.session_state.final_confidence,
        followed_ai=followed_ai_value,
        changed_estimate=absolute > 0,
        absolute_update=absolute,
        signed_update=signed,
        ai_influence=influence,
        initial_decision_correct=initial_correct,
        final_decision_correct=final_correct,
        decision_correct=final_correct,
        response_time=response_time,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def save_current_trial() -> TrialResponse:
    """Save the current trial exactly once."""

    if st.session_state.trial_saved:
        raise ValueError("Current trial has already been saved.")

    response = build_trial_response()

    storage = CSVStorage()
    storage.append_response(response)

    st.session_state.responses.append(response)
    st.session_state.trial_saved = True

    return response


def advance_to_next_trial(
    scenarios: list[DecisionScenario],
) -> None:
    """Move to the next experimental trial."""

    st.session_state.current_trial += 1

    if st.session_state.current_trial >= TOTAL_TRIALS:
        st.session_state.experiment_completed = True
        return

    load_current_trial(scenarios)