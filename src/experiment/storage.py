import csv
from dataclasses import asdict
from pathlib import Path

from src.experiment.experiment import DecisionRecord


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "raw"

DATA_FILE = DATA_DIR / "decisions.csv"


def ensure_data_directory():
    """Create the data directory if it does not exist."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_decision(record: DecisionRecord):
    """
    Append one decision record to the CSV dataset.
    """

    ensure_data_directory()

    record_data = asdict(record)

    file_exists = DATA_FILE.exists()

    with DATA_FILE.open(
        mode="a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=record_data.keys(),
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(record_data)


def get_data_file() -> Path:
    """Return the location of the experiment dataset."""

    ensure_data_directory()

    return DATA_FILE