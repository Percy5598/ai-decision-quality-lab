import random
import uuid

import streamlit as st

from src.ai.advisor import generate_advice
from src.decisions.scenarios import SCENARIOS
from src.experiment.experiment import (
    DecisionRecord,
    assign_condition,
)
from src.experiment.storage import save_decision


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Decision Quality Lab",
    page_icon="🧠",
    layout="centered",
)


# ==================================================
# SESSION INITIALIZATION
# ==================================================

if "participant_id" not in st.session_state:
    st.session_state.participant_id = str(uuid.uuid4())


if "condition" not in st.session_state:
    st.session_state.condition = assign_condition()


if "scenario" not in st.session_state:
    st.session_state.scenario = random.choice(SCENARIOS)


if "stage" not in st.session_state:
    st.session_state.stage = "initial"


if "initial_decision" not in st.session_state:
    st.session_state.initial_decision = None


if "initial_confidence" not in st.session_state:
    st.session_state.initial_confidence = None


if "final_decision" not in st.session_state:
    st.session_state.final_decision = None


if "final_confidence" not in st.session_state:
    st.session_state.final_confidence = None


# ==================================================
# SESSION VARIABLES
# ==================================================

participant_id = st.session_state.participant_id
condition = st.session_state.condition
scenario = st.session_state.scenario


# ==================================================
# AI ACCURACY
# ==================================================

if "ai_correct" not in st.session_state:

    st.session_state.ai_correct = random.choice(
        [True, False]
    )

ai_correct = st.session_state.ai_correct


# ==================================================
# AI ADVICE
# ==================================================

advice = generate_advice(
    scenario=scenario,
    condition=condition,
    ai_correct=ai_correct,
)


# ==================================================
# PAGE HEADER
# ==================================================

st.title("🧠 AI Decision Quality Lab")

st.write(
    """
    This experiment studies how people make decisions
    when interacting with AI recommendations.
    """
)

st.caption(
    "Please make your initial decision before seeing the AI recommendation."
)

st.divider()


# ==================================================
# SCENARIO
# ==================================================

st.subheader("📊 Decision Scenario")

st.write(scenario.title)

st.write(scenario.description)


# --------------------------------------------------
# Scenario information
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Expected Return",
        f"{scenario.expected_return:.0%}",
    )

    st.metric(
        "Success Probability",
        f"{scenario.success_probability:.0%}",
    )

with col2:

    st.metric(
        "Potential Loss",
        f"€{scenario.potential_loss:,.0f}",
    )

    st.metric(
        "Investment",
        f"€{scenario.investment:,.0f}",
    )


st.divider()


# ==================================================
# STAGE 1 — INITIAL DECISION
# ==================================================

if st.session_state.stage == "initial":

    st.subheader("1️⃣ Your Initial Decision")

    st.write(
        """
        Based only on the information above,
        what would you decide?
        """
    )

    initial_decision = st.radio(
        "Choose one:",
        options=[
            "Invest",
            "Do not invest",
        ],
        key="initial_decision_input",
    )


    # --------------------------------------------------
    # Initial confidence
    # --------------------------------------------------

    st.subheader("🎯 Your Initial Confidence")

    initial_confidence = st.slider(
        "How confident are you in your decision?",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key="initial_confidence_input",
    )

    st.write(
        f"Confidence: **{initial_confidence}%**"
    )


    st.divider()


    # --------------------------------------------------
    # Continue
    # --------------------------------------------------

    if st.button(
        "Continue to AI Advice",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.initial_decision = (
            initial_decision
        )

        st.session_state.initial_confidence = (
            initial_confidence
        )

        st.session_state.stage = "ai"

        st.rerun()


# ==================================================
# STAGE 2 — AI ADVICE + FINAL DECISION
# ==================================================

elif st.session_state.stage == "ai":

    st.subheader("2️⃣ AI Advisor")

    # --------------------------------------------------
    # Human-only condition
    # --------------------------------------------------

    if advice is None:

        st.info(
            """
            You have been assigned to the
            **human-only condition**.

            No AI recommendation will be provided.
            """
        )

    # --------------------------------------------------
    # AI condition
    # --------------------------------------------------

    else:

        st.info(
            f"""
            **AI Recommendation: {advice.recommendation}**
            """
        )

        if condition.value == "ai_point_estimate":

            st.write(
                "Estimated probability of success:"
            )

            st.metric(
                "AI Estimate",
                f"{advice.probability:.0%}",
            )

        elif condition.value == "ai_uncertainty":

            st.write(
                "Estimated probability of success:"
            )

            st.metric(
                "AI Estimated Range",
                (
                    f"{advice.uncertainty_lower:.0%}"
                    f"–"
                    f"{advice.uncertainty_upper:.0%}"
                ),
            )

            st.caption(
                "The AI expresses uncertainty using a probability range."
            )

        st.write(
            f"AI confidence: **{advice.confidence}%**"
        )


    st.divider()


    # ==================================================
    # FINAL DECISION
    # ==================================================

    st.subheader("3️⃣ Your Final Decision")

    st.write(
        """
        After considering the information above,
        what is your final decision?
        """
    )

    final_decision = st.radio(
        "Choose one:",
        options=[
            "Invest",
            "Do not invest",
        ],
        key="final_decision_input",
    )


    # --------------------------------------------------
    # Final confidence
    # --------------------------------------------------

    st.subheader("🎯 Your Final Confidence")

    final_confidence = st.slider(
        "How confident are you now?",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key="final_confidence_input",
    )

    st.write(
        f"Confidence: **{final_confidence}%**"
    )


    st.divider()


    # ==================================================
    # SUBMIT EXPERIMENT
    # ==================================================

    if st.button(
        "Submit Experiment",
        type="primary",
        use_container_width=True,
    ):

        # --------------------------------------------------
        # Decision quality
        # --------------------------------------------------

        decision_quality = int(
            final_decision
            == scenario.optimal_decision
        )


        # --------------------------------------------------
        # Create record
        # --------------------------------------------------

        record = DecisionRecord(

            participant_id=participant_id,

            scenario_id=scenario.scenario_id,

            condition=condition,

            initial_decision=(
                st.session_state.initial_decision
            ),

            initial_confidence=(
                st.session_state.initial_confidence
            ),

            ai_recommendation=(
                advice.recommendation
                if advice is not None
                else None
            ),

            ai_confidence=(
                advice.confidence
                if advice is not None
                else None
            ),

            ai_correct=(
                advice.correct
                if advice is not None
                else None
            ),

            final_decision=final_decision,

            final_confidence=final_confidence,

            optimal_decision=scenario.optimal_decision,

            expected_value=scenario.expected_value,

            decision_quality=decision_quality,
        )


        # --------------------------------------------------
        # Save
        # --------------------------------------------------

        save_decision(record)


        # --------------------------------------------------
        # Store final values
        # --------------------------------------------------

        st.session_state.final_decision = (
            final_decision
        )

        st.session_state.final_confidence = (
            final_confidence
        )

        st.session_state.stage = "complete"

        st.rerun()


# ==================================================
# STAGE 3 — COMPLETION
# ==================================================

elif st.session_state.stage == "complete":

    st.success(
        "✅ Experiment completed successfully!"
    )

    st.subheader("Thank you")

    st.write(
        """
        Your decision has been recorded.

        The experiment is designed to study how AI
        recommendations affect human decision-making.
        """
    )

    st.divider()

    st.subheader("Your responses")

    st.write(
        {
            "Initial decision": (
                st.session_state.initial_decision
            ),
            "Initial confidence": (
                st.session_state.initial_confidence
            ),
            "Final decision": (
                st.session_state.final_decision
            ),
            "Final confidence": (
                st.session_state.final_confidence
            ),
        }
    )

    # --------------------------------------------------
    # Behavioral change
    # --------------------------------------------------

    changed = (
        st.session_state.initial_decision
        != st.session_state.final_decision
    )

    st.write(
        f"Decision changed after AI exposure: **{changed}**"
    )

    confidence_change = (
        st.session_state.final_confidence
        - st.session_state.initial_confidence
    )

    st.write(
        f"Confidence change: **{confidence_change:+d} points**"
    )

