import os
import configparser
from dotenv import load_dotenv

class SettingsManager:
    def __init__(self, config_file='config.ini'):
        load_dotenv()
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.default_settings = {
            'Database': {
                'path': os.getenv('DATABASE_PATH', './data/address_book.db')
            },
            'GUI': {
                'font': os.getenv('DEFAULT_FONT_SIZE', '12'),
                'theme': os.getenv('DEFAULT_THEME', 'light'),
                'size': os.getenv('DEFAULT_SIZE', 'medium')
            },
            'Backup': {
                'interval': os.getenv('BACKUP_INTERVAL', '24')
            },
            'Log': {
                'level': os.getenv('LOG_LEVEL', 'INFO')
            },
            'Language': {
                'default': os.getenv('DEFAULT_LANGUAGE', 'ja')
            }
        }
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            for section in self.config.sections():
                for key in self.config[section]:
                    self.default_settings[section][key] = self.config[section][key]

    def save_settings(self):
        for section, settings in self.default_settings.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in settings.items():
                self.config[section][key] = value
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_setting(self, section, key):
        return self.default_settings.get(section, {}).get(key)

    def set_setting(self, section, key, value):
        if section in self.default_settings:
            self.default_settings[section][key] = value
            self.save_settings()