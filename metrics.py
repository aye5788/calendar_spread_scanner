import numpy as np

def compute_calendar_metrics(short_opt, long_opt, core):
    """
    Compute calendar spread greeks, extrinsic, ratios, IV structure metrics,
    and everything needed for scoring.

    All fields + logic verified directly against ORATS Delayed Data format.
    """

    # -------------------------------
    # Greeks (ORATS gives call greeks only)
    # -------------------------------
    net_vega = long_opt["vega"] - short_opt["vega"]
    net_theta = long_opt["theta"] - short_opt["theta"]
    net_delta = long_opt["delta"] - short_opt["delta"]
    net_gamma = long_opt["gamma"] - short_opt["gamma"]

    # -------------------------------
    # DTE ratio (avoid division by zero)
    # -------------------------------
    try:
        dte_ratio = long_opt["dte"] / short_opt["dte"]
    except Exception:
        dte_ratio = np.nan

    # -------------------------------
    # CALL midprice helper
    # -------------------------------
    def call_mid(o):
        return (o["callBidPrice"] + o["callAskPrice"]) / 2

    short_mid = call_mid(short_opt)
    long_mid  = call_mid(long_opt)
    debit = long_mid - short_mid

    # -------------------------------
    # Extrinsic Value (CALL)
    # -------------------------------
    def extrinsic_call(o):
        intrinsic = max(o["spotPrice"] - o["strike"], 0)
        return call_mid(o) - intrinsic

    extr_short = extrinsic_call(short_opt)
    extr_long  = extrinsic_call(long_opt)

    if extr_long > 0:
        extr_ratio = extr_short / extr_long
    else:
        extr_ratio = np.nan

    # -------------------------------
    # Vega / Theta ratio
    # -------------------------------
    vtr = abs(net_vega) / abs(net_theta) if net_theta != 0 else np.nan

    # -------------------------------
    # IV term structure (core)
    # -------------------------------
    iv_front = core.get("iv20d", np.nan)
    iv_back  = core.get("iv60d", np.nan)
    iv_decay_diff = iv_front - iv_back if iv_front is not None and iv_back is not None else np.nan

    # -------------------------------
    # Earnings implied move proxy
    # core does NOT have "impliedMove" but has:
    #   "impliedEarningsMove"
    # We use that as a proxy if present.
    # -------------------------------
    implied_move = core.get("impliedEarningsMove", np.nan)

    if implied_move and implied_move > 0:
        breakeven_width = implied_move * 0.90
        em_ratio = breakeven_width / implied_move
    else:
        breakeven_width = np.nan
        em_ratio = np.nan

    # -------------------------------
    # Peak / Cost ratio
    # -------------------------------
    peak_cost_ratio = extr_short / debit if debit not in [0, None] else np.nan

    # -------------------------------
    # RETURN DICT
    # -------------------------------
    return {
        "strike": short_opt["strike"],
        "short_exp": short_opt["expirDate"],
        "long_exp": long_opt["expirDate"],

        "net_vega": net_vega,
        "net_theta": net_theta,
        "net_gamma": net_gamma,
        "net_delta": net_delta,

        "dte_ratio": dte_ratio,
        "extr_ratio": extr_ratio,
        "vtr": vtr,

        "iv_front": iv_front,
        "iv_back": iv_back,
        "iv_decay_diff": iv_decay_diff,

        "implied_move": implied_move,
        "breakeven_width": breakeven_width,
        "em_ratio": em_ratio,

        "debit": debit,
        "peak_cost_ratio": peak_cost_ratio,
    }

