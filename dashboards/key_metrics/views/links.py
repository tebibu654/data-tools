import streamlit as st
from dashboards.utils.display import display_cards

# card configs
perps_cards = [
    {
        "title": "Base Perps",
        "text": "Synthetix V3 Perps on Base",
        "url": "https://synthetix-all.streamlit.app/base?page=Perps",
    },
    {
        "title": "Arbitrum Perps",
        "text": "Synthetix V3 Perps on Arbitrum",
        "url": "https://synthetix-all.streamlit.app/arbitrum?page=Perps",
    },
    {
        "title": "V2 Perps",
        "text": "Synthetix V2 Perps on Optimism",
        "url": "https://synthetix-all.streamlit.app/optimism?page=Perps%20V2",
    },
]

lp_cards = [
    {
        "title": "Base LP",
        "text": "Synthetix V3 liquidity pools on Base",
        "url": "https://synthetix-all.streamlit.app/base?page=Perps",
    },
    {
        "title": "Arbitrum LP",
        "text": "Synthetix V3 liquidity pools on Arbitrum",
        "url": "https://synthetix-all.streamlit.app/arbitrum?page=Perps",
    },
    {
        "title": "Ethereum LP",
        "text": "Synthetix V3 liquidity pools on Ethereum",
        "url": "https://synthetix-all.streamlit.app/optimism?page=Perps%20V2",
    },
]

community_cards = [
    {
        "title": "Watcher",
        "text": "Real-time dashboard monitoring Synthetix Perps",
        "url": "https://dune.com/synthetix_community/synthetix-stats",
    },
    {
        "title": "Dune",
        "text": "Dune dashboards maintained by the community",
        "url": "https://dune.com/synthetix_community/synthetix-stats",
    },
]

st.markdown("# Perps")
display_cards(perps_cards)

st.markdown("# LPs")
display_cards(lp_cards)

st.markdown("# Community")
display_cards(community_cards)
