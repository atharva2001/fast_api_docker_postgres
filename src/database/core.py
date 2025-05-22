'''
Core database connection and query execution module.
'''

import psycopg2 
from log_util import get_logger

# Setup logger
logging = get_logger("database.log", "DatabaseLogger")

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="test_db",
            user="postgres",
            password="postgres",
            host="0.0.0.0",
            port="5432"
        )
        logging.info("Connected to the database")
        return conn
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        raise e 




