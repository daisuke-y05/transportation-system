import psycopg
from psycopg.rows import dict_row
from config import Config


def get_db_connection():
    return psycopg.connect(
        Config.DATABASE_URL,
        row_factory=dict_row
    )


def init_db():
    with get_db_connection() as conn:
        with open("schema.sql", "r", encoding="utf-8") as f:
            conn.execute(f.read())
        conn.commit()