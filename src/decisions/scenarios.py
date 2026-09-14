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
        """
        Calculate the expected monetary value of investing.

        EV =
        probability of success × gain
        -
        probability of failure × loss
        """

        return (
            self.success_probability * self.successful_payoff
            - (1 - self.success_probability) * self.potential_loss
        )

    @property
    def optimal_decision(self) -> str:
        """
        Return the benchmark decision under the
        risk-neutral expected-value model.
        """

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

    DecisionScenario(
        scenario_id="investment_002",
        title="Healthcare Innovation",
        description=(
            "A company is considering funding a new healthcare technology."
        ),
        expected_return=0.15,
        success_probability=0.80,
        potential_loss=150_000,
        investment=500_000,
    ),

    DecisionScenario(
        scenario_id="investment_003",
        title="Green Energy Project",
        description=(
            "A company is considering investing in a renewable energy project."
        ),
        expected_return=0.12,
        success_probability=0.55,
        potential_loss=300_000,
        investment=800_000,
    ),

    DecisionScenario(
        scenario_id="investment_004",
        title="AI Software Platform",
        description=(
            "A company is considering investing in a new AI software platform."
        ),
        expected_return=0.20,
        success_probability=0.65,
        potential_loss=250_000,
        investment=600_000,
    ),

    DecisionScenario(
        scenario_id="investment_005",
        title="Logistics Automation",
        description=(
            "A company is considering investing in an automated logistics system."
        ),
        expected_return=0.10,
        success_probability=0.40,
        potential_loss=250_000,
        investment=700_000,
    ),
]