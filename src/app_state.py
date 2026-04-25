from __future__ import annotations

import streamlit as st


ARIMA_RESULTS_KEY = "arima_results"


def save_arima_results(**results) -> None:
    """Persist ARIMA results in Streamlit session state."""
    st.session_state[ARIMA_RESULTS_KEY] = results


def get_arima_results() -> dict | None:
    """Read ARIMA results from Streamlit session state."""
    return st.session_state.get(ARIMA_RESULTS_KEY)


def clear_arima_results() -> None:
    """Remove saved ARIMA results from session state."""
    st.session_state.pop(ARIMA_RESULTS_KEY, None)
