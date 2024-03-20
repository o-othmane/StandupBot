import csv
import os
import psycopg2
import sys
from datetime import datetime

def connect_to_database():
    try:
        connection = psycopg2.connect(
            host=os.environ['HOST'],
            database=os.environ['DATABASE'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD']
        )
        connection.set_session(autocommit=True)
        return connection
    except psycopg2.OperationalError as e:
        print("Error connecting to the database:", e)
        sys.exit(1)

def execute_sql_query(connection, sql_query):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
    except psycopg2.Error as e:
        print("Error executing SQL query:", e)

def create_tables_in_db(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS standups
    (
        user_id     TEXT,
        date        DATE,
        yesterday   TEXT,
        today       TEXT,
        blocker     TEXT,
        channel     TEXT,
        modified_at TIMESTAMP DEFAULT NOW(),
        UNIQUE(user_id, date)
    );
    """
    execute_sql_query(connection, create_table_query)

def drop_tables_in_db(connection):
    drop_table_query = "DROP TABLE IF EXISTS standups;"
    execute_sql_query(connection, drop_table_query)

def upsert_today_standup_status(connection, user_id, channel=None, column_name=None, message=None):
    create_tables_in_db(connection)
    today = datetime.today().date()
    now = datetime.today()
    sql_query = """
    INSERT INTO standups (
        user_id,
        date,
        {column_name}
        {channel}
        modified_at
    )
    VALUES (%s, %s::DATE, %s, %s::TIMESTAMP)
    ON CONFLICT(user_id, date) DO UPDATE SET
        {column_conflict_clause}
        {channel_conflict_clause}
    ;
    """.format(
        column_name=f'{column_name},' if column_name else '',
        channel=f'channel,' if channel else '',
        column_conflict_clause=f'{column_name}=excluded.{column_name}' if column_name else '',
        channel_conflict_clause='channel=excluded.channel' if channel else ''
    )
    try:
        cursor = connection.cursor()
        if channel:
            cursor.execute(sql_query, (user_id, today, channel, now))
        else:
            cursor.execute(sql_query, (user_id, today, message, now))
    except psycopg2.Error as e:
        print("Error upserting standup status:", e)

def get_today_standup_status(connection, user_id):
    today = datetime.today()
    sql_query = """
    SELECT * FROM standups WHERE user_id=%s AND date=%s;
    """
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query, (user_id, today))
        return cursor.fetchone()
    except psycopg2.Error as e:
        print("Error fetching today's standup status:", e)

def generate_report(connection, username, start_date, end_date):
    sql_query = """
    SELECT * FROM standups
    WHERE user_id=%s
    AND date>=%s
    AND date<=%s;
    """
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query, (username, start_date, end_date))
        csv_filename = f'<@{username}>-standup-report.csv'
        with open(csv_filename, 'w+', newline='') as report:
            fieldnames = ['date', 'user_id', 'yesterday', 'today', 'blocker']
            writer = csv.writer(report)
            writer.writerow(fieldnames)
            for row in cursor.fetchall():
                writer.writerow([row[1], row[0], row[2], row[3], row[4]])
        return csv_filename
    except psycopg2.Error as e:
        print("Error generating report:", e)

if __name__ == "__main__":
    try:
        connection = connect_to_database()
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
    
    if len(sys.argv) > 1 and sys.argv[1] == "drop-tables":
        drop_tables_in_db(connection)

    create_tables_in_db(connection)
