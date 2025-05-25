#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator to stream user ages from the database."""
    connection = seed.connect_to_airbnb_db()  # updated connection function
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user")  # updated table name
    
    try:
        for row in cursor:
            yield row['age']
    finally:
        cursor.close()
        connection.close()

def calculate_average_age():
    """Calculate the average age using the stream_user_ages generator."""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        if age is not None:
            total_age += age
            count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found")

# Run the function
if __name__ == "__main__":
    calculate_average_age()
