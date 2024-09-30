from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from synthetix import Synthetix
from synthetix.utils import wei_to_ether
from eth_utils import encode_hex

from dashboards.system_monitor.modules.settings import settings

st.markdown("# Synthetix V3: Core")


# add the settings dropdown
settings()


# get the core configuration
@st.cache_data(ttl=3600, hash_funcs={Synthetix: lambda x: x.network_id})
def get_configs(snx):
    raw_configs = snx.core.core_proxy.functions.getCollateralConfigurations(
        False
    ).call()

    configs = {}
    for config in raw_configs:
        (
            enabled,
            issuance_ratio,
            liquidation_ratio,
            liquidation_reward,
            oracle_node_id,
            token_address,
            min_delegation,
        ) = config

        token = snx.web3.eth.contract(
            address=token_address, abi=snx.contracts["common"]["ERC20"]["abi"]
        )
        try:
            # get the token name if its ERC20 compliant
            token_name = token.functions.name().call()
            token_symbol = token.functions.symbol().call()
            token_description = f"{token_name} ({token_symbol})"
        except:
            # if not an ERC20 token, use a default name
            token_name = "Unknown Token"
            token_description = f"{token_name}"

        configs[token_address] = {
            "token": token_description,
            "enabled": enabled,
            "min_delegation": wei_to_ether(min_delegation),
            "issuance_ratio": wei_to_ether(issuance_ratio),
            "liquidation_ratio": wei_to_ether(liquidation_ratio),
            "liquidation_reward": wei_to_ether(liquidation_reward),
            "token_address": token_address,
            "oracle_node_id": encode_hex(oracle_node_id),
        }

    # create a dataframe and clean it
    df = pd.DataFrame.from_dict(configs, orient="index")

    # replace all values over 1e59 with "Infinity"
    df = df.applymap(lambda x: "Infinity" if type(x) is float and x > 1e59 else x)

    # change some types to percentages
    df["issuance_ratio"] = df["issuance_ratio"].astype(float).map("{:.2%}".format)
    df["liquidation_ratio"] = df["liquidation_ratio"].astype(float).map("{:.2%}".format)
    return df


# format the configurations
configs = get_configs(st.session_state.snx)

# display
st.dataframe(configs, hide_index=True)
