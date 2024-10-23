import streamlit as st

from api.internal_api import SynthetixAPI, get_db_config
from dashboards.utils import performance

st.markdown("# Query Performance")

if "result_df" not in st.session_state:
    st.session_state.result_df = None


def time_queries():
    api = SynthetixAPI(db_config=get_db_config(streamlit=True))
    results = performance.run_benchmarks(api)

    # create dataframe
    df = performance.create_benchmark_dataframe(results)
    st.session_state.result_df = df


st.button("Run queries", on_click=time_queries)

if st.session_state.result_df is not None:
    st.dataframe(st.session_state.result_df)
