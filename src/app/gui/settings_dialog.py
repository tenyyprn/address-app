import React, { useState } from 'react';
import { Button, Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from 'src/components';

const SettingsDialog: React.FC = () => {
  const [language, setLanguage] = useState('ja');
  const [theme, setTheme] = useState('light');
  const [fontSize, setFontSize] = useState(12);
  const [backupInterval, setBackupInterval] = useState(24);
  const [databasePath, setDatabasePath] = useState('./data/address_book.db');

  const handleSave = () => {
    // 設定を保存する処理
  };

  return (
    <Card className="w-full bg-card">
      <CardHeader className="bg-card">
        <CardTitle className="bg-card">設定</CardTitle>
        <CardDescription className="bg-card">アプリケーションの設定を管理します。</CardDescription>
      </CardHeader>
      <CardContent className="bg-card">
        <div>
          <label>言語設定:</label>
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="ja">日本語</option>
            <option value="en">英語</option>
          </select>
        </div>
        <div>
          <label>テーマ設定:</label>
          <select value={theme} onChange={(e) => setTheme(e.target.value)}>
            <option value="light">ライト</option>
            <option value="dark">ダーク</option>
          </select>
        </div>
        <div>
          <label>フォントサイズ:</label>
          <input type="number" value={fontSize} onChange={(e) => setFontSize(Number(e.target.value))} />
        </div>
        <div>
          <label>バックアップ間隔 (時間):</label>
          <input type="number" value={backupInterval} onChange={(e) => setBackupInterval(Number(e.target.value))} />
        </div>
        <div>
          <label>データベースパス:</label>
          <input type="text" value={databasePath} onChange={(e) => setDatabasePath(e.target.value)} />
        </div>
      </CardContent>
      <CardFooter className="bg-card">
        <Button onClick={handleSave}>保存</Button>
      </CardFooter>
    </Card>
  );
};

export default SettingsDialog;