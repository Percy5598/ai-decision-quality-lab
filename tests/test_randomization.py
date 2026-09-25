"""
Tests for experimental randomization.
"""

from collections import Counter

from src.config import (
    CONDITION_HUMAN_ONLY,
    CONDITION_AI_POINT,
    CONDITION_AI_UNCERTAINTY,
)

from src.experiment.randomization import (
    build_condition_sequence,
    build_trial_assignments,
    participant_seed,
)

from src.experiment.trial_generator import (
    load_scenarios,
)


def test_participant_seed_is_deterministic():
    seed_a = participant_seed(
        "participant-001"
    )

    seed_b = participant_seed(
        "participant-001"
    )

    assert seed_a == seed_b


def test_different_participants_have_different_seeds():
    seed_a = participant_seed(
        "participant-001"
    )

    seed_b = participant_seed(
        "participant-002"
    )

    assert seed_a != seed_b


def test_condition_counts():
    conditions = build_condition_sequence(
        "participant-001"
    )

    counts = Counter(conditions)

    assert counts[
        CONDITION_HUMAN_ONLY
    ] == 7

    assert counts[
        CONDITION_AI_POINT
    ] == 7

    assert counts[
        CONDITION_AI_UNCERTAINTY
    ] == 6


def test_condition_sequence_has_20_trials():
    conditions = build_condition_sequence(
        "participant-001"
    )

    assert len(conditions) == 20


def test_condition_sequence_is_reproducible():
    first = build_condition_sequence(
        "participant-001"
    )

    second = build_condition_sequence(
        "participant-001"
    )

    assert first == second


def test_trial_assignments_have_20_trials():
    scenarios = load_scenarios()

    assignments = build_trial_assignments(
        participant_id="participant-001",
        scenarios=scenarios,
    )

    assert len(assignments) == 20


def test_no_question_is_repeated():
    scenarios = load_scenarios()

    assignments = build_trial_assignments(
        participant_id="participant-001",
        scenarios=scenarios,
    )

    question_ids = [
        assignment.question_id
        for assignment in assignments
    ]

    assert len(question_ids) == len(
        set(question_ids)
    )


def test_trial_numbers_are_sequential():
    scenarios = load_scenarios()

    assignments = build_trial_assignments(
        participant_id="participant-001",
        scenarios=scenarios,
    )

    trial_numbers = [
        assignment.trial_number
        for assignment in assignments
    ]

    assert trial_numbers == list(
        range(1, 21)
    )


def test_same_participant_gets_same_trials():
    scenarios = load_scenarios()

    first = build_trial_assignments(
        participant_id="participant-001",
        scenarios=scenarios,
    )

    second = build_trial_assignments(
        participant_id="participant-001",
        scenarios=scenarios,
    )

    assert first == second
