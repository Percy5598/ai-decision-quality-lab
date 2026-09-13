import uuid

import streamlit as st

from src.decisions.scenarios import SCENARIOS
from src.experiment.experiment import (
    DecisionRecord,
    assign_condition,
)
from src.experiment.storage import save_decision


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Decision Quality Lab",
    page_icon="🧠",
    layout="centered",
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🧠 AI Decision Quality Lab")

st.write(
    """
    Does AI actually improve human decision-making,
    or does it simply make people more confident?
    """
)

st.divider()


# --------------------------------------------------
# Participant ID
# --------------------------------------------------

if "participant_id" not in st.session_state:
    st.session_state.participant_id = str(uuid.uuid4())

participant_id = st.session_state.participant_id


# --------------------------------------------------
# Experimental condition
# --------------------------------------------------

if "condition" not in st.session_state:
    st.session_state.condition = assign_condition()

condition = st.session_state.condition


# --------------------------------------------------
# Development information
# --------------------------------------------------

st.caption(
    f"Experimental condition: {condition.value}"
)


# --------------------------------------------------
# Scenario
# --------------------------------------------------

scenario = SCENARIOS[0]

st.subheader(scenario.title)

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


# --------------------------------------------------
# Human decision
# --------------------------------------------------

st.subheader("Your Decision")

decision = st.radio(
    "What would you decide?",
    [
        "Invest",
        "Do not invest",
    ],
)


# --------------------------------------------------
# Confidence
# --------------------------------------------------

confidence = st.slider(
    "How confident are you in your decision?",
    min_value=0,
    max_value=100,
    value=50,
    step=1,
)

st.write(f"Confidence: **{confidence}%**")


st.divider()


# --------------------------------------------------
# Submit decision
# --------------------------------------------------

if st.button(
    "Submit Decision",
    type="primary",
):

    record = DecisionRecord(
        participant_id=participant_id,
        scenario_id=scenario.scenario_id,
        condition=condition,
        initial_decision=None,
        initial_confidence=None,
        ai_recommendation=None,
        ai_confidence=None,
        final_decision=decision,
        final_confidence=confidence,
    )

    save_decision(record)

    st.success("Decision recorded successfully!")

    st.subheader("Recorded Observation")

    st.write(
        {
            "participant_id": record.participant_id,
            "scenario_id": record.scenario_id,
            "condition": record.condition.value,
            "decision": record.final_decision,
            "confidence": record.final_confidence,
        }
    )