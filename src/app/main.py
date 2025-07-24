import tkinter as tk
import logging
import os
from dotenv import load_dotenv

# 依存ファイルのインポート
# from src.app.gui.main_window import MainWindow  # main_window.pyの内容に合わせて修正
# from src.app.database.db_manager import DBManager  # db_manager.pyの内容に合わせて修正
# from src.app.config.settings import Settings  # settings.pyの内容に合わせて修正
# from src.app.utils.logger import setup_logger  # logger.pyの内容に合わせて修正

# ダミーのインポート (実際のファイル内容に合わせて修正)
class MainWindow:
    def __init__(self, master):
        pass
class DBManager:
    def __init__(self, db_path):
        pass
    def connect(self):
        pass
    def close(self):
        pass
class Settings:
    def __init__(self):
        pass
    def load_settings(self):
        pass
def setup_logger(log_level, log_path):
    pass

def main():
    # 環境変数の読み込み
    load_dotenv()

    # 設定ファイルの読み込み
    settings = Settings()
    settings.load_settings()

    # ログ設定
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_path = os.getenv("LOG_PATH", "./logs")
    setup_logger(log_level, log_path)
    logger = logging.getLogger(__name__)

    try:
        # データベース接続の確立
        db_path = os.getenv("DATABASE_PATH", "./data/address_book.db")
        db_manager = DBManager(db_path)
        db_manager.connect()

        # メインGUIウィンドウの起動
        root = tk.Tk()
        main_window = MainWindow(root)  # MainWindowクラスのインスタンス化
        root.mainloop()

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

    finally:
        # アプリケーション終了時の処理
        if 'db_manager' in locals():
            db_manager.close()
        logger.info("Application exiting.")

if __name__ == "__main__":
    main();