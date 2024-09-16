import streamlit as st
from dashboards.dash_all_metrics.modules.v2 import (
    perp_stats,
    perp_monitor,
    perp_markets,
    perp_integrators,
)

st.session_state.chain = "optimism_mainnet"

pages = {
    "Perps V2": perp_stats.main,
    "Perps V2 Monitor": perp_monitor.main,
    "Perps V2 Markets": perp_markets.main,
    "Perps V2 Integrators": perp_integrators.main,
}
state_page = None
state_page = st.sidebar.radio(
    "Optimism",
    tuple(pages.keys()),
    index=tuple(pages.keys()).index(state_page) if state_page else 0,
)
pages[state_page]()
