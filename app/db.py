import psycopg2
import os

# Define database connection parameters
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

    # Define database initialization functions (create_tables_in_db, drop_tables_in_db, etc.)
    ...

    # Call the function to create tables
    create_tables_in_db()
    print("Tables created successfully")  # Debug message

except psycopg2.Error as e:
    print("Error: Unable to connect to the database:", e)  # Error message
