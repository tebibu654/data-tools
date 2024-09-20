import streamlit as st
from dashboards.all_metrics.modules.v3 import (
    chain_core_stats,
    chain_perp_stats,
    chain_perp_markets,
    chain_perp_monitor,
    chain_perp_integrators,
    chain_perp_keepers,
    chain_perp_account,
    chain_spot_markets,
)

st.session_state.chain = "base_mainnet"

pages = {
    "LP": chain_core_stats.main,
    "Perps": chain_perp_stats.main,
    "Perps Markets": chain_perp_markets.main,
    "Perps Monitor": chain_perp_monitor.main,
    "Perps Integrators": chain_perp_integrators.main,
    "Perps Keepers": chain_perp_keepers.main,
    "Perps Account": chain_perp_account.main,
    "Spot": chain_spot_markets.main,
}

page_query = st.query_params["page"] if "page" in st.query_params else None
state_page = st.sidebar.radio(
    "Base",
    tuple(pages.keys()),
    index=(
        tuple(pages.keys()).index(page_query)
        if page_query and page_query in pages.keys()
        else 0
    ),
)
pages[state_page]()
