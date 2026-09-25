"""
Tests for research metrics.
"""

from src.analysis.metrics import (
    absolute_update,
    ai_influence,
    ai_was_correct,
    calibration_error,
    changed_decision,
    decision_is_correct,
    over_reliance,
    signed_update,
    under_reliance,
)


def test_signed_update_positive():
    assert signed_update(40, 60) == 20


def test_signed_update_negative():
    assert signed_update(70, 50) == -20


def test_signed_update_zero():
    assert signed_update(50, 50) == 0


def test_absolute_update():
    assert absolute_update(70, 40) == 30


def test_ai_influence_half():
    result = ai_influence(
        initial_estimate=50,
        final_estimate=70,
        ai_estimate=90,
    )

    assert result == 0.5


def test_ai_influence_no_ai():
    assert (
        ai_influence(
            50,
            70,
            None,
        )
        is None
    )


def test_ai_influence_zero_distance():
    assert (
        ai_influence(
            50,
            50,
            50,
        )
        == 0.0
    )


def test_decision_correct():
    assert decision_is_correct(
        "Invest",
        "Invest",
    )


def test_decision_incorrect():
    assert not decision_is_correct(
        "Invest",
        "Do not invest",
    )


def test_calibration_correct():
    assert calibration_error(
        confidence=80,
        correct=True,
    ) == 20


def test_calibration_incorrect():
    assert calibration_error(
        confidence=80,
        correct=False,
    ) == 80


def test_followed_ai():
    from src.analysis.metrics import followed_ai

    assert followed_ai(
        "Invest",
        "Invest",
        "Invest",
    )


def test_rejected_ai():
    from src.analysis.metrics import followed_ai

    assert not followed_ai(
        "Invest",
        "Do not invest",
        "Invest",
    )


def test_changed_decision():
    assert changed_decision(
        "Invest",
        "Do not invest",
    )


def test_unchanged_decision():
    assert not changed_decision(
        "Invest",
        "Invest",
    )


def test_correct_ai():
    assert ai_was_correct(
        ai_estimate=70,
        true_probability=75,
        decision_threshold=50,
    )


def test_incorrect_ai():
    assert not ai_was_correct(
        ai_estimate=40,
        true_probability=75,
        decision_threshold=50,
    )


def test_over_reliance():
    assert over_reliance(
        followed_ai_value=True,
        ai_correct=False,
    )


def test_not_over_reliance():
    assert not over_reliance(
        followed_ai_value=True,
        ai_correct=True,
    )


def test_under_reliance():
    assert under_reliance(
        followed_ai_value=False,
        ai_correct=True,
    )


def test_not_under_reliance():
    assert not under_reliance(
        followed_ai_value=True,
        ai_correct=True,
    )
