import requests
import streamlit as st

BASE_URL = "https://api.orats.io/data/v2"

def _headers():
    return {"Authorization": f"Bearer {st.secrets['ORATS_API_KEY']}"}

# -------------------------------
# GET EXPIRATION DATES
# -------------------------------
def get_expirations(ticker):
    url = f"{BASE_URL}/cores/{ticker}"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    data = r.json()
    exp_list = data.get("expirations", [])
    return exp_list


# -------------------------------
# GET STRIKE-LEVEL OPTION DATA
# For a specific expiration & ticker
# -------------------------------
def get_strikes(ticker, expiry):
    url = f"{BASE_URL}/strikes/{ticker}/{expiry}"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json()


# -------------------------------
# GET CORE (IV, ATM Greeks, IV surfaces, HV, skew)
# -------------------------------
def get_core_data(ticker):
    url = f"{BASE_URL}/cores/{ticker}"
    r = requests.get(url, headers=_headers())
    r.raise_for_status()
    return r.json()


# -------------------------------
# Find a specific option (call or put) by strike
# -------------------------------
def filter_option(strikes_data, strike, call=True):
    key = "calls" if call else "puts"
    for opt in strikes_data.get(key, []):
        if float(opt["strike"]) == float(strike):
            return opt
    return None

