import os
from datetime import datetime, timedelta
import streamlit as st
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import Dict, Any, Generator
from dotenv import load_dotenv


def get_db_config(streamlit=True):
    if streamlit:
        DB_NAME = st.secrets.database.DB_NAME
        DB_USER = st.secrets.database.DB_USER
        DB_PASS = st.secrets.database.DB_PASS
        DB_HOST = st.secrets.database.DB_HOST
        DB_PORT = st.secrets.database.DB_PORT
    else:
        load_dotenv()
        DB_NAME = os.environ.get("DB_NAME")
        DB_USER = os.environ.get("DB_USER")
        DB_PASS = os.environ.get("DB_PASS")
        DB_HOST = os.environ.get("DB_HOST")
        DB_PORT = os.environ.get("DB_PORT")

    return {
        "dbname": DB_NAME,
        "user": DB_USER,
        "password": DB_PASS,
        "host": DB_HOST,
        "port": DB_PORT,
    }


def get_connection(db_config):
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = sqlalchemy.create_engine(connection_string)
    conn = engine.connect()
    return conn


class SynthetixAPI:
    def __init__(
        self, db_config: dict, environment: str = "prod", streamlit: bool = True
    ):
        """
        Initialize the SynthetixAPI.

        Args:
            environment (str): The environment to query data for ('prod' or 'dev')
        """
        self.environment = environment
        self.db_config = get_db_config(streamlit)
        self.engine = self._create_engine()
        self.Session = sessionmaker(bind=self.engine)

    def _create_engine(self):
        """Create and return a database engine with connection pooling."""
        connection_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['dbname']}"
        return sqlalchemy.create_engine(connection_string, pool_size=5, max_overflow=10)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.engine.dispose()

    @contextmanager
    def get_connection(
        self,
    ) -> Generator[sqlalchemy.engine.base.Connection, None, None]:
        """Context manager for database connections."""
        connection = self.engine.connect()
        try:
            yield connection
        finally:
            connection.close()

    # queries
    def get_volume(
        self,
        chain: str,
        start_date: datetime,
        end_date: datetime,
        resolution: str = "daily",
    ) -> pd.DataFrame:
        """
        Get trading volume data for a specified chain.

        Args:
            chain (str): Chain to query (e.g., 'base_mainnet', 'optimism_mainnet')
            start_date (datetime): Start date for the query
            end_date (datetime): End date for the query
            resolution (str): Data resolution ('daily' or 'hourly')

        Returns:
            pandas.DataFrame: Volume data with columns 'ts', 'volume', 'cumulative_volume'
        """
        query = f"""
        SELECT
            ts,
            volume,
            cumulative_volume
        FROM {self.environment}_{chain}.fct_perp_stats_{resolution}_{chain}
        WHERE ts >= '{start_date}' and ts <= '{end_date}'
        ORDER BY ts
        """
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)

    def get_tvl_by_chain(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> pd.DataFrame:
        """
        Get Total Value Locked (TVL) data for all chains.

        Args:
            start_date (datetime): Start date for the query
            end_date (datetime): End date for the query
            resolution (str): Data resolution ('daily' or 'hourly')

        Returns:
            pandas.DataFrame: TVL data with columns 'ts', 'chain', 'tvl'
        """
        query = f"""
        SELECT
            ts,
            'Arbitrum' AS label,
            SUM(collateral_value) AS collateral_value,
            SUM(cumulative_pnl) AS cumulative_pnl
        FROM {self.environment}_arbitrum_mainnet.fct_core_apr_arbitrum_mainnet AS apr
        WHERE ts >= '{start_date}' and ts <= '{end_date}'
        GROUP BY ts, label

        UNION ALL

        SELECT
            ts,
            'Base' AS label,
            SUM(collateral_value) AS collateral_value,
            SUM(cumulative_pnl) AS cumulative_pnl
        FROM {self.environment}_base_mainnet.fct_core_apr_base_mainnet AS apr
        WHERE ts >= '{start_date}' and ts <= '{end_date}'
        GROUP BY ts, label
        ORDER BY ts
        """
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
