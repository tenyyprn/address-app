#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定ダイアログ
Settings Dialog
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any
import logging
import os
from config.settings import Settings


class SettingsDialog:
    """設定ダイアログクラス"""
    
    def __init__(self, parent):
        self.parent = parent
        self.settings = Settings()
        self.logger = logging.getLogger(__name__)
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("設定")
        self.dialog.geometry("500x400")
        self.dialog.resizable(True, True)
        
        # モーダルダイアログにする
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._load_settings()
        
        # ダイアログを中央に配置
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Escapeキーでキャンセル
        self.dialog.bind('<Escape>', lambda e: self._cancel())
        
        # ダイアログが閉じられるまで待機
        self.dialog.wait_window()
    
    def _create_widgets(self):
        """ウィジェットの作成"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ノートブック（タブ）
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # データベース設定タブ
        self._create_database_tab()
        
        # 表示設定タブ
        self._create_display_tab()
        
        # バックアップ設定タブ
        self._create_backup_tab()
        
        # ログ設定タブ
        self._create_logging_tab()
        
        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="OK", command=self._save_and_close).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="適用", command=self._apply).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="キャンセル", command=self._cancel).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="デフォルトに戻す", command=self._reset_defaults).pack(side=tk.LEFT)
    
    def _create_database_tab(self):
        """データベース設定タブの作成"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="データベース")
        
        # データベースパス
        ttk.Label(frame, text="データベースファイルパス:").grid(row=0, column=0, sticky=tk.W, pady=5)
        path_frame = ttk.Frame(frame)
        path_frame.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
        
        self.db_path_var = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.db_path_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(path_frame, text="参照", command=self._browse_db_path).pack(side=tk.RIGHT, padx=(5, 0))
        
        # バックアップ間隔
        ttk.Label(frame, text="バックアップ間隔（時間）:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.backup_interval_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.backup_interval_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # データベース情報表示
        info_frame = ttk.LabelFrame(frame, text="データベース情報", padding="10")
        info_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        self.db_info_text = tk.Text(info_frame, height=6, width=50, state=tk.DISABLED)
        self.db_info_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(info_frame, text="情報更新", command=self._update_db_info).pack(pady=(5, 0))
        
        frame.columnconfigure(1, weight=1)
        path_frame.columnconfigure(0, weight=1)
    
    def _create_display_tab(self):
        """表示設定タブの作成"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="表示")
        
        # テーマ設定
        ttk.Label(frame, text="テーマ:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(frame, textvariable=self.theme_var, 
                                  values=["light", "dark"], state="readonly", width=15)
        theme_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # フォントサイズ
        ttk.Label(frame, text="フォントサイズ:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.font_size_var = tk.StringVar()
        font_size_combo = ttk.Combobox(frame, textvariable=self.font_size_var,
                                      values=["8", "9", "10", "11", "12", "14", "16", "18", "20"],
                                      state="readonly", width=10)
        font_size_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 言語設定
        ttk.Label(frame, text="言語:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.language_var = tk.StringVar()
        language_combo = ttk.Combobox(frame, textvariable=self.language_var,
                                     values=["ja", "en"], state="readonly", width=10)
        language_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # プレビューエリア
        preview_frame = ttk.LabelFrame(frame, text="プレビュー", padding="10")
        preview_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        self.preview_label = ttk.Label(preview_frame, text="サンプルテキスト\nSample Text")
        self.preview_label.pack()
    
    def _create_backup_tab(self):
        """バックアップ設定タブの作成"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="バックアップ")
        
        # 自動バックアップ設定
        self.auto_backup_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="自動バックアップを有効にする", 
                       variable=self.auto_backup_var).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # バックアップパス
        ttk.Label(frame, text="バックアップ保存先:").grid(row=1, column=0, sticky=tk.W, pady=5)
        backup_path_frame = ttk.Frame(frame)
        backup_path_frame.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
        
        self.backup_path_var = tk.StringVar()
        ttk.Entry(backup_path_frame, textvariable=self.backup_path_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(backup_path_frame, text="参照", command=self._browse_backup_path).pack(side=tk.RIGHT, padx=(5, 0))
        
        # バックアップ操作
        operation_frame = ttk.LabelFrame(frame, text="バックアップ操作", padding="10")
        operation_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Button(operation_frame, text="今すぐバックアップ", command=self._backup_now).pack(side=tk.LEFT, padx=5)
        ttk.Button(operation_frame, text="バックアップから復元", command=self._restore_backup).pack(side=tk.LEFT, padx=5)
        
        frame.columnconfigure(1, weight=1)
        backup_path_frame.columnconfigure(0, weight=1)
    
    def _create_logging_tab(self):
        """ログ設定タブの作成"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="ログ")
        
        # ログレベル
        ttk.Label(frame, text="ログレベル:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.log_level_var = tk.StringVar()
        log_level_combo = ttk.Combobox(frame, textvariable=self.log_level_var,
                                      values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                                      state="readonly", width=15)
        log_level_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # ログパス
        ttk.Label(frame, text="ログ保存先:").grid(row=1, column=0, sticky=tk.W, pady=5)
        log_path_frame = ttk.Frame(frame)
        log_path_frame.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=5)
        
        self.log_path_var = tk.StringVar()
        ttk.Entry(log_path_frame, textvariable=self.log_path_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(log_path_frame, text="参照", command=self._browse_log_path).pack(side=tk.RIGHT, padx=(5, 0))
        
        # ログファイル操作
        log_operation_frame = ttk.LabelFrame(frame, text="ログファイル操作", padding="10")
        log_operation_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Button(log_operation_frame, text="ログフォルダを開く", command=self._open_log_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(log_operation_frame, text="古いログを削除", command=self._cleanup_logs).pack(side=tk.LEFT, padx=5)
        
        frame.columnconfigure(1, weight=1)
        log_path_frame.columnconfigure(0, weight=1)
    
    def _load_settings(self):
        """設定の読み込み"""
        try:
            # データベース設定
            self.db_path_var.set(self.settings.get_database_path())
            self.backup_interval_var.set(str(self.settings.get_backup_interval()))
            
            # 表示設定
            self.theme_var.set(self.settings.get_theme())
            self.font_size_var.set(str(self.settings.get_font_size()))
            self.language_var.set(self.settings.get_language())
            
            # バックアップ設定
            self.auto_backup_var.set(self.settings.is_auto_backup_enabled())
            self.backup_path_var.set(self.settings.get_backup_path())
            
            # ログ設定
            self.log_level_var.set(self.settings.get('Logging', 'level', 'INFO'))
            self.log_path_var.set(self.settings.get('Logging', 'path', './logs'))
            
            # データベース情報を更新
            self._update_db_info()
            
        except Exception as e:
            self.logger.error(f"設定読み込みエラー: {e}")
    
    def _save_and_close(self):
        """設定を保存して閉じる"""
        if self._apply():
            self.dialog.destroy()
    
    def _apply(self):
        """設定を適用"""
        try:
            # データベース設定
            self.settings.set('Database', 'path', self.db_path_var.get())
            self.settings.set('Database', 'backup_interval', self.backup_interval_var.get())
            
            # 表示設定
            self.settings.set('Display', 'theme', self.theme_var.get())
            self.settings.set('Display', 'font_size', self.font_size_var.get())
            self.settings.set('Display', 'language', self.language_var.get())
            
            # バックアップ設定
            self.settings.set('Backup', 'auto_backup', 'true' if self.auto_backup_var.get() else 'false')
            self.settings.set('Backup', 'backup_path', self.backup_path_var.get())
            
            # ログ設定
            self.settings.set('Logging', 'level', self.log_level_var.get())
            self.settings.set('Logging', 'path', self.log_path_var.get())
            
            # 設定ファイルに保存
            self.settings.save_settings()
            
            messagebox.showinfo("完了", "設定を保存しました。\n一部の設定は再起動後に反映されます。")
            return True
            
        except Exception as e:
            self.logger.error(f"設定保存エラー: {e}")
            messagebox.showerror("エラー", "設定の保存に失敗しました")
            return False
    
    def _cancel(self):
        """キャンセル"""
        self.dialog.destroy()
    
    def _reset_defaults(self):
        """デフォルト設定に戻す"""
        if messagebox.askyesno("確認", "設定をデフォルトに戻しますか？"):
            try:
                self.settings.create_default_config()
                self._load_settings()
                messagebox.showinfo("完了", "デフォルト設定に戻しました")
            except Exception as e:
                self.logger.error(f"デフォルト設定復元エラー: {e}")
                messagebox.showerror("エラー", "デフォルト設定の復元に失敗しました")
    
    def _browse_db_path(self):
        """データベースパスの参照"""
        filename = filedialog.asksaveasfilename(
            title="データベースファイルの選択",
            defaultextension=".db",
            filetypes=[("SQLite files", "*.db"), ("All files", "*.*")]
        )
        if filename:
            self.db_path_var.set(filename)
    
    def _browse_backup_path(self):
        """バックアップパスの参照"""
        dirname = filedialog.askdirectory(title="バックアップ保存先の選択")
        if dirname:
            self.backup_path_var.set(dirname)
    
    def _browse_log_path(self):
        """ログパスの参照"""
        dirname = filedialog.askdirectory(title="ログ保存先の選択")
        if dirname:
            self.log_path_var.set(dirname)
    
    def _update_db_info(self):
        """データベース情報を更新"""
        try:
            from database.db_manager import DBManager
            db_manager = DBManager()
            info = db_manager.get_database_info()
            
            if info:
                info_text = f"パス: {info['path']}\n"
                info_text += f"ファイルサイズ: {info['size']:,} bytes\n"
                info_text += "テーブル情報:\n"
                for table, count in info['tables'].items():
                    info_text += f"  {table}: {count} レコード\n"
            else:
                info_text = "データベース情報を取得できませんでした"
            
            self.db_info_text.config(state=tk.NORMAL)
            self.db_info_text.delete(1.0, tk.END)
            self.db_info_text.insert(1.0, info_text)
            self.db_info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.logger.error(f"データベース情報取得エラー: {e}")
    
    def _backup_now(self):
        """今すぐバックアップ"""
        try:
            from database.db_manager import DBManager
            db_manager = DBManager()
            backup_path = db_manager.backup_database()
            messagebox.showinfo("完了", f"バックアップが完了しました:\n{backup_path}")
        except Exception as e:
            self.logger.error(f"バックアップエラー: {e}")
            messagebox.showerror("エラー", "バックアップに失敗しました")
    
    def _restore_backup(self):
        """バックアップから復元"""
        filename = filedialog.askopenfilename(
            title="復元するバックアップファイルの選択",
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
        )
        if filename:
            if messagebox.askyesno("確認", "現在のデータは上書きされます。続行しますか？"):
                try:
                    from database.db_manager import DBManager
                    db_manager = DBManager()
                    db_manager.restore_database(filename)
                    messagebox.showinfo("完了", "復元が完了しました")
                except Exception as e:
                    self.logger.error(f"復元エラー: {e}")
                    messagebox.showerror("エラー", "復元に失敗しました")
    
    def _open_log_folder(self):
        """ログフォルダを開く"""
        try:
            log_path = self.log_path_var.get()
            if os.path.exists(log_path):
                os.startfile(log_path)  # Windows
                # macOS: os.system(f"open {log_path}")
                # Linux: os.system(f"xdg-open {log_path}")
            else:
                messagebox.showwarning("警告", "ログフォルダが存在しません")
        except Exception as e:
            self.logger.error(f"ログフォルダオープンエラー: {e}")
            messagebox.showerror("エラー", "ログフォルダを開けませんでした")
    
    def _cleanup_logs(self):
        """古いログを削除"""
        if messagebox.askyesno("確認", "30日以上古いログファイルを削除しますか？"):
            try:
                import glob
                from datetime import datetime, timedelta
                
                log_path = self.log_path_var.get()
                cutoff_date = datetime.now() - timedelta(days=30)
                deleted_count = 0
                
                for log_file in glob.glob(os.path.join(log_path, "*.log")):
                    if os.path.getmtime(log_file) < cutoff_date.timestamp():
                        os.remove(log_file)
                        deleted_count += 1
                
                messagebox.showinfo("完了", f"{deleted_count}個のログファイルを削除しました")
                
            except Exception as e:
                self.logger.error(f"ログクリーンアップエラー: {e}")
                messagebox.showerror("エラー", "ログクリーンアップに失敗しました")
