from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from synthetix import Synthetix
from synthetix.utils import wei_to_ether
from eth_utils import encode_hex

from dashboards.system_monitor.modules.settings import settings

st.markdown("# Synthetix V3: Perps")

PERPS_NETWORKS = [
    8453,
    84532,
    42161,
    421614,
]

# add the settings dropdown
settings(enabled_markets=PERPS_NETWORKS)


# get the core configuration
@st.cache_data(ttl=3600, hash_funcs={Synthetix: lambda x: x.network_id})
def get_configs(snx):
    markets = snx.perps.markets_by_name

    # create a dataframe and clean it
    df = pd.DataFrame.from_dict(markets, orient="index").sort_values("market_id")

    # change some types to percentages
    percent_cols = [
        "maker_fee",
        "taker_fee",
        "current_funding_rate",
        "current_funding_velocity",
        "interest_rate",
    ]
    for col in percent_cols:
        df[col] = df[col].astype(float).map("{:.2%}".format)

    return df


# format the configurations
configs = get_configs(st.session_state.snx)

# display
st.dataframe(configs, hide_index=True)


st.write(sum(configs["max_market_value"]))

st.write(sum(configs["size"] * configs["index_price"]))
st.write(sum(configs["max_open_interest"] * configs["index_price"]))
