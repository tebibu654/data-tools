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
@st.cache_data(ttl=300, hash_funcs={Synthetix: lambda x: x.network_id})
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


def clean_markets(configs):
    # add OI
    configs["open_interest"] = configs["size"] * configs["index_price"]
    configs["long_oi"] = (
        (configs["size"] + configs["skew"]) / 2 * configs["index_price"]
    )
    configs["short_oi"] = (
        (configs["size"] - configs["skew"]) / 2 * configs["index_price"]
    )
    configs["long_pct"] = configs.apply(
        lambda x: (
            f"{(x['long_oi'] / x['open_interest']) * 100:.2f}%"
            if x["open_interest"] > 0
            else "0%"
        ),
        axis=1,
    )
    configs["short_pct"] = configs.apply(
        lambda x: (
            f"{(x['short_oi'] / x['open_interest']) * 100:.2f}%"
            if x["open_interest"] > 0
            else "0%"
        ),
        axis=1,
    )

    # calculate amount of oi used
    # it is the larger of the size versus max_open_interest OR the size * index_price versus the max_market_value
    configs["oi_used"] = configs.apply(
        lambda x: max(
            x["size"] / x["max_open_interest"] if x["max_open_interest"] > 0 else 0,
            (
                (x["size"] * x["index_price"]) / x["max_market_value"]
                if x["max_market_value"] > 0
                else 0
            ),
        ),
        axis=1,
    )
    configs["oi_used_pct"] = configs["oi_used"].map("{:.2%}".format)
    return configs


# format the configurations
configs = get_configs(st.session_state.snx)
clean_configs = clean_markets(configs)

# display
st.markdown("### Market Configurations")
settings_cols = [
    "market_id",
    "market_name",
    "max_open_interest",
    "max_market_value",
    "skew_scale",
    "maker_fee",
    "taker_fee",
    "max_funding_velocity",
    "feed_id",
]
st.dataframe(configs[settings_cols], hide_index=True, use_container_width=True)

st.markdown("### Market Information")
info_cols = [
    "market_name",
    "size",
    "index_price",
    "open_interest",
    "long_oi",
    "short_oi",
    "long_pct",
    "short_pct",
    "oi_used_pct",
]
st.dataframe(configs[info_cols], hide_index=True, use_container_width=True)
