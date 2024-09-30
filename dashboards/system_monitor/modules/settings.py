import os
import streamlit as st
from synthetix import Synthetix
from api.internal_api import SynthetixAPI, get_db_config

# constants
ALCHEMY_KEY = os.getenv("WEB3_ALCHEMY_API_KEY")

NETWORK_CONFIGS = {
    1: {
        "network_id": 1,
        "network_name": "Ethereum Mainnet",
        "provider_rpc": f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_KEY}",
    },
    8453: {
        "network_id": 8453,
        "network_name": "Base Mainnet",
        "provider_rpc": f"https://base-mainnet.g.alchemy.com/v2/{ALCHEMY_KEY}",
    },
    42161: {
        "network_id": 42161,
        "network_name": "Arbitrum Mainnet",
        "provider_rpc": f"https://arb-mainnet.g.alchemy.com/v2/{ALCHEMY_KEY}",
    },
    # 10: {
    #     "network_id": 10,
    #     "network_name": "Optimism Mainnet",
    #     "provider_rpc": f"https://opt-mainnet.g.alchemy.com/v2/{ALCHEMY_KEY}",
    # },
    11155111: {
        "network_id": 11155111,
        "network_name": "Ethereum Sepolia",
        "provider_rpc": f"https://eth-sepolia.g.alchemy.com/v2/{ALCHEMY_KEY}",
    },
    84532: {
        "network_id": 84532,
        "network_name": "Base Sepolia",
        "provider_rpc": f"https://base-sepolia.g.alchemy.com/v2/{ALCHEMY_KEY}",
    },
    421614: {
        "network_id": 421614,
        "network_name": "Arbitrum Sepolia",
        "provider_rpc": f"https://arb-sepolia.g.alchemy.com/v2/{ALCHEMY_KEY}",
    },
    # 420: {
    #     "network_id": 420,
    #     "network_name": "Optimism Sepolia",
    #     "provider_rpc": f"https://opt-sepolia.g.alchemy.com/v2/{ALCHEMY_KEY}",
    # },
}


# set the API
@st.cache_resource
def load_api():
    return SynthetixAPI(db_config=get_db_config(streamlit=True))


@st.cache_resource(ttl=3600)
def load_snx(network_id=8453):
    provider_rpc = NETWORK_CONFIGS[network_id]["provider_rpc"]
    return Synthetix(
        provider_rpc=provider_rpc,
    )


def settings(enabled_markets=NETWORK_CONFIGS.keys()):
    networks = list(NETWORK_CONFIGS.keys())
    networks = [network for network in networks if network in enabled_markets]

    # select the network
    network_id = st.selectbox(
        "Network",
        options=networks,
        format_func=lambda x: NETWORK_CONFIGS[x]["network_name"],
    )

    # save the network
    st.session_state.network_id = network_id

    # initialize the values
    st.session_state.api = load_api()
    st.session_state.snx = load_snx(st.session_state.network_id)
