#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
検索ダイアログ
Search Dialog
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any
import logging


class SearchDialog:
    """検索ダイアログクラス"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.logger = logging.getLogger(__name__)
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("詳細検索")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # モーダルダイアログにする
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        
        # ダイアログを中央に配置
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Enterキーで検索、Escapeキーでキャンセル
        self.dialog.bind('<Return>', lambda e: self._search())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
        
        # キーワードフィールドにフォーカス
        self.keyword_entry.focus()
        
        # ダイアログが閉じられるまで待機
        self.dialog.wait_window()
    
    def _create_widgets(self):
        """ウィジェットの作成"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        title_label = ttk.Label(main_frame, text="検索条件を入力してください", 
                               font=("", 12, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 検索フィールドフレーム
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        # キーワード検索
        ttk.Label(search_frame, text="キーワード:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.keyword_entry = ttk.Entry(search_frame, width=30)
        self.keyword_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # 名前検索
        ttk.Label(search_frame, text="名前:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(search_frame, width=30)
        self.name_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # 電話番号検索
        ttk.Label(search_frame, text="電話番号:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.phone_entry = ttk.Entry(search_frame, width=30)
        self.phone_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # メールアドレス検索
        ttk.Label(search_frame, text="メール:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.email_entry = ttk.Entry(search_frame, width=30)
        self.email_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # 住所検索
        ttk.Label(search_frame, text="住所:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.address_entry = ttk.Entry(search_frame, width=30)
        self.address_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # グリッドの設定
        search_frame.columnconfigure(1, weight=1)
        
        # 説明テキスト
        help_text = ttk.Label(main_frame, 
                             text="※ 複数の条件を入力した場合はAND検索になります\n"
                                  "※ キーワード検索は全てのフィールドを対象とします",
                             font=("", 9),
                             foreground="gray")
        help_text.pack(pady=10)
        
        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="検索", command=self._search).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="クリア", command=self._clear).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="キャンセル", command=self._cancel).pack(side=tk.RIGHT)
    
    def _search(self):
        """検索実行"""
        try:
            # 検索条件の取得
            criteria = {}
            
            # 各フィールドの値を取得
            keyword = self.keyword_entry.get().strip()
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            email = self.email_entry.get().strip()
            address = self.address_entry.get().strip()
            
            # 空でない条件のみ追加
            if keyword:
                criteria["keyword"] = keyword
            if name:
                criteria["name"] = name
            if phone:
                criteria["phone"] = phone
            if email:
                criteria["email"] = email
            if address:
                criteria["address"] = address
            
            # 何も入力されていない場合の警告
            if not criteria:
                tk.messagebox.showwarning("警告", "検索条件を入力してください")
                return
            
            self.logger.info(f"検索条件: {criteria}")
            self.result = criteria
            self.dialog.destroy()
            
        except Exception as e:
            self.logger.error(f"検索実行エラー: {e}")
            tk.messagebox.showerror("エラー", "検索の実行中にエラーが発生しました")
    
    def _clear(self):
        """フィールドクリア"""
        try:
            self.keyword_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.address_entry.delete(0, tk.END)
            
            self.keyword_entry.focus()
            
        except Exception as e:
            self.logger.error(f"フィールドクリアエラー: {e}")
    
    def _cancel(self):
        """キャンセル"""
        self.result = None
        self.dialog.destroy()
