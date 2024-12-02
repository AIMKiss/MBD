import pandas as pd
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional

class Database:
    def __init__(self, user: str, password: str, host: str, database: str) -> None:
        self.engine: Engine = create_engine(
            f'mssql+pyodbc://{user}:{password}@{host}/{database}?'
            'TrustServerCertificate=yes&'
            'driver=ODBC+Driver+17+for+SQL+Server'
        )
        self.Session: sessionmaker = sessionmaker(bind=self.engine)

    def fetch_data(self, query: str) -> pd.DataFrame:
        return pd.read_sql(query, self.engine)

    def test_connection(self) -> bool:
        try:
            with self.engine.connect() as connection:
                return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
