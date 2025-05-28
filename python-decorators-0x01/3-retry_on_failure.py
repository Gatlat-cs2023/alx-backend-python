#!/usr/bin/env python3
import time
import functools
import mysql.connector
from mysql.connector import Error

# Your MySQL config
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Faithoverfear@1998',
    'database': 'alx_airbnb_database'
}

# Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(**DB_CONFIG)
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Retry decorator
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        print("All retry attempts failed.")
                        raise
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    return cursor.fetchall()

# Fetch and print users
users = fetch_users_with_retry()
for u in users:
    print(u)
