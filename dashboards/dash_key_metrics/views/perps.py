from datetime import datetime, timedelta

import streamlit as st

from dashboards.utils.charts import chart_bars

st.markdown("# Perps")

if "chain" not in st.session_state:
    st.session_state.chain = "All"
if "date_range" not in st.session_state:
    st.session_state.date_range = "30d"


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

    perps_stats_by_chain = st.session_state.api.get_perps_stats_by_chain(
        start_date=start_date.date(),
        end_date=end_date.date(),
        chain=chain,
        resolution="daily",
    )

    return {
        "perps_stats_by_chain": perps_stats_by_chain,
    }


filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    st.radio(
        "Select date range",
        ["30d", "90d", "1y", "all"],
        index=0,
        key="date_range",
    )
with filter_col2:
    st.radio(
        "Select chain",
        ["All", "Arbitrum", "Base"],
        index=0,
        key="chain",
    )

data = fetch_data(st.session_state.date_range, st.session_state.chain)

chart_perps_volume_by_chain = chart_bars(
    data["perps_stats_by_chain"],
    x_col="ts",
    y_cols="volume",
    title="Volume",
    color="chain",
)
chart_perps_exchange_fees_by_chain = chart_bars(
    data["perps_stats_by_chain"],
    x_col="ts",
    y_cols="exchange_fees",
    title="Exchange Fees",
    color="chain",
)


chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.plotly_chart(chart_perps_volume_by_chain, use_container_width=True)
with chart_col2:
    st.plotly_chart(chart_perps_exchange_fees_by_chain, use_container_width=True)
