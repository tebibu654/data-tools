import streamlit as st
from dashboards.all_metrics.modules.v3 import (
    all_core,
    all_perps,
)

pages = {
    "LP": all_core.main,
    "Perps": all_perps.main,
}

page_query = st.query_params["page"] if "page" in st.query_params else None
state_page = st.sidebar.radio(
    "All Chains",
    tuple(pages.keys()),
    index=(
        tuple(pages.keys()).index(page_query)
        if page_query and page_query in pages.keys()
        else 0
    ),
)
pages[state_page]()
