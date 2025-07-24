# 📇 住所録管理システム (Address Book Management System)

モダンなWebベースの住所録管理アプリケーションです。ブラウザだけで動作し、インストール不要で使用できます。

![住所録管理システム](https://img.shields.io/badge/Version-2.0-blue.svg)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

## 🌐 デモ

**👉 [ライブデモを見る](https://tenyyprn.github.io/address-app/) 👈**

## ✨ 機能 (Features)

### 🔥 **主要機能**
- **連絡先管理**: 追加・編集・削除・表示
- **リアルタイム検索**: 名前、電話番号、メール、住所での高速検索
- **データの永続化**: ブラウザのローカルストレージに自動保存
- **CSV インポート/エクスポート**: データの一括管理
- **統計表示**: 連絡先数、電話番号・メール保有数の表示
- **レスポンシブデザイン**: PC・タブレット・スマートフォン対応

### 🎨 **UI/UX特徴**
- **モダンデザイン**: グラデーション・シャドウ・アニメーション
- **直感的操作**: ワンクリックで各種操作が完了
- **通知システム**: 操作結果をリアルタイム表示
- **ダークモード対応**: 見やすいコントラスト設計
- **アクセシビリティ**: キーボードショートカット対応

### 🛡️ **セキュリティ・安全性**
- **オフライン動作**: インターネット接続不要
- **プライバシー保護**: データは端末内のみに保存
- **データバックアップ**: CSV形式でのエクスポート機能
- **入力検証**: メールアドレス形式チェック等

## 🚀 システム要件 (System Requirements)

### **必須要件**
- **ブラウザ**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **JavaScript**: 有効化必須
- **ローカルストレージ**: 対応ブラウザ（現代的なブラウザはすべて対応）

### **推奨環境**
- **OS**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 18.04+)
- **メモリ**: 1GB以上
- **ディスク**: 1MB程度の空き容量

## 📥 インストール (Installation)

### **方法1: 直接ダウンロード**
```bash
# GitHubからダウンロード
curl -O https://raw.githubusercontent.com/tenyyprn/address-app/main/index.html

# またはwgetを使用
wget https://raw.githubusercontent.com/tenyyprn/address-app/main/index.html
```

### **方法2: リポジトリクローン**
```bash
git clone https://github.com/tenyyprn/address-app.git
cd address-app
```

### **方法3: 直接作成**
1. 新しいHTMLファイルを作成
2. [index.html](index.html)の内容をコピー&ペースト
3. 保存してブラウザで開く

## 📖 使用方法 (Usage)

### **基本的な起動方法**

#### **Windows**
```cmd
# エクスプローラーでファイルをダブルクリック
# または
start index.html
```

#### **macOS**
```bash
# Finderでファイルをダブルクリック
# または
open index.html
```

#### **Linux**
```bash
# デフォルトブラウザで開く
xdg-open index.html

# 特定のブラウザで開く
firefox index.html
google-chrome index.html
```

### **📋 基本操作**

#### **1. 連絡先の追加**
- 「➕ 新規追加」ボタンをクリック
- 必要事項を入力（名前は必須）
- 「保存」ボタンで追加完了

#### **2. 連絡先の編集**
- 連絡先カードの「✏️」ボタンをクリック
- 情報を修正
- 「保存」ボタンで更新完了

#### **3. 連絡先の削除**
- 連絡先カードの「🗑️」ボタンをクリック
- 確認ダイアログで「OK」をクリック

#### **4. 検索機能**
- 上部の検索ボックスに検索語を入力
- リアルタイムで結果が絞り込まれる
- 空にすると全件表示に戻る

#### **5. データ管理**

**エクスポート（バックアップ）**
```
1. 「📤 エクスポート」ボタンをクリック
2. CSV形式のファイルが自動ダウンロード
3. ファイル名: contacts_YYYY-MM-DD.csv
```

**インポート（復元・一括追加）**
```
1. 「📥 インポート」ボタンをクリック
2. CSVファイルを選択
3. データが自動的に追加される
```

**全データ削除**
```
1. 「🗑️ 全削除」ボタンをクリック
2. 確認ダイアログで「OK」をクリック
3. すべてのデータがクリアされる
```

## 🗂️ データ形式 (Data Format)

### **CSV形式**
```csv
名前,ふりがな,電話番号,メールアドレス,住所,生年月日,メモ
山田太郎,やまだたろう,03-1234-5678,yamada@example.com,東京都渋谷区神南1-1-1,1990-01-15,営業部の責任者
佐藤花子,さとうはなこ,090-8765-4321,sato@example.com,大阪府大阪市北区梅田2-2-2,1985-03-22,マーケティング担当
```

### **ローカルストレージ形式**
```json
[
  {
    "id": 1,
    "name": "山田太郎",
    "furigana": "やまだたろう",
    "phone": "03-1234-5678",
    "email": "yamada@example.com",
    "address": "東京都渋谷区神南1-1-1",
    "birthday": "1990-01-15",
    "notes": "営業部の責任者"
  }
]
```

## 🎯 入力項目 (Input Fields)

| 項目 | 必須 | 形式 | 例 |
|------|------|------|-----|
| **名前** | ✅ | テキスト | 山田太郎 |
| **ふりがな** | ❌ | ひらがな | やまだたろう |
| **電話番号** | ❌ | 数字・ハイフン | 03-1234-5678 |
| **メールアドレス** | ❌ | email形式 | example@domain.com |
| **住所** | ❌ | テキスト（複数行） | 東京都渋谷区... |
| **生年月日** | ❌ | 日付 | 1990-01-15 |
| **メモ** | ❌ | テキスト（複数行） | 自由記入 |

## 🔧 カスタマイズ (Customization)

### **カラーテーマの変更**
```css
/* メインカラーの変更 */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #28a745;
    --danger-color: #dc3545;
}
```

### **フォントの変更**
```css
body {
    font-family: 'Noto Sans JP', 'Yu Gothic', sans-serif;
}
```

### **レイアウトの調整**
```css
/* カードの幅を変更 */
.contact-grid {
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
}
```

## 📱 レスポンシブ対応 (Responsive Design)

### **ブレークポイント**
- **デスクトップ**: 1200px以上
- **タブレット**: 768px - 1199px
- **スマートフォン**: 767px以下

### **各デバイスでの表示**
- **PC**: 3-4列のカードレイアウト
- **タブレット**: 2列のカードレイアウト
- **スマホ**: 1列の縦並びレイアウト

## 🔍 トラブルシューティング (Troubleshooting)

### **よくある問題と解決方法**

#### **Q1: データが保存されない**
```
A: ブラウザの設定を確認してください
- JavaScript が有効になっているか
- ローカルストレージが許可されているか
- プライベートブラウジングモードでないか
```

#### **Q2: 文字化けが発生する**
```
A: 以下を確認してください
- ブラウザのエンコーディング設定（UTF-8）
- CSVファイルの文字コード
- 使用フォントがインストールされているか
```

#### **Q3: CSVインポートが失敗する**
```
A: CSVファイルの形式を確認してください
- 文字コード: UTF-8
- 形式: カンマ区切り
- ヘッダー行: 必須
- データ形式: 上記の例を参照
```

#### **Q4: レイアウトが崩れる**
```
A: ブラウザを確認してください
- 対応ブラウザを使用しているか
- ブラウザのズーム設定（100%推奨）
- キャッシュのクリア
```

### **デバッグ方法**
```javascript
// ブラウザの開発者ツール（F12）でデータ確認
console.log(localStorage.getItem('addressbook_contacts'));

// データのリセット
localStorage.removeItem('addressbook_contacts');
location.reload();
```

## 🔐 セキュリティ注意事項 (Security Notes)

### **データ保護**
- データはブラウザのローカルストレージに保存されます
- 他のWebサイトからはアクセスできません
- 定期的にCSVエクスポートでバックアップを取ることを推奨

### **プライバシー**
- インターネット接続は不要です
- データが外部に送信されることはありません
- ブラウザを閉じてもデータは保持されます

### **注意点**
- ブラウザのデータクリア時にデータが消失する可能性があります
- 複数デバイス間でのデータ同期は行われません
- パスワード保護機能はありません

## 🚧 開発・拡張 (Development)

### **開発環境**
```bash
# 開発に必要なツールは特にありません
# テキストエディタとブラウザがあれば開発可能

# 推奨エディタ
- Visual Studio Code
- Sublime Text
- Atom
```

### **機能拡張のアイデア**
- [ ] パスワード保護機能
- [ ] データ同期機能（Googleドライブ等）
- [ ] グループ・カテゴリ機能
- [ ] 写真添付機能
- [ ] QRコード生成機能
- [ ] 印刷機能

### **貢献方法**
1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📊 パフォーマンス (Performance)

### **ファイルサイズ**
- **HTML**: 約25KB（圧縮前）
- **総サイズ**: 25KB（単一ファイル）
- **ロード時間**: 1秒未満（ローカル）

### **動作速度**
- **起動時間**: 即座
- **検索速度**: リアルタイム（1000件程度まで）
- **データ保存**: 即座

## 📞 サポート (Support)

### **質問・問題報告**
- **GitHub Issues**: https://github.com/tenyyprn/address-app/issues
- **ディスカッション**: https://github.com/tenyyprn/address-app/discussions

### **機能要望**
新機能のご要望は GitHub Issues にて「enhancement」ラベルを付けてご投稿ください。

### **バグ報告**
バグを発見された場合は、以下の情報を含めてご報告ください：
- 使用ブラウザとバージョン
- OS情報
- 再現手順
- 期待する動作と実際の動作

## 📄 ライセンス (License)

```
MIT License

Copyright (c) 2024 tenyyprn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## ✨ 作者・謝辞 (Author & Acknowledgments)

### **作者**
- **GitHub**: https://github.com/tenyyprn
- **Email**: [設定次第で公開]

### **謝辞**
- Web標準技術（HTML5, CSS3, JavaScript ES6+）
- ローカルストレージAPI
- オープンソースコミュニティの皆様

### **インスピレーション**
- モダンWebアプリケーションのデザイントレンド
- ユーザビリティファーストの設計思想
- アクセシビリティガイドライン（WCAG 2.1）

## 🎉 更新履歴 (Changelog)

### **v2.0.0** (2024-07-24)
- 🎉 **HTML版として完全リニューアル**
- ✨ モダンなUI/UXデザイン
- 🚀 レスポンシブデザイン対応
- 📱 全デバイス対応
- 🔍 リアルタイム検索機能
- 📤 CSV インポート/エクスポート機能
- 📢 通知システム
- 🗑️ 全削除機能
- 🛡️ 入力検証強化
- 🌐 文字化け対策

### **v1.0.0** (2024-07-24) - 廃止
- ~~Python tkinter版~~
- ~~SQLiteデータベース~~
- ~~基本的なCRUD操作~~

---

## 🎯 今すぐ始める (Get Started Now)

### **✨ オンラインで試す**
**👉 [https://tenyyprn.github.io/address-app/](https://tenyyprn.github.io/address-app/) 👈**

### **💻 ローカルで使用**
```bash
# 1. ファイルをダウンロード
curl -O https://raw.githubusercontent.com/tenyyprn/address-app/main/index.html

# 2. ブラウザで開く
start index.html  # Windows
open index.html   # macOS
xdg-open index.html  # Linux

# 3. 使い始める！
# 「新規追加」ボタンをクリックして最初の連絡先を追加
```

**🎊 これで住所録管理システムの準備完了です！**

シンプル、高速、安全な住所録管理をお楽しみください。

---

⭐ **気に入ったらStarをお願いします！** ⭐
