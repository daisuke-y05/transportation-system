import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from config import Config


def get_db_connection():
    connect_kwargs = {"row_factory": dict_row}

    if os.environ.get("RENDER") == "true":
        connect_kwargs["sslmode"] = "require"

    return psycopg.connect(
        Config.DATABASE_URL,
        **connect_kwargs
    )


def init_db():

    schema_path = Path(__file__).with_name("schema.sql")

    with schema_path.open("r", encoding="utf-8") as f:
        schema_sql = f.read()

    with get_db_connection() as conn:
        conn.execute(schema_sql)
        conn.commit()