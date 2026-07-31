import os

class Config:
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "dbname=transportation user=postgres password=postgres host=localhost port=5432"
    )