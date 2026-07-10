"""
health_analyzer.py
------------------
Reads sample_data/health_data.csv and returns a summary dictionary with:
  - Averages for Sleep_Hours, Resting_Heart_Rate, HRV, Steps
  - Trend direction for Sleep_Hours and Resting_Heart_Rate
  - Recovery Score (0-100)
  - Wellness Score (0-100)

No AI is used. All logic is deterministic.
"""

import pandas as pd
import numpy as np


CSV_PATH = "sample_data/health_data.csv"

# ── Reference ranges used for scoring ────────────────────────────────────────
# Sleep: 7–9 h is optimal (National Sleep Foundation)
SLEEP_OPTIMAL_MIN = 7.0
SLEEP_OPTIMAL_MAX = 9.0
SLEEP_ABS_MIN = 4.0      # floor: below this scores 0
SLEEP_ABS_MAX = 10.0     # ceiling: above this scores 0 (oversleeping)

# Resting HR: lower is generally better; 40–60 elite, 60–100 normal
RHR_BEST = 50            # score of 100
RHR_WORST = 100          # score of 0

# HRV: higher is better; 20 ms floor → 100 ms ceiling
HRV_BEST = 100
HRV_WORST = 20

# Steps: 10 000 steps/day is widely cited as a healthy target
STEPS_TARGET = 10_000
STEPS_FLOOR = 0
STEPS_MAX = 20_000       # cap for normalisation


def _linear_score(value: float, best: float, worst: float) -> float:
    """Return a 0-100 score where `best` maps to 100 and `worst` maps to 0."""
    if best == worst:
        return 100.0
    score = (value - worst) / (best - worst) * 100.0
    return float(np.clip(score, 0.0, 100.0))


def _sleep_score(hours: float) -> float:
    """
    Tent function: peaks at the midpoint of the optimal range.
    Falls linearly on both sides to the absolute min/max.
    """
    midpoint = (SLEEP_OPTIMAL_MIN + SLEEP_OPTIMAL_MAX) / 2.0
    if SLEEP_OPTIMAL_MIN <= hours <= SLEEP_OPTIMAL_MAX:
        # Inside optimal band — how close to midpoint
        deviation = abs(hours - midpoint) / ((SLEEP_OPTIMAL_MAX - SLEEP_OPTIMAL_MIN) / 2.0)
        return float(np.clip(100.0 - deviation * 10.0, 90.0, 100.0))
    elif hours < SLEEP_OPTIMAL_MIN:
        return float(np.clip((hours - SLEEP_ABS_MIN) / (SLEEP_OPTIMAL_MIN - SLEEP_ABS_MIN) * 100.0, 0.0, 100.0))
    else:
        return float(np.clip((SLEEP_ABS_MAX - hours) / (SLEEP_ABS_MAX - SLEEP_OPTIMAL_MAX) * 100.0, 0.0, 100.0))


def _trend(series: pd.Series) -> str:
    """
    Fit a 1-degree polynomial (least-squares) over ordinal indices.
    Returns 'increasing', 'decreasing', or 'stable' based on the slope.
    """
    if len(series) < 2:
        return "stable"
    x = np.arange(len(series), dtype=float)
    y = series.to_numpy(dtype=float)
    slope = float(np.polyfit(x, y, 1)[0])
    # Threshold: < 1 % of the mean per day is treated as stable
    threshold = abs(y.mean()) * 0.01 if y.mean() != 0 else 0.01
    if slope > threshold:
        return "increasing"
    elif slope < -threshold:
        return "decreasing"
    return "stable"


def analyze(csv_path: str = CSV_PATH) -> dict:
    """
    Read the CSV and return a summary dictionary.

    Returns
    -------
    dict with keys:
        averages, trends, recovery_score, wellness_score, row_count
    """
    df = pd.read_csv(csv_path, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    # ── Averages ──────────────────────────────────────────────────────────────
    avg_sleep = float(df["Sleep_Hours"].mean())
    avg_rhr   = float(df["Resting_Heart_Rate"].mean())
    avg_hrv   = float(df["HRV"].mean())
    avg_steps = float(df["Steps"].mean())

    # ── Trends ────────────────────────────────────────────────────────────────
    sleep_trend = _trend(df["Sleep_Hours"])
    rhr_trend   = _trend(df["Resting_Heart_Rate"])

    # ── Recovery Score (Sleep 40 %, HRV 40 %, RHR 20 %) ─────────────────────
    s_sleep    = _sleep_score(avg_sleep)
    s_hrv      = _linear_score(avg_hrv,   best=HRV_BEST,  worst=HRV_WORST)
    s_rhr      = _linear_score(avg_rhr,   best=RHR_BEST,  worst=RHR_WORST)
    recovery_score = round(0.40 * s_sleep + 0.40 * s_hrv + 0.20 * s_rhr, 1)

    # ── Wellness Score (Recovery 50 %, Steps 50 %) ───────────────────────────
    s_steps = _linear_score(avg_steps, best=STEPS_MAX, worst=STEPS_FLOOR)
    # Normalise steps against a realistic target rather than the absolute max
    s_steps_targeted = float(np.clip(avg_steps / STEPS_TARGET * 100.0, 0.0, 100.0))
    wellness_score = round(0.50 * recovery_score + 0.50 * s_steps_targeted, 1)

    return {
        "row_count": int(len(df)),
        "averages": {
            "Sleep_Hours":          round(avg_sleep, 2),
            "Resting_Heart_Rate":   round(avg_rhr,   2),
            "HRV":                  round(avg_hrv,   2),
            "Steps":                round(avg_steps, 1),
        },
        "trends": {
            "Sleep_Hours":          sleep_trend,
            "Resting_Heart_Rate":   rhr_trend,
        },
        "recovery_score":  recovery_score,
        "wellness_score":  wellness_score,
    }


if __name__ == "__main__":
    import json
    result = analyze()
    print(json.dumps(result, indent=2))
