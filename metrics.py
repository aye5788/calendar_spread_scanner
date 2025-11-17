import numpy as np

def compute_calendar_metrics(short_opt, long_opt, core_data, short_exp, long_exp):
    # -----------------------------
    # Basic Greeks
    # -----------------------------
    net_vega = long_opt["vega"] - short_opt["vega"]
    net_theta = long_opt["theta"] - short_opt["theta"]
    net_gamma = long_opt["gamma"] - short_opt["gamma"]
    net_delta = long_opt["delta"] - short_opt["delta"]

    # -----------------------------
    # DTE ratio
    # -----------------------------
    dte_short = short_opt.get("dte", 0)
    dte_long  = long_opt.get("dte", 0)
    dte_ratio = dte_long / dte_short if dte_short > 0 else np.nan

    # -----------------------------
    # Extrinsic values
    # -----------------------------
    def extrinsic(opt):
        intrinsic = max(opt["underlyingPrice"] - opt["strike"], 0) if opt["callPut"] == "call" else \
                    max(opt["strike"] - opt["underlyingPrice"], 0)
        return opt["mid"] - intrinsic

    extr_short = extrinsic(short_opt)
    extr_long  = extrinsic(long_opt)
    extr_ratio = extr_short / extr_long if extr_long > 0 else np.nan

    # -----------------------------
    # Vega/Theta Ratio (VTR)
    # -----------------------------
    vtr = abs(net_vega) / abs(net_theta) if net_theta != 0 else np.nan

    # -----------------------------
    # IV decay differential
    # Using ORATS: short-term IV vs medium-term IV
    # -----------------------------
    iv_front = core_data.get("iv20d", np.nan)
    iv_back = core_data.get("iv60d", np.nan)
    iv_decay_diff = (iv_front - iv_back)

    # -----------------------------
    # Implied Move ratio
    # -----------------------------
    implied_move = core_data.get("impliedMove", np.nan)
    # Placeholder width until full modeling
    breakeven_width = implied_move * 0.9  
    em_ratio = breakeven_width / implied_move if implied_move else np.nan

    # -----------------------------
    # Peak/Cost ratio (simple approx)
    # -----------------------------
    debit = long_opt["mid"] - short_opt["mid"]
    peak_value = extr_short  # Simplified pin-value placeholder
    peak_cost_ratio = peak_value / debit if debit != 0 else np.nan

    # -----------------------------
    # Package results
    # -----------------------------
    return {
        "net_vega": net_vega,
        "net_theta": net_theta,
        "net_gamma": net_gamma,
        "net_delta": net_delta,
        "dte_ratio": dte_ratio,
        "extrinsic_ratio": extr_ratio,
        "vtr": vtr,
        "iv_front": iv_front,
        "iv_back": iv_back,
        "iv_decay_diff": iv_decay_diff,
        "implied_move": implied_move,
        "breakeven_width": breakeven_width,
        "em_ratio": em_ratio,
        "debit": debit,
        "peak_cost_ratio": peak_cost_ratio,
        "short_exp": short_exp,
        "long_exp": long_exp,
        "strike": short_opt["strike"],
    }

