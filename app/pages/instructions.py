import streamlit as st


def show_instructions() -> None:
    st.title("Instructions")

    st.write(
        "Each trial presents a short decision scenario."
    )

    st.markdown("### For each trial")

    st.markdown(
        """
        **1. Initial estimate**

        Estimate the probability of the stated outcome from 0% to 100%.

        **2. Initial decision**

        Choose between the two available options.

        **3. Confidence**

        Indicate how confident you are in your decision.

        **4. AI information**

        Some trials will provide an AI estimate. Some will also "
        "provide an uncertainty range.

        **5. Final response**

        After reviewing the available information, provide your "
        "revised probability estimate, decision, and confidence.
        """
    )

    st.warning(
        "The AI recommendation may or may not be correct. "
        "Use the information provided to make your own judgment."
    )

    st.write(
        "The study does not provide feedback about whether your "
        "answers or the AI recommendations are correct during the experiment."
    )

    st.write(
        "Please respond based on your judgment for each individual trial."
    )