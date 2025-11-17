def score_calendar(m):

    score = 0

    if m["vtr"] and m["vtr"] > 3:
        score += 2

    if m["em_ratio"] and m["em_ratio"] > 1.1:
        score += 2

    if m["peak_cost_ratio"] and m["peak_cost_ratio"] > 2:
        score += 2

    if m["iv_decay_diff"] > 0:
        score += 1

    if m["dte_ratio"] and 3 <= m["dte_ratio"] <= 6:
        score += 1

    if m["net_gamma"] < 0.005:
        score += 1

    return score
