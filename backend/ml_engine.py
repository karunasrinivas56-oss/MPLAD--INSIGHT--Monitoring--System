"""
ML Engine module for MPLAD Management System
Analyzes project budget and timeline parameters to evaluate process delays,
cost overruns, and detect anomalies/risks.
"""


def evaluate_process_delays(
    timeline_months: int,
    actual_months: int,
    estimated_budget: float,
    actual_expenditure: float
) -> dict:
    """
    Evaluates project execution metrics to detect financial anomalies and timeline delays.
    Returns anomaly flag, risk metrics, score, and detailed reasons.
    """
    cost_overrun_ratio = actual_expenditure / max(estimated_budget, 1.0)
    time_delay_ratio = actual_months / max(timeline_months, 1)

    reasons = []

    # 1. Cost overrun checks
    if cost_overrun_ratio >= 1.5:
        reasons.append(f"Severe Expenditure Overrun ({cost_overrun_ratio:.2f}x)")
    elif cost_overrun_ratio >= 1.25:
        reasons.append(f"Moderate Cost Overrun ({cost_overrun_ratio:.2f}x)")

    # 2. Time delay checks
    if time_delay_ratio >= 1.4:
        reasons.append(f"Critical Timeline Delay ({time_delay_ratio:.2f}x)")
    elif time_delay_ratio >= 1.2:
        reasons.append(f"Moderate Timeline Delay ({time_delay_ratio:.2f}x)")

    # 3. Anomaly detection flag
    is_anomaly = 1 if (cost_overrun_ratio >= 1.25 or time_delay_ratio >= 1.3) else 0

    # 4. Calculate Risk Score (Normalized 0 to 100)
    risk_score = round(
        min(
            100.0,
            ((cost_overrun_ratio - 1.0) * 40 + (time_delay_ratio - 1.0) * 40)
        ),
        2
    )
    risk_score = max(0.0, risk_score)

    # 5. Determine Risk Level
    if risk_score >= 60.0 or is_anomaly == 1:
        risk_level = "High"
    elif risk_score >= 30.0:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "anomaly_flag": is_anomaly,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": " | ".join(reasons) if reasons else "Compliant Progress",
        "cost_ratio": round(cost_overrun_ratio, 2),
        "time_ratio": round(time_delay_ratio, 2)
    }