from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import RAW_RESULTS_FILE
from src.data.models import TrialResponse


RESULT_COLUMNS = [
    "participant_id",
    "trial_id",
    "question_id",
    "condition",
    "question_domain",
    "true_probability",
    "human_initial_estimate",
    "ai_estimate",
    "ai_lower_bound",
    "ai_upper_bound",
    "human_final_estimate",
    "initial_decision",
    "final_decision",
    "initial_confidence",
    "final_confidence",
    "followed_ai",
    "changed_estimate",
    "absolute_update",
    "signed_update",
    "ai_influence",
    "initial_decision_correct",
    "final_decision_correct",
    "decision_correct",
    "response_time",
    "timestamp",
]


class CSVStorage:
    """
    CSV-based storage for experiment trial responses.

    This class provides a simple storage interface that can later
    be replaced by SQLite or PostgreSQL without changing the
    experiment logic.
    """

    def __init__(self, path: Path = RAW_RESULTS_FILE) -> None:
        self.path = Path(path)

    def _ensure_directory(self) -> None:
        """Create the parent directory if it does not exist."""
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _response_to_dict(self, response: TrialResponse) -> dict:
        """Convert a TrialResponse into the research dataset schema."""
        return {
            "participant_id": response.participant_id,
            "trial_id": response.trial_id,
            "question_id": response.question_id,
            "condition": response.condition,
            "question_domain": response.question_domain,
            "true_probability": response.true_probability,
            "human_initial_estimate": response.human_initial_estimate,
            "ai_estimate": response.ai_estimate,
            "ai_lower_bound": response.ai_lower_bound,
            "ai_upper_bound": response.ai_upper_bound,
            "human_final_estimate": response.human_final_estimate,
            "initial_decision": response.initial_decision,
            "final_decision": response.final_decision,
            "initial_confidence": response.initial_confidence,
            "final_confidence": response.final_confidence,
            "followed_ai": response.followed_ai,
            "changed_estimate": response.changed_estimate,
            "absolute_update": response.absolute_update,
            "signed_update": response.signed_update,
            "ai_influence": response.ai_influence,
            "initial_decision_correct": response.initial_decision_correct,
            "final_decision_correct": response.final_decision_correct,
            "decision_correct": response.decision_correct,
            "response_time": response.response_time,
            "timestamp": response.timestamp,
        }

    def append_response(self, response: TrialResponse) -> None:
        """
        Append one trial response to the CSV file.

        Existing participant data is preserved.
        Duplicate trial IDs are rejected.
        """
        self._ensure_directory()

        row = self._response_to_dict(response)

        if self.path.exists():
            existing = pd.read_csv(self.path)

            if "trial_id" in existing.columns:
                if response.trial_id in existing["trial_id"].astype(str).values:
                    raise ValueError(
                        f"Trial '{response.trial_id}' already exists."
                    )

        dataframe = pd.DataFrame([row], columns=RESULT_COLUMNS)

        dataframe.to_csv(
            self.path,
            mode="a",
            header=not self.path.exists(),
            index=False,
        )

    def read_all(self) -> pd.DataFrame:
        """
        Read all stored experiment responses.

        Returns an empty DataFrame with the correct schema
        if no data exists yet.
        """
        if not self.path.exists():
            return pd.DataFrame(columns=RESULT_COLUMNS)

        dataframe = pd.read_csv(self.path)

        missing_columns = set(RESULT_COLUMNS) - set(dataframe.columns)

        if missing_columns:
            raise ValueError(
                f"Stored dataset is missing columns: {sorted(missing_columns)}"
            )

        return dataframe[RESULT_COLUMNS]