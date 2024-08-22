import streamlit as st
from datetime import datetime

st.markdown("# Base")

data = st.session_state.api.get_volume(
    chain="base_mainnet", start_date=datetime(2024, 6, 1), end_date=datetime(2024, 7, 1)
)

st.write(data)
