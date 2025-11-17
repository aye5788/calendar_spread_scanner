import requests
import streamlit as st

BASE_URL = "https://api.orats.io/datav2"

def token():
    return st.secrets["ORATS_API_KEY"]

# -------------------------------
# GET STRIKES CHAIN
# -------------------------------
def get_strikes_chain(ticker):
    url = f"{BASE_URL}/strikes?token={token()}&ticker={ticker}"
    r = requests.get(url)
    r.raise_for_status()

    data = r.json()

    # ORATS delayed API puts the list inside "data"
    return data["data"]

# -------------------------------
# GET CORE DATA
# -------------------------------
def get_core_data(ticker):
    url = f"{BASE_URL}/cores?token={token()}&ticker={ticker}"
    r = requests.get(url)
    r.raise_for_status()

    data = r.json()
    return data["data"]

# -------------------------------
# Extract expirations
# -------------------------------
def extract_expirations(chain):
    return sorted({item["expirDate"] for item in chain})

# -------------------------------
# Find option for specific strike + expiration
# ORATS only provides ONE object containing call+put data
# -------------------------------
def find_option(chain, expiration, strike):
    for opt in chain:
        if opt["expirDate"] == expiration and float(opt["strike"]) == float(strike):
            return opt
    return None

