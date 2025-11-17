import numpy as np

def compute_calendar_metrics(short_opt, long_opt, core):

    # -------------------------------
    # Greeks
    # -------------------------------
    net_vega  = long_opt["vega"]  - short_opt["vega"]
    net_theta = long_opt["theta"] - short_opt["theta"]
    net_gamma = long_opt["gamma"] - short_opt["gamma"]
    net_delta = long_opt["delta"] - short_opt["delta"]

    # -------------------------------
    # DTE Ratio
    # -------------------------------
    dte_ratio = None
    try:
        dte_ratio = long_opt["dte"] / short_opt["dte"]
    except:
        dte_ratio = np.nan

    # -------------------------------
    # Extrinsic Values
    # -------------------------------
    def extrinsic(o):
        intrinsic = max(o["underlyingPrice"] - o["strike"], 0) if o["callPut"] == "call" else \
                    max(o["strike"] - o["underlyingPrice"], 0)
        return o["mid"] - intrinsic

    extr_short = extrinsic(short_opt)
    extr_long  = extrinsic(long_opt)

    extr_ratio = extr_short / extr_long if extr_long > 0 else np.nan

    # -------------------------------
    # Vega/Theta Ratio (VTR)
    # -------------------------------
    vtr = abs(net_vega) / abs(net_theta) if net_theta != 0 else np.nan

    # -------------------------------
    # IV Decay Differential (using core IVs)
    # -------------------------------
    iv_front = core.get("iv20d", np.nan)
    iv_back  = core.get("iv60d", np.nan)
    iv_decay_diff = iv_front - iv_back

    # -------------------------------
    # Implied Move Ratio
    # -------------------------------
    implied_move = core.get("impliedMove", np.nan)
    breakeven_width = implied_move * 0.9
    em_ratio = breakeven_width / implied_move if implied_move else np.nan

    # -------------------------------
    # Peak/Cost Ratio (simplified)
    # -------------------------------
    debit = long_opt["mid"] - short_opt["mid"]
    peak_value = extr_short
    peak_cost_ratio = peak_value / debit if debit != 0 else np.nan

    return {
        "strike": short_opt["strike"],
        "expiration_short": short_opt["expiration"],
        "expiration_long": long_opt["expiration"],

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
        "peak_cost_ratio": peak_cost_ratio
    }
