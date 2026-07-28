import mysql.connector
from config import (
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE
)

def get_connection():
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    return connection

def get_cursor():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    return connection, cursor