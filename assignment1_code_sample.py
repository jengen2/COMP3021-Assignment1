import os
import pymysql
import subprocess
import requests
import re

# Use environment variables instead of hardcoded credentials
db_config = {
    'host': os.getenv('DB_HOST', 'default_host'),
    'user': os.getenv('DB_USER', 'default_user'),
    'password': os.getenv('DB_PASSWORD', 'default_password')
}

def get_user_input():
    user_input = input('Enter your name: ').strip()
    if not re.match("^[a-zA-Z ]{1,50}$", user_input):  # Allow only letters and spaces
        print("Invalid input. Please enter a valid name.")
        return None
    return user_input

def send_email(to, subject, body):
    subprocess.run(["mail", "-s", subject, to], input=body.encode(), check=True)

def get_data():
    url = 'https://secure-api.com/get-data'  # Ensure HTTPS
    try:
        response = requests.get(url, timeout=5)  # Add timeout
        response.raise_for_status()  # Raise error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None  # Return None if the request fails

def save_to_db(data):
    if data is None:  # Avoid inserting None values
        print("No data to save.")
        return

    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query, (data, 'Another Value'))
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    if user_input:  # Only proceed if input is valid
        data = get_data()
        save_to_db(data)
        send_email('admin@example.com', 'User Input', user_input)
