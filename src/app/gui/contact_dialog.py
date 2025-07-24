import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
import os

from src.app.database.contact_model import Contact
from src.app.utils.validator import Validator
from src.app.utils.image_handler import ImageHandler

class ContactDialog:
    def __init__(self, parent, contact=None):
        self.parent = parent
        self.contact = contact
        self.validator = Validator()
        self.image_handler = ImageHandler()
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("連絡先の追加" if contact is None else "連絡先の編集")
        self.dialog.geometry("600x800")
        self.dialog.resizable(False, False)
        
        self.create_widgets()
        
        if contact:
            self.load_contact_data()

    def create_widgets(self):
        # メインフレーム
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 必須項目のラベルスタイル
        required_style = ttk.Style()
        required_style.configure("Required.TLabel", foreground="red")

        # 入力フィールド
        fields = [
            ("氏名", "name", True),
            ("ふりがな", "furigana", True),
            ("住所", "address", True),
            ("電話番号", "phone", True),
            ("メールアドレス", "email", True),
            ("誕生日", "birthday", False),
            ("メモ", "memo", False)
        ]

        self.entries = {}
        
        for i, (label, key, required) in enumerate(fields):
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=5)
            
            label_text = f"{label}{'*' if required else ''}"
            ttk.Label(
                frame,
                text=label_text,
                style="Required.TLabel" if required else "TLabel"
            ).pack(side=tk.LEFT)
            
            if key == "memo":
                entry = tk.Text(frame, height=4, width=40)
            elif key == "birthday":
                entry = ttk.Entry(frame, width=20)
                entry.insert(0, "YYYY-MM-DD")
            else:
                entry = ttk.Entry(frame, width=40)
            
            entry.pack(side=tk.LEFT, padx=5)
            self.entries[key] = entry

        # 画像選択ボタン
        image_frame = ttk.Frame(main_frame)
        image_frame.pack(fill=tk.X, pady=10)
        
        self.image_path = None
        self.image_label = ttk.Label(image_frame, text="写真なし")
        self.image_label.pack(side=tk.LEFT)
        
        ttk.Button(
            image_frame,
            text="画像を選択",
            command=self.select_image
        ).pack(side=tk.LEFT, padx=5)

        # 保存/キャンセルボタン
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(
            button_frame,
            text="保存",
            command=self.save_contact
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="キャンセル",
            command=self.dialog.destroy
        ).pack(side=tk.RIGHT)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")]
        )
        if file_path:
            self.image_path = file_path
            self.image_label.config(text=os.path.basename(file_path))

    def validate_inputs(self):
        errors = []
        
        # 必須項目チェック
        required_fields = {
            "name": "氏名",
            "furigana": "ふりがな",
            "address": "住所",
            "phone": "電話番号",
            "email": "メールアドレス"
        }
        
        for key, label in required_fields.items():
            value = self.entries[key].get().strip()
            if not value:
                errors.append(f"{label}は必須項目です")
                continue
            
            # 各フィールドの個別バリデーション
            if key == "phone" and not self.validator.validate_phone(value):
                errors.append("電話番号の形式が正しくありません")
            elif key == "email" and not self.validator.validate_email(value):
                errors.append("メールアドレスの形式が正しくありません")

        # 誕生日の形式チェック
        birthday = self.entries["birthday"].get().strip()
        if birthday and not self.validator.validate_date(birthday):
            errors.append("誕生日の形式が正しくありません (YYYY-MM-DD)")

        return errors

    def save_contact(self):
        errors = self.validate_inputs()
        if errors:
            messagebox.showerror(
                "入力エラー",
                "\n".join(errors)
            )
            return

        contact_data = {
            "name": self.entries["name"].get().strip(),
            "furigana": self.entries["furigana"].get().strip(),
            "address": self.entries["address"].get().strip(),
            "phone": self.entries["phone"].get().strip(),
            "email": self.entries["email"].get().strip(),
            "birthday": self.entries["birthday"].get().strip(),
            "memo": self.entries["memo"].get("1.0", tk.END).strip()
        }

        if self.image_path:
            contact_data["image"] = self.image_handler.process_image(self.image_path)

        try:
            if self.contact:
                contact_data["id"] = self.contact.id
                Contact.update(contact_data)
            else:
                Contact.create(contact_data)
            
            self.dialog.destroy()
            messagebox.showinfo(
                "成功",
                "連絡先を保存しました"
            )
        except Exception as e:
            messagebox.showerror(
                "エラー",
                f"保存中にエラーが発生しました:\n{str(e)}"
            )

    def load_contact_data(self):
        self.entries["name"].insert(0, self.contact.name)
        self.entries["furigana"].insert(0, self.contact.furigana)
        self.entries["address"].insert(0, self.contact.address)
        self.entries["phone"].insert(0, self.contact.phone)
        self.entries["email"].insert(0, self.contact.email)
        self.entries["birthday"].insert(0, self.contact.birthday or "")
        self.entries["memo"].insert("1.0", self.contact.memo or "")
        
        if self.contact.image:
            self.image_path = self.contact.image
            self.image_label.config(text=os.path.basename(self.contact.image))