import streamlit as st
from api.internal_api import SynthetixAPI, get_db_config

st.set_page_config(
    page_title="Synthetix Stats - All",
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
    DB_ENV = st.secrets.database.DB_ENV
    return SynthetixAPI(db_config=get_db_config(streamlit=True), environment=DB_ENV)


st.session_state.api = load_api()

# pages
all_chains = st.Page("views/all_chains.py", title="Synthetix V3")
ethereum = st.Page("views/ethereum.py", title="Ethereum")
base = st.Page("views/base.py", title="Base")
arbitrum = st.Page("views/arbitrum.py", title="Arbitrum")
optimism = st.Page("views/optimism.py", title="Optimism")


# navigation
pages = {
    "": [all_chains, ethereum, base, arbitrum, optimism],
}
nav = st.navigation(pages)
nav.run()
