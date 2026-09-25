"""
Participant-specific experimental randomization.

The participant ID is converted into a deterministic seed so that
the same participant receives the same randomized trial sequence.
"""

import hashlib
import random

from src.config import CONDITION_COUNTS
from src.data.models import DecisionScenario, TrialAssignment


def participant_seed(participant_id: str) -> int:
    """
    Convert a participant ID into a deterministic integer seed.

    This allows the experimental sequence to be reproduced for the
    same participant ID.
    """

    digest = hashlib.sha256(
        participant_id.encode("utf-8")
    ).hexdigest()

    return int(digest[:16], 16)


def build_condition_sequence(
    participant_id: str,
) -> list[str]:
    """
    Create a balanced randomized condition sequence.

    Default 20-trial allocation:

        human_only          = 7
        ai_point_estimate   = 7
        ai_uncertainty      = 6

    The order is randomized using a deterministic seed.
    """

    conditions: list[str] = []

    for condition, count in CONDITION_COUNTS.items():
        conditions.extend([condition] * count)

    rng = random.Random(
        participant_seed(participant_id)
    )

    rng.shuffle(conditions)

    return conditions


def build_trial_assignments(
    participant_id: str,
    scenarios: list[DecisionScenario],
) -> list[TrialAssignment]:
    """
    Assign unique scenarios and randomized conditions
    to participant trials.

    No scenario is repeated for the same participant.
    """

    required_trials = sum(
        CONDITION_COUNTS.values()
    )

    if len(scenarios) < required_trials:
        raise ValueError(
            f"Need at least {required_trials} scenarios, "
            f"but only {len(scenarios)} were provided."
        )

    rng = random.Random(
        participant_seed(participant_id)
    )

    scenario_pool = list(scenarios)

    rng.shuffle(scenario_pool)

    selected_scenarios = scenario_pool[
        :required_trials
    ]

    conditions = build_condition_sequence(
        participant_id
    )

    assignments: list[TrialAssignment] = []

    for index in range(required_trials):

        trial_number = index + 1

        scenario = selected_scenarios[index]

        assignments.append(
            TrialAssignment(
                trial_id=(
                    f"{participant_id[:8]}"
                    f"_trial_{trial_number:02d}"
                ),
                trial_number=trial_number,
                question_id=scenario.question_id,
                condition=conditions[index],
            )
        )

    return assignments