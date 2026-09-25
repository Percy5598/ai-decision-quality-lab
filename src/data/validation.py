"""
Validation functions for the AI Decision Quality Lab.

These checks protect the integrity of the experimental dataset
and question bank.
"""

from src.data.models import DecisionScenario


def validate_probability(
    value: float,
    name: str,
) -> None:
    """
    Validate that a probability is between 0 and 100.
    """

    if not 0 <= value <= 100:
        raise ValueError(
            f"{name} must be between 0 and 100. "
            f"Got {value}."
        )


def validate_scenario(
    scenario: DecisionScenario,
) -> None:
    """
    Validate one decision scenario.
    """

    validate_probability(
        scenario.true_probability,
        "true_probability",
    )

    validate_probability(
        scenario.ai_estimate,
        "ai_estimate",
    )

    validate_probability(
        scenario.ai_lower_bound,
        "ai_lower_bound",
    )

    validate_probability(
        scenario.ai_upper_bound,
        "ai_upper_bound",
    )

    validate_probability(
        scenario.decision_threshold,
        "decision_threshold",
    )

    if not scenario.question_id.strip():
        raise ValueError(
            "question_id cannot be empty."
        )

    if not scenario.domain.strip():
        raise ValueError(
            f"{scenario.question_id}: "
            "domain cannot be empty."
        )

    if not scenario.scenario_text.strip():
        raise ValueError(
            f"{scenario.question_id}: "
            "scenario_text cannot be empty."
        )

    if not scenario.option_a.strip():
        raise ValueError(
            f"{scenario.question_id}: "
            "option_a cannot be empty."
        )

    if not scenario.option_b.strip():
        raise ValueError(
            f"{scenario.question_id}: "
            "option_b cannot be empty."
        )

    if scenario.ai_lower_bound > scenario.ai_estimate:
        raise ValueError(
            f"{scenario.question_id}: "
            "AI lower bound cannot exceed AI estimate."
        )

    if scenario.ai_upper_bound < scenario.ai_estimate:
        raise ValueError(
            f"{scenario.question_id}: "
            "AI upper bound cannot be below AI estimate."
        )

    if scenario.ai_lower_bound > scenario.ai_upper_bound:
        raise ValueError(
            f"{scenario.question_id}: "
            "AI lower bound cannot exceed upper bound."
        )


def validate_question_bank(
    scenarios: list[DecisionScenario],
    minimum_size: int = 30,
) -> None:
    """
    Validate the complete question bank.
    """

    if len(scenarios) < minimum_size:
        raise ValueError(
            f"Question bank must contain at least "
            f"{minimum_size} scenarios. "
            f"Found {len(scenarios)}."
        )

    question_ids = [
        scenario.question_id
        for scenario in scenarios
    ]

    if len(question_ids) != len(set(question_ids)):
        raise ValueError(
            "Question bank contains duplicate question IDs."
        )

    for scenario in scenarios:
        validate_scenario(scenario)
