from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Scenario:
    scenario_id: int
    title: str
    context: str
    question: str

    option_a: str
    option_b: str

    probability_a: float
    probability_b: float

    payoff_a: float
    payoff_b: float

    ai_recommendation: str
    ai_confidence: float
    ai_reasoning: str

    correct_option: str


SCENARIOS: List[Scenario] = [
    Scenario(
        scenario_id=1,
        title="Investment A vs B",
        context=(
            "You are considering two investments for a one-year period. "
            "Investment A has a 70% probability of returning €1,200 and a "
            "30% probability of returning €600. Investment B has a 90% "
            "probability of returning €1,000 and a 10% probability of "
            "returning €700."
        ),
        question="Which investment would you choose?",
        option_a="Investment A",
        option_b="Investment B",
        probability_a=0.70,
        probability_b=0.90,
        payoff_a=1200,
        payoff_b=1000,
        ai_recommendation="Investment A",
        ai_confidence=0.78,
        ai_reasoning=(
            "Investment A has a higher expected monetary value based on "
            "the stated probabilities and payoffs."
        ),
        correct_option="A",
    ),

    Scenario(
        scenario_id=2,
        title="Project X vs Y",
        context=(
            "A company is choosing between two projects. Project X has a "
            "60% chance of generating €2,000 and a 40% chance of generating "
            "€500. Project Y has an 80% chance of generating €1,400 and a "
            "20% chance of generating €900."
        ),
        question="Which project would you choose?",
        option_a="Project X",
        option_b="Project Y",
        probability_a=0.60,
        probability_b=0.80,
        payoff_a=2000,
        payoff_b=1400,
        ai_recommendation="Project X",
        ai_confidence=0.71,
        ai_reasoning=(
            "Project X provides the higher expected monetary value, although "
            "its outcome is less certain."
        ),
        correct_option="A",
    ),

    Scenario(
        scenario_id=3,
        title="Savings Option",
        context=(
            "You can place €10,000 in either Account A or Account B. "
            "Account A has a 95% probability of producing a €700 gain. "
            "Account B has a 65% probability of producing a €1,200 gain."
        ),
        question="Which account would you choose?",
        option_a="Account A",
        option_b="Account B",
        probability_a=0.95,
        probability_b=0.65,
        payoff_a=700,
        payoff_b=1200,
        ai_recommendation="Account A",
        ai_confidence=0.62,
        ai_reasoning=(
            "Account A provides a lower potential gain but considerably "
            "greater probability of achieving that gain."
        ),
        correct_option="A",
    ),

    Scenario(
        scenario_id=4,
        title="Technology Investment",
        context=(
            "A technology company is considering two investments. "
            "Investment A has a 40% chance of returning €3,000 and a 60% "
            "chance of returning €500. Investment B has a 75% chance of "
            "returning €1,500 and a 25% chance of returning €800."
        ),
        question="Which investment would you choose?",
        option_a="Investment A",
        option_b="Investment B",
        probability_a=0.40,
        probability_b=0.75,
        payoff_a=3000,
        payoff_b=1500,
        ai_recommendation="Investment B",
        ai_confidence=0.68,
        ai_reasoning=(
            "Investment B offers a more predictable outcome, although the "
            "expected monetary values are relatively close."
        ),
        correct_option="B",
    ),

    Scenario(
        scenario_id=5,
        title="Business Expansion",
        context=(
            "A small company can expand into Market A or Market B. "
            "Market A has a 55% probability of producing €5,000 profit "
            "and a 45% probability of producing €1,000 profit. "
            "Market B has a 75% probability of producing €3,500 profit "
            "and a 25% probability of producing €1,500 profit."
        ),
        question="Which market would you enter?",
        option_a="Market A",
        option_b="Market B",
        probability_a=0.55,
        probability_b=0.75,
        payoff_a=5000,
        payoff_b=3500,
        ai_recommendation="Market A",
        ai_confidence=0.73,
        ai_reasoning=(
            "Market A has the higher expected monetary value despite having "
            "greater uncertainty."
        ),
        correct_option="A",
    ),

    Scenario(
        scenario_id=6,
        title="Loan Choice",
        context=(
            "You need to choose between two lending opportunities. "
            "Option A has a 90% chance of producing a €900 return. "
            "Option B has a 60% chance of producing a €1,600 return."
        ),
        question="Which option would you choose?",
        option_a="Option A",
        option_b="Option B",
        probability_a=0.90,
        probability_b=0.60,
        payoff_a=900,
        payoff_b=1600,
        ai_recommendation="Option A",
        ai_confidence=0.66,
        ai_reasoning=(
            "Option A offers a substantially higher probability of achieving "
            "a positive return."
        ),
        correct_option="A",
    ),

    Scenario(
        scenario_id=7,
        title="Startup Investment",
        context=(
            "Startup A has a 25% probability of generating €10,000 and a "
            "75% probability of generating €1,000. Startup B has a 70% "
            "probability of generating €3,000 and a 30% probability of "
            "generating €1,500."
        ),
        question="Which startup would you invest in?",
        option_a="Startup A",
        option_b="Startup B",
        probability_a=0.25,
        probability_b=0.70,
        payoff_a=10000,
        payoff_b=3000,
        ai_recommendation="Startup B",
        ai_confidence=0.69,
        ai_reasoning=(
            "Startup B provides a more predictable return and lower downside "
            "uncertainty."
        ),
        correct_option="B",
    ),

    Scenario(
        scenario_id=8,
        title="Portfolio Allocation",
        context=(
            "Portfolio A has a 50% chance of returning €2,500 and a 50% "
            "chance of returning €800. Portfolio B has an 80% chance of "
            "returning €1,700 and a 20% chance of returning €1,000."
        ),
        question="Which portfolio would you choose?",
        option_a="Portfolio A",
        option_b="Portfolio B",
        probability_a=0.50,
        probability_b=0.80,
        payoff_a=2500,
        payoff_b=1700,
        ai_recommendation="Portfolio A",
        ai_confidence=0.64,
        ai_reasoning=(
            "Portfolio A has a higher expected monetary value but also "
            "contains greater outcome uncertainty."
        ),
        correct_option="A",
    ),

    Scenario(
        scenario_id=9,
        title="Energy Project",
        context=(
            "Energy Project A has a 65% probability of generating €4,000 "
            "and a 35% probability of generating €500. Energy Project B "
            "has an 85% probability of generating €2,800 and a 15% "
            "probability of generating €1,000."
        ),
        question="Which energy project would you choose?",
        option_a="Project A",
        option_b="Project B",
        probability_a=0.65,
        probability_b=0.85,
        payoff_a=4000,
        payoff_b=2800,
        ai_recommendation="Project A",
        ai_confidence=0.74,
        ai_reasoning=(
            "Project A has the higher expected monetary value despite "
            "greater variability in possible outcomes."
        ),
        correct_option="A",
    ),

    Scenario(
        scenario_id=10,
        title="Final Investment",
        context=(
            "Investment A has a 30% probability of producing €5,000 and a "
            "70% probability of producing €700. Investment B has a 75% "
            "probability of producing €2,000 and a 25% probability of "
            "producing €900."
        ),
        question="Which investment would you choose?",
        option_a="Investment A",
        option_b="Investment B",
        probability_a=0.30,
        probability_b=0.75,
        payoff_a=5000,
        payoff_b=2000,
        ai_recommendation="Investment B",
        ai_confidence=0.70,
        ai_reasoning=(
            "Investment B offers a substantially more predictable outcome "
            "with a competitive expected return."
        ),
        correct_option="B",
    ),
]


def get_scenarios() -> List[Scenario]:
    """Return all available scenarios."""
    return SCENARIOS.copy()


def get_scenario(scenario_id: int) -> Scenario:
    """Return a scenario by ID."""
    for scenario in SCENARIOS:
        if scenario.scenario_id == scenario_id:
            return scenario

    raise ValueError(f"Scenario {scenario_id} does not exist.")
