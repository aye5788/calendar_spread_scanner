import streamlit as st
from orats_api import get_expirations, get_strikes, get_core_data, filter_option
from metrics import compute_calendar_metrics
from scoring import score_calendar

st.set_page_config(page_title="Calendar Spread Scanner", layout="wide")

st.title("📊 Calendar Spread Scanner (ORATS Powered)")

# -------------------------------
# User Inputs Panel
# -------------------------------
ticker = st.text_input("Ticker", "SPY")

if ticker:
    expirations = get_expirations(ticker)
    short_exp = st.selectbox("Short Expiration", expirations)
    long_exp = st.selectbox("Long Expiration", expirations, index=min(2, len(expirations)-1))

    # Retrieve strike chains
    if st.button("Load Strikes"):
        strikes_short = get_strikes(ticker, short_exp)
        strikes_long = get_strikes(ticker, long_exp)

        # Build strike list
        strike_list = sorted(list({float(o["strike"]) for o in strikes_short["calls"]}))
        strike = st.selectbox("Strike", strike_list)

    if st.button("SCAN CALENDAR"):
        core_data = get_core_data(ticker)
        strikes_short = get_strikes(ticker, short_exp)
        strikes_long = get_strikes(ticker, long_exp)

        call_short = filter_option(strikes_short, strike, call=True)
        call_long  = filter_option(strikes_long, strike, call=True)

        metrics = compute_calendar_metrics(call_short, call_long, core_data, short_exp, long_exp)
        score = score_calendar(metrics)

        st.subheader("📈 Calendar Spread Metrics")
        st.json(metrics)

        st.subheader("⭐ Calendar Score")
        st.write(score)

