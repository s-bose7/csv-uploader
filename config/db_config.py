import os
from dotenv import load_dotenv


def get_database_url(environment: str)->str:

    # Load environment variables from .env file   
    load_dotenv()

    # Read the database credentials based on the environment
    if environment == "production":
        DB_HOST = os.getenv("PROD_DB_HOST")
        DB_PORT = os.getenv("PROD_DB_PORT")
        DB_NAME = os.getenv("PROD_DB_NAME")
        DB_USER = os.getenv("PROD_DB_USER")
        DB_PASSWORD = os.getenv("PROD_DB_PASSWORD")
    else:
        DB_HOST = os.getenv("DEV_DB_HOST")
        DB_PORT = os.getenv("DEV_DB_PORT")
        DB_NAME = os.getenv("DEV_DB_NAME")
        DB_USER = os.getenv("DEV_DB_USER")
        DB_PASSWORD = os.getenv("DEV_DB_PASSWORD")

    # Construct the database connection string
    DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    return DB_URL