import requests
import streamlit as st

BASE_URL = "https://api.orats.io/datav2"

def _headers():
    return {
        "Authorization": f"Bearer {st.secrets['ORATS_API_KEY']}"
    }

# ----------------------------------------------------
# Get Ticker Core Data (IVs, HVs, aggregates)
# ----------------------------------------------------
def get_core_data(ticker: str):
    url = f"{BASE_URL}/core?ticker={ticker}"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json()

# ----------------------------------------------------
# Get Strikes Chain (ALL expirations & strikes)
# ----------------------------------------------------
def get_strikes_chain(ticker: str):
    url = f"{BASE_URL}/strikes?ticker={ticker}"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json()

# ----------------------------------------------------
# Extract list of expirations from strikes data
# ----------------------------------------------------
def extract_expirations(strikes_chain):
    exps = sorted(list({item["expiration"] for item in strikes_chain}))
    return exps

# ----------------------------------------------------
# Filter a specific option by expiration + strike
# ----------------------------------------------------
def find_option(strikes_chain, expiration, strike, call=True):
    cp = "call" if call else "put"
    for opt in strikes_chain:
        if (
            opt["expiration"] == expiration and
            float(opt["strike"]) == float(strike) and
            opt["callPut"] == cp
        ):
            return opt
    return None

