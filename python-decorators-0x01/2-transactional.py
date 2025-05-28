#!/usr/bin/env python3
import mysql.connector
import functools

# --- Configure MySQL Connection Parameters ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',        # Replace with your actual MySQL username
    'password': 'Faithoverfear@1998',    # Replace with your actual MySQL password
    'database': 'alx_airbnb_database'     # Your working database
}

# --- Decorator: Manage MySQL connection ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(**DB_CONFIG)
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# --- Decorator: Handle transactions ---
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise
    return wrapper

# --- Main logic: Update user email ---
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    query = "UPDATE user SET email = %s WHERE user_id = %s"
    cursor.execute(query, (new_email, user_id))
    
    if cursor.rowcount == 0:
        print(f"No user found with user_id {user_id}")
    else:
        print(f"Email updated for user_id {user_id}")

# --- Call function to test ---
update_user_email(user_id='08368f37-5fad-47a3-8b2b-85212db625cc', new_email='Crawford_Cartwright@hotmail.com')
