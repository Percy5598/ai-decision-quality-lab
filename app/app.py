import random
import uuid

import streamlit as st

from src.ai.advisor import generate_advice
from src.decisions.scenarios import SCENARIOS
from src.experiment.experiment import (
    DecisionRecord,
    assign_condition,
    calculate_behavioral_measures,
)
from src.experiment.storage import save_decision


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Decision Quality Lab",
    page_icon="🧠",
    layout="centered",
)


# ---------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------

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

if "ai_correct" not in st.session_state:
    st.session_state.ai_correct = random.choice([True, False])


# ---------------------------------------------------------
# Experiment variables
# ---------------------------------------------------------

participant_id = st.session_state.participant_id
condition = st.session_state.condition
scenario = st.session_state.scenario
ai_correct = st.session_state.ai_correct


# ---------------------------------------------------------
# Generate AI advice
# ---------------------------------------------------------

advice = generate_advice(
    scenario=scenario,
    condition=condition,
    ai_correct=ai_correct,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🧠 AI Decision Quality Lab")

st.write(
    """
    This experiment studies how AI recommendations affect
    human decision-making, confidence, and reliance on AI.
    """
)

st.divider()


# ---------------------------------------------------------
# Scenario
# ---------------------------------------------------------

st.subheader("📋 Decision Scenario")

st.markdown(f"### {scenario.title}")

st.write(scenario.description)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Potential investment",
        f"€{scenario.investment:,.0f}",
    )

with col2:
    st.metric(
        "Potential loss",
        f"€{scenario.potential_loss:,.0f}",
    )

st.write(
    f"Expected return if successful: **{scenario.expected_return:.0%}**"
)

st.write(
    f"Success probability information: **{scenario.success_probability:.0%}**"
)

st.divider()


# =========================================================
# STAGE 1 — INITIAL DECISION
# =========================================================

if st.session_state.stage == "initial":

    st.subheader("1️⃣ Your Initial Decision")

    st.write(
        """
        Based only on the scenario information above,
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

    if st.button(
        "Continue to AI Advice",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.initial_decision = initial_decision
        st.session_state.initial_confidence = initial_confidence
        st.session_state.stage = "ai"

        st.rerun()


# =========================================================
# STAGE 2 — AI ADVICE + FINAL DECISION
# =========================================================

elif st.session_state.stage == "ai":

    st.subheader("2️⃣ AI Advisor")

    if advice is None:

        st.info(
            """
            You have been assigned to the
            **Human-Only condition**.

            No AI recommendation is provided.
            """
        )

    else:

        st.info(
            f"""
            **AI Recommendation: {advice.recommendation}**
            """
        )

        if condition.value == "ai_point_estimate":

            st.write(
                "The AI provides a point estimate."
            )

            st.metric(
                "AI Estimated Probability",
                f"{advice.probability:.0%}",
            )

        elif condition.value == "ai_uncertainty":

            st.write(
                "The AI provides an estimate together with uncertainty."
            )

            st.metric(
                "AI Estimated Probability",
                f"{advice.probability:.0%}",
            )

            st.metric(
                "AI Uncertainty Range",
                (
                    f"{advice.uncertainty_lower:.0%}"
                    f" – "
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

    # -----------------------------------------------------
    # Final decision
    # -----------------------------------------------------

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

    if st.button(
        "Submit Experiment",
        type="primary",
        use_container_width=True,
    ):

        # -------------------------------------------------
        # Calculate behavioral measures
        # -------------------------------------------------

        behavioral_measures = calculate_behavioral_measures(
            initial_decision=st.session_state.initial_decision,
            final_decision=final_decision,
            initial_confidence=st.session_state.initial_confidence,
            final_confidence=final_confidence,
            ai_recommendation=(
                advice.recommendation
                if advice is not None
                else None
            ),
            ai_correct=(
                advice.correct
                if advice is not None
                else None
            ),
            optimal_decision=scenario.optimal_decision,
        )

        # -------------------------------------------------
        # Decision quality
        # -------------------------------------------------

        decision_quality = int(
            behavioral_measures["final_correct"]
        )

        # -------------------------------------------------
        # Create experiment record
        # -------------------------------------------------

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

            decision_changed=(
                behavioral_measures["decision_changed"]
            ),

            initial_correct=(
                behavioral_measures["initial_correct"]
            ),

            final_correct=(
                behavioral_measures["final_correct"]
            ),

            followed_ai=(
                behavioral_measures["followed_ai"]
            ),

            confidence_change=(
                behavioral_measures["confidence_change"]
            ),

            over_reliance=(
                behavioral_measures["over_reliance"]
            ),
        )

        # -------------------------------------------------
        # Save experiment
        # -------------------------------------------------

        save_decision(record)

        # -------------------------------------------------
        # Store final state
        # -------------------------------------------------

        st.session_state.final_decision = final_decision
        st.session_state.final_confidence = final_confidence
        st.session_state.stage = "complete"

        st.rerun()


# =========================================================
# STAGE 3 — COMPLETION
# =========================================================

elif st.session_state.stage == "complete":

    st.success(
        "✅ Experiment completed successfully!"
    )

    st.subheader("Thank you")

    st.write(
        """
        Your decision has been recorded.

        This experiment is designed to study how AI
        recommendations affect human decision-making.
        """
    )

    st.divider()

    st.subheader("Your Responses")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Initial decision**")

        st.write(
            st.session_state.initial_decision
        )

        st.write("**Initial confidence**")

        st.write(
            f"{st.session_state.initial_confidence}%"
        )

    with col2:

        st.write("**Final decision**")

        st.write(
            st.session_state.final_decision
        )

        st.write("**Final confidence**")

        st.write(
            f"{st.session_state.final_confidence}%"
        )

    st.divider()

    # -----------------------------------------------------
    # Behavioral outcomes
    # -----------------------------------------------------

    decision_changed = (
        st.session_state.initial_decision
        != st.session_state.final_decision
    )

    confidence_change = (
        st.session_state.final_confidence
        - st.session_state.initial_confidence
    )

    st.subheader("Behavioral Outcomes")

    st.write(
        f"Decision changed after AI exposure: "
        f"**{decision_changed}**"
    )

    st.write(
        f"Confidence change: "
        f"**{confidence_change:+d} points**"
    )

    st.divider()

    st.caption(
        f"Experiment ID: {participant_id}"
    )