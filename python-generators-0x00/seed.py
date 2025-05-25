#!/usr/bin/python3
import mysql.connector
import csv
import uuid

def connect_db():
    """Connects to the MySQL server (no database specified)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Faithoverfear@1998"  # <-- Replace with your actual password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the alx_airbnb_database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS alx_airbnb_database")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Database creation error: {err}")

def connect_to_airbnb_db():
    """Connects directly to the alx_airbnb_database database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Faithoverfear@1998",  # <-- Replace here too
            database="alx_airbnb_database"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection to alx_airbnb_database error: {err}")
        return None

def create_user_table(connection):
    """Creates the user table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS user (
            user_id CHAR(36) PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20),
            role VARCHAR(50),
            age INT,
            INDEX (user_id)
        );
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Table user created successfully")
    except mysql.connector.Error as err:
        print(f"Table creation error: {err}")

def insert_users_from_csv(connection, filename):
    """Inserts data from a CSV file into the user table if email does not exist."""
    try:
        cursor = connection.cursor()
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = str(uuid.uuid4())
                full_name = row['name']
                first_name, last_name = full_name.split(" ", 1) if " " in full_name else (full_name, "")
                email = row['email']
                password_hash = row.get('password_hash', 'default_hash')
                phone_number = row.get('phone_number', None)
                role = row.get('role', 'guest')
                age = int(row.get('age', 0))

                # Check if email already exists
                cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO user (user_id, first_name, last_name, email, password_hash, phone_number, role, age)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, first_name, last_name, email, password_hash, phone_number, role, age))
        connection.commit()
        cursor.close()
        print("User data inserted successfully")
    except Exception as e:
        print(f"Data insertion error: {e}")

# Example usage:
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    conn = connect_to_airbnb_db()
    if conn:
        create_user_table(conn)
        insert_users_from_csv(conn, 'user_data.csv')  # Make sure this file exists in the same folder
        conn.close()
