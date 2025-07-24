import sqlite3
from src.app.database.db_manager import DBManager
from src.app.utils.validator import Validator

class Contact:
    def __init__(self, name, kana, address, phone, email, birthday, notes):
        self.name = name
        self.kana = kana
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday
        self.notes = notes

    @staticmethod
    def create_table():
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    kana TEXT,
                    address TEXT,
                    phone TEXT,
                    email TEXT,
                    birthday TEXT,
                    notes TEXT
                )
            ''')
            conn.commit()

    @staticmethod
    def add_contact(contact):
        if not Validator.validate_contact(contact):
            raise ValueError("Invalid contact data")
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contacts (name, kana, address, phone, email, birthday, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (contact.name, contact.kana, contact.address, contact.phone, contact.email, contact.birthday, contact.notes))
            conn.commit()

    @staticmethod
    def get_contact(contact_id):
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
            return cursor.fetchone()

    @staticmethod
    def update_contact(contact_id, contact):
        if not Validator.validate_contact(contact):
            raise ValueError("Invalid contact data")
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE contacts
                SET name = ?, kana = ?, address = ?, phone = ?, email = ?, birthday = ?, notes = ?
                WHERE id = ?
            ''', (contact.name, contact.kana, contact.address, contact.phone, contact.email, contact.birthday, contact.notes, contact_id))
            conn.commit()

    @staticmethod
    def delete_contact(contact_id):
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            conn.commit()

    @staticmethod
    def search_contacts(query):
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM contacts WHERE name LIKE ?', ('%' + query + '%',))
            return cursor.fetchall()

    @staticmethod
    def serialize(contact):
        return {
            'name': contact.name,
            'kana': contact.kana,
            'address': contact.address,
            'phone': contact.phone,
            'email': contact.email,
            'birthday': contact.birthday,
            'notes': contact.notes
        }

    @staticmethod
    def check_duplicate(contact):
        with DBManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM contacts WHERE name = ? AND phone = ?', (contact.name, contact.phone))
            return cursor.fetchone() is not None