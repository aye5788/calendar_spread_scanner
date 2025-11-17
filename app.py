import streamlit as st
from orats_api import get_core_data, get_strikes_chain, extract_expirations, find_option
from metrics import compute_calendar_metrics
from scoring import score_calendar

st.set_page_config(page_title="Calendar Spread Scanner", layout="wide")
st.title("📊 ORATS Calendar Spread Scanner (Delayed Data API)")

ticker = st.text_input("Ticker", "SPY")

if ticker:

    # Load strikes chain
    if st.button("Load Expirations"):
        chain = get_strikes_chain(ticker)
        expirations = extract_expirations(chain)
        st.session_state["chain"] = chain
        st.session_state["expirations"] = expirations

    if "expirations" in st.session_state:
        exp_list = st.session_state["expirations"]

        short_exp = st.selectbox("Short Expiration", exp_list)
        long_exp  = st.selectbox("Long Expiration", exp_list)

        # Extract strikes available at short_exp
        chain = st.session_state["chain"]
        available_strikes = sorted(list({float(item["strike"]) for item in chain if item["expiration"] == short_exp}))

        strike = st.selectbox("Strike", available_strikes)

        if st.button("SCAN CALENDAR"):
            core_data = get_core_data(ticker)
            short_opt = find_option(chain, short_exp, strike, call=True)
            long_opt  = find_option(chain, long_exp, strike, call=True)

            # Compute metrics
            metrics = compute_calendar_metrics(short_opt, long_opt, core_data)
            score = score_calendar(metrics)

            st.subheader("📈 Calendar Metrics")
            st.json(metrics)

            st.subheader("⭐ Score")
            st.write(score)


