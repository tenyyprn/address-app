import sqlite3
import os
from src.app.config.settings import DATABASE_PATH
from src.app.utils.logger import Logger

class DBManager:
    def __init__(self):
        self.connection = None
        self.logger = Logger()

    def connect(self):
        try:
            if not os.path.exists(DATABASE_PATH):
                self.logger.error("Database file does not exist.")
                return False
            self.connection = sqlite3.connect(DATABASE_PATH)
            self.logger.info("Database connected successfully.")
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Error connecting to database: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed.")

    def initialize_tables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                address TEXT,
                                phone TEXT,
                                email TEXT)''')
            self.connection.commit()
            self.logger.info("Tables initialized successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Error initializing tables: {e}")

    def backup_database(self, backup_path):
        try:
            with open(backup_path, 'w') as backup_file:
                for line in self.connection.iterdump():
                    backup_file.write(f'{line}\n')
            self.logger.info("Database backup completed.")
        except Exception as e:
            self.logger.error(f"Error during backup: {e}")

    def restore_database(self, backup_path):
        try:
            with open(backup_path, 'r') as backup_file:
                sql_script = backup_file.read()
            self.connection.executescript(sql_script)
            self.connection.commit()
            self.logger.info("Database restored successfully.")
        except Exception as e:
            self.logger.error(f"Error during restore: {e}")

    def optimize_database(self):
        try:
            self.connection.execute("VACUUM")
            self.logger.info("Database optimized.")
        except sqlite3.Error as e:
            self.logger.error(f"Error optimizing database: {e}")

    def migrate(self, migration_script):
        try:
            self.connection.executescript(migration_script)
            self.connection.commit()
            self.logger.info("Migration completed successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Error during migration: {e}")

    def execute_transaction(self, queries):
        try:
            cursor = self.connection.cursor()
            for query in queries:
                cursor.execute(query)
            self.connection.commit()
            self.logger.info("Transaction executed successfully.")
        except sqlite3.Error as e:
            self.connection.rollback()
            self.logger.error(f"Error during transaction: {e}")
