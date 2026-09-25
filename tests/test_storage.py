from pathlib import Path

import pandas as pd
import pytest

from src.data.models import TrialResponse
from src.data.storage import CSVStorage, RESULT_COLUMNS


def make_response(trial_id: str = "participant_trial_01") -> TrialResponse:
    return TrialResponse(
        participant_id="participant_001",
        trial_id=trial_id,
        question_id="finance_001",
        condition="ai_point_estimate",
        question_domain="finance",
        true_probability=70.0,
        human_initial_estimate=55.0,
        ai_estimate=72.0,
        ai_lower_bound=None,
        ai_upper_bound=None,
        human_final_estimate=65.0,
        initial_decision="option_a",
        final_decision="option_a",
        initial_confidence=60.0,
        final_confidence=70.0,
        followed_ai=True,
        changed_estimate=True,
        absolute_update=10.0,
        signed_update=10.0,
        ai_influence=0.588,
        initial_decision_correct=True,
        final_decision_correct=True,
        decision_correct=True,
        response_time=4.2,
        timestamp="2026-09-24T12:00:00",
    )


def test_append_creates_file(tmp_path: Path):
    path = tmp_path / "experiment_results.csv"

    storage = CSVStorage(path)

    response = make_response()

    storage.append_response(response)

    assert path.exists()


def test_append_preserves_previous_responses(tmp_path: Path):
    path = tmp_path / "experiment_results.csv"

    storage = CSVStorage(path)

    storage.append_response(
        make_response("participant_trial_01")
    )

    storage.append_response(
        make_response("participant_trial_02")
    )

    dataframe = storage.read_all()

    assert len(dataframe) == 2
    assert dataframe.iloc[0]["trial_id"] == "participant_trial_01"
    assert dataframe.iloc[1]["trial_id"] == "participant_trial_02"


def test_duplicate_trial_is_rejected(tmp_path: Path):
    path = tmp_path / "experiment_results.csv"

    storage = CSVStorage(path)

    response = make_response()

    storage.append_response(response)

    with pytest.raises(ValueError):
        storage.append_response(response)


def test_dataset_has_expected_columns(tmp_path: Path):
    path = tmp_path / "experiment_results.csv"

    storage = CSVStorage(path)

    storage.append_response(make_response())

    dataframe = storage.read_all()

    assert list(dataframe.columns) == RESULT_COLUMNS


def test_empty_storage_has_expected_schema(tmp_path: Path):
    path = tmp_path / "experiment_results.csv"

    storage = CSVStorage(path)

    dataframe = storage.read_all()

    assert isinstance(dataframe, pd.DataFrame)
    assert list(dataframe.columns) == RESULT_COLUMNS
    assert dataframe.empty