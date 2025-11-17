import requests
import streamlit as st

BASE_URL = "https://api.orats.io/datav2"

def token():
    return st.secrets["ORATS_API_KEY"]

# ------------------------
# GET CORE DATA
# ------------------------
def get_core_data(ticker):
    url = f"{BASE_URL}/cores?token={token()}&ticker={ticker}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

# ------------------------
# GET FULL STRIKES CHAIN
# ------------------------
def get_strikes_chain(ticker):
    url = f"{BASE_URL}/strikes?token={token()}&ticker={ticker}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

# ------------------------
# EXTRACT EXPIRATIONS
# ------------------------
def extract_expirations(chain):
    # chain is a LIST of option objects
    expirations = sorted({item["expiration"] for item in chain})
    return expirations

# ------------------------
# FIND SPECIFIC OPTION
# ------------------------
def find_option(chain, expiration, strike, call=True):
    cp = "call" if call else "put"
    for opt in chain:
        if (
            opt["expiration"] == expiration and
            float(opt["strike"]) == float(strike) and
            opt["callPut"] == cp
        ):
            return opt
    return None
