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

    @property
    def successful_payoff(self) -> float:
        """Return the monetary gain if the investment succeeds."""
        return self.investment * self.expected_return

    @property
    def expected_value(self) -> float:
        """Calculate the expected monetary value of investing."""

        return (
            self.success_probability * self.successful_payoff
            - (1 - self.success_probability) * self.potential_loss
        )

    @property
    def optimal_decision(self) -> str:
        """Return the economically optimal decision."""

        if self.expected_value > 0:
            return "Invest"

        return "Do not invest"


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