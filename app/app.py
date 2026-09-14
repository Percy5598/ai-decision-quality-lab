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
# PARTICIPANT
# ==================================================

if "participant_id" not in st.session_state:
    st.session_state.participant_id = str(uuid.uuid4())

participant_id = st.session_state.participant_id


# ==================================================
# EXPERIMENTAL CONDITION
# ==================================================

if "condition" not in st.session_state:
    st.session_state.condition = assign_condition()

condition = st.session_state.condition


# ==================================================
# SCENARIO
# ==================================================

scenario = SCENARIOS[0]


# ==================================================
# AI ADVICE
# ==================================================

advice = generate_advice(
    scenario=scenario,
    condition=condition,
)


# ==================================================
# PAGE TITLE
# ==================================================

st.title("🧠 AI Decision Quality Lab")

st.write(
    """
    ### Does AI actually improve human decision-making?

    This experiment studies how people make decisions
    when they receive different types of AI advice.
    """
)

st.caption(
    "Your responses are recorded anonymously using a random session ID."
)

st.divider()


# ==================================================
# SCENARIO
# ==================================================

st.subheader("📊 Decision Scenario")

st.write(scenario.description)


# --------------------------------------------------
# Scenario metrics
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.metric(
        label="Expected Return",
        value=f"{scenario.expected_return:.0%}",
    )

    st.metric(
        label="Success Probability",
        value=f"{scenario.success_probability:.0%}",
    )

with col2:

    st.metric(
        label="Potential Loss",
        value=f"€{scenario.potential_loss:,.0f}",
    )

    st.metric(
        label="Investment",
        value=f"€{scenario.investment:,.0f}",
    )


st.divider()


# ==================================================
# AI INFORMATION
# ==================================================

if advice is not None:

    st.subheader("🤖 AI Advisor")

    st.info(
        f"""
        **AI Recommendation:** {advice.recommendation}
        """
    )

    # --------------------------------------------------
    # Point estimate condition
    # --------------------------------------------------

    if condition.value == "ai_point_estimate":

        st.write(
            "Estimated probability of success:"
        )

        st.metric(
            label="AI Estimate",
            value=f"{advice.probability:.0%}",
        )

    # --------------------------------------------------
    # Uncertainty condition
    # --------------------------------------------------

    elif condition.value == "ai_uncertainty":

        st.write(
            "Estimated probability of success:"
        )

        st.metric(
            label="AI Estimated Range",
            value=(
                f"{advice.uncertainty_lower:.0%}"
                f"–"
                f"{advice.uncertainty_upper:.0%}"
            ),
        )

        st.caption(
            "The AI provides a range because it is uncertain "
            "about the exact probability."
        )

    # --------------------------------------------------
    # AI confidence
    # --------------------------------------------------

    st.write(
        f"AI confidence: **{advice.confidence}%**"
    )

    st.divider()


# ==================================================
# HUMAN DECISION
# ==================================================

st.subheader("🧑 Your Decision")

st.write(
    "Based on the information above, what would you decide?"
)

decision = st.radio(
    "Choose one:",
    options=[
        "Invest",
        "Do not invest",
    ],
)


# ==================================================
# HUMAN CONFIDENCE
# ==================================================

st.subheader("🎯 Your Confidence")

confidence = st.slider(
    "How confident are you in your decision?",
    min_value=0,
    max_value=100,
    value=50,
    step=1,
)

st.write(
    f"Your confidence: **{confidence}%**"
)


st.divider()


# ==================================================
# SUBMIT DECISION
# ==================================================

if st.button(
    "Submit Decision",
    type="primary",
    use_container_width=True,
):

    # --------------------------------------------------
    # Calculate decision quality
    # --------------------------------------------------

    decision_quality = int(
        decision == scenario.optimal_decision
    )

    # --------------------------------------------------
    # Create decision record
    # --------------------------------------------------

    record = DecisionRecord(
        participant_id=participant_id,
        scenario_id=scenario.scenario_id,
        condition=condition,

        initial_decision=None,
        initial_confidence=None,

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

        final_decision=decision,
        final_confidence=confidence,

        optimal_decision=scenario.optimal_decision,
        expected_value=scenario.expected_value,
        decision_quality=decision_quality,
    )

    # --------------------------------------------------
    # Save observation
    # --------------------------------------------------

    save_decision(record)

    # --------------------------------------------------
    # Confirmation
    # --------------------------------------------------

    st.success(
        "✅ Decision recorded successfully!"
    )

    # --------------------------------------------------
    # Show result
    # --------------------------------------------------

    st.subheader("📋 Recorded Observation")

    st.write(
        {
            "scenario_id": record.scenario_id,
            "condition": record.condition.value,
            "ai_recommendation": record.ai_recommendation,
            "ai_confidence": record.ai_confidence,
            "final_decision": record.final_decision,
            "final_confidence": record.final_confidence,
            "optimal_decision": record.optimal_decision,
            "expected_value": record.expected_value,
            "decision_quality": record.decision_quality,
        }
    )

    # --------------------------------------------------
    # Explain decision quality
    # --------------------------------------------------

    if decision_quality == 1:

        st.success(
            "Your decision matches the model-optimal benchmark."
        )

    else:

        st.warning(
            "Your decision differs from the model-optimal benchmark."
        )

    st.caption(
        "Decision quality is currently measured as whether "
        "your decision matches the specified economic benchmark."
    )
