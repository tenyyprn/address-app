import os
import shutil
import zipfile
from datetime import datetime, timedelta
from src.app.database.db_manager import DBManager
from src.app.config.settings import Settings
from src.app.utils.logger import Logger

class BackupManager:
    def __init__(self):
        self.db_manager = DBManager()
        self.settings = Settings()
        self.logger = Logger()
        self.backup_path = self.settings.get('BACKUP_PATH')
        self.backup_interval = int(self.settings.get('BACKUP_INTERVAL'))
        self.max_backup_files = int(self.settings.get('MAX_BACKUP_FILES'))

    def create_backup(self):
        try:
            backup_file = os.path.join(self.backup_path, f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip")
            with zipfile.ZipFile(backup_file, 'w') as zipf:
                zipf.write(self.db_manager.get_db_path(), os.path.basename(self.db_manager.get_db_path()))
            self.logger.info(f"Backup created: {backup_file}")
            self.manage_backup_files()
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")

    def manage_backup_files(self):
        try:
            backups = sorted([f for f in os.listdir(self.backup_path) if f.endswith('.zip')], reverse=True)
            while len(backups) > self.max_backup_files:
                os.remove(os.path.join(self.backup_path, backups.pop()))
                self.logger.info(f"Old backup removed: {backups[-1]}")
        except Exception as e:
            self.logger.error(f"Failed to manage backup files: {e}")

    def restore_backup(self, backup_file):
        try:
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(os.path.dirname(self.db_manager.get_db_path()))
            self.logger.info(f"Backup restored from: {backup_file}")
        except Exception as e:
            self.logger.error(f"Failed to restore backup: {e}")

    def schedule_backup(self):
        last_backup_time = datetime.now() - timedelta(hours=self.backup_interval)
        if datetime.now() >= last_backup_time + timedelta(hours=self.backup_interval):
            self.create_backup()

    def validate_backup(self, backup_file):
        try:
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                is_valid = zipf.testzip() is None
            self.logger.info(f"Backup validation for {backup_file}: {'Valid' if is_valid else 'Invalid'}")
            return is_valid
        except Exception as e:
            self.logger.error(f"Failed to validate backup: {e}")
            return False

    def compress_backup(self, backup_file):
        try:
            compressed_file = backup_file.replace('.zip', '_compressed.zip')
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                with zipfile.ZipFile(compressed_file, 'w', zipfile.ZIP_DEFLATED) as zipf_compressed:
                    for file_info in zipf.infolist():
                        zipf_compressed.writestr(file_info, zipf.read(file_info.filename))
            self.logger.info(f"Backup compressed: {compressed_file}")
        except Exception as e:
            self.logger.error(f"Failed to compress backup: {e}")