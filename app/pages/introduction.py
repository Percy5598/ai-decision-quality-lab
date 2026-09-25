import streamlit as st


def show_introduction() -> None:
    st.title("AI Decision Quality Lab")

    st.write(
        "This study examines decision-making when people receive "
        "information from an AI system."
    )

    st.write(
        "You will complete a series of short decision tasks. "
        "For some tasks, you will receive an AI recommendation. "
        "Some AI recommendations may also include information "
        "about uncertainty."
    )

    st.write(
        "The study takes approximately 10–15 minutes."
    )

    st.markdown("### What you will do")

    st.markdown(
        """
        1. Read a short decision scenario.
        2. Estimate the probability of an outcome.
        3. Make a decision and indicate your confidence.
        4. On some trials, review information from an AI system.
        5. Revise your estimate and decision.
        """
    )

    st.info(
        "There are no questions about your personal identity or "
        "private information."
    )