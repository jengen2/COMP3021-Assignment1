import os
import pymysql
from urllib.request import urlopen

db_config = {
    'host': 'mydatabase.com',
    'user': 'admin',
    'password': 'secret123'
} #This db_config file has sensitive data not encrypted and literally hardcoded into it. This is just a major free pass to any attacker to easily get admin privilages for this data.
  #This falls under Identification and Authentication Failures category for the OWASP top 10. The way to remedy this is to take it out of the code and store this information in environment variables or a secrets management service.

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

def send_email(to, subject, body):
    os.system(f'echo {body} | mail -s "{subject}" {to}')
# The function above is not secure as it uses os.system to execute user input directly which can lead to malicious attacks. This would be known as command injection and is part of the Injection category in the OWASP top 10
# The fix for this would be to have some security checks in place before the user input gets executed by os.system. Or even ditch os.system and use an email library from python to do this.

def get_data():
    url = 'http://insecure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data

def save_to_db(data): 
    query = f"INSERT INTO mytable (column1, column2) VALUES ('{data}', 'Another Value')"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
# The above function opens up the door for possible SQL injection. For the OWASP top 10 this falls under the injection category
# To mitigate against the SQL injection do not have the query execute whatever is in there without doing checks to make sure it follows the format we want and includes the data we expect.

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
