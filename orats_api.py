import requests
import streamlit as st

BASE_URL = "https://api.orats.io/datav2"

def _token():
    return st.secrets["ORATS_API_KEY"]

# ----------------------------------------------------
# Get Core Data
# ----------------------------------------------------
def get_core_data(ticker: str):
    url = f"{BASE_URL}/core?ticker={ticker}&token={_token()}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

# ----------------------------------------------------
# Get ALL strikes chain (all expirations)
# ----------------------------------------------------
def get_strikes_chain(ticker: str):
    url = f"{BASE_URL}/strikes?ticker={ticker}&token={_token()}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

# ----------------------------------------------------
# Extract expirations
# ----------------------------------------------------
def extract_expirations(strikes_chain):
    exps = sorted(list({item["expiration"] for item in strikes_chain}))
    return exps

# ----------------------------------------------------
# Find specific option
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

