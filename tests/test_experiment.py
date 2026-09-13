from src.decisions.scenarios import SCENARIOS
from src.experiment.experiment import (
    DecisionRecord,
    ExperimentCondition,
    assign_condition,
)


def test_scenario_exists():
    assert len(SCENARIOS) > 0


def test_scenario_probability():
    scenario = SCENARIOS[0]

    assert 0 <= scenario.success_probability <= 1


def test_decision_record():
    record = DecisionRecord(
        participant_id="test_001",
        scenario_id="investment_001",
        condition=ExperimentCondition.HUMAN_ONLY,
        initial_decision=None,
        initial_confidence=None,
        ai_recommendation=None,
        ai_confidence=None,
        final_decision="Invest",
        final_confidence=80,
    )

    assert record.final_decision == "Invest"
    assert record.final_confidence == 80


def test_condition_assignment():
    condition = assign_condition()

    assert condition in list(ExperimentCondition)