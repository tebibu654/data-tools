import streamlit as st
from dashboards.all_metrics.modules.v2 import (
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

page_query = st.query_params["page"] if "page" in st.query_params else None
state_page = st.sidebar.radio(
    "Optimism",
    tuple(pages.keys()),
    index=(
        tuple(pages.keys()).index(page_query)
        if page_query and page_query in pages.keys()
        else 0
    ),
)
pages[state_page]()
