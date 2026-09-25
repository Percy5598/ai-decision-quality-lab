import streamlit as st


def show_progress(
    current_trial: int,
    total_trials: int,
) -> None:
    """Display participant progress."""

    completed = min(current_trial, total_trials)

    st.progress(
        completed / total_trials,
        text=f"Trial {completed} of {total_trials}",
    )