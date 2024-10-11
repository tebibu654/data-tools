import time
from datetime import datetime, timedelta
from api.internal_api import SynthetixAPI, get_db_config


def time_query(api, query_name, *args, **kwargs):
    start_time = time.time()
    getattr(api, query_name)(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time


def run_benchmarks(api, num_runs=3):
    benchmarks = {}

    # Define test scenarios
    end_date = datetime.now()
    start_date_1d = end_date - timedelta(days=1)
    start_date_7d = end_date - timedelta(days=7)
    start_date_30d = end_date - timedelta(days=30)

    # Get the names of the queries from the SynthetixAPI class
    queries = [
        method
        for method in dir(api)
        if method.startswith("get_") and callable(getattr(api, method))
    ]
    v3_queries = [query for query in queries if "v2" not in query]
    v2_queries = [query for query in queries if "v2" in query]

    scenarios = [
        (
            query_name,
            {
                "start_date": start_date,
                "end_date": end_date,
                "chain": chain,
            },
        )
        for query_name in v3_queries
        for start_date in [start_date_1d, start_date_7d, start_date_30d]
        for chain in ["arbitrum_mainnet", "base_mainnet"]
    ]

    for query_name, params in scenarios:
        benchmarks[f"{query_name} - {params}"] = []
        for _ in range(num_runs):
            try:
                execution_time = time_query(api, query_name, **params)
                benchmarks[f"{query_name} - {params}"].append(execution_time)
            except:
                pass

    return benchmarks


def print_report(benchmarks):
    print("SynthetixAPI Benchmark Report")
    print("=============================")
    for query, times in benchmarks.items():
        if len(times) == 0:
            print(f"\n{query}")
            print("  No data available")
            continue

        avg_time = sum(times) / len(times)
        print(f"\n{query}")
        print(f"  Average execution time: {avg_time:.4f} seconds")
        print(f"  Min execution time: {min(times):.4f} seconds")
        print(f"  Max execution time: {max(times):.4f} seconds")


if __name__ == "__main__":
    db_config = get_db_config(streamlit=False)
    api = SynthetixAPI(db_config, environment="prod", streamlit=False)

    benchmarks = run_benchmarks(api)
    print_report(benchmarks)
