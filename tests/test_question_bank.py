"""
Tests for the experimental question bank.
"""

from src.data.validation import (
    validate_scenario,
    validate_question_bank,
)

from src.experiment.trial_generator import (
    load_scenarios,
)


def test_question_bank_has_at_least_30_questions():
    scenarios = load_scenarios()

    assert len(scenarios) >= 30


def test_question_ids_are_unique():
    scenarios = load_scenarios()

    question_ids = [
        scenario.question_id
        for scenario in scenarios
    ]

    assert len(question_ids) == len(
        set(question_ids)
    )


def test_all_scenarios_are_valid():
    scenarios = load_scenarios()

    for scenario in scenarios:
        validate_scenario(scenario)


def test_question_bank_is_valid():
    scenarios = load_scenarios()

    validate_question_bank(
        scenarios,
        minimum_size=30,
    )
