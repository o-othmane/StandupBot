import csv
import os
import psycopg2
import sys
from datetime import datetime

# Database connection parameters
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Connect to the database
try:
    CON = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    CON.set_session(autocommit=True)
    CURSOR = CON.cursor()
    print("Connected to the database successfully")  # Debug message

    # Define database initialization functions
    def create_tables_in_db():
        ...
        # Your existing code to create tables goes here
        ...

    def drop_tables_in_db():
        ...
        # Your existing code to drop tables goes here
        ...

    # Call the function to create tables
    create_tables_in_db()
    print("Tables created successfully")  # Debug message

except psycopg2.Error as e:
    print("Error: Unable to connect to the database:", e)  # Error message
    sys.exit(1)

# Define other database-related functions
...

# Your existing database-related functions go here
...

# Your existing main application code goes here
...
