#!/usr/bin/env python3
import mysql.connector
import functools
from datetime import datetime

# MySQL connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Faithoverfear@1998',
    'database': 'alx_airbnb_database'
}

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"[{datetime.now()}] Executing SQL Query: {query}")
        return func(query, *args, **kwargs)
    return wrapper

@log_queries
def fetch_all(query):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Example usage: Fetch all rows from the user table
users = fetch_all("SELECT * FROM user")
for user in users:
    print(user)
