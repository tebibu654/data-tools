import streamlit as st
from dashboards.dash_all_metrics.modules.v3 import (
    chain_core_stats,
)

st.session_state.chain = "eth_mainnet"

pages = {
    "LP": chain_core_stats.main,
}
state_page = None
state_page = st.sidebar.radio(
    "Ethereum",
    tuple(pages.keys()),
    index=tuple(pages.keys()).index(state_page) if state_page else 0,
)
pages[state_page]()
