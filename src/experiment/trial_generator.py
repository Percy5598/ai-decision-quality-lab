from __future__ import annotations

import json
from pathlib import Path

from src.data.models import DecisionScenario, TrialAssignment
from src.data.validation import validate_question_bank
from src.experiment.randomization import build_trial_assignments


DEFAULT_QUESTION_FILE = Path("data/questions.json")


def load_scenarios(
    path: Path = DEFAULT_QUESTION_FILE,
) -> list[DecisionScenario]:
    """
    Load and validate decision scenarios from JSON.

    If a question does not explicitly define a decision threshold,
    the experiment uses 50%.
    """

    if not path.exists():
        raise FileNotFoundError(
            f"Question bank not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        raw_questions = json.load(file)

    scenarios = [
        DecisionScenario(
            question_id=item["question_id"],
            domain=item["domain"],
            title=item["title"],
            scenario_text=item["scenario_text"],
            option_a=item["option_a"],
            option_b=item["option_b"],
            true_probability=float(
                item["true_probability"]
            ),
            decision_threshold=float(
                item.get("decision_threshold", 50.0)
            ),
            ai_estimate=float(
                item["ai_estimate"]
            ),
            ai_lower_bound=float(
                item["ai_lower_bound"]
            ),
            ai_upper_bound=float(
                item["ai_upper_bound"]
            ),
        )
        for item in raw_questions
    ]

    validate_question_bank(scenarios)

    return scenarios


def generate_trials(
    participant_id: str,
    path: Path = DEFAULT_QUESTION_FILE,
) -> tuple[list[DecisionScenario], list[TrialAssignment]]:
    """
    Load the question bank and generate randomized trials
    for one participant.
    """

    scenarios = load_scenarios(path)

    assignments = build_trial_assignments(
        participant_id,
        scenarios,
    )

    return scenarios, assignments