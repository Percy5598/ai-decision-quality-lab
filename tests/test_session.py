from src.analysis.metrics import decision_from_estimate


def test_decision_from_estimate_above_threshold():
    assert decision_from_estimate(72.0, 50.0) == "option_a"


def test_decision_from_estimate_below_threshold():
    assert decision_from_estimate(42.0, 50.0) == "option_b"


def test_decision_from_estimate_at_threshold():
    assert decision_from_estimate(50.0, 50.0) == "option_a"
    