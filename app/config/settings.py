#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定管理モジュール
Configuration Management Module
"""

import configparser
import os
from typing import Dict, Any
import logging


# デフォルト設定
DEFAULT_CONFIG = {
    'Database': {
        'path': './data/address_book.db',
        'backup_interval': '24'
    },
    'Display': {
        'theme': 'light',
        'font_size': '12',
        'language': 'ja'
    },
    'Backup': {
        'auto_backup': 'true',
        'backup_path': './backups'
    },
    'Logging': {
        'level': 'INFO',
        'path': './logs'
    }
}

# データベースパス
DATABASE_PATH = './data/address_book.db'


class Settings:
    """設定管理クラス"""
    
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(__name__)
        self.load_settings()
    
    def load_settings(self):
        """設定ファイルを読み込む"""
        try:
            if os.path.exists(self.config_file):
                self.config.read(self.config_file, encoding='utf-8')
                self.logger.info(f"設定ファイルを読み込みました: {self.config_file}")
            else:
                self.logger.info("設定ファイルが見つかりません。デフォルト設定を作成します。")
                self.create_default_config()
        except Exception as e:
            self.logger.error(f"設定ファイル読み込みエラー: {e}")
            self.create_default_config()
    
    def create_default_config(self):
        """デフォルト設定ファイルを作成"""
        try:
            for section, options in DEFAULT_CONFIG.items():
                self.config.add_section(section)
                for key, value in options.items():
                    self.config.set(section, key, value)
            
            self.save_settings()
            self.logger.info("デフォルト設定ファイルを作成しました。")
        except Exception as e:
            self.logger.error(f"デフォルト設定作成エラー: {e}")
    
    def save_settings(self):
        """設定をファイルに保存"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            self.logger.info("設定を保存しました。")
        except Exception as e:
            self.logger.error(f"設定保存エラー: {e}")
    
    def get(self, section: str, key: str, fallback: str = None) -> str:
        """設定値を取得"""
        try:
            return self.config.get(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def set(self, section: str, key: str, value: str):
        """設定値を設定"""
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, key, value)
        except Exception as e:
            self.logger.error(f"設定値設定エラー: {e}")
    
    def get_database_path(self) -> str:
        """データベースパスを取得"""
        return self.get('Database', 'path', './data/address_book.db')
    
    def get_backup_path(self) -> str:
        """バックアップパスを取得"""
        return self.get('Backup', 'backup_path', './backups')
    
    def get_language(self) -> str:
        """言語設定を取得"""
        return self.get('Display', 'language', 'ja')
    
    def get_theme(self) -> str:
        """テーマ設定を取得"""
        return self.get('Display', 'theme', 'light')
    
    def get_font_size(self) -> int:
        """フォントサイズを取得"""
        try:
            return int(self.get('Display', 'font_size', '12'))
        except ValueError:
            return 12
    
    def is_auto_backup_enabled(self) -> bool:
        """自動バックアップが有効かチェック"""
        return self.get('Backup', 'auto_backup', 'true').lower() == 'true'
    
    def get_backup_interval(self) -> int:
        """バックアップ間隔（時間）を取得"""
        try:
            return int(self.get('Database', 'backup_interval', '24'))
        except ValueError:
            return 24
    
    def get_all_settings(self) -> Dict[str, Dict[str, str]]:
        """全設定を辞書形式で取得"""
        result = {}
        for section_name in self.config.sections():
            result[section_name] = dict(self.config.items(section_name))
        return result
