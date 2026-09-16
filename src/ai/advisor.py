from dataclasses import dataclass

from src.decisions.scenarios import Scenario


@dataclass(frozen=True)
class Advice:
    recommendation: str
    confidence: float
    reasoning: str


def generate_advice(scenario: Scenario) -> Advice:
    """
    Return controlled AI advice for the experimental scenario.

    The advisor is deterministic so that experimental conditions remain
    reproducible and comparable.
    """

    return Advice(
        recommendation=scenario.ai_recommendation,
        confidence=scenario.ai_confidence,
        reasoning=scenario.ai_reasoning,
    )


def format_advice(advice: Advice) -> str:
    """Format AI advice for display in the Streamlit application."""

    return (
        f"**AI recommendation:** {advice.recommendation}\n\n"
        f"**AI confidence:** {advice.confidence:.0%}\n\n"
        f"**AI reasoning:** {advice.reasoning}"
    )