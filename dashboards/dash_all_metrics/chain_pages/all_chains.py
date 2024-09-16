import streamlit as st
from dashboards.dash_all_metrics.modules.v3 import (
    all_core,
    all_perps,
)

pages = {
    "LP": all_core.main,
    "Perps": all_perps.main,
}
state_page = None
state_page = st.sidebar.radio(
    "All Chains",
    tuple(pages.keys()),
    index=tuple(pages.keys()).index(state_page) if state_page else 0,
)
pages[state_page]()
