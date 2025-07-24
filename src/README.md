# Pythonが未インストールの場合
# https://www.python.org/downloads/ からダウンロードしてインストール

git clone https://github.com/your-repo/address-book.git
cd address-book
pip install -r requirements.txt

python setup.py

python main.py

[Database]
path = ./data/address_book.db
backup_interval = 24

[Display]
theme = light
font_size = 12
language = ja

[Backup]
auto_backup = true
backup_path = ./backups

# 開発環境の準備
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

pytest tests/;