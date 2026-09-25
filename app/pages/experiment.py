from __future__ import annotations

import streamlit as st

from components.progress import show_progress
from components.trial_ui import (
    show_ai_information,
    show_final_inputs,
    show_initial_inputs,
    show_scenario,
)
from src.config import TOTAL_TRIALS
from src.experiment.session import (
    advance_to_next_trial,
    record_final_response,
    record_initial_response,
    reveal_ai,
    save_current_trial,
)


def show_experiment(
    scenarios,
) -> None:
    """Run the participant-facing experimental trials."""

    current_trial = st.session_state.current_trial
    condition = st.session_state.current_condition
    scenario = st.session_state.current_question

    show_progress(
        current_trial + 1,
        TOTAL_TRIALS,
    )

    st.markdown("---")

    show_scenario(scenario)

    # ---------------------------------------------------------
    # Initial stage
    # ---------------------------------------------------------

    if not st.session_state.initial_response_recorded:

        estimate, decision, confidence = show_initial_inputs(
            scenario
        )

        if st.button(
            "Continue",
            type="primary",
            key="submit_initial",
        ):
            record_initial_response(
                estimate,
                decision,
                confidence,
            )

            st.rerun()

        return

    # ---------------------------------------------------------
    # AI / information stage
    # ---------------------------------------------------------

    if condition != "human_only":

        if not st.session_state.ai_revealed:

            show_ai_information(
                scenario,
                condition,
            )

            if st.button(
                "Continue to final judgment",
                type="primary",
                key="reveal_ai",
            ):
                reveal_ai()
                st.rerun()

            return

    else:

        if not st.session_state.ai_revealed:

            st.info(
                "There is no AI recommendation for this trial. "
                "Please continue to your final judgment."
            )

            if st.button(
                "Continue to final judgment",
                type="primary",
                key="continue_human_only",
            ):
                reveal_ai()
                st.rerun()

            return

    # ---------------------------------------------------------
    # Final stage
    # ---------------------------------------------------------

    estimate, decision, confidence = show_final_inputs(
        scenario
    )

    if st.button(
        "Submit final response",
        type="primary",
        key="submit_final",
    ):
        record_final_response(
            estimate,
            decision,
            confidence,
        )

        save_current_trial()

        if current_trial + 1 >= TOTAL_TRIALS:
            st.session_state.experiment_completed = True
            st.rerun()

        advance_to_next_trial(scenarios)

        st.rerun()