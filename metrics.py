import numpy as np

def compute_calendar_metrics(short_opt, long_opt, core):
    # -------------------------------
    # Greeks (CALLS)
    # -------------------------------
    net_vega = long_opt["vega"] - short_opt["vega"]
    net_theta = long_opt["theta"] - short_opt["theta"]
    net_delta = long_opt["delta"] - short_opt["delta"]
    net_gamma = long_opt["gamma"] - short_opt["gamma"]

    # -------------------------------
    # DTE Ratio
    # -------------------------------
    dte_ratio = long_opt["dte"] / short_opt["dte"] if short_opt["dte"] > 0 else np.nan

    # -------------------------------
    # Mid prices (CALL)
    # -------------------------------
    short_mid = (short_opt["callBidPrice"] + short_opt["callAskPrice"]) / 2
    long_mid  = (long_opt["callBidPrice"]  + long_opt["callAskPrice"])  / 2

    debit = long_mid - short_mid

    # -------------------------------
    # Extrinsic Values
    # -------------------------------
    def extrinsic_call(o):
        intrinsic = max(o["spotPrice"] - o["strike"], 0)
        mid = (o["callBidPrice"] + o["callAskPrice"]) / 2
        return mid - intrinsic

    extr_short = extrinsic_call(short_opt)
    extr_long  = extrinsic_call(long_opt)

    extr_ratio = extr_short / extr_long if extr_long > 0 else np.nan

    # -------------------------------
    # Vega / Theta ratio
    # -------------------------------
    vtr = abs(net_vega) / abs(net_theta) if net_theta != 0 else np.nan

    # -------------------------------
    # IV decay differential (front vs back)
    # -------------------------------
    iv_front = core.get("iv20d", np.nan)
    iv_back  = core.get("iv60d", np.nan)
    iv_decay_diff = iv_front - iv_back

    # -------------------------------
    # Implied move ratio
    # -------------------------------
    implied_move = core.get("impliedMove", np.nan)
    breakeven_width = implied_move * 0.9
    em_ratio = breakeven_width / implied_move if implied_move else np.nan

    # -------------------------------
    # Peak / Cost ratio
    # -------------------------------
    peak_cost_ratio = extr_short / debit if debit != 0 else np.nan

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
