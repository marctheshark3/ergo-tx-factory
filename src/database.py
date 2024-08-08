# database.py

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

class PostgresDB:
    def __init__(self):
        load_dotenv()

        # Use environment variables, with fallback to Docker-specific values
        self.db_name = os.getenv('DB_NAME', 'SIGS-CORE')
        self.user = os.getenv('DB_USER', 'sigs_user')
        self.password = os.getenv('DB_PASSWORD', 'sigs_password')
        self.host = os.getenv('DB_HOST', 'db')  # 'db' is the service name in docker-compose
        self.port = os.getenv('DB_PORT', '5432')

    def connect(self):
        return psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def create_db(self):
        conn = psycopg2.connect(
            dbname='postgres',
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(self.db_name)))
        cur.close()
        conn.close()

    def delete_db(self):
        conn = psycopg2.connect(
            dbname='postgres',
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(self.db_name)))
        cur.close()
        conn.close()

    def create_table(self, table_name, columns):
        conn = self.connect()
        cur = conn.cursor()
        column_definitions = ', '.join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
        cur.execute(sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(column_definitions)
        ))
        conn.commit()
        cur.close()
        conn.close()

    def delete_table(self, table_name):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(
            sql.Identifier(table_name)))
        conn.commit()
        cur.close()
        conn.close()

    def insert_data(self, table_name, data):
        conn = self.connect()
        cur = conn.cursor()
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        cur.execute(sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(columns),
            sql.SQL(values)
        ), list(data.values()))
        conn.commit()
        cur.close()
        conn.close()

    def fetch_data(self, table_name, conditions=None):
        conn = self.connect()
        cur = conn.cursor()
        query = f"SELECT * FROM {table_name}"
        if conditions:
            where_clauses = []
            values = []
            for k, v in conditions.items():
                if v.startswith('>') or v.startswith('<'):
                    where_clauses.append(f"{k} {v[0]} %s")
                    values.append(v[1:])
                else:
                    where_clauses.append(f"{k} = %s")
                    values.append(v)
            query += " WHERE " + " AND ".join(where_clauses)
        else:
            values = None
        cur.execute(query, values)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_column_names(self, table_name):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} LIMIT 0")
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        return column_names

    def execute_query(self, query):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()