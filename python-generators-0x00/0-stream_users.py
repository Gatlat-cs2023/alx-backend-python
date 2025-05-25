import mysql.connector


def stream_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Faithoverfear@1998",
        database="alx_airbnb_database"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
# Test
for user in stream_users():
    print(user)