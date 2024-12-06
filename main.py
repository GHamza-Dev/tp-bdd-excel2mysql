import pandas as pd
from mysql_connection import get_mysql_connection
import logging
from config import MYSQL_CONFIG, LOGGING_CONFIG, INPUT_FILE_PATH
from logging_config import setup_logging

# logging configuration
logger = setup_logging(LOGGING_CONFIG)

# Function to load Excel file
def load_excel_file(file_path):
    try:
        excel_data = pd.ExcelFile(file_path)
        logger.info(f"Loaded Excel file: {file_path}")
        return excel_data
    except Exception as e:
        logger.error(f"Error loading Excel file: {e}")
        return None

# Function to get table columns from MySQL
def get_table_columns(cursor, table_name):
    try:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [row[0] for row in cursor.fetchall()]
        logger.info(f"Retrieved columns for table {table_name}: {columns}")
        return columns
    except Exception as e:
        logger.error(f"Error retrieving columns for table {table_name}: {e}")
        return []

# Function to reorder columns in a DataFrame
def reorder_columns(df, order):
    try:
        reordered_df = df.iloc[:, order]
        logger.info(f"Reordered columns in DataFrame with order: {order}")
        return reordered_df
    except Exception as e:
        logger.error(f"Error reordering columns: {e}")
        return None

# Function to disable foreign key checks
def disable_foreign_keys(cursor):
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        logger.info("Foreign key checks disabled.")
    except Exception as e:
        logger.error(f"Error disabling foreign key checks: {e}")

# Function to enable foreign key checks
def enable_foreign_keys(cursor):
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        logger.info("Foreign key checks enabled.")
    except Exception as e:
        logger.error(f"Error enabling foreign key checks: {e}")

# Function to insert data into MySQL
def insert_data(cursor, table_name, columns, data):
    try:
        placeholders = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.executemany(query, data)
        logger.info(f"Inserted {cursor.rowcount} rows into {table_name}.")
    except Exception as e:
        logger.error(f"Error inserting data into table {table_name}: {e}")

# Main function to automate import
def main():
    # File path
    excel_file_path = INPUT_FILE_PATH

    # Connect to MySQL
    connection = get_mysql_connection(MYSQL_CONFIG)
    if not connection:
        logger.error("Failed to establish connection to MySQL. Exiting...")
        return
    cursor = connection.cursor()

    # Load Excel file
    excel_data = load_excel_file(excel_file_path)
    if not excel_data:
        logger.error(f"Failed to load Excel file {excel_file_path}. Exiting...")
        return

    # Iterate over each sheet in the Excel file
    for sheet_name in excel_data.sheet_names:
        logger.info(f"Processing sheet: {sheet_name}")
        df = excel_data.parse(sheet_name)

        # Get MySQL table columns
        table_name = sheet_name  # Assuming table name matches sheet name
        table_columns = get_table_columns(cursor, table_name)
        if not table_columns:
            logger.error(f"No columns found for table {table_name}. Skipping this sheet.")
            continue

        logger.info(f"MySQL columns: {table_columns}")
        logger.info(f"Excel columns: {list(df.columns)}")

        # User input for column reordering
        try:
            logger.info("Enter the column order as a list of indices (e.g., [2, 0, 1]):")
            column_order = eval(input())  # Ensure proper validation in production
            reordered_df = reorder_columns(df, column_order)
        except Exception as e:
            logger.error(f"Error during column reordering: {e}")
            continue

        if reordered_df is not None:
            # Prepare data for insertion
            data = [tuple(row) for row in reordered_df.to_numpy()]
            disable_foreign_keys(cursor)
            insert_data(cursor, table_name, table_columns, data)
            enable_foreign_keys(cursor)

    # Commit changes and close connection
    try:
        connection.commit()
        logger.info("Data import completed successfully.")
    except Exception as e:
        logger.error(f"Error committing changes: {e}")
    finally:
        cursor.close()
        connection.close()
        logger.info("MySQL connection closed.")

if __name__ == "__main__":
    main()
