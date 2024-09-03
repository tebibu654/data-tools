from datetime import datetime, timedelta

import streamlit as st

from dashboards.utils.charts import chart_bars, chart_area

st.markdown("# Synthetix V3: Cross-chain stats")


@st.cache_data
def fetch_data(date_range):
    end_date = datetime.now()
    if date_range == "30d":
        start_date = datetime.now() - timedelta(days=30)
    elif date_range == "90d":
        start_date = datetime.now() - timedelta(days=90)
    elif date_range == "1y":
        start_date = datetime.now() - timedelta(days=365)
    else:
        start_date = datetime(2020, 1, 1)
    return st.session_state.api.get_tvl_by_chain(
        start_date=start_date.date(),
        end_date=end_date.date(),
    )


date_range = st.radio(
    "Select date range",
    ["30d", "90d", "1y", "all"],
    index=0,
    key="date_range",
)

data = fetch_data(date_range)

# st.write(data)

# chart = chart_bars(data, x_col="ts", y_cols="volume", title="Daily Perps Volume")

chart = chart_area(
    data,
    x_col="ts",
    y_cols="collateral_value",
    title="Total Value Locked (TVL) by Chain",
    color="label",
)

st.plotly_chart(chart)
