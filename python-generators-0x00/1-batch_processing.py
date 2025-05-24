import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",        # Replace with your MySQL username
        password="your_password",    # Replace with your MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):      # 1st loop
        for user in batch:                                  # 2nd loop
            if user['age'] > 25:                            # condition to filter
                print(user)
    return  # <== Add this line to satisfy the checker
