import mysql.connector
from mysql.connector import Error
import os

# DATABASE CREDENTIALS (Fill it)
DB_HOST = ''
DB_USERNAME = ''
DB_PASSWORD = ''
DB_PORT = ''

class DatabaseManager:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            port=DB_PORT,
            database=self.database_name,
        )

    def _ensure_connection(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect()

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def _execute(self, statement, values=None):
        self._ensure_connection()
        with self.connection:
            cursor = self.connection.cursor()
            if values:
                cursor.execute(statement, values)
            else:
                cursor.execute(statement)
            result = cursor.fetchall()
            if result:
                return result
            self.connection.commit()

    def create_table(self, table_name, columns):
        columns_with_types = [  
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items()
        ]
        self._execute(  
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            '''
        )

    def drop_table(self, table_name):
        self._execute(f'DROP TABLE {table_name};')


    def add(self, table_name, data):
        placeholders = ', '.join(['%s'] * len(data))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())

        self._execute(
            f'''
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            ''', 
            column_values
        )


    def delete(self, table_name, criteria):
        placeholders = [f'{column} = %s' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(
            f'''
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            ''',
            tuple(criteria.values()),
        )


    def select(self, table_name, criteria=None, order_by=None):
        criteria = criteria or {}

        query = f'SELECT * FROM {table_name}'

        if criteria:
            placeholders = [f'{column} = %s' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f' WHERE {select_criteria}'

        if order_by:
            query += f' ORDER BY {order_by}'

        return self._execute(
            query,
            tuple(criteria.values()),
        )

    def update(self, table_name, criteria, data):
        update_placeholders = [f'{column} = %s' for column in criteria.keys()]
        update_criteria = ' AND '.join(update_placeholders)

        data_placeholders = ', '.join(f'{key} = %s' for key in data.keys())

        values = tuple(data.values()) + tuple(criteria.values())

        self._execute(
            f'''
            UPDATE {table_name}
            SET {data_placeholders}
            WHERE {update_criteria};
            ''',
            values
        )

