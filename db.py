import psycopg
from config import Config


def get_db_connection():
    conn = psycopg.connect(
        Config.DATABASE_URL,
        row_factory=psycopg.rows.dict_row
    )
    return conn