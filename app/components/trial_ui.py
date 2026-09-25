from __future__ import annotations

import streamlit as st

from src.config import (
    CONDITION_AI_POINT,
    CONDITION_AI_UNCERTAINTY,
    CONDITION_HUMAN_ONLY,
)
from src.data.models import DecisionScenario


def show_scenario(
    scenario: DecisionScenario,
) -> None:
    """Display the current scenario."""

    st.subheader(scenario.title)

    st.write(scenario.scenario_text)

    st.markdown("### Your initial judgment")

    st.write(
        "Estimate the probability that the stated outcome "
        "will occur."
    )


def show_initial_inputs(
    scenario: DecisionScenario,
) -> tuple[float, str, float]:
    """Collect the initial probability, decision and confidence."""

    estimate = st.slider(
        "Initial probability estimate (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key="initial_estimate_widget",
    )

    decision = st.radio(
        "What is your initial decision?",
        options=["option_a", "option_b"],
        format_func=lambda option: (
            scenario.option_a
            if option == "option_a"
            else scenario.option_b
        ),
        key="initial_decision_widget",
    )

    confidence = st.slider(
        "How confident are you in your initial decision? (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key="initial_confidence_widget",
    )

    return estimate, decision, confidence


def show_ai_information(
    scenario: DecisionScenario,
    condition: str,
) -> None:
    """Display AI information according to the experimental condition."""

    if condition == CONDITION_HUMAN_ONLY:
        st.info(
            "No AI recommendation is provided for this trial."
        )
        return

    st.markdown("### AI information")

    st.info(
        f"AI estimated probability: "
        f"**{scenario.ai_estimate:.0f}%**"
    )

    if condition == CONDITION_AI_UNCERTAINTY:
        st.info(
            f"AI uncertainty range: "
            f"**{scenario.ai_lower_bound:.0f}% – "
            f"{scenario.ai_upper_bound:.0f}%**"
        )

        st.write(
            "The model has moderate confidence in this estimate."
        )

    elif condition == CONDITION_AI_POINT:
        st.write(
            "The AI provides a point estimate for this outcome."
        )


def show_final_inputs(
    scenario: DecisionScenario,
) -> tuple[float, str, float]:
    """Collect the final probability, decision and confidence."""

    st.markdown("### Your final judgment")

    estimate = st.slider(
        "Final probability estimate (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key="final_estimate_widget",
    )

    decision = st.radio(
        "What is your final decision?",
        options=["option_a", "option_b"],
        format_func=lambda option: (
            scenario.option_a
            if option == "option_a"
            else scenario.option_b
        ),
        key="final_decision_widget",
    )

    confidence = st.slider(
        "How confident are you in your final decision? (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key="final_confidence_widget",
    )

    return estimate, decision, confidence