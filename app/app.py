import sys
from pathlib import Path
import random
import uuid

# -------------------------------------------------------------------
# Make the project root importable.
# This fixes Streamlit Cloud imports such as:
# from src.ai.advisor import generate_advice
# -------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


import streamlit as st

from src.ai.advisor import generate_advice
from src.ai.advisor import format_advice
from src.decisions.scenarios import get_scenarios
from src.experiment.experiment import create_decision_record
from src.experiment.storage import save_decision


# -------------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------------

st.set_page_config(
    page_title="AI Decision Quality Lab",
    page_icon="🧠",
    layout="centered",
)


# -------------------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------------------

CONDITIONS = [
    "human_only",
    "ai_point_estimate",
    "ai_uncertainty",
]

CONDITION_LABELS = {
    "human_only": "Human Only",
    "ai_point_estimate": "AI Point Estimate",
    "ai_uncertainty": "AI + Uncertainty",
}


# -------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------------------------

def initialize_session():
    """Initialize the experiment session."""

    if "initialized" not in st.session_state:

        st.session_state.initialized = True

        st.session_state.participant_id = (
            f"P-{uuid.uuid4().hex[:8].upper()}"
        )

        st.session_state.condition = random.choice(
            CONDITIONS
        )

        scenarios = get_scenarios()

        # Randomize scenario order for each participant.
        scenario_ids = [
            scenario.scenario_id
            for scenario in scenarios
        ]

        random.shuffle(scenario_ids)

        st.session_state.scenario_order = scenario_ids

        st.session_state.current_index = 0

        st.session_state.phase = "initial"

        st.session_state.initial_decision = None
        st.session_state.initial_confidence = None

        st.session_state.ai_recommendation = None
        st.session_state.ai_confidence = None
        st.session_state.ai_reasoning = None

        st.session_state.completed_records = []

        st.session_state.experiment_complete = False


initialize_session()


# -------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------

def get_current_scenario():
    """Return the current scenario."""

    scenario_id = st.session_state.scenario_order[
        st.session_state.current_index
    ]

    scenarios = get_scenarios()

    for scenario in scenarios:
        if scenario.scenario_id == scenario_id:
            return scenario

    raise ValueError(
        f"Scenario {scenario_id} could not be found."
    )


def reset_experiment():
    """Reset the entire experiment."""

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    initialize_session()


def submit_initial_decision(
    decision: str,
    confidence: int,
    scenario,
):
    """Store the initial decision and prepare AI information."""

    st.session_state.initial_decision = decision
    st.session_state.initial_confidence = confidence

    advice = generate_advice(scenario)

    st.session_state.ai_recommendation = (
        advice.recommendation
    )

    st.session_state.ai_confidence = (
        advice.confidence
    )

    st.session_state.ai_reasoning = (
        advice.reasoning
    )

    st.session_state.phase = "ai"


def submit_final_decision(
    decision: str,
    confidence: int,
    scenario,
):
    """Create and store the completed decision record."""

    record = create_decision_record(
        participant_id=st.session_state.participant_id,
        scenario_id=scenario.scenario_id,
        condition=st.session_state.condition,
        initial_decision=st.session_state.initial_decision,
        initial_confidence=st.session_state.initial_confidence,
        ai_recommendation=(
            st.session_state.ai_recommendation
            if st.session_state.condition != "human_only"
            else None
        ),
        ai_confidence=(
            st.session_state.ai_confidence
            if st.session_state.condition != "human_only"
            else None
        ),
        ai_reasoning=(
            st.session_state.ai_reasoning
            if st.session_state.condition != "human_only"
            else None
        ),
        final_decision=decision,
        final_confidence=confidence,
        correct_option=scenario.correct_option,
    )

    save_decision(record)

    st.session_state.completed_records.append(record)

    st.session_state.current_index += 1

    if (
        st.session_state.current_index
        >= len(st.session_state.scenario_order)
    ):
        st.session_state.experiment_complete = True
        st.session_state.phase = "complete"

    else:
        st.session_state.initial_decision = None
        st.session_state.initial_confidence = None

        st.session_state.ai_recommendation = None
        st.session_state.ai_confidence = None
        st.session_state.ai_reasoning = None

        st.session_state.phase = "initial"


# -------------------------------------------------------------------
# HEADER
# -------------------------------------------------------------------

st.title("🧠 AI Decision Quality Lab")

st.markdown(
    """
### Human–AI Decision-Making Experiment

This prototype studies how AI recommendations and
uncertainty information may affect:

- decision-making
- confidence
- reliance on AI
- decision changes
- decision accuracy
"""
)


# -------------------------------------------------------------------
# EXPERIMENT INFORMATION
# -------------------------------------------------------------------

with st.expander("About this experiment"):

    st.markdown(
        """
You will complete a series of decision-making scenarios.

For each scenario:

**1. Initial decision**

You will make a decision without seeing the AI recommendation.

**2. AI information**

Depending on your experimental condition, you may receive:

- no AI information;
- an AI recommendation;
- an AI recommendation with confidence information.

**3. Final decision**

You will make the decision again and report your confidence.

Your responses are used to calculate behavioral measures
such as decision changes, accuracy, AI reliance, and confidence changes.
"""
    )


# -------------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------------

with st.sidebar:

    st.header("Experiment")

    st.write(
        f"**Participant:** "
        f"{st.session_state.participant_id}"
    )

    st.write(
        f"**Condition:** "
        f"{CONDITION_LABELS[st.session_state.condition]}"
    )

    total_scenarios = len(
        st.session_state.scenario_order
    )

    completed = len(
        st.session_state.completed_records
    )

    st.progress(
        completed / total_scenarios
    )

    st.write(
        f"Progress: {completed} / {total_scenarios}"
    )

    st.divider()

    if st.button(
        "Restart experiment",
        use_container_width=True,
    ):
        reset_experiment()
        st.rerun()


# -------------------------------------------------------------------
# COMPLETION PAGE
# -------------------------------------------------------------------

if st.session_state.experiment_complete:

    st.success(
        "Experiment completed successfully."
    )

    st.header("Thank you")

    st.write(
        "You have completed all decision scenarios."
    )

    records = st.session_state.completed_records

    if records:

        initial_accuracy = sum(
            record.initial_correct
            for record in records
        ) / len(records)

        final_accuracy = sum(
            record.final_correct
            for record in records
        ) / len(records)

        decision_changes = sum(
            record.decision_changed
            for record in records
        )

        average_confidence_change = sum(
            record.confidence_change
            for record in records
        ) / len(records)

        st.subheader("Your session summary")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Initial accuracy",
                f"{initial_accuracy:.0%}",
            )

            st.metric(
                "Final accuracy",
                f"{final_accuracy:.0%}",
            )

        with col2:

            st.metric(
                "Decision changes",
                decision_changes,
            )

            st.metric(
                "Average confidence change",
                f"{average_confidence_change:+.1f}",
            )

    st.info(
        "Your responses have been recorded for this prototype."
    )

    st.stop()


# -------------------------------------------------------------------
# CURRENT SCENARIO
# -------------------------------------------------------------------

scenario = get_current_scenario()

current_number = (
    st.session_state.current_index + 1
)

total_number = len(
    st.session_state.scenario_order
)


st.caption(
    f"Scenario {current_number} of {total_number}"
)

st.progress(
    current_number / total_number
)

st.header(scenario.title)

st.markdown(
    scenario.context
)

st.divider()


# ===================================================================
# PHASE 1 — INITIAL DECISION
# ===================================================================

if st.session_state.phase == "initial":

    st.subheader("Step 1 — Make your initial decision")

    st.write(
        scenario.question
    )

    with st.form(
        key=f"initial_form_{scenario.scenario_id}"
    ):

        initial_decision = st.radio(
            "Choose one:",
            options=["A", "B"],
            format_func=lambda x: (
                scenario.option_a
                if x == "A"
                else scenario.option_b
            ),
        )

        initial_confidence = st.slider(
            "How confident are you in your decision?",
            min_value=0,
            max_value=100,
            value=50,
            step=1,
            format="%d%%",
        )

        submitted = st.form_submit_button(
            "Continue",
            use_container_width=True,
        )

        if submitted:

            submit_initial_decision(
                decision=initial_decision,
                confidence=initial_confidence,
                scenario=scenario,
            )

            st.rerun()


# ===================================================================
# PHASE 2 — AI INFORMATION
# ===================================================================

elif st.session_state.phase == "ai":

    st.subheader(
        "Step 2 — Review additional information"
    )

    st.write(
        "Your initial decision has been recorded."
    )

    st.divider()

    condition = st.session_state.condition

    if condition == "human_only":

        st.info(
            "You are in the Human Only condition. "
            "No AI recommendation is provided."
        )

    elif condition == "ai_point_estimate":

        st.info(
            "The system provides an AI recommendation."
        )

        st.markdown(
            f"""
**AI recommendation**

{st.session_state.ai_recommendation}
"""
        )

        st.caption(
            "The AI recommendation is presented without "
            "an explicit uncertainty estimate."
        )

    elif condition == "ai_uncertainty":

        st.info(
            "The system provides an AI recommendation "
            "together with its confidence."
        )

        st.markdown(
            f"""
**AI recommendation**

{st.session_state.ai_recommendation}

**AI confidence**

{st.session_state.ai_confidence:.0%}

**AI reasoning**

{st.session_state.ai_reasoning}
"""
        )

    st.divider()

    st.subheader(
        "Step 3 — Make your final decision"
    )

    st.write(
        scenario.question
    )

    with st.form(
        key=f"final_form_{scenario.scenario_id}"
    ):

        final_decision = st.radio(
            "Choose one:",
            options=["A", "B"],
            format_func=lambda x: (
                scenario.option_a
                if x == "A"
                else scenario.option_b
            ),
        )

        final_confidence = st.slider(
            "How confident are you now?",
            min_value=0,
            max_value=100,
            value=50,
            step=1,
            format="%d%%",
        )

        submitted = st.form_submit_button(
            "Submit final decision",
            use_container_width=True,
        )

        if submitted:

            submit_final_decision(
                decision=final_decision,
                confidence=final_confidence,
                scenario=scenario,
            )

            st.rerun()
