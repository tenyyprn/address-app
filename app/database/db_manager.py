#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
データベース管理モジュール
Database Management Module
"""

import sqlite3
import os
import threading
import logging
from contextlib import contextmanager
from config.settings import Settings


class DBManager:
    """データベース管理クラス"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """シングルトンパターンの実装"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.settings = Settings()
        self.db_path = self.settings.get_database_path()
        self.connection = None
        self.logger = logging.getLogger(__name__)
        self._initialized = True
    
    def connect(self):
        """データベースに接続"""
        try:
            # データベースディレクトリの作成
            db_dir = os.path.dirname(self.db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=30.0
            )
            self.connection.row_factory = sqlite3.Row
            
            # 外部キー制約を有効化
            self.connection.execute("PRAGMA foreign_keys = ON")
            
            self.logger.info(f"データベースに接続しました: {self.db_path}")
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"データベース接続エラー: {e}")
            return False
    
    def disconnect(self):
        """データベース接続を切断"""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.logger.info("データベース接続を切断しました。")
            except sqlite3.Error as e:
                self.logger.error(f"データベース切断エラー: {e}")
    
    @contextmanager
    def get_connection(self):
        """コンテキストマネージャーでデータベース接続を取得"""
        if not self.connection:
            if not self.connect():
                raise sqlite3.Error("データベース接続に失敗しました")
        
        try:
            yield self.connection
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"データベース操作エラー: {e}")
            raise
        else:
            self.connection.commit()
    
    def initialize_tables(self):
        """テーブルの初期化"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # contactsテーブルの作成
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        furigana TEXT,
                        address TEXT,
                        phone TEXT,
                        email TEXT,
                        birthday DATE,
                        notes TEXT,
                        image_path TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # インデックスの作成
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_furigana ON contacts(furigana)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_phone ON contacts(phone)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email)')
                
                # 設定テーブルの作成
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS app_settings (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                self.logger.info("データベーステーブルの初期化が完了しました。")
                
        except sqlite3.Error as e:
            self.logger.error(f"テーブル初期化エラー: {e}")
            raise
    
    def backup_database(self, backup_path=None):
        """データベースのバックアップ"""
        if not backup_path:
            backup_dir = self.settings.get_backup_path()
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f'address_book_backup_{timestamp}.sql')
        
        try:
            with self.get_connection() as conn:
                with open(backup_path, 'w', encoding='utf-8') as backup_file:
                    for line in conn.iterdump():
                        backup_file.write(f'{line}\n')
            
            self.logger.info(f"データベースバックアップが完了しました: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"バックアップエラー: {e}")
            raise
    
    def restore_database(self, backup_path):
        """データベースの復元"""
        try:
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"バックアップファイルが見つかりません: {backup_path}")
            
            with self.get_connection() as conn:
                with open(backup_path, 'r', encoding='utf-8') as backup_file:
                    sql_script = backup_file.read()
                conn.executescript(sql_script)
            
            self.logger.info(f"データベース復元が完了しました: {backup_path}")
            
        except Exception as e:
            self.logger.error(f"復元エラー: {e}")
            raise
    
    def optimize_database(self):
        """データベースの最適化"""
        try:
            with self.get_connection() as conn:
                conn.execute("VACUUM")
                conn.execute("ANALYZE")
            
            self.logger.info("データベースの最適化が完了しました。")
            
        except sqlite3.Error as e:
            self.logger.error(f"最適化エラー: {e}")
            raise
    
    def get_database_info(self):
        """データベース情報を取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # テーブル一覧取得
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                # レコード数取得
                table_info = {}
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    table_info[table] = count
                
                # データベースファイルサイズ
                file_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                
                return {
                    'path': self.db_path,
                    'size': file_size,
                    'tables': table_info
                }
                
        except Exception as e:
            self.logger.error(f"データベース情報取得エラー: {e}")
            return None
