def score_calendar(metrics):
    score = 0

    # Weighting logic
    if metrics["vtr"] and metrics["vtr"] > 3:
        score += 2
    elif metrics["vtr"] > 1:
        score += 1

    if metrics["em_ratio"] and metrics["em_ratio"] > 1.1:
        score += 2

    if metrics["peak_cost_ratio"] and metrics["peak_cost_ratio"] > 2:
        score += 2

    if metrics["iv_decay_diff"] > 0:
        score += 1

    if metrics["dte_ratio"] and 3 <= metrics["dte_ratio"] <= 6:
        score += 1

    if metrics["net_gamma"] < 0.005:
        score += 1

    return score

