from dataclasses import dataclass


@dataclass
class DecisionScenario:
    scenario_id: str
    title: str
    description: str
    expected_return: float
    success_probability: float
    potential_loss: float
    investment: float


SCENARIOS = [
    DecisionScenario(
        scenario_id="investment_001",
        title="Technology Investment",
        description=(
            "A company is considering investing in a new technology project."
        ),
        expected_return=0.08,
        success_probability=0.70,
        potential_loss=200_000,
        investment=1_000_000,
    ),
]