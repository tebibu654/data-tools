import streamlit as st
from dashboards.dash_all_metrics.modules.v3 import (
    chain_core_stats,
)

st.session_state.chain = "eth_mainnet"

pages = {
    "LP": chain_core_stats.main,
}

page_query = st.query_params["page"] if "page" in st.query_params else None
state_page = st.sidebar.radio(
    "Ethereum",
    tuple(pages.keys()),
    index=(
        tuple(pages.keys()).index(page_query)
        if page_query and page_query in pages.keys()
        else 0
    ),
)
pages[state_page]()
