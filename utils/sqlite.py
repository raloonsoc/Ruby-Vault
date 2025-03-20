import sqlite3
import os

class SQLite():
    def __init__(self):
        self.database = None
        self.cursor = None
    
    def connect_database(self, name):
        try:
            connect = sqlite3.connect(f'./databases/{name}.db')
            self.database = connect
            self.cursor = connect.cursor()
        except sqlite3.Error:
            pass
    def create_database(self, name):
        try:
            # Creating directory
            os.makedirs('./databases', exist_ok=True)
            # Checking the existence of the database
            db_path = f'./databases/{name}.db'
            if os.path.exists(db_path):
                return False
            
            # Connect to the database
            connect = sqlite3.connect(f'./databases/{name}.db')
            # Create the database and initialize the table
            self.database = connect
            self.cursor = connect.cursor()
            cursor = connect.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, secret TEXT NOT NULL)")
            cursor.execute("CREATE TABLE IF NOT EXISTS master (id INTEGER PRIMARY KEY AUTOINCREMENT, salt BLOB NOT NULL, verifier TEXT NOT NULL)")
            return True
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False
    
    def insert_data(self, name, secret):
        try:
            if self.database is None or self.cursor is None:
                print("No database connection. Please connect to a database first.")
                return False
            self.cursor.execute("INSERT INTO secrets (name, secret) VALUES (?, ?)", (name, secret))
            self.database.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while inserting data: {e}")
            return False
    def view_data(self):
        try:
            if self.database is None or self.cursor is None:
                print("No database connection. Please connect to a database first.")
                return None
            self.cursor.execute("SELECT id,name FROM secrets")
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"An error occurred while viewing data: {e}")
            return None
    def save_master_to_db(self, salt, verifier):
        self.cursor.execute("INSERT INTO master (salt, verifier) VALUES (?, ?)", (salt,verifier,))
        self.database.commit()

    def get_master_from_db(self):
        self.cursor.execute("SELECT salt,verifier FROM master")
        result = self.cursor.fetchone()
        if result:
            return result[0], result[1]
        else:
            return None
    def get_password(self, id):
        self.cursor.execute("SELECT secret FROM secrets WHERE id = (?)", (id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    def delete_database(self, name):
        try:
            self.exit()
            os.remove(f'./databases/{name}.db')
            return True
        except Exception:
            return False
    def exit(self):
        self.database.close()
        return True