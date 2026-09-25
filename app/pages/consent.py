import streamlit as st


def show_consent() -> bool:
    """Display consent information and return consent status."""

    st.title("Consent")

    st.write(
        "Please read the following information before "
        "continuing."
    )

    st.markdown(
        """
        By participating:

        - You will complete a series of decision-making tasks.
        - Your responses will be recorded for research purposes.
        - No direct personal identifiers are required.
        - You may stop participating at any time.
        """
    )

    return st.checkbox(
        "I have read the information above and agree to participate.",
        key="consent_given",
    )