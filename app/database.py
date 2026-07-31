import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")

def get_connection():                                         #connect to postgrelSQL server
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    return psycopg.connect(database_url)

