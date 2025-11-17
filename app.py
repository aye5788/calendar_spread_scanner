import streamlit as st
from orats_api import get_strikes_chain, extract_expirations, find_option, get_core_data
from metrics import compute_calendar_metrics
from scoring import score_calendar

st.set_page_config(page_title="Calendar Spread Scanner (ORATS)", layout="wide")
st.title("📊 Calendar Spread Scanner (ORATS Delayed Data)")

ticker = st.text_input("Ticker", "SPY")

if st.button("Load Data"):
    try:
        chain = get_strikes_chain(ticker)
        st.session_state["chain"] = chain
        st.session_state["expirations"] = extract_expirations(chain)
        st.success("Loaded!")
    except Exception as e:
        st.error(f"Error fetching strikes: {e}")

if "expirations" in st.session_state:

    exp_list = st.session_state["expirations"]

    short_exp = st.selectbox("Short Expiration", exp_list)
    long_exp  = st.selectbox("Long Expiration", exp_list)

    chain = st.session_state["chain"]

    strike_list = sorted({float(item["strike"]) for item in chain if item["expirDate"] == short_exp})
    strike = st.selectbox("Strike", strike_list)

    if st.button("SCAN CALENDAR"):
        core = get_core_data(ticker)
        short_opt = find_option(chain, short_exp, strike)
        long_opt  = find_option(chain, long_exp, strike)

        metrics = compute_calendar_metrics(short_opt, long_opt, core)
        score = score_calendar(metrics)

        st.subheader("📈 Metrics")
        st.json(metrics)
        st.subheader("⭐ Score")
        st.write(score)


