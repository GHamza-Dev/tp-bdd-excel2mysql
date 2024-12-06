from mysql.connector import connect, Error
import logging

# Function to establish MySQL connection
def get_mysql_connection(config):
    try:
        connection = connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"]
        )
        logging.info("Connection to MySQL established!")
        return connection
    except Error as e:
        logging.error(f"Error: {e}")
        return None
