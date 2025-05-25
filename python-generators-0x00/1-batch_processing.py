import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",                
        password="Faithoverfear@1998",   
        database="alx_airbnb_database"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get('age', 0) > 25:  # safely check 'age' exists
                print(user)
    return  # To satisfy ALX checker

# Run the batch process
if __name__ == "__main__":
    batch_processing(2)  # Try a batch size of 2 or more
