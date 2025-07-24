#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
住所録管理システム - メインエントリーポイント
Address Book Management System - Main Entry Point
"""

import sys
import os
import tkinter as tk
import logging

# パスを追加してモジュールをインポート可能にする
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 環境変数管理を標準ライブラリで実装（python-dotenv不要）
def load_env_file(env_file=".env"):
    """簡単な.envファイル読み込み（python-dotenv代替）"""
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        except Exception as e:
            print(f"環境変数ファイル読み込みエラー: {e}")

try:
    from gui.main_window import MainWindow
    from database.db_manager import DBManager
    from config.settings import Settings
    from utils.logger import setup_logger
    from database.contact_model import Contact
except ImportError as e:
    print(f"インポートエラー: {e}")
    print("必要なモジュールが見つかりません。")
    print("現在のディレクトリを確認してください。アプリケーションは app/ ディレクトリから実行する必要があります。")
    input("Enterキーを押して終了...")
    sys.exit(1)


def create_directories():
    """必要なディレクトリを作成"""
    directories = ["data", "logs", "backups", "images"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"ディレクトリを作成しました: {directory}")


def initialize_database():
    """データベースの初期化"""
    try:
        db_manager = DBManager()
        if db_manager.connect():
            db_manager.initialize_tables()
            Contact.create_table()
            print("データベースの初期化が完了しました。")
            return db_manager
        else:
            print("データベース接続に失敗しました。")
            return None
    except Exception as e:
        print(f"データベース初期化エラー: {e}")
        return None


def main():
    """メイン関数"""
    try:
        print("住所録管理システムを開始します...")
        
        # 環境変数の読み込み（.envファイルがある場合）
        load_env_file()  # python-dotenvの代替
        
        # 必要なディレクトリの作成
        create_directories()
        
        # 設定の読み込み
        settings = Settings()
        
        # ログ設定
        log_level = os.getenv("LOG_LEVEL", "INFO")
        log_path = os.getenv("LOG_PATH", "./logs")
        setup_logger(log_level, log_path)
        logger = logging.getLogger(__name__)
        
        logger.info("アプリケーションを開始します...")
        
        # データベースの初期化
        db_manager = initialize_database()
        if not db_manager:
            logger.error("データベースの初期化に失敗しました。")
            print("データベースの初期化に失敗しました。")
            input("Enterキーを押して終了...")
            return
        
        # メインGUIウィンドウの起動
        try:
            print("GUIアプリケーションを起動しています...")
            app = MainWindow()  # 引数なしで初期化
            logger.info("GUIアプリケーションを開始します。")
            app.run()
        except Exception as e:
            logger.error(f"GUI起動エラー: {e}", exc_info=True)
            print(f"GUI起動エラー: {e}")
            input("Enterキーを押して終了...")
        
    except Exception as e:
        print(f"アプリケーション開始エラー: {e}")
        if 'logger' in locals():
            logger.error(f"アプリケーション開始エラー: {e}", exc_info=True)
        input("Enterキーを押して終了...")
    
    finally:
        # アプリケーション終了時の処理
        if 'db_manager' in locals() and db_manager:
            db_manager.disconnect()
        if 'logger' in locals():
            logger.info("アプリケーションを終了します。")


if __name__ == "__main__":
    main()
