from datetime import datetime, timedelta

import streamlit as st

from dashboards.utils.charts import chart_area

st.markdown("# Perps")

if "chain" not in st.session_state:
    st.session_state.chain = "All"


@st.cache_data
def fetch_data(date_range, chain):
    end_date = datetime.now()
    if date_range == "30d":
        start_date = datetime.now() - timedelta(days=30)
    elif date_range == "90d":
        start_date = datetime.now() - timedelta(days=90)
    elif date_range == "1y":
        start_date = datetime.now() - timedelta(days=365)
    else:
        start_date = datetime(2020, 1, 1)
    return st.session_state.api.get_tvl_by_collateral(
        start_date=start_date.date(),
        end_date=end_date.date(),
        resolution="24h",
        chain=chain,
    )


col1, col2 = st.columns(2)

with col1:
    date_range = st.radio(
        "Select date range",
        ["30d", "90d", "1y", "all"],
        index=0,
        key="date_range",
    )
with col2:
    chain = st.radio(
        "Select chain",
        ["All", "Arbitrum", "Base"],
        index=0,
        key="chain",
    )

data = fetch_data(st.session_state.date_range, st.session_state.chain)

chart = chart_area(
    data,
    x_col="ts",
    y_cols="collateral_value",
    title="TVL by Collateral",
    color="label",
)

st.plotly_chart(chart)
