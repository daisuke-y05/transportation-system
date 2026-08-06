import os

class Config:
    APP_NAME = "交通費管理システム"
    APP_VERSION = "Ver4.2"

    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "dbname=transportation user=transportation_user password=transport123 host=localhost port=5432"
    )