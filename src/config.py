"""
Experiment configuration.

Centralizes research-design parameters so that the experimental
protocol is not hard-coded throughout the Streamlit application.
"""

TOTAL_TRIALS = 20

PRACTICE_TRIALS = 3

RANDOMIZATION_SEED_VERSION = "v1"

CONDITION_HUMAN_ONLY = "human_only"
CONDITION_AI_POINT = "ai_point_estimate"
CONDITION_AI_UNCERTAINTY = "ai_uncertainty"

CONDITIONS = (
    CONDITION_HUMAN_ONLY,
    CONDITION_AI_POINT,
    CONDITION_AI_UNCERTAINTY,
)

# Target allocation for 20 experimental trials.
#
# Human only:       7
# AI point:         7
# AI uncertainty:  6
#
# The exact order is randomized for every participant.
CONDITION_COUNTS = {
    CONDITION_HUMAN_ONLY: 7,
    CONDITION_AI_POINT: 7,
    CONDITION_AI_UNCERTAINTY: 6,
}

MIN_QUESTION_BANK_SIZE = 30

PROBABILITY_MIN = 0.0
PROBABILITY_MAX = 100.0

CONFIDENCE_MIN = 0.0
CONFIDENCE_MAX = 100.0

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

RAW_RESULTS_FILE = RAW_DATA_DIR / "experiment_results.csv"
PROCESSED_RESULTS_FILE = PROCESSED_DATA_DIR / "trial_level.csv"