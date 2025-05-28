#!/usr/bin/env python3
import mysql.connector
import functools

# Your actual MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',                     # Replace with your real username if different
    'password': 'Faithoverfear@1998',   # Replace with your actual password
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

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    query = "SELECT * FROM user WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

# Example UUID string (replace with a valid UUID from your user table)
sample_user_id = "08368f37-5fad-47a3-8b2b-85212db625cc"  # Replace this!

user = get_user_by_id(user_id=sample_user_id)
print(user)
