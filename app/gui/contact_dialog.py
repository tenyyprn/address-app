#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
連絡先ダイアログ
Contact Dialog
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any
import logging


class ContactDialog:
    """連絡先編集ダイアログクラス"""
    
    def __init__(self, parent, contact_data: Optional[Dict[str, Any]] = None):
        self.parent = parent
        self.contact_data = contact_data or {}
        self.result = None
        self.logger = logging.getLogger(__name__)
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("連絡先編集" if contact_data else "新規連絡先")
        self.dialog.geometry("450x550")
        self.dialog.resizable(False, False)
        
        # モーダルダイアログにする
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # ダイアログアイコンの設定
        try:
            self.dialog.iconbitmap(parent.iconbitmap())
        except:
            pass
        
        self._create_widgets()
        self._load_data()
        
        # ダイアログを中央に配置
        self._center_dialog()
        
        # キーバインド
        self.dialog.bind('<Return>', self._on_enter)
        self.dialog.bind('<Escape>', lambda e: self._cancel())
        
        # フォーカスを名前フィールドに設定
        self.name_entry.focus()
        
        # ダイアログが閉じられるまで待機
        self.dialog.wait_window()
    
    def _center_dialog(self):
        """ダイアログを画面中央に配置"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_widgets(self):
        """ウィジェットの作成"""
        # メインフレーム
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        title_text = "連絡先を編集" if self.contact_data else "新しい連絡先を追加"
        title_label = ttk.Label(main_frame, text=title_text, font=("", 12, "bold"))
        title_label.pack(pady=(0, 20))
        
        # スクロール可能エリア
        canvas = tk.Canvas(main_frame, height=350)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 入力フィールドの定義
        fields = [
            ("名前", "name", "必須", False),
            ("ふりがな", "furigana", "", False),
            ("電話番号", "phone", "例: 03-1234-5678", False),
            ("メールアドレス", "email", "例: example@domain.com", False),
            ("住所", "address", "", True),
            ("生年月日", "birthday", "例: 1990-01-01", False),
        ]
        
        self.entries = {}
        
        # 各フィールドの作成
        for i, (label, key, placeholder, is_multiline) in enumerate(fields):
            # ラベルフレーム
            label_frame = ttk.Frame(scrollable_frame)
            label_frame.grid(row=i*2, column=0, columnspan=2, sticky=tk.EW, pady=(10, 2))
            
            # ラベル
            label_text = f"{label} {'*' if placeholder == '必須' else ''}"
            ttk.Label(label_frame, text=label_text, font=("", 9, "bold")).pack(side=tk.LEFT)
            
            # プレースホルダー
            if placeholder and placeholder != "必須":
                ttk.Label(label_frame, text=f"({placeholder})", 
                         font=("", 8), foreground="gray").pack(side=tk.RIGHT)
            
            # 入力フィールド
            if is_multiline:
                # 複数行入力（住所用）
                text_frame = ttk.Frame(scrollable_frame)
                text_frame.grid(row=i*2+1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 5))
                
                entry = tk.Text(text_frame, height=3, width=40, wrap=tk.WORD)
                entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                # スクロールバー
                text_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=entry.yview)
                text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
                entry.configure(yscrollcommand=text_scroll.set)
                
                text_frame.columnconfigure(0, weight=1)
            else:
                # 単行入力
                entry = ttk.Entry(scrollable_frame, width=50, font=("", 10))
                entry.grid(row=i*2+1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 5))
            
            self.entries[key] = entry
        
        # メモ欄
        memo_label_frame = ttk.Frame(scrollable_frame)
        memo_label_frame.grid(row=len(fields)*2, column=0, columnspan=2, sticky=tk.EW, pady=(15, 2))
        ttk.Label(memo_label_frame, text="メモ", font=("", 9, "bold")).pack(side=tk.LEFT)
        
        memo_frame = ttk.Frame(scrollable_frame)
        memo_frame.grid(row=len(fields)*2+1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))
        
        self.notes_text = tk.Text(memo_frame, height=4, width=40, wrap=tk.WORD)
        self.notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        notes_scroll = ttk.Scrollbar(memo_frame, orient=tk.VERTICAL, command=self.notes_text.yview)
        notes_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.notes_text.configure(yscrollcommand=notes_scroll.set)
        
        memo_frame.columnconfigure(0, weight=1)
        
        # グリッド設定
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.columnconfigure(1, weight=1)
        
        # スクロールエリアの配置
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        # ボタン
        ttk.Button(button_frame, text="キャンセル", command=self._cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="保存", command=self._save).pack(side=tk.RIGHT)
        
        # 名前エントリへの参照を保存（フォーカス用）
        self.name_entry = self.entries["name"]
        
        # マウスホイールでスクロール
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
    
    def _load_data(self):
        """既存データの読み込み"""
        if not self.contact_data:
            return
        
        try:
            # 通常のエントリフィールド
            for key, entry in self.entries.items():
                value = str(self.contact_data.get(key, ""))
                if isinstance(entry, tk.Text):
                    entry.delete(1.0, tk.END)
                    entry.insert(1.0, value)
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, value)
            
            # メモ欄
            notes = str(self.contact_data.get("notes", ""))
            self.notes_text.delete(1.0, tk.END)
            self.notes_text.insert(1.0, notes)
            
            self.logger.info(f"データ読み込み完了: {self.contact_data.get('name', 'Unknown')}")
            
        except Exception as e:
            self.logger.error(f"データ読み込みエラー: {e}")
            messagebox.showerror("エラー", "データの読み込みに失敗しました")
    
    def _save(self):
        """データの保存"""
        try:
            # データの取得
            data = {}
            for key, entry in self.entries.items():
                if isinstance(entry, tk.Text):
                    data[key] = entry.get(1.0, tk.END).strip()
                else:
                    data[key] = entry.get().strip()
            
            # メモの取得
            data["notes"] = self.notes_text.get(1.0, tk.END).strip()
            
            # バリデーション
            validation_errors = self._validate_data(data)
            if validation_errors:
                messagebox.showwarning("入力エラー", "\n".join(validation_errors))
                return
            
            self.result = data
            self.logger.info(f"データ保存: {data.get('name', 'Unknown')}")
            self.dialog.destroy()
            
        except Exception as e:
            self.logger.error(f"保存エラー: {e}")
            messagebox.showerror("エラー", "データの保存に失敗しました")
    
    def _validate_data(self, data):
        """データのバリデーション"""
        errors = []
        
        # 名前は必須
        if not data.get("name", "").strip():
            errors.append("• 名前は必須項目です")
        
        # 名前の長さチェック
        if len(data.get("name", "")) > 100:
            errors.append("• 名前は100文字以内で入力してください")
        
        # メールアドレスの形式チェック
        email = data.get("email", "").strip()
        if email and not self._validate_email(email):
            errors.append("• メールアドレスの形式が正しくありません")
        
        # 電話番号の形式チェック（簡易）
        phone = data.get("phone", "").strip()
        if phone and not self._validate_phone(phone):
            errors.append("• 電話番号の形式が正しくありません")
        
        # 生年月日の形式チェック
        birthday = data.get("birthday", "").strip()
        if birthday and not self._validate_date(birthday):
            errors.append("• 生年月日の形式が正しくありません（例: 1990-01-01）")
        
        return errors
    
    def _validate_email(self, email):
        """メールアドレスの簡易バリデーション"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _validate_phone(self, phone):
        """電話番号の簡易バリデーション"""
        import re
        # 日本の電話番号パターン（簡易版）
        patterns = [
            r'^\d{2,4}-\d{2,4}-\d{4}$',  # 03-1234-5678
            r'^\d{10,11}$',               # 0312345678
            r'^\+81-\d{1,4}-\d{2,4}-\d{4}$'  # +81-3-1234-5678
        ]
        return any(re.match(pattern, phone) for pattern in patterns)
    
    def _validate_date(self, date_str):
        """日付の簡易バリデーション"""
        import re
        from datetime import datetime
        
        # YYYY-MM-DD形式をチェック
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                return True
            except ValueError:
                return False
        return False
    
    def _cancel(self):
        """キャンセル"""
        self.result = None
        self.dialog.destroy()
    
    def _on_enter(self, event):
        """Enterキー押下時の処理"""
        # Textウィジェット内でのEnterは改行として処理
        if isinstance(event.widget, tk.Text):
            return
        # その他の場合は保存処理
        self._save()


# テスト用のコード
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示
    
    # テストデータ
    test_data = {
        "name": "山田太郎",
        "furigana": "やまだたろう",
        "phone": "03-1234-5678",
        "email": "yamada@example.com",
        "address": "東京都渋谷区...",
        "birthday": "1990-01-01",
        "notes": "テストデータです"
    }
    
    dialog = ContactDialog(root, test_data)
    
    if dialog.result:
        print("保存されたデータ:")
        for key, value in dialog.result.items():
            print(f"  {key}: {value}")
    else:
        print("キャンセルされました")
    
    root.destroy()
