#!/usr/bin/env python3
import functools
import mysql.connector

query_cache = {}

# MySQL connection config - update your credentials here
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Faithoverfear@1998',
    'database': 'alx_airbnb_database',
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

# Decorator to cache query results based on query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Returning cached result")
            return query_cache[query]
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM user")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM user")

print(users)
print(users_again)
