from sqlalchemy import create_engine, text
from api.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL)


def execute_query(query: str, params: dict | None = None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        columns = result.keys()
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]


def execute_write(query: str, params: dict | None = None):
    with engine.begin() as conn:
        result = conn.execute(text(query), params or {})
        return result.rowcount
