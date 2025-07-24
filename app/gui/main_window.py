#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
メインウィンドウ
Main Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any
import json
import os
import logging

# 絶対インポートに変更
try:
    from contact_dialog import ContactDialog
    from search_dialog import SearchDialog
    from settings_dialog import SettingsDialog
except ImportError:
    try:
        from gui.contact_dialog import ContactDialog
        from gui.search_dialog import SearchDialog
        from gui.settings_dialog import SettingsDialog
    except ImportError:
        print("GUIモジュールのインポートに失敗しました")

try:
    from database.contact_model import ContactModel
    from utils.validator import Validator
except ImportError:
    print("データベースまたはバリデーションモジュールのインポートに失敗しました")
    # ダミークラスを作成
    class ContactModel:
        def __init__(self):
            pass
        def create(self, data):
            return 1
        def read(self, id):
            return {"id": id, "name": "テスト", "furigana": "テスト", "phone": "", "email": "", "address": "", "notes": ""}
        def read_all(self):
            return []
        def update(self, id, data):
            return True
        def delete(self, id):
            return True
        def search(self, criteria):
            return []
    
    class Validator:
        def __init__(self):
            pass
        def validate_contact(self, data):
            return True


class MainWindow:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.root = tk.Tk()
        self.root.title("住所録管理システム")
        self.root.geometry("800x600")
        
        # アイコンの設定（オプション）
        try:
            # self.root.iconbitmap("icon.ico")  # アイコンファイルがある場合
            pass
        except:
            pass
        
        # モデルとバリデーターの初期化
        try:
            self.contact_model = ContactModel()
            self.validator = Validator()
        except Exception as e:
            self.logger.error(f"モデル初期化エラー: {e}")
            messagebox.showerror("初期化エラー", f"アプリケーションの初期化中にエラーが発生しました: {e}")
            return
        
        # ウィンドウ終了時の処理
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        # UIコンポーネントの作成
        self._create_menu()
        self._create_toolbar()
        self._create_treeview()
        self._create_statusbar()
        self._setup_shortcuts()
        
        # ウィンドウ状態の読み込み
        self.load_window_state()
        
        self.logger.info("MainWindowが初期化されました")
        
    def _create_menu(self):
        """メニューバーの作成"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # ファイルメニュー
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        file_menu.add_command(label="新規作成", command=self.new_contact, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="インポート", command=self.import_data)
        file_menu.add_command(label="エクスポート", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="設定", command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.quit_app, accelerator="Alt+F4")
        
        # 編集メニュー
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="編集", menu=edit_menu)
        edit_menu.add_command(label="追加", command=self.new_contact, accelerator="Ctrl+N")
        edit_menu.add_command(label="編集", command=self.edit_contact, accelerator="Ctrl+E")
        edit_menu.add_command(label="削除", command=self.delete_contact, accelerator="Ctrl+D")
        
        # 表示メニュー
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="表示", menu=view_menu)
        view_menu.add_command(label="検索", command=self.show_search, accelerator="Ctrl+F")
        view_menu.add_command(label="更新", command=self.refresh_list, accelerator="F5")
        
        # ヘルプメニュー
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ヘルプ", menu=help_menu)
        help_menu.add_command(label="バージョン情報", command=self.show_about)
        
    def _create_toolbar(self):
        """ツールバーの作成"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=3)
        
        # ボタンフレーム
        button_frame = ttk.Frame(toolbar)
        button_frame.pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="追加", command=self.new_contact).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="編集", command=self.edit_contact).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="削除", command=self.delete_contact).pack(side=tk.LEFT, padx=2)
        
        # セパレータ
        ttk.Separator(button_frame, orient='vertical').pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        ttk.Button(button_frame, text="更新", command=self.refresh_list).pack(side=tk.LEFT, padx=2)
        
        # 検索フレーム
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(search_frame, text="検索:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT)
        
        ttk.Button(search_frame, text="詳細検索", command=self.show_search).pack(side=tk.LEFT, padx=(2, 0))
        
    def _create_treeview(self):
        """連絡先リストの作成"""
        # フレーム作成
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # カラム定義
        columns = ("ID", "名前", "ふりがな", "電話番号", "メールアドレス", "住所")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # カラムの設定
        self.tree.column("ID", width=50, minwidth=50)
        self.tree.column("名前", width=120, minwidth=100)
        self.tree.column("ふりがな", width=120, minwidth=100)
        self.tree.column("電話番号", width=120, minwidth=100)
        self.tree.column("メールアドレス", width=180, minwidth=150)
        self.tree.column("住所", width=200, minwidth=150)
        
        # ヘッダーの設定
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
        
        # スクロールバー
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 配置
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # グリッドの重み設定
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # イベントバインド
        self.tree.bind("<Double-1>", lambda e: self.edit_contact())
        self.tree.bind("<Return>", lambda e: self.edit_contact())
        self.tree.bind("<Delete>", lambda e: self.delete_contact())
        
    def _create_statusbar(self):
        """ステータスバーの作成"""
        self.status_var = tk.StringVar()
        self.statusbar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=2)
        self.status_var.set("準備完了")
        
    def _setup_shortcuts(self):
        """キーボードショートカットの設定"""
        self.root.bind("<Control-n>", lambda e: self.new_contact())
        self.root.bind("<Control-e>", lambda e: self.edit_contact())
        self.root.bind("<Control-d>", lambda e: self.delete_contact())
        self.root.bind("<Control-f>", lambda e: self.show_search())
        self.root.bind("<F5>", lambda e: self.refresh_list())
        self.root.bind("<Control-q>", lambda e: self.quit_app())
        
    def load_window_state(self):
        """ウィンドウ状態の読み込み"""
        try:
            if os.path.exists("window_state.json"):
                with open("window_state.json", "r", encoding="utf-8") as f:
                    state = json.load(f)
                    geometry = f"{state.get('width', 800)}x{state.get('height', 600)}"
                    geometry += f"+{state.get('x', 100)}+{state.get('y', 100)}"
                    self.root.geometry(geometry)
        except Exception as e:
            self.logger.warning(f"ウィンドウ状態読み込みエラー: {e}")
            
    def save_window_state(self):
        """ウィンドウ状態の保存"""
        try:
            state = {
                "width": self.root.winfo_width(),
                "height": self.root.winfo_height(),
                "x": self.root.winfo_x(),
                "y": self.root.winfo_y()
            }
            with open("window_state.json", "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"ウィンドウ状態保存エラー: {e}")
            
    def new_contact(self):
        """新規連絡先の追加"""
        try:
            dialog = ContactDialog(self.root)
            if dialog.result:
                contact_id = self.contact_model.create(dialog.result)
                if contact_id:
                    self.refresh_list()
                    self.status_var.set("新規連絡先を追加しました")
                    self.logger.info(f"新規連絡先追加: ID {contact_id}")
                else:
                    messagebox.showerror("エラー", "連絡先の追加に失敗しました")
        except Exception as e:
            self.logger.error(f"新規連絡先追加エラー: {e}")
            messagebox.showerror("エラー", f"連絡先の追加中にエラーが発生しました: {e}")
            
    def edit_contact(self):
        """連絡先の編集"""
        try:
            selection = self.tree.selection()
            if not selection:
                messagebox.showwarning("警告", "編集する連絡先を選択してください")
                return
                
            item = self.tree.item(selection[0])
            contact_id = item["values"][0]
            contact = self.contact_model.read(contact_id)
            
            if not contact:
                messagebox.showerror("エラー", "連絡先の読み込みに失敗しました")
                return
            
            dialog = ContactDialog(self.root, contact)
            
            if dialog.result:
                if self.contact_model.update(contact_id, dialog.result):
                    self.refresh_list()
                    self.status_var.set("連絡先を更新しました")
                    self.logger.info(f"連絡先更新: ID {contact_id}")
                else:
                    messagebox.showerror("エラー", "連絡先の更新に失敗しました")
        except Exception as e:
            self.logger.error(f"連絡先編集エラー: {e}")
            messagebox.showerror("エラー", f"連絡先の編集中にエラーが発生しました: {e}")
            
    def delete_contact(self):
        """連絡先の削除"""
        try:
            selection = self.tree.selection()
            if not selection:
                messagebox.showwarning("警告", "削除する連絡先を選択してください")
                return
                
            item = self.tree.item(selection[0])
            contact_name = item["values"][1]  # 名前を取得
            
            if messagebox.askyesno("確認", f"「{contact_name}」を削除しますか？"):
                contact_id = item["values"][0]
                if self.contact_model.delete(contact_id):
                    self.refresh_list()
                    self.status_var.set("連絡先を削除しました")
                    self.logger.info(f"連絡先削除: ID {contact_id}")
                else:
                    messagebox.showerror("エラー", "連絡先の削除に失敗しました")
        except Exception as e:
            self.logger.error(f"連絡先削除エラー: {e}")
            messagebox.showerror("エラー", f"連絡先の削除中にエラーが発生しました: {e}")
            
    def show_search(self):
        """詳細検索ダイアログの表示"""
        try:
            dialog = SearchDialog(self.root)
            if dialog.result:
                self.search_contacts(dialog.result)
        except Exception as e:
            self.logger.error(f"検索ダイアログエラー: {e}")
            messagebox.showerror("エラー", f"検索中にエラーが発生しました: {e}")
            
    def on_search_change(self, *args):
        """検索フィールドの変更時処理"""
        try:
            search_text = self.search_var.get().strip()
            if search_text:
                self.search_contacts({"keyword": search_text})
            else:
                self.refresh_list()
        except Exception as e:
            self.logger.error(f"検索変更エラー: {e}")
            
    def search_contacts(self, criteria: Dict[str, Any]):
        """連絡先検索"""
        try:
            results = self.contact_model.search(criteria)
            self.update_treeview(results)
            self.status_var.set(f"{len(results)}件の検索結果")
            self.logger.info(f"検索実行: {len(results)}件")
        except Exception as e:
            self.logger.error(f"連絡先検索エラー: {e}")
            messagebox.showerror("エラー", f"検索中にエラーが発生しました: {e}")
        
    def refresh_list(self):
        """連絡先リストの更新"""
        try:
            contacts = self.contact_model.read_all()
            self.update_treeview(contacts)
            self.status_var.set(f"全{len(contacts)}件")
            # 検索フィールドをクリア
            self.search_var.set("")
            self.logger.info(f"リスト更新: {len(contacts)}件")
        except Exception as e:
            self.logger.error(f"リスト更新エラー: {e}")
            messagebox.showerror("エラー", f"リストの更新中にエラーが発生しました: {e}")
        
    def update_treeview(self, contacts):
        """ツリービューの更新"""
        try:
            # 既存のアイテムを削除
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # 新しいアイテムを追加
            for contact in contacts:
                self.tree.insert("", tk.END, values=(
                    contact.get("id", ""),
                    contact.get("name", ""),
                    contact.get("furigana", ""),
                    contact.get("phone", ""),
                    contact.get("email", ""),
                    contact.get("address", "")
                ))
        except Exception as e:
            self.logger.error(f"ツリービュー更新エラー: {e}")
            
    def sort_treeview(self, col):
        """ツリービューのソート"""
        try:
            # カラムインデックスの取得
            columns = ("ID", "名前", "ふりがな", "電話番号", "メールアドレス", "住所")
            col_index = columns.index(col)
            
            # データの取得とソート
            data = [(self.tree.set(item, col), item) for item in self.tree.get_children("")]
            data.sort()
            
            # アイテムの並び替え
            for index, (_, item) in enumerate(data):
                self.tree.move(item, "", index)
                
            self.logger.info(f"ソート実行: {col}")
        except Exception as e:
            self.logger.error(f"ソートエラー: {e}")
    
    def show_settings(self):
        """設定ダイアログの表示"""
        try:
            dialog = SettingsDialog(self.root)
        except Exception as e:
            self.logger.error(f"設定ダイアログエラー: {e}")
            messagebox.showerror("エラー", "設定ダイアログの表示中にエラーが発生しました")
            
    def import_data(self):
        """CSVインポート処理"""
        messagebox.showinfo("情報", "CSVインポート機能は今後実装予定です")
        
    def export_data(self):
        """CSVエクスポート処理"""
        messagebox.showinfo("情報", "CSVエクスポート機能は今後実装予定です")
        
    def show_about(self):
        """バージョン情報の表示"""
        about_text = """住所録管理システム v1.0

Python tkinter を使用したデスクトップアプリケーション

機能:
• 連絡先の追加・編集・削除
• 検索・フィルタリング
• データベース管理
• バックアップ機能

©2024 Your Company"""
        
        messagebox.showinfo("バージョン情報", about_text)
        
    def quit_app(self):
        """アプリケーション終了"""
        try:
            if messagebox.askyesno("確認", "アプリケーションを終了しますか？"):
                self.save_window_state()
                self.logger.info("アプリケーション終了")
                self.root.quit()
        except Exception as e:
            self.logger.error(f"終了処理エラー: {e}")
            self.root.quit()
            
    def run(self):
        """アプリケーションの実行"""
        try:
            # 初期データの読み込み
            self.refresh_list()
            
            # メインループの開始
            self.logger.info("メインループ開始")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"実行エラー: {e}")
            messagebox.showerror("実行エラー", f"アプリケーションの実行中にエラーが発生しました: {e}")


if __name__ == "__main__":
    app = MainWindow()
    app.run()
