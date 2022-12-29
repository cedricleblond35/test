import mysql.connector

#https://pynative.com/python-mysql-database-connection/
# https://pynative.com/python-mysql-select-query-to-fetch-data/

# from mysql.connector import Error

# pip3 install mysql-connector
# https://dev.mysql.com/doc/connector-python/en/connector-python-reference.html

class dbQuery():
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="0.0.0.0",
            port=3310,
            user="root",
            passwd="MYsql",
            database="ASL")

    def query(self, sql, args):
        cursor = self.connection.cursor()
        cursor.execute(sql, args)
        return cursor

    def insert(self, sql, args):
        cursor = self.query(sql, args)
        id = cursor.lastrowid
        self.connection.commit()
        cursor.close()
        return id

    # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-executemany.html
    def insertmany(self, sql, args):
        cursor = self.connection.cursor()
        cursor.executemany(sql, args)
        rowcount = cursor.rowcount
        self.connection.commit()
        cursor.close()
        return rowcount

    def update(self, sql, args):
        cursor = self.query(sql, args)
        rowcount = cursor.rowcount
        self.connection.commit()
        cursor.close()
        return rowcount

    def fetch(self, sql, args):
        rows = []
        cursor = self.query(sql, args)
        if cursor.with_rows:
            rows = cursor.fetchall()
            print(rows)
        cursor.close()
        return rows

    def fetchone(self, sql, args):
        row = None
        cursor = self.query(sql, args)
        print(cursor.with_rows)
        print(cursor)
        if cursor.with_rows:
            row = cursor.fetchone()
            print("row :", row)
        
        
        for (name, lastname) in cursor:
            print("name :", name, lastname)
        
        
        
        
        
        
        
        
        
        cursor.close()
        return row

    def __del__(self):
        self.connection.close()