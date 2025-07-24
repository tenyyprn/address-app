import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from src.app.config.settings import LOG_LEVEL, LOG_PATH

class Logger:
    def __init__(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(LOG_LEVEL)
        handler = RotatingFileHandler(LOG_PATH, maxBytes=10**6, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)

    def log_debug_info(self, info):
        self.logger.debug(f'Debug Info: {info}')