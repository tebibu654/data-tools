import os
from datetime import datetime, timedelta
import streamlit as st
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import Generator, List
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
    SUPPORTED_CHAINS = ["Arbitrum", "Base"]

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

    def _get_chain_label(self, chain: str) -> str:
        """
        Get the SQL-friendly chain label string.

        Args:
            chain (str): Chain to query (e.g., 'Arbitrum', 'Base', 'All')

        Returns:
            str: SQL-friendly chain label string
        """
        if chain == "All":
            return ", ".join(f"'{c}'" for c in self.SUPPORTED_CHAINS)
        elif chain in self.SUPPORTED_CHAINS:
            return f"'{chain}'"
        else:
            raise ValueError(f"Unsupported chain: {chain}")

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

    def get_core_stats_by_chain(
        self,
        start_date: datetime,
        end_date: datetime,
        chain: str = "All",
    ) -> pd.DataFrame:
        """
        Get core stats by chain.

        Args:
            start_date (datetime): Start date for the query
            end_date (datetime): End date for the query
            chain (str): Chain to query (e.g., 'arbitrum_mainnet', 'base_mainnet')

        Returns:
            pandas.DataFrame: Core stats with columns 'ts', 'chain', 'collateral_value'
        """
        label = self._get_chain_label(chain)
        query = f"""
        WITH tvl AS (
            SELECT
                ts,
                'Arbitrum' AS chain,
                SUM(collateral_value) AS collateral_value
            FROM {self.environment}_arbitrum_mainnet.fct_core_apr_arbitrum_mainnet AS apr
            GROUP BY ts, chain

            UNION ALL

            SELECT
                ts,
                'Base' AS chain,
                SUM(collateral_value) AS collateral_value
            FROM {self.environment}_base_mainnet.fct_core_apr_base_mainnet AS apr
            GROUP BY ts, chain

            ORDER BY ts
        )

        SELECT
            ts,
            chain,
            collateral_value
        FROM tvl
        WHERE 
            ts >= '{start_date}' and ts <= '{end_date}'
            AND chain in ({label})

        """
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)

    def get_core_stats_by_collateral(
        self,
        start_date: datetime,
        end_date: datetime,
        chain: str = "All",
        resolution: str = "28d",
    ) -> pd.DataFrame:
        """
        Get core stats by collateral.
        This function retrieves detailed core stats including
        collateral value, debt, PNL, rewards, issuance, and APR
        for each collateral type on both Arbitrum and Base chains.

        Args:
            start_date (datetime): Start date for the query
            end_date (datetime): End date for the query
            chain (str): Chain to query (e.g., 'arbitrum_mainnet', 'base_mainnet')
            resolution (str): Data resolution ('daily' or 'hourly')

        Returns:
            pandas.DataFrame: TVL data with columns:
                'ts', 'label', 'chain', 'collateral_value', 'apr', 'debt', 'rewards_usd'
        """
        label = self._get_chain_label(chain)
        query = f"""
        WITH tvl AS (
            SELECT 
                ts,
                CONCAT(coalesce(tk.token_symbol, collateral_type), ' (Arbitrum)') as label,
                'Arbitrum' as chain,
                collateral_value,
                debt,
                rewards_usd,
                apr_{resolution} as apr,
                apr_{resolution}_rewards as apr_rewards
            FROM {self.environment}_arbitrum_mainnet.fct_core_apr_arbitrum_mainnet apr
            LEFT JOIN {self.environment}_seeds.arbitrum_mainnet_tokens tk on lower(apr.collateral_type) = lower(tk.token_address)

            UNION ALL

            SELECT 
                ts,
                CONCAT(coalesce(tk.token_symbol, collateral_type), ' (Base)') as label,
                'Base' as chain,
                collateral_value,
                debt,
                rewards_usd,
                apr_{resolution} as apr,
                apr_{resolution}_rewards as apr_rewards
            FROM {self.environment}_base_mainnet.fct_core_apr_base_mainnet apr
            LEFT JOIN {self.environment}_seeds.base_mainnet_tokens tk on lower(apr.collateral_type) = lower(tk.token_address)
        )

        SELECT 
            ts,
            label,
            chain,
            collateral_value,
            debt,
            rewards_usd,
            apr,
            apr_rewards
        FROM tvl
        WHERE 
            ts >= '{start_date}' and ts <= '{end_date}'
            AND chain in ({label})
        ORDER BY ts
        """
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)

    def get_perps_stats_by_chain(
        self,
        start_date: datetime,
        end_date: datetime,
        chain: str = "All",
        resolution: str = "daily",
    ) -> pd.DataFrame:
        """
        Get perps stats by chain.

        Args:
            start_date (datetime): Start date for the query
            end_date (datetime): End date for the query
            chain (str): Chain to query (e.g., 'arbitrum_mainnet', 'base_mainnet')

        Returns:
            pandas.DataFrame: Perps stats with columns:
                'ts', 'volume', 'exchange_fees'
        """
        label = self._get_chain_label(chain)
        query = f"""
        WITH perps_stats AS (
            SELECT
                ts,
                'Arbitrum' as chain,
                volume,
                exchange_fees
            FROM {self.environment}_arbitrum_mainnet.fct_perp_stats_{resolution}_arbitrum_mainnet

            UNION ALL

            SELECT
                ts,
                'Base' as chain,
                volume,
                exchange_fees
            FROM {self.environment}_base_mainnet.fct_perp_stats_{resolution}_base_mainnet
        )

        SELECT
            ts,
            chain,
            volume,
            exchange_fees
        FROM perps_stats
        WHERE
            ts >= '{start_date}' and ts <= '{end_date}'
            AND chain in ({label})
        """
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
