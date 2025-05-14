# 🧬 Seed Script – User Data Seeding to MySQL

## 📁 Directory: `python-generators-0x00`
This script is part of the **ALX Backend Python Track** and handles:
- Database connection
- Creating a MySQL database and table
- Populating data from a CSV file

---

## 📦 Files

- `seed.py`: Python script to create database, table, and insert user data.
- `user_data.csv`: CSV file with user records.
- `0-main.py`: Main entry to execute the seed operations.

---

## 🧪 Features

- Creates database `ALX_prodev` if not existing.
- Creates table `user_data` with fields:
  - `user_id` (UUID, PK, Indexed)
  - `name` (VARCHAR)
  - `email` (VARCHAR)
  - `age` (DECIMAL)
- Prevents duplicate entries based on email.
- Loads data from `user_data.csv`.

---

## 🛠️ Function Prototypes

```python
def connect_db() -> mysql.connector.connection: 
    # Connects to MySQL server

def create_database(connection): 
    # Creates ALX_prodev database

def connect_to_prodev() -> mysql.connector.connection: 
    # Connects to ALX_prodev DB

def create_table(connection): 
    # Creates user_data table

def insert_data(connection, filename): 
    # Inserts data from CSV into DB
```

## 🚀 Usage
```bash
$ chmod +x 0-main.py
$ ./0-main.py
```

Expected Output:
```text
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('uuid1', 'name1', 'email1', age), ...]
```

## 🧩 Requirements

- Python 3.x
- `mysql-connector-python`:
```bash
pip install mysql-connector-python
```

## 📌 Notes
- Ensure MySQL server is running and credentials in `seed.py` are valid
- Place `user_data.csv` in the same directory as `seed.py`
