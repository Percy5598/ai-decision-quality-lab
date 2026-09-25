import streamlit as st


def show_completion() -> None:
    """Display the completion screen."""

    st.title("Experiment complete")

    st.success("Thank you for participating.")

    st.write(
        "Your responses have been recorded."
    )

    st.write(
        "The experiment is now complete."
    )

    st.info(
        "No individual correctness feedback is provided "
        "as part of the experiment."
    )