import streamlit as st
from api.internal_api import SynthetixAPI, get_db_config

st.set_page_config(
    page_title="Synthetix V3 All Metrics",
    page_icon=f"dashboards/static/favicon.ico",
    layout="wide",
)

hide_footer = """
    <style>
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)


# set the API
@st.cache_resource
def load_api():
    return SynthetixAPI(db_config=get_db_config(streamlit=True))


st.session_state.api = load_api()

# pages
all_chains = st.Page("pages/all_chains.py", title="Synthetix V3")
ethereum = st.Page("pages/ethereum.py", title="Ethereum")
base = st.Page("pages/base.py", title="Base")
arbitrum = st.Page("pages/arbitrum.py", title="Arbitrum")
optimism = st.Page("pages/optimism.py", title="Optimism")


# navigation
pages = {
    "": [all_chains, ethereum, base, arbitrum, optimism],
}
nav = st.navigation(pages)
nav.run()
