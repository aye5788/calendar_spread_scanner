import requests
import streamlit as st

BASE_URL = "https://api.orats.io/datav2"

def token():
    return st.secrets["ORATS_API_KEY"]


# ---------------------------------------------------
# GET STRIKES CHAIN (returns LIST)
# ---------------------------------------------------
def get_strikes_chain(ticker):
    url = f"{BASE_URL}/strikes?token={token()}&ticker={ticker}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    # MUST return the list under "data"
    return data["data"]


# ---------------------------------------------------
# GET CORE DATA (returns DICT — NOT list)
# ---------------------------------------------------
def get_core_data(ticker):
    url = f"{BASE_URL}/cores?token={token()}&ticker={ticker}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    # MUST return first element in data[]
    if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
        return data["data"][0]

    # fallback
    return {}
    

# ---------------------------------------------------
# Extract expirations
# ---------------------------------------------------
def extract_expirations(chain):
    return sorted({item["expirDate"] for item in chain})


# ---------------------------------------------------
# Find strike record
# ---------------------------------------------------
def find_option(chain, expiration, strike):
    for opt in chain:
        if opt["expirDate"] == expiration and float(opt["strike"]) == float(strike):
            return opt
    return None

