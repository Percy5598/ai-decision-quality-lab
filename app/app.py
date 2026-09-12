import sys
from pathlib import Path

# Add project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import uuid

import streamlit as st

from src.decisions.scenarios import SCENARIOS
from src.experiment.experiment import (
    DecisionRecord,
    ExperimentCondition,
)
from src.experiment.storage import save_decision

st.set_page_config(
    page_title="AI Decision Quality Lab",
    page_icon="🧠",
    layout="centered",
)


st.title("🧠 AI Decision Quality Lab")

st.write(
    """
    Does AI actually improve human decision-making,
    or does it simply make people more confident?
    """
)

st.divider()


# --------------------------------------------------
# Participant
# --------------------------------------------------

if "participant_id" not in st.session_state:
    st.session_state.participant_id = str(uuid.uuid4())


participant_id = st.session_state.participant_id


# --------------------------------------------------
# Scenario
# --------------------------------------------------

scenario = SCENARIOS[0]

st.subheader(scenario.title)

st.write(scenario.description)

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

confidence = st.slider(
    "How confident are you?",
    min_value=0,
    max_value=100,
    value=50,
    step=1,
)


# --------------------------------------------------
# Submit
# --------------------------------------------------

if st.button(
    "Submit Decision",
    type="primary",
):

    record = DecisionRecord(
        participant_id=participant_id,
        scenario_id=scenario.scenario_id,
        condition=ExperimentCondition.HUMAN_ONLY,
        initial_decision=None,
        initial_confidence=None,
        ai_recommendation=None,
        ai_confidence=None,
        final_decision=decision,
        final_confidence=confidence,
    )

    save_decision(record)

    st.success("Decision recorded!")

    st.write("### Recorded observation")

    st.write(
        {
            "participant_id": record.participant_id,
            "scenario_id": record.scenario_id,
            "condition": record.condition.value,
            "decision": record.final_decision,
            "confidence": record.final_confidence,
        }
    )