DATABASE_TABLE_NAME = "contacts"

FIELD_NAME_CONSTANTS = {
    "NAME": "name",
    "KANA": "kana",
    "ADDRESS": "address",
    "PHONE": "phone",
    "EMAIL": "email",
    "BIRTHDAY": "birthday",
    "MEMO": "memo"
}

ERROR_MESSAGES = {
    "REQUIRED": "このフィールドは必須です。",
    "INVALID_EMAIL": "無効なメールアドレスです。",
    "INVALID_PHONE": "無効な電話番号です。",
    "DUPLICATE_ENTRY": "このエントリはすでに存在します。"
}

GUI_SETTINGS = {
    "PRIMARY_COLOR": "#3498db",
    "SECONDARY_COLOR": "#2ecc71",
    "FONT_SIZE": 12,
    "WINDOW_WIDTH": 800,
    "WINDOW_HEIGHT": 600
}

FILE_PATH_CONSTANTS = {
    "DATABASE_PATH": "./data/address_book.db",
    "BACKUP_PATH": "./backups/",
    "LOG_PATH": "./logs/"
}

VALIDATION_CONSTANTS = {
    "EMAIL_REGEX": r"^[\w\.-]+@[\w\.-]+\.\w+$",
    "PHONE_REGEX": r"^\+?[0-9]{10,15}$",
    "MAX_NAME_LENGTH": 50,
    "MAX_ADDRESS_LENGTH": 100
}

APPLICATION_INFO = {
    "VERSION": "1.0.0",
    "NAME": "住所録管理プログラム"
}