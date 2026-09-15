import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

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


# ============================================================
# CONFIGURATION
# ============================================================

TOTAL_TRIALS = min(5, len(SCENARIOS))


st.set_page_config(
    page_title="AI Decision Quality Lab",
    page_icon="🧠",
    layout="centered",
)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "participant_id" not in st.session_state:
    st.session_state.participant_id = str(
        uuid.uuid4()
    )

if "condition" not in st.session_state:
    st.session_state.condition = assign_condition()

if "scenario_order" not in st.session_state:

    scenario_indices = list(
        range(len(SCENARIOS))
    )

    random.shuffle(scenario_indices)

    st.session_state.scenario_order = (
        scenario_indices[:TOTAL_TRIALS]
    )

if "trial_number" not in st.session_state:
    st.session_state.trial_number = 1

if "stage" not in st.session_state:
    st.session_state.stage = "initial"

if "ai_correct" not in st.session_state:
    st.session_state.ai_correct = random.choice(
        [True, False]
    )


# ============================================================
# CURRENT TRIAL
# ============================================================

trial_number = st.session_state.trial_number

scenario_index = st.session_state.scenario_order[
    trial_number - 1
]

scenario = SCENARIOS[scenario_index]

condition = st.session_state.condition

ai_correct = st.session_state.ai_correct


# ============================================================
# AI ADVICE
# ============================================================

advice = generate_advice(
    scenario=scenario,
    condition=condition,
    ai_correct=ai_correct,
)


# ============================================================
# HEADER
# ============================================================

st.title("🧠 AI Decision Quality Lab")

st.write(
    """
    This experiment studies how AI recommendations
    affect human decision-making, confidence,
    perceived risk, and reliance on AI.
    """
)


# ============================================================
# PROGRESS
# ============================================================

st.subheader(
    f"Trial {trial_number} of {TOTAL_TRIALS}"
)

progress = (
    trial_number / TOTAL_TRIALS
)

st.progress(progress)

st.caption(
    f"Experimental condition: {condition.value}"
)


st.divider()


# ============================================================
# SCENARIO
# ============================================================

st.subheader("📋 Decision Scenario")

st.markdown(
    f"### {scenario.title}"
)

st.write(
    scenario.description
)


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


# ============================================================
# STAGE 1 — INITIAL DECISION
# ============================================================

if st.session_state.stage == "initial":

    st.subheader(
        "1️⃣ Before seeing any AI recommendation"
    )

    st.info(
        """
        Please make your decision based only on
        the information provided in the scenario.
        """
    )

    # -------------------------
    # Question 1
    # -------------------------

    st.markdown("### Question 1")

    initial_decision = st.radio(
        "What would you decide?",
        [
            "Invest",
            "Do not invest",
        ],
        key=f"initial_decision_{trial_number}",
    )

    # -------------------------
    # Question 2
    # -------------------------

    st.markdown("### Question 2")

    initial_confidence = st.slider(
        "How confident are you in your decision?",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key=f"initial_confidence_{trial_number}",
    )

    st.caption(
        f"Confidence: {initial_confidence}/100"
    )

    # -------------------------
    # Question 3
    # -------------------------

    st.markdown("### Question 3")

    perceived_risk_initial = st.slider(
        "How risky do you think this decision is?",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key=f"risk_initial_{trial_number}",
    )

    # -------------------------
    # Question 4
    # -------------------------

    st.markdown("### Question 4")

    financial_attractiveness_initial = st.slider(
        "How financially attractive is this investment?",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key=f"attractiveness_{trial_number}",
    )

    # -------------------------
    # Question 5
    # -------------------------

    st.markdown("### Question 5")

    perceived_uncertainty_initial = st.slider(
        "How uncertain do you think the outcome is?",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key=f"uncertainty_initial_{trial_number}",
    )

    # -------------------------
    # Question 6
    # -------------------------

    st.markdown("### Question 6")

    decision_difficulty = st.slider(
        "How difficult was this decision?",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key=f"difficulty_{trial_number}",
    )

    st.divider()

    if st.button(
        "Continue to AI information →",
        type="primary",
        use_container_width=True,
    ):

        # Store all initial responses.
        st.session_state.initial_decision = (
            initial_decision
        )

        st.session_state.initial_confidence = (
            initial_confidence
        )

        st.session_state.perceived_risk_initial = (
            perceived_risk_initial
        )

        st.session_state.financial_attractiveness_initial = (
            financial_attractiveness_initial
        )

        st.session_state.perceived_uncertainty_initial = (
            perceived_uncertainty_initial
        )

        st.session_state.decision_difficulty = (
            decision_difficulty
        )

        st.session_state.stage = "ai"

        st.rerun()


# ============================================================
# STAGE 2 — AI INFORMATION + FINAL DECISION
# ============================================================

elif st.session_state.stage == "ai":

    st.subheader(
        "2️⃣ AI information"
    )

    if advice is None:

        st.info(
            """
            You are in the **Human-Only condition**.

            No AI recommendation is provided.
            """
        )

    else:

        st.info(
            f"""
            **AI Recommendation**

            {advice.recommendation}
            """
        )

        st.metric(
            "AI Estimated Probability",
            f"{advice.probability:.0%}",
        )

        st.write(
            f"AI confidence: **{advice.confidence}%**"
        )

        if condition.value == "ai_point_estimate":

            st.write(
                """
                The AI provides a point probability
                estimate without an explicit uncertainty range.
                """
            )

        elif condition.value == "ai_uncertainty":

            st.write(
                """
                The AI provides a probability estimate
                together with an uncertainty range.
                """
            )

            st.metric(
                "AI Uncertainty Range",
                (
                    f"{advice.uncertainty_lower:.0%}"
                    f" – "
                    f"{advice.uncertainty_upper:.0%}"
                ),
            )


    st.divider()


    # ========================================================
    # FINAL DECISION
    # ========================================================

    st.subheader(
        "3️⃣ After considering the information"
    )

    # -------------------------
    # Question 7
    # -------------------------

    st.markdown("### Question 7")

    final_decision = st.radio(
        "What is your final decision?",
        [
            "Invest",
            "Do not invest",
        ],
        key=f"final_decision_{trial_number}",
    )

    # -------------------------
    # Question 8
    # -------------------------

    st.markdown("### Question 8")

    final_confidence = st.slider(
        "How confident are you in your final decision?",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key=f"final_confidence_{trial_number}",
    )

    # -------------------------
    # Question 9
    # -------------------------

    st.markdown("### Question 9")

    perceived_risk_final = st.slider(
        "How risky do you think the decision is now?",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key=f"risk_final_{trial_number}",
    )

    # -------------------------
    # Question 10
    # -------------------------

    st.markdown("### Question 10")

    perceived_uncertainty_final = st.slider(
        "How uncertain do you think the outcome is now?",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key=f"uncertainty_final_{trial_number}",
    )


    # ========================================================
    # AI EVALUATION
    # ========================================================

    st.divider()

    if advice is not None:

        st.subheader(
            "4️⃣ Evaluation of the AI"
        )

        # -------------------------
        # Question 11
        # -------------------------

        st.markdown("### Question 11")

        trust_in_ai = st.slider(
            "How much do you trust the AI recommendation?",
            min_value=0,
            max_value=100,
            value=50,
            step=1,
            key=f"trust_{trial_number}",
        )

        # -------------------------
        # Question 12
        # -------------------------

        st.markdown("### Question 12")

        perceived_ai_reliability = st.slider(
            "How reliable do you think the AI is?",
            min_value=0,
            max_value=100,
            value=50,
            step=1,
            key=f"reliability_{trial_number}",
        )

        # -------------------------
        # Question 13
        # -------------------------

        st.markdown("### Question 13")

        ai_clarity = st.slider(
            "How clear was the AI information?",
            min_value=0,
            max_value=100,
            value=50,
            step=1,
            key=f"clarity_{trial_number}",
        )

        # -------------------------
        # Question 14
        # -------------------------

        st.markdown("### Question 14")

        ai_agreement = st.slider(
            "How much did you agree with the AI recommendation?",
            min_value=0,
            max_value=100,
            value=50,
            step=1,
            key=f"agreement_{trial_number}",
        )

        # -------------------------
        # Question 15
        # -------------------------

        st.markdown("### Question 15")

        ai_influence = st.slider(
            "How much did the AI influence your final decision?",
            min_value=0,
            max_value=100,
            value=50,
            step=1,
            key=f"influence_{trial_number}",
        )

        # -------------------------
        # Question 16
        # -------------------------

        st.markdown("### Question 16")

        decision_reason = st.radio(
            "What was the main reason for your final decision?",
            [
                "I agreed with the AI",
                "I disagreed with the AI",
                "The AI increased my confidence",
                "The AI decreased my confidence",
                "I focused mainly on the probability of success",
                "I focused mainly on the potential loss",
                "I made my own judgment regardless of the AI",
            ],
            key=f"reason_{trial_number}",
        )

    else:

        # Human-only condition.
        trust_in_ai = None
        perceived_ai_reliability = None
        ai_clarity = None
        ai_agreement = None
        ai_influence = None

        st.subheader(
            "4️⃣ Reason for your final decision"
        )

        decision_reason = st.radio(
            "What was the main reason for your final decision?",
            [
                "I focused mainly on the probability of success",
                "I focused mainly on the potential loss",
                "The investment appeared financially attractive",
                "The investment appeared financially unattractive",
                "I felt confident in my initial judgment",
                "I felt uncertain about the decision",
                "I made my own overall judgment",
            ],
            key=f"reason_{trial_number}",
        )


    st.divider()


    # ========================================================
    # SUBMIT TRIAL
    # ========================================================

    if st.button(
        "Submit Trial",
        type="primary",
        use_container_width=True,
    ):

        behavioral_measures = (
            calculate_behavioral_measures(
                initial_decision=(
                    st.session_state.initial_decision
                ),
                final_decision=final_decision,
                initial_confidence=(
                    st.session_state.initial_confidence
                ),
                final_confidence=final_confidence,
                perceived_risk_initial=(
                    st.session_state.perceived_risk_initial
                ),
                perceived_risk_final=(
                    perceived_risk_final
                ),
                perceived_uncertainty_initial=(
                    st.session_state.perceived_uncertainty_initial
                ),
                perceived_uncertainty_final=(
                    perceived_uncertainty_final
                ),
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
                optimal_decision=(
                    scenario.optimal_decision
                ),
            )
        )


        # ====================================================
        # CREATE TRIAL RECORD
        # ====================================================

        record = DecisionRecord(
            participant_id=(
                st.session_state.participant_id
            ),

            trial_number=trial_number,

            scenario_id=scenario.scenario_id,

            condition=condition,

            # BEFORE AI
            initial_decision=(
                st.session_state.initial_decision
            ),

            initial_confidence=(
                st.session_state.initial_confidence
            ),

            perceived_risk_initial=(
                st.session_state.perceived_risk_initial
            ),

            financial_attractiveness_initial=(
                st.session_state.financial_attractiveness_initial
            ),

            perceived_uncertainty_initial=(
                st.session_state.perceived_uncertainty_initial
            ),

            decision_difficulty=(
                st.session_state.decision_difficulty
            ),

            # AI
            ai_recommendation=(
                advice.recommendation
                if advice is not None
                else None
            ),

            ai_probability=(
                advice.probability
                if advice is not None
                else None
            ),

            ai_confidence=(
                advice.confidence
                if advice is not None
                else None
            ),

            ai_uncertainty_lower=(
                advice.uncertainty_lower
                if advice is not None
                else None
            ),

            ai_uncertainty_upper=(
                advice.uncertainty_upper
                if advice is not None
                else None
            ),

            ai_correct=(
                advice.correct
                if advice is not None
                else None
            ),

            # AFTER AI
            final_decision=final_decision,

            final_confidence=final_confidence,

            perceived_risk_final=(
                perceived_risk_final
            ),

            perceived_uncertainty_final=(
                perceived_uncertainty_final
            ),

            # AI EVALUATION
            trust_in_ai=trust_in_ai,

            perceived_ai_reliability=(
                perceived_ai_reliability
            ),

            ai_clarity=ai_clarity,

            ai_agreement=ai_agreement,

            ai_influence=ai_influence,

            decision_reason=decision_reason,

            # ECONOMIC BENCHMARK
            optimal_decision=(
                scenario.optimal_decision
            ),

            expected_value=(
                scenario.expected_value
            ),

            # BEHAVIORAL OUTCOMES
            decision_quality=(
                behavioral_measures[
                    "decision_quality"
                ]
            ),

            decision_changed=(
                behavioral_measures[
                    "decision_changed"
                ]
            ),

            initial_correct=(
                behavioral_measures[
                    "initial_correct"
                ]
            ),

            final_correct=(
                behavioral_measures[
                    "final_correct"
                ]
            ),

            followed_ai=(
                behavioral_measures[
                    "followed_ai"
                ]
            ),

            confidence_change=(
                behavioral_measures[
                    "confidence_change"
                ]
            ),

            risk_change=(
                behavioral_measures[
                    "risk_change"
                ]
            ),

            uncertainty_change=(
                behavioral_measures[
                    "uncertainty_change"
                ]
            ),

            # RELIANCE
            over_reliance=(
                behavioral_measures[
                    "over_reliance"
                ]
            ),

            under_reliance=(
                behavioral_measures[
                    "under_reliance"
                ]
            ),
        )


        # ====================================================
        # SAVE TRIAL
        # ====================================================

        save_decision(record)


        # ====================================================
        # MOVE TO NEXT TRIAL
        # ====================================================

        if trial_number < TOTAL_TRIALS:

            st.session_state.trial_number += 1

            st.session_state.stage = "initial"

            # New AI correctness for the next trial.
            st.session_state.ai_correct = random.choice(
                [True, False]
            )

            st.rerun()

        else:

            st.session_state.stage = "complete"

            st.rerun()


# ============================================================
# EXPERIMENT COMPLETE
# ============================================================

elif st.session_state.stage == "complete":

    st.success(
        "🎉 Experiment completed successfully!"
    )

    st.title(
        "Thank you for participating"
    )

    st.write(
        """
        You have completed all decision-making trials.

        Your responses have been recorded for analysis.
        """
    )

    st.divider()

    st.subheader(
        "Experiment Summary"
    )

    st.metric(
        "Trials completed",
        TOTAL_TRIALS,
    )

    st.write(
        f"Participant ID: "
        f"`{st.session_state.participant_id}`"
    )

    st.write(
        f"Experimental condition: "
        f"**{condition.value}**"
    )

    st.divider()

    st.subheader(
        "What this experiment measures"
    )

    st.write(
        """
        The experiment collects information about:

        • Human decision quality

        • Confidence

        • Risk perception

        • Uncertainty perception

        • Decision difficulty

        • Trust in AI

        • Perceived AI reliability

        • AI clarity

        • AI agreement

        • AI influence

        • Changes in decisions after AI exposure

        • Over-reliance on incorrect AI

        • Under-reliance on correct AI
        """
    )

    st.divider()

    st.info(
        """
        The experiment uses a model-based economic benchmark
        to evaluate decision quality. This benchmark represents
        the optimal decision under the assumptions encoded in
        the scenario model; it is not a universal definition
        of a correct real-world decision.
        """
    )