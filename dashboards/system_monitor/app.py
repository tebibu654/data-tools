import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

if "network_id" not in st.session_state:
    st.session_state.network_id = 1


st.set_page_config(
    page_title="Synthetix System Monitor",
    page_icon=f"dashboards/static/favicon.ico",
    layout="wide",
)

hide_footer = """
    <style>
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)


# pages
core = st.Page("views/core.py", title="Core System")
perps = st.Page("views/perps.py", title="Perps Markets")
performance = st.Page("views/performance.py", title="Query Performance")

# navigation
pages = {
    "": [core, perps, performance],
}
nav = st.navigation(pages)
nav.run()
