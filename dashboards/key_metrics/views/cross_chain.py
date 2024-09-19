from datetime import datetime, timedelta

import streamlit as st

from dashboards.utils.charts import chart_area, chart_lines, chart_bars
from dashboards.utils.date_utils import get_start_date

st.markdown("# Cross-chain stats")

if "chain" not in st.session_state:
    st.session_state.chain = "All"
if "date_range" not in st.session_state:
    st.session_state.date_range = "30d"


@st.cache_data
def fetch_data(date_range, chain):
    end_date = datetime.now()
    start_date = get_start_date(date_range)

    core_stats_by_collateral = st.session_state.api.get_core_stats_by_collateral(
        start_date=start_date.date(),
        end_date=end_date.date(),
        chain=chain,
        resolution="28d",
    )
    core_stats_by_chain = st.session_state.api.get_core_stats_by_chain(
        start_date=start_date.date(),
        end_date=end_date.date(),
        chain=chain,
    )
    perps_stats_by_chain = st.session_state.api.get_perps_stats_by_chain(
        start_date=start_date.date(),
        end_date=end_date.date(),
        chain=chain,
        resolution="daily",
    )

    return {
        "core_stats_by_chain": core_stats_by_chain,
        "core_stats_by_collateral": core_stats_by_collateral,
        "perps_stats_by_chain": perps_stats_by_chain,
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
        ["All", "Arbitrum", "Base"],
        index=0,
        key="chain",
    )

chart_core_tvl_by_chain = chart_area(
    data["core_stats_by_chain"],
    x_col="ts",
    y_cols="collateral_value",
    title="TVL by Chain",
    color="chain",
)
chart_core_tvl_by_collateral = chart_area(
    data["core_stats_by_collateral"],
    x_col="ts",
    y_cols="collateral_value",
    title="TVL by Collateral",
    color="label",
)
chart_core_apr_by_collateral = chart_lines(
    data["core_stats_by_collateral"],
    x_col="ts",
    y_cols="apr",
    title="APR by Collateral (28d average)",
    color="label",
    y_format="%",
)
chart_perps_volume_by_chain = chart_bars(
    data["perps_stats_by_chain"],
    x_col="ts",
    y_cols="volume",
    title="Perps Volume by Chain",
    color="chain",
)
chart_perps_fees_by_chain = chart_bars(
    data["perps_stats_by_chain"],
    x_col="ts",
    y_cols="exchange_fees",
    title="Exchange Fees by Chain",
    color="chain",
)


st.plotly_chart(chart_core_apr_by_collateral, use_container_width=True)

core_chart_col1, core_chart_col2 = st.columns(2)

with core_chart_col1:
    st.plotly_chart(chart_core_tvl_by_chain, use_container_width=True)
with core_chart_col2:
    st.plotly_chart(chart_core_tvl_by_collateral, use_container_width=True)

st.markdown("## Perps")
perps_chart_col1, perps_chart_col2 = st.columns(2)
with perps_chart_col1:
    st.plotly_chart(chart_perps_volume_by_chain, use_container_width=True)
with perps_chart_col2:
    st.plotly_chart(chart_perps_fees_by_chain, use_container_width=True)
