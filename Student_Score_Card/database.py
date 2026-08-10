import os
import sqlite3
os.makedirs("data", exist_ok=True)

database_name = "data/school.db"

def get_connection():
    """
        connect with sql database
    """
    conn = sqlite3.connect(database_name)
    conn.row_factory = sqlite3.Row
    return conn