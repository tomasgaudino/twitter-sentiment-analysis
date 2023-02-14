import psycopg2
from dotenv import load_dotenv
import os
import time

load_dotenv()


class Database:
    def __init__(self, db_name, db_user, db_password, db_host, db_port, max_retries, retry_interval):
        self.dbname = db_name
        self.user = db_user
        self.password = db_password
        self.host = db_host
        self.port = db_port
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.conn = None

        # Attempt to connect to the connector up to max_retries times
        for i in range(max_retries):
            try:
                self.conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                break
            except psycopg2.OperationalError as e:
                print(f"Error connecting to database: {e}")
                if i < max_retries - 1:
                    print(f"Retrying in {retry_interval} seconds...")
                    time.sleep(retry_interval)
        else:
            raise Exception(f"Could not connect to database after {max_retries} attempts")

        self.cur = self.conn.cursor()
        self.create_table()

    def insert_tweets(self, tweets):
        # TODO: Batch insert tweets into the connector. Need to know schema
        self.conn.commit()

    def create_table(self):
        # TODO: Define tables and schemas
        # TODO: Create table if missing. Else skip
        pass

    def disconnect(self):
        self.cur.close()
        self.conn.close()
