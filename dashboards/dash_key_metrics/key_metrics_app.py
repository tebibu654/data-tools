import streamlit as st
from api.internal_api import SynthetixAPI, get_db_config

st.set_page_config(
    page_title="Synthetix V3 Key Metrics",
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
cross_chain = st.Page("views/cross_chain.py", title="Synthetix V3: Cross-chain stats")

# navigation
pages = {
    "Cross-chain Stats": [cross_chain],
}
nav = st.navigation(pages)
nav.run()
