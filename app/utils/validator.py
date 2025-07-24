#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
バリデーションユーティリティ
Validation Utilities
"""

import re
import logging
from typing import Dict, Any, List, Tuple


class Validator:
    """データバリデーションクラス"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_contact(self, contact_data: Dict[str, Any]) -> bool:
        """連絡先データのバリデーション"""
        try:
            # 必須フィールドのチェック
            if not contact_data.get('name', '').strip():
                self.logger.warning("名前が入力されていません")
                return False
            
            # 名前の長さチェック
            if len(contact_data.get('name', '')) > 100:
                self.logger.warning("名前が長すぎます（100文字以内）")
                return False
            
            # メールアドレスのバリデーション
            email = contact_data.get('email', '').strip()
            if email and not self.validate_email(email):
                self.logger.warning(f"無効なメールアドレス: {email}")
                return False
            
            # 電話番号のバリデーション
            phone = contact_data.get('phone', '').strip()
            if phone and not self.validate_phone(phone):
                self.logger.warning(f"無効な電話番号: {phone}")
                return False
            
            # 生年月日のバリデーション
            birthday = contact_data.get('birthday', '').strip()
            if birthday and not self.validate_date(birthday):
                self.logger.warning(f"无效な生年月日: {birthday}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"バリデーションエラー: {e}")
            return False
    
    def validate_email(self, email: str) -> bool:
        """メールアドレスのバリデーション"""
        if not email:
            return True  # 空の場合は有効とする
        
        # RFC 5322準拠の簡単なパターン
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email.strip()) is not None
    
    def validate_phone(self, phone: str) -> bool:
        """電話番号のバリデーション"""
        if not phone:
            return True  # 空の場合は有効とする
        
        # 日本の電話番号パターン（ハイフン有り無し対応）
        patterns = [
            r'^\d{2,4}-\d{2,4}-\d{4}$',  # 03-1234-5678形式
            r'^\d{10,11}$',               # 03123456789形式
            r'^\+81-\d{1,4}-\d{2,4}-\d{4}$',  # +81-3-1234-5678形式
            r'^0\d{9,10}$'                # 0312345678形式
        ]
        
        phone_clean = phone.strip()
        return any(re.match(pattern, phone_clean) for pattern in patterns)
    
    def validate_date(self, date_str: str) -> bool:
        """日付のバリデーション"""
        if not date_str:
            return True  # 空の場合は有効とする
        
        # 複数の日付フォーマットに対応
        patterns = [
            r'^\d{4}-\d{2}-\d{2}$',      # YYYY-MM-DD
            r'^\d{4}/\d{2}/\d{2}$',      # YYYY/MM/DD
            r'^\d{2}/\d{2}/\d{4}$',      # MM/DD/YYYY
            r'^\d{4}\.\d{2}\.\d{2}$',    # YYYY.MM.DD
            r'^\d{4}年\d{1,2}月\d{1,2}日$'  # YYYY年M月D日
        ]
        
        date_clean = date_str.strip()
        if not any(re.match(pattern, date_clean) for pattern in patterns):
            return False
        
        # 実際の日付として有効かチェック
        try:
            from datetime import datetime
            
            # 各フォーマットでパース試行
            formats = [
                '%Y-%m-%d',
                '%Y/%m/%d',
                '%m/%d/%Y',
                '%Y.%m.%d'
            ]
            
            for fmt in formats:
                try:
                    datetime.strptime(date_clean, fmt)
                    return True
                except ValueError:
                    continue
            
            # 日本語形式の場合
            if '年' in date_clean and '月' in date_clean and '日' in date_clean:
                # YYYY年M月D日 形式を YYYY-MM-DD に変換
                import re
                match = re.match(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_clean)
                if match:
                    year, month, day = match.groups()
                    try:
                        datetime(int(year), int(month), int(day))
                        return True
                    except ValueError:
                        return False
            
            return False
            
        except Exception:
            return False
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, List[str]]:
        """必須フィールドのバリデーション"""
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                missing_fields.append(field)
        
        return len(missing_fields) == 0, missing_fields
    
    def validate_string_length(self, text: str, max_length: int, field_name: str = "") -> bool:
        """文字列長のバリデーション"""
        if len(text) > max_length:
            self.logger.warning(f"{field_name}が長すぎます（{max_length}文字以内）: {len(text)}文字")
            return False
        return True
    
    def sanitize_input(self, text: str) -> str:
        """入力文字列のサニタイズ"""
        if not isinstance(text, str):
            text = str(text)
        
        # 改行文字を統一
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # 前後の空白を削除
        text = text.strip()
        
        # 制御文字を除去（改行とタブは保持）
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
        
        return text
    
    def get_validation_errors(self, contact_data: Dict[str, Any]) -> List[str]:
        """バリデーションエラーのリストを取得"""
        errors = []
        
        try:
            # 名前チェック
            name = contact_data.get('name', '').strip()
            if not name:
                errors.append("名前は必須です")
            elif len(name) > 100:
                errors.append("名前は100文字以内で入力してください")
            
            # メールアドレスチェック
            email = contact_data.get('email', '').strip()
            if email and not self.validate_email(email):
                errors.append("メールアドレスの形式が正しくありません")
            
            # 電話番号チェック
            phone = contact_data.get('phone', '').strip()
            if phone and not self.validate_phone(phone):
                errors.append("電話番号の形式が正しくありません")
            
            # 生年月日チェック
            birthday = contact_data.get('birthday', '').strip()
            if birthday and not self.validate_date(birthday):
                errors.append("生年月日の形式が正しくありません")
            
            # 各フィールドの長さチェック
            field_limits = {
                'furigana': 100,
                'address': 500,
                'phone': 50,
                'email': 100,
                'notes': 1000,
                'image_path': 500
            }
            
            for field, limit in field_limits.items():
                value = contact_data.get(field, '')
                if len(value) > limit:
                    errors.append(f"{field}は{limit}文字以内で入力してください")
            
        except Exception as e:
            self.logger.error(f"バリデーションエラー取得中のエラー: {e}")
            errors.append("バリデーション処理中にエラーが発生しました")
        
        return errors
