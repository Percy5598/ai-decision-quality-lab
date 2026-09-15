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


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Decision Quality Lab",
    page_icon="🧠",
    layout="centered",
)


# =========================================================
# SESSION STATE
# =========================================================

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

if "perceived_risk_initial" not in st.session_state:
    st.session_state.perceived_risk_initial = None

if "final_decision" not in st.session_state:
    st.session_state.final_decision = None

if "final_confidence" not in st.session_state:
    st.session_state.final_confidence = None

if "perceived_risk_final" not in st.session_state:
    st.session_state.perceived_risk_final = None

if "trust_in_ai" not in st.session_state:
    st.session_state.trust_in_ai = None

if "perceived_ai_reliability" not in st.session_state:
    st.session_state.perceived_ai_reliability = None

if "ai_influence" not in st.session_state:
    st.session_state.ai_influence = None

if "decision_reason" not in st.session_state:
    st.session_state.decision_reason = None

if "ai_correct" not in st.session_state:
    st.session_state.ai_correct = random.choice([True, False])


# =========================================================
# VARIABLES
# =========================================================

participant_id = st.session_state.participant_id
condition = st.session_state.condition
scenario = st.session_state.scenario
ai_correct = st.session_state.ai_correct


# =========================================================
# AI ADVICE
# =========================================================

advice = generate_advice(
    scenario=scenario,
    condition=condition,
    ai_correct=ai_correct,
)


# =========================================================
# HEADER
# =========================================================

st.title("🧠 AI Decision Quality Lab")

st.write(
    """
    This experiment studies how AI recommendations affect
    human decision-making, confidence, risk perception,
    and reliance on AI.
    """
)

st.divider()


# =========================================================
# SCENARIO
# =========================================================

st.subheader("📋 Decision Scenario")

st.markdown(f"### {scenario.title}")

st.write(scenario.description)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Investment",
        f"€{scenario.investment:,.0f}",
    )

with col2:
    st.metric(
        "Potential Loss",
        f"€{scenario.potential_loss:,.0f}",
    )

st.write(
    f"Expected return if successful: "
    f"**{scenario.expected_return:.0%}**"
)

st.write(
    f"Probability of success: "
    f"**{scenario.success_probability:.0%}**"
)

st.divider()


# =========================================================
# STAGE 1 — INITIAL DECISION
# =========================================================

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
        [
            "Invest",
            "Do not invest",
        ],
        key="initial_decision_input",
    )

    st.subheader("🎯 Confidence")

    initial_confidence = st.slider(
        "How confident are you in your decision?",
        0,
        100,
        50,
        1,
        key="initial_confidence_input",
    )

    st.write(
        f"Confidence: **{initial_confidence}%**"
    )

    st.subheader("⚠️ Perceived Risk")

    perceived_risk_initial = st.slider(
        "How risky do you think this decision is?",
        0,
        100,
        50,
        1,
        key="perceived_risk_initial_input",
    )

    st.write(
        f"Perceived risk: **{perceived_risk_initial}/100**"
    )

    if st.button(
        "Continue",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.initial_decision = initial_decision
        st.session_state.initial_confidence = initial_confidence
        st.session_state.perceived_risk_initial = (
            perceived_risk_initial
        )

        st.session_state.stage = "ai"

        st.rerun()


# =========================================================
# STAGE 2 — AI + FINAL DECISION
# =========================================================

elif st.session_state.stage == "ai":

    st.subheader("2️⃣ AI Advisor")

    # -----------------------------------------------------
    # Human-only condition
    # -----------------------------------------------------

    if advice is None:

        st.info(
            """
            You have been assigned to the
            **Human-Only condition**.

            No AI recommendation is provided.
            """
        )

        trust_in_ai = None
        perceived_ai_reliability = None
        ai_influence = None

    # -----------------------------------------------------
    # AI conditions
    # -----------------------------------------------------

    else:

        st.info(
            f"""
            **AI Recommendation: {advice.recommendation}**
            """
        )

        if condition.value == "ai_point_estimate":

            st.write(
                "The AI provides a point probability estimate."
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

        st.subheader("🤖 Your Evaluation of the AI")

        trust_in_ai = st.slider(
            "How much do you trust the AI recommendation?",
            0,
            100,
            50,
            1,
            key="trust_in_ai_input",
        )

        perceived_ai_reliability = st.slider(
            "How reliable do you think this AI is?",
            0,
            100,
            50,
            1,
            key="perceived_ai_reliability_input",
        )

        ai_influence = st.slider(
            "How much did the AI influence your decision?",
            0,
            100,
            50,
            1,
            key="ai_influence_input",
        )

    # -----------------------------------------------------
    # Final decision
    # -----------------------------------------------------

    st.divider()

    st.subheader("3️⃣ Your Final Decision")

    st.write(
        """
        After considering the information above,
        what is your final decision?
        """
    )

    final_decision = st.radio(
        "Choose one:",
        [
            "Invest",
            "Do not invest",
        ],
        key="final_decision_input",
    )

    st.subheader("🎯 Final Confidence")

    final_confidence = st.slider(
        "How confident are you now?",
        0,
        100,
        50,
        1,
        key="final_confidence_input",
    )

    st.write(
        f"Final confidence: **{final_confidence}%**"
    )

    st.subheader("⚠️ Final Perceived Risk")

    perceived_risk_final = st.slider(
        "How risky do you think this decision is now?",
        0,
        100,
        50,
        1,
        key="perceived_risk_final_input",
    )

    st.write(
        f"Final perceived risk: **{perceived_risk_final}/100**"
    )

    st.subheader("💭 Why did you make this final decision?")

    decision_reason = st.radio(
        "Select the main reason:",
        [
            "I agreed with the AI",
            "I disagreed with the AI",
            "The AI increased my confidence",
            "The AI decreased my confidence",
            "I focused mainly on the probability of success",
            "I focused mainly on the potential loss",
            "I made my own judgment regardless of the AI",
        ],
        key="decision_reason_input",
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
            initial_decision=(
                st.session_state.initial_decision
            ),
            final_decision=final_decision,
            initial_confidence=(
                st.session_state.initial_confidence
            ),
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
        # Create record
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

            perceived_risk_initial=(
                st.session_state.perceived_risk_initial
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

            trust_in_ai=trust_in_ai,

            perceived_ai_reliability=(
                perceived_ai_reliability
            ),

            ai_influence=ai_influence,

            final_decision=final_decision,

            final_confidence=final_confidence,

            perceived_risk_final=(
                perceived_risk_final
            ),

            decision_reason=decision_reason,

            optimal_decision=(
                scenario.optimal_decision
            ),

            expected_value=(
                scenario.expected_value
            ),

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

            under_reliance=(
                behavioral_measures["under_reliance"]
            ),
        )

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        save_decision(record)

        # -------------------------------------------------
        # Store results
        # -------------------------------------------------

        st.session_state.final_decision = final_decision
        st.session_state.final_confidence = final_confidence
        st.session_state.perceived_risk_final = (
            perceived_risk_final
        )
        st.session_state.trust_in_ai = trust_in_ai
        st.session_state.perceived_ai_reliability = (
            perceived_ai_reliability
        )
        st.session_state.ai_influence = ai_influence
        st.session_state.decision_reason = decision_reason

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
        Your responses have been recorded.

        The experiment studies how AI affects human
        decision-making, confidence, risk perception,
        and reliance.
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

        st.write("**Initial perceived risk**")

        st.write(
            f"{st.session_state.perceived_risk_initial}/100"
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

        st.write("**Final perceived risk**")

        st.write(
            f"{st.session_state.perceived_risk_final}/100"
        )

    st.divider()

    decision_changed = (
        st.session_state.initial_decision
        != st.session_state.final_decision
    )

    confidence_change = (
        st.session_state.final_confidence
        - st.session_state.initial_confidence
    )

    risk_change = (
        st.session_state.perceived_risk_final
        - st.session_state.perceived_risk_initial
    )

    st.subheader("Behavioral Outcomes")

    st.write(
        f"Decision changed: **{decision_changed}**"
    )

    st.write(
        f"Confidence change: **{confidence_change:+d} points**"
    )

    st.write(
        f"Risk perception change: **{risk_change:+d} points**"
    )

    if st.session_state.trust_in_ai is not None:

        st.write(
            f"Trust in AI: "
            f"**{st.session_state.trust_in_ai}/100**"
        )

        st.write(
            f"Perceived AI reliability: "
            f"**{st.session_state.perceived_ai_reliability}/100**"
        )

        st.write(
            f"AI influence: "
            f"**{st.session_state.ai_influence}/100**"
        )

    st.divider()

    st.caption(
        f"Experiment ID: {participant_id}"
    )