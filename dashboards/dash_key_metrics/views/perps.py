from datetime import datetime

import streamlit as st
import pandas as pd

from dashboards.utils.charts import chart_bars, chart_lines, chart_oi
from dashboards.utils.date_utils import get_start_date
from dashboards.dash_key_metrics.constants import SUPPORTED_CHAINS_PERPS

st.markdown("# Perps")

if "chain" not in st.session_state:
    st.session_state.chain = "All"
if "date_range" not in st.session_state:
    st.session_state.date_range = "30d"
if "asset" not in st.session_state:
    st.session_state.asset = "ETH (Base)"


@st.cache_data(ttl="30m")
def fetch_data(date_range, chain):
    end_date = datetime.now()
    start_date = get_start_date(date_range)

    chains_to_fetch = [*SUPPORTED_CHAINS_PERPS] if chain == "All" else [chain]

    perps_stats = [
        st.session_state.api.get_perps_stats(
            start_date=start_date.date(),
            end_date=end_date.date(),
            chain=current_chain,
            resolution="daily",
        )
        for current_chain in chains_to_fetch
        if current_chain in SUPPORTED_CHAINS_PERPS
    ]
    perps_markets_history = [
        st.session_state.api.get_perps_markets_history(
            start_date=start_date.date(),
            end_date=end_date.date(),
            chain=current_chain,
        )
        for current_chain in chains_to_fetch
        if current_chain in SUPPORTED_CHAINS_PERPS
    ]

    return {
        "perps_stats": pd.concat(perps_stats, ignore_index=True),
        "perps_markets_history": pd.concat(perps_markets_history, ignore_index=True),
    }


data = fetch_data(st.session_state.date_range, st.session_state.chain)

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
        ["All", *SUPPORTED_CHAINS_PERPS],
        index=0,
        format_func=lambda x: "All" if x == "All" else SUPPORTED_CHAINS_PERPS[x],
        on_change=lambda: st.session_state.update(
            {
                "asset": (
                    "ETH (Base)"
                    if st.session_state.chain == "All"
                    else f"ETH ({SUPPORTED_CHAINS_PERPS[st.session_state.chain]})"
                )
            }
        ),
        key="chain",
    )

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

chart_perps_volume = chart_bars(
    data["perps_stats"],
    x_col="ts",
    y_cols="volume",
    title="Volume",
    color="chain",
)
chart_perps_exchange_fees = chart_bars(
    data["perps_stats"],
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
    st.plotly_chart(chart_perps_volume, use_container_width=True)
    st.plotly_chart(chart_perps_markets_oi_total, use_container_width=True)
with chart_col2:
    st.plotly_chart(chart_perps_exchange_fees, use_container_width=True)
    st.plotly_chart(chart_perps_markets_oi_pct, use_container_width=True)
