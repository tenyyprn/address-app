#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ロガー設定モジュール
Logger Configuration Module
"""

import logging
import logging.handlers
import os
from datetime import datetime


def setup_logger(log_level="INFO", log_path="./logs"):
    """
    ロガーの設定を行う
    
    Args:
        log_level (str): ログレベル (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_path (str): ログファイルの保存パス
    """
    # ログディレクトリの作成
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    
    # ログレベルの設定
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    # ログフォーマットの設定
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # ルートロガーの設定
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # 既存のハンドラーをクリア
    root_logger.handlers.clear()
    
    # コンソールハンドラーの設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # ファイルハンドラーの設定（日付ごとにローテーション）
    log_filename = os.path.join(log_path, f"address_book_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=30,  # 30日分保持
        encoding='utf-8'
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # エラーログファイルハンドラー
    error_log_filename = os.path.join(log_path, f"error_{datetime.now().strftime('%Y%m%d')}.log")
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_filename,
        maxBytes=10*1024*1024,
        backupCount=30,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    logging.info(f"ログ設定が完了しました。レベル: {log_level}, パス: {log_path}")


class Logger:
    """
    ロガークラス - 下位互換性のため
    """
    def __init__(self, name=None):
        self.logger = logging.getLogger(name or __name__)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)
