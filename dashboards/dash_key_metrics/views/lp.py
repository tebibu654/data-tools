from datetime import datetime, timedelta

import streamlit as st

from dashboards.utils.charts import chart_area
from dashboards.utils.date_utils import get_start_date

st.markdown("# Liquidity Providers")

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

    return {
        "core_stats_by_collateral": core_stats_by_collateral,
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

chart_core_tvl_by_collateral = chart_area(
    data["core_stats_by_collateral"],
    x_col="ts",
    y_cols="collateral_value",
    title="TVL",
    color="label",
)
chart_core_apr_by_collateral = chart_area(
    data["core_stats_by_collateral"],
    x_col="ts",
    y_cols="apr",
    title="APR",
    color="label",
)
chart_core_apr_rewards_by_collateral = chart_area(
    data["core_stats_by_collateral"],
    x_col="ts",
    y_cols="apr_rewards",
    title="APR (Rewards)",
    color="label",
)
chart_core_debt_by_collateral = chart_area(
    data["core_stats_by_collateral"],
    x_col="ts",
    y_cols="debt",
    title="Debt",
    color="label",
)
chart_core_rewards_usd_by_collateral = chart_area(
    data["core_stats_by_collateral"],
    x_col="ts",
    y_cols="rewards_usd",
    title="Rewards (USD)",
    color="label",
)


st.plotly_chart(chart_core_tvl_by_collateral, use_container_width=True)
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.plotly_chart(chart_core_apr_by_collateral, use_container_width=True)
    st.plotly_chart(chart_core_debt_by_collateral, use_container_width=True)
with chart_col2:
    st.plotly_chart(chart_core_apr_rewards_by_collateral, use_container_width=True)
    st.plotly_chart(chart_core_rewards_usd_by_collateral, use_container_width=True)
