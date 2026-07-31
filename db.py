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

        conn.execute("""

        CREATE TABLE IF NOT EXISTS transportation (

            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

            name TEXT NOT NULL,
            month TEXT NOT NULL,

            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,

            departure TEXT NOT NULL,
            destination TEXT NOT NULL,

            transport TEXT NOT NULL,
            trip_type TEXT NOT NULL,

            fare INTEGER NOT NULL,

            updated_at TEXT NOT NULL

        );

        """)

        conn.execute("""

        CREATE TABLE IF NOT EXISTS submissions (

            name TEXT NOT NULL,
            month TEXT NOT NULL,

            submitted_at TIMESTAMP NOT NULL,

            UNIQUE(name, month)

        );

        """)

        conn.commit()