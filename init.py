import mysql.connector
from mysql.connector import Error
from config import MYSQL_CONFIG
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a stream handler to log to console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Method to initialize the test database
def init_test_database():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host=MYSQL_CONFIG["host"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"]
        )
        cursor = connection.cursor()

        # Warn the user
        logger.warning("WARNING: This will drop the 'gestion_employes' database if it exists and recreate it. All data will be lost!")

        # Ask for confirmation
        confirmation = input("Are you sure you want to proceed? (yes/no): ")
        if confirmation.lower() != "yes":
            logger.info("Operation canceled by user.")
            return

        # Drop the database if it exists and create the new one
        cursor.execute("DROP DATABASE IF EXISTS gestion_employes;")
        cursor.execute("CREATE DATABASE IF NOT EXISTS gestion_employes;")
        cursor.execute("USE gestion_employes;")

        # Create the 'employes' table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employes (
            id INT PRIMARY KEY,
            nom VARCHAR(255) NOT NULL,
            prenom VARCHAR(255) NOT NULL,
            date_embauche DATE NOT NULL,
            poste VARCHAR(255) NOT NULL
        );
        """)

        # Create the 'enfants' table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS enfants (
            id INT PRIMARY KEY,
            employe_id INT NOT NULL,
            nom VARCHAR(255) NOT NULL,
            date_naissance DATE NOT NULL,
            indemnites DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (employe_id) REFERENCES employes(id) ON DELETE CASCADE
        );
        """)

        logger.info("Test database 'gestion_employes' and tables 'employes' and 'enfants' created successfully.")
        
        # Commit and close connection
        connection.commit()

    except Error as e:
        logger.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    init_test_database()
