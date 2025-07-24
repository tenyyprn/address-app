#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
連絡先モデル
Contact Model
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from database.db_manager import DBManager
from utils.validator import Validator


class Contact:
    """連絡先クラス"""
    
    def __init__(self, name: str, furigana: str = "", address: str = "", 
                 phone: str = "", email: str = "", birthday: str = "", 
                 notes: str = "", image_path: str = ""):
        self.name = name
        self.furigana = furigana
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday
        self.notes = notes
        self.image_path = image_path


class ContactModel:
    """連絡先データモデル"""
    
    def __init__(self):
        self.db_manager = DBManager()
        self.validator = Validator()
        self.logger = logging.getLogger(__name__)
    
    def create(self, contact_data: Dict[str, Any]) -> Optional[int]:
        """新しい連絡先を作成"""
        try:
            # バリデーション
            if not self.validator.validate_contact(contact_data):
                raise ValueError("連絡先データが無効です")
            
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO contacts (name, furigana, address, phone, email, 
                                        birthday, notes, image_path, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (
                    contact_data.get('name', ''),
                    contact_data.get('furigana', ''),
                    contact_data.get('address', ''),
                    contact_data.get('phone', ''),
                    contact_data.get('email', ''),
                    contact_data.get('birthday', ''),
                    contact_data.get('notes', ''),
                    contact_data.get('image_path', '')
                ))
                
                contact_id = cursor.lastrowid
                self.logger.info(f"新しい連絡先を作成しました: ID {contact_id}")
                return contact_id
                
        except Exception as e:
            self.logger.error(f"連絡先作成エラー: {e}")
            raise
    
    def read(self, contact_id: int) -> Optional[Dict[str, Any]]:
        """指定IDの連絡先を取得"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return None
                
        except Exception as e:
            self.logger.error(f"連絡先取得エラー: {e}")
            return None
    
    def read_all(self) -> List[Dict[str, Any]]:
        """全ての連絡先を取得"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM contacts ORDER BY furigana, name')
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            self.logger.error(f"全連絡先取得エラー: {e}")
            return []
    
    def update(self, contact_id: int, contact_data: Dict[str, Any]) -> bool:
        """連絡先を更新"""
        try:
            if not self.validator.validate_contact(contact_data):
                raise ValueError("連絡先データが無効です")
            
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE contacts
                    SET name = ?, furigana = ?, address = ?, phone = ?, email = ?,
                        birthday = ?, notes = ?, image_path = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (
                    contact_data.get('name', ''),
                    contact_data.get('furigana', ''),
                    contact_data.get('address', ''),
                    contact_data.get('phone', ''),
                    contact_data.get('email', ''),
                    contact_data.get('birthday', ''),
                    contact_data.get('notes', ''),
                    contact_data.get('image_path', ''),
                    contact_id
                ))
                
                return cursor.rowcount > 0
                    
        except Exception as e:
            self.logger.error(f"連絡先更新エラー: {e}")
            raise
    
    def delete(self, contact_id: int) -> bool:
        """連絡先を削除"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
                return cursor.rowcount > 0
                    
        except Exception as e:
            self.logger.error(f"連絡先削除エラー: {e}")
            raise
    
    def search(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """連絡先を検索"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM contacts WHERE 1=1"
                params = []
                
                if 'keyword' in criteria and criteria['keyword']:
                    keyword = f"%{criteria['keyword']}%"
                    query += """ AND (name LIKE ? OR furigana LIKE ? OR 
                                     address LIKE ? OR phone LIKE ? OR 
                                     email LIKE ? OR notes LIKE ?)"""
                    params.extend([keyword] * 6)
                
                query += " ORDER BY furigana, name"
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            self.logger.error(f"連絡先検索エラー: {e}")
            return []
    
    @staticmethod
    def create_table():
        """テーブル作成（互換性のため）"""
        db_manager = DBManager()
        db_manager.initialize_tables()
