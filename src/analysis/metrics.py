"""
Research metrics for the AI Decision Quality Lab.

These functions contain the mathematical definitions of the
experiment's dependent variables.

The functions are deliberately small and independent of Streamlit
so they can later be reused in notebooks, statistical analysis,
or a research pipeline.
"""

from typing import Optional


def signed_update(
    initial_estimate: float,
    final_estimate: float,
) -> float:
    """
    Calculate the directional change in a participant's belief.

    Positive value:
        participant increased their estimate.

    Negative value:
        participant decreased their estimate.

    Zero:
        participant did not change their estimate.
    """

    return final_estimate - initial_estimate


def absolute_update(
    initial_estimate: float,
    final_estimate: float,
) -> float:
    """
    Calculate the magnitude of belief updating.

    Unlike signed_update(), this ignores direction.
    """

    return abs(
        final_estimate - initial_estimate
    )


def ai_influence(
    initial_estimate: float,
    final_estimate: float,
    ai_estimate: Optional[float],
) -> Optional[float]:
    """
    Calculate how strongly the participant moved toward
    the AI estimate.

    Formula:

        |final - initial|
        -----------------
        |AI - initial|

    Returns None when there is no meaningful AI comparison,
    such as a human-only trial.

    Returns 0 when the participant did not move.

    Returns 1 when the participant moved exactly to the AI estimate.

    Values greater than 1 indicate movement beyond the AI estimate.
    """

    if ai_estimate is None:
        return None

    denominator = abs(
        ai_estimate - initial_estimate
    )

    if denominator == 0:
        return 0.0

    numerator = abs(
        final_estimate - initial_estimate
    )

    return numerator / denominator


def decision_is_correct(
    decision: str,
    correct_decision: str,
) -> bool:
    """
    Check whether the participant's decision matches
    the known correct decision.
    """

    return decision == correct_decision
    
def decision_from_probability(
    true_probability: float,
    decision_threshold: float = 50.0,
) -> str:
    """
    Convert a probability into the objectively correct
    binary decision using the scenario threshold.
    """

    if true_probability >= decision_threshold:
        return "option_a"

    return "option_b"

def calibration_error(
    confidence: float,
    correct: bool,
) -> float:
    """
    Calculate absolute calibration error.

    A correct answer has target confidence = 100.
    An incorrect answer has target confidence = 0.

    Therefore:

        correct + 80% confidence
            -> error = 20

        incorrect + 80% confidence
            -> error = 80
    """

    target = 100.0 if correct else 0.0

    return abs(
        confidence - target
    )


def confidence_adjusted_accuracy(
    confidence: float,
    correct: bool,
) -> float:
    """
    Return confidence as a signed correctness-weighted value.

    Correct:
        +confidence

    Incorrect:
        -confidence

    This is useful for descriptive analysis but should not replace
    proper calibration analysis.
    """

    if correct:
        return confidence

    return -confidence


def followed_ai(
    initial_decision: str,
    final_decision: str,
    ai_decision: Optional[str],
) -> Optional[bool]:
    """
    Determine whether the participant's final decision matches
    the AI recommendation.

    This measure is only meaningful when AI advice was shown.
    """

    if ai_decision is None:
        return None

    return final_decision == ai_decision


def changed_decision(
    initial_decision: str,
    final_decision: str,
) -> bool:
    """
    Determine whether the participant changed their decision
    after receiving AI information.
    """

    return initial_decision != final_decision


def ai_was_correct(
    ai_estimate: Optional[float],
    true_probability: float,
    decision_threshold: float = 50.0,
) -> Optional[bool]:
    """
    Determine whether the AI recommendation corresponds to
    the ground-truth decision.

    The AI recommendation is:

        option A if AI estimate >= threshold
        option B otherwise.

    The ground-truth decision is:

        option A if true probability >= threshold
        option B otherwise.
    """

    if ai_estimate is None:
        return None

    true_decision_a = (
        true_probability >= decision_threshold
    )

    ai_decision_a = (
        ai_estimate >= decision_threshold
    )

    return true_decision_a == ai_decision_a

def over_reliance(
    followed_ai_value: Optional[bool],
    ai_correct: Optional[bool],
) -> Optional[bool]:
    """
    Identify potential over-reliance.

    Over-reliance occurs when the participant follows an incorrect
    AI recommendation.
    """

    if (
        followed_ai_value is None
        or ai_correct is None
    ):
        return None

    return (
        followed_ai_value
        and not ai_correct
    )


def under_reliance(
    followed_ai_value: Optional[bool],
    ai_correct: Optional[bool],
) -> Optional[bool]:
    """
    Identify potential under-reliance.

    Under-reliance occurs when the participant does not follow
    a correct AI recommendation.
    """

    if (
        followed_ai_value is None
        or ai_correct is None
    ):
        return None

    return (
        not followed_ai_value
        and ai_correct
    )
def correct_decision(
    true_probability: float,
    decision_threshold: float = 50.0,
) -> str:
    """
    Convert ground-truth probability into the researcher-defined
    correct decision.

    This prototype uses option A for probabilities at or above
    the threshold and option B otherwise.

    The returned value is a symbolic label. The scenario's actual
    option text is handled by the experiment UI.
    """

    if true_probability >= decision_threshold:
        return "option_a"

    return "option_b"

def ai_decision(
    ai_estimate: Optional[float],
    decision_threshold: float = 50.0,
) -> Optional[str]:
    """
    Convert the AI probability estimate into its implied decision.
    """

    if ai_estimate is None:
        return None

    if ai_estimate >= decision_threshold:
        return "option_a"

    return "option_b"        

def decision_from_estimate(
    estimate: float,
    decision_threshold: float = 50.0,
) -> str:
    """
    Convert a probability estimate into the corresponding decision.

    Estimates at or above the threshold map to option_a.
    Estimates below the threshold map to option_b.
    """

    if estimate >= decision_threshold:
        return "option_a"

    return "option_b"