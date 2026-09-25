from __future__ import annotations

import streamlit as st

from pages.completion import show_completion
from pages.consent import show_consent
from pages.experiment import show_experiment
from pages.instructions import show_instructions
from pages.introduction import show_introduction

from src.experiment.session import (
    initialize_session,
    set_trial_assignments,
)

from src.experiment.trial_generator import generate_trials

st.set_page_config(
    page_title="AI Decision Quality Lab",
    page_icon="🧠",
    layout="centered",
)


def initialize_experiment() -> None:
    """Initialize participant session and randomized trials."""

    initialize_session()

    if not st.session_state.trial_order:

        scenarios, assignments = generate_trials(
            st.session_state.participant_id
        )

        st.session_state.scenarios = scenarios

        set_trial_assignments(
            assignments,
            scenarios,
        )


def main() -> None:
    """Main Streamlit application."""

    initialize_experiment()

    if st.session_state.experiment_completed:
        show_completion()
        return

    stage = st.session_state.get(
        "stage",
        "introduction",
    )

    # ---------------------------------------------------------
    # Introduction
    # ---------------------------------------------------------

    if stage == "introduction":

        show_introduction()

        st.markdown("---")

        if st.button(
            "Continue",
            type="primary",
        ):
            st.session_state.stage = "consent"
            st.rerun()

        return

    # ---------------------------------------------------------
    # Consent
    # ---------------------------------------------------------

    if stage == "consent":

        consent_given = show_consent()

        st.markdown("---")

        if not consent_given:
            st.warning(
                "Please confirm your consent before continuing."
            )
            return

        if st.button(
            "Continue",
            type="primary",
        ):
            st.session_state.stage = "instructions"
            st.rerun()

        return

    # ---------------------------------------------------------
    # Instructions
    # ---------------------------------------------------------

    if stage == "instructions":

        show_instructions()

        st.markdown("---")

        if st.button(
            "Start practice",
            type="primary",
        ):
            st.session_state.stage = "practice"
            st.session_state.practice_trial = 0
            st.rerun()

        return

    # ---------------------------------------------------------
    # Practice
    # ---------------------------------------------------------

    if stage == "practice":

        show_practice_trial()

        return

    # ---------------------------------------------------------
    # Experimental trials
    # ---------------------------------------------------------

    if stage == "experiment":

        show_experiment(
            st.session_state.scenarios
        )

        return


def show_practice_trial() -> None:
    """Display a simple practice task.

    Practice trials are not saved to the research dataset.
    """

    practice_trials = [
        {
            "question": (
                "A weather forecast says there is a 70% chance "
                "of rain tomorrow. How likely do you think rain is?"
            ),
            "answer": 70,
        },
        {
            "question": (
                "A product test estimates a 60% probability that "
                "a new product will meet its target. What is your "
                "estimate?"
            ),
            "answer": 60,
        },
        {
            "question": (
                "A business forecast estimates a 40% probability "
                "of reaching a sales target. What is your estimate?"
            ),
            "answer": 40,
        },
    ]

    index = st.session_state.practice_trial

    if index >= len(practice_trials):
        st.session_state.stage = "experiment"
        st.session_state.experiment_started = True
        st.rerun()

        return

    trial = practice_trials[index]

    st.title("Practice")

    st.caption(
        f"Practice trial {index + 1} of "
        f"{len(practice_trials)}"
    )

    st.write(trial["question"])

    st.slider(
        "Your probability estimate (%)",
        0,
        100,
        50,
        key=f"practice_estimate_{index}",
    )

    st.radio(
        "Choose an option",
        ["Option A", "Option B"],
        key=f"practice_decision_{index}",
    )

    if st.button(
        "Continue",
        type="primary",
        key=f"practice_continue_{index}",
    ):
        st.session_state.practice_trial += 1
        st.rerun()


if __name__ == "__main__":
    main()