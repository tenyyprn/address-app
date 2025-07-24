import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any
import json
import os

from .contact_dialog import ContactDialog
from .search_dialog import SearchDialog
from .settings_dialog import SettingsDialog
from ..database.contact_model import ContactModel
from ..utils.validator import Validator

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("住所録管理システム")
        self.root.geometry("800x600")
        
        self.contact_model = ContactModel()
        self.validator = Validator()
        
        self._create_menu()
        self._create_toolbar()
        self._create_treeview()
        self._create_statusbar()
        self._setup_shortcuts()
        
        self.load_window_state()
        
    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # ファイルメニュー
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        file_menu.add_command(label="新規作成", command=self.new_contact)
        file_menu.add_command(label="インポート", command=self.import_data)
        file_menu.add_command(label="エクスポート", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.quit_app)
        
        # 編集メニュー
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="編集", menu=edit_menu)
        edit_menu.add_command(label="追加", command=self.new_contact)
        edit_menu.add_command(label="編集", command=self.edit_contact)
        edit_menu.add_command(label="削除", command=self.delete_contact)
        
        # 表示メニュー
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="表示", menu=view_menu)
        view_menu.add_command(label="検索", command=self.show_search)
        view_menu.add_command(label="更新", command=self.refresh_list)
        
        # ヘルプメニュー
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ヘルプ", menu=help_menu)
        help_menu.add_command(label="バージョン情報", command=self.show_about)
        
    def _create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=3)
        
        ttk.Button(toolbar, text="追加", command=self.new_contact).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="編集", command=self.edit_contact).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="削除", command=self.delete_contact).pack(side=tk.LEFT, padx=2)
        
        # 検索フレーム
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="検索", command=self.show_search).pack(side=tk.LEFT, padx=2)
        
    def _create_treeview(self):
        columns = ("名前", "ふりがな", "電話番号", "メールアドレス", "住所")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=120)
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # スクロールバー
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.bind("<Double-1>", lambda e: self.edit_contact())
        
    def _create_statusbar(self):
        self.status_var = tk.StringVar()
        self.statusbar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set("準備完了")
        
    def _setup_shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.new_contact())
        self.root.bind("<Control-e>", lambda e: self.edit_contact())
        self.root.bind("<Control-d>", lambda e: self.delete_contact())
        self.root.bind("<Control-f>", lambda e: self.show_search())
        self.root.bind("<F5>", lambda e: self.refresh_list())
        
    def load_window_state(self):
        try:
            with open("window_state.json", "r") as f:
                state = json.load(f)
                self.root.geometry(f"{state['width']}x{state['height']}+{state['x']}+{state['y']}")
        except:
            pass
            
    def save_window_state(self):
        state = {
            "width": self.root.winfo_width(),
            "height": self.root.winfo_height(),
            "x": self.root.winfo_x(),
            "y": self.root.winfo_y()
        }
        with open("window_state.json", "w") as f:
            json.dump(state, f)
            
    def new_contact(self):
        dialog = ContactDialog(self.root)
        if dialog.result:
            self.contact_model.create(dialog.result)
            self.refresh_list()
            self.status_var.set("新規連絡先を追加しました")
            
    def edit_contact(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "編集する連絡先を選択してください")
            return
            
        contact_id = self.tree.item(selection[0])["values"][0]
        contact = self.contact_model.read(contact_id)
        dialog = ContactDialog(self.root, contact)
        
        if dialog.result:
            self.contact_model.update(contact_id, dialog.result)
            self.refresh_list()
            self.status_var.set("連絡先を更新しました")
            
    def delete_contact(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "削除する連絡先を選択してください")
            return
            
        if messagebox.askyesno("確認", "選択した連絡先を削除しますか？"):
            contact_id = self.tree.item(selection[0])["values"][0]
            self.contact_model.delete(contact_id)
            self.refresh_list()
            self.status_var.set("連絡先を削除しました")
            
    def show_search(self):
        dialog = SearchDialog(self.root)
        if dialog.result:
            self.search_contacts(dialog.result)
            
    def on_search_change(self, *args):
        search_text = self.search_var.get()
        if search_text:
            self.search_contacts({"keyword": search_text})
        else:
            self.refresh_list()
            
    def search_contacts(self, criteria: Dict[str, Any]):
        results = self.contact_model.search(criteria)
        self.update_treeview(results)
        self.status_var.set(f"{len(results)}件の検索結果")
        
    def refresh_list(self):
        contacts = self.contact_model.read_all()
        self.update_treeview(contacts)
        self.status_var.set(f"全{len(contacts)}件")
        
    def update_treeview(self, contacts):
        self.tree.delete(*self.tree.get_children())
        for contact in contacts:
            self.tree.insert("", tk.END, values=(
                contact["name"],
                contact["furigana"],
                contact["phone"],
                contact["email"],
                contact["address"]
            ))
            
    def sort_treeview(self, col):
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children("")]
        items.sort()
        for index, (_, item) in enumerate(items):
            self.tree.move(item, "", index)
            
    def import_data(self):
        # CSVインポート処理の実装
        pass
        
    def export_data(self):
        # CSVエクスポート処理の実装
        pass
        
    def show_about(self):
        messagebox.showinfo(
            "バージョン情報",
            "住所録管理システム v1.0\n©2024 Your Company"
        )
        
    def quit_app(self):
        if messagebox.askyesno("確認", "アプリケーションを終了しますか？"):
            self.save_window_state()
            self.root.quit()
            
    def run(self):
        self.refresh_list()
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()