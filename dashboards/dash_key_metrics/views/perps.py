from datetime import datetime, timedelta

import streamlit as st

from dashboards.utils.charts import chart_bars, chart_lines, chart_oi
from dashboards.utils.date_utils import get_start_date

st.markdown("# Perps")

if "chain" not in st.session_state:
    st.session_state.chain = "All"
if "date_range" not in st.session_state:
    st.session_state.date_range = "30d"
if "asset" not in st.session_state:
    st.session_state.asset = "ETH (Base)"


@st.cache_data
def fetch_data(date_range, chain):
    end_date = datetime.now()
    start_date = get_start_date(date_range)

    perps_stats_by_chain = st.session_state.api.get_perps_stats_by_chain(
        start_date=start_date.date(),
        end_date=end_date.date(),
        chain=chain,
        resolution="daily",
    )
    perps_markets_history = st.session_state.api.get_perps_markets_history(
        start_date=start_date.date(),
        end_date=end_date.date(),
        chain=chain,
    )

    return {
        "perps_stats_by_chain": perps_stats_by_chain,
        "perps_markets_history": perps_markets_history,
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

assets = sorted(
    data["perps_markets_history"]["market_symbol"].unique(),
    key=lambda x: (
        x != "ETH (Base)",
        x != "BTC (Base)",
        x != "ETH (Arbitrum)",
        x != "BTC (Arbitrum)",
        x,
    ),
)

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
chart_perps_markets_oi_total = chart_lines(
    data["perps_markets_history"][
        data["perps_markets_history"]["market_symbol"] == st.session_state.asset
    ],
    x_col="ts",
    y_cols="size_usd",
    title="Open Interest (Total)",
    color="chain",
)
chart_perps_markets_oi_pct = chart_oi(
    data["perps_markets_history"][
        data["perps_markets_history"]["market_symbol"] == st.session_state.asset
    ],
    x_col="ts",
    title="Open Interest (Long vs. Short)",
)

asset = st.selectbox("Select asset", assets, index=0, key="asset")

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.plotly_chart(chart_perps_volume_by_chain, use_container_width=True)
    st.plotly_chart(chart_perps_markets_oi_total, use_container_width=True)
with chart_col2:
    st.plotly_chart(chart_perps_exchange_fees_by_chain, use_container_width=True)
    st.plotly_chart(chart_perps_markets_oi_pct, use_container_width=True)
