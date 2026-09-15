import csv
from dataclasses import asdict
from pathlib import Path

from src.experiment.experiment import DecisionRecord


DATA_FILE = Path("data/raw/decisions.csv")


def save_decision(record: DecisionRecord) -> None:
    """
    Append one trial record to the experiment CSV.
    """

    DATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    row = asdict(record)

    # Convert Enum to its underlying string value.
    row["condition"] = record.condition.value

    file_exists = DATA_FILE.exists()

    with DATA_FILE.open(
        mode="a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=row.keys(),
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)