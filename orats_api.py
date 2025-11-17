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
    data = r.json()

    # ORATS also wraps this in "data"
    return data["data"]

# ------------------------
# GET FULL STRIKES CHAIN
# ------------------------
def get_strikes_chain(ticker):
    url = f"{BASE_URL}/strikes?token={token()}&ticker={ticker}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    # IMPORTANT: RETURN THE LIST INSIDE "data"
    return data["data"]

# ------------------------
# EXTRACT EXPIRATIONS
# ------------------------
def extract_expirations(chain):
    expirations = sorted({item["expirDate"] for item in chain})
    return expirations

# ------------------------
# FIND SPECIFIC OPTION
# ------------------------
def find_option(chain, expiration, strike, call=True):
    for opt in chain:
        if (
            opt["expirDate"] == expiration and
            float(opt["strike"]) == float(strike)
        ):
            # ORATS does NOT separate call/put into separate objects
            # They are BOTH inside each record
            return opt
    return None

