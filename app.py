import streamlit as st
from orats_api import get_core_data, get_strikes_chain, extract_expirations, find_option
from metrics import compute_calendar_metrics
from scoring import score_calendar

st.set_page_config(page_title="Calendar Spread Tool", layout="wide")
st.title("📊 Calendar Spread Scanner (ORATS - Delayed Data)")

# ------------------------
# USER INPUT
# ------------------------
ticker = st.text_input("Ticker", value="SPY")

if st.button("Load Data"):
    with st.spinner("Loading strikes..."):
        try:
            chain = get_strikes_chain(ticker)
            st.session_state["chain"] = chain
            st.session_state["expirations"] = extract_expirations(chain)
            st.success("Data loaded!")
        except Exception as e:
            st.error(f"Error fetching strikes: {e}")

# ------------------------
# ONLY SHOW NEXT UI AFTER SUCCESSFUL LOAD
# ------------------------
if "expirations" in st.session_state:

    exp_list = st.session_state["expirations"]

    short_exp = st.selectbox("Short Expiration", exp_list)
    long_exp  = st.selectbox("Long Expiration", exp_list)

    # strike list based on short expiration
    chain = st.session_state["chain"]
    strike_list = sorted({float(opt["strike"]) for opt in chain if opt["expiration"] == short_exp})

    strike = st.selectbox("Strike", strike_list)

    if st.button("SCAN CALENDAR"):
        with st.spinner("Scanning..."):
            core = get_core_data(ticker)
            short_opt = find_option(chain, short_exp, strike, call=True)
            long_opt = find_option(chain, long_exp, strike, call=True)

            m = compute_calendar_metrics(short_opt, long_opt, core)
            score = score_calendar(m)

            st.subheader("📈 Metrics")
            st.json(m)

            st.subheader("⭐ Score")
            st.write(score)


