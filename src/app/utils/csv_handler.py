import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, Button, Input, Label, Separator } from 'src/components/ui/shadcn';

const csv_handler: React.FC = () => {
  const [importFile, setImportFile] = useState<File | null>(null);
  const [exportData, setExportData] = useState<string>('');
  const [message, setMessage] = useState<string>('');

  const handleImportChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setImportFile(e.target.files[0]);
    }
  };

  const handleImport = async () => {
    if (!importFile) {
      setMessage('インポートするCSVファイルを選択してください。');
      return;
    }

    try {
      // ここにCSVファイルの読み込み、データ変換、バリデーション、重複チェックのロジックを実装
      // 例: const data = await parseCSV(importFile);
      // 例: validateData(data);
      // 例: checkDuplicates(data);

      setMessage('CSVファイルのインポートが完了しました。');
    } catch (error: any) {
      setMessage(`CSVファイルのインポート中にエラーが発生しました: ${error.message}`);
    }
  };

  const handleExport = () => {
    // ここにデータのエクスポート、CSV形式への変換ロジックを実装
    // 例: const csvData = convertToCSV(data);
    // 例: setExportData(csvData);

    setMessage('CSVファイルのエクスポートが完了しました。');
  };

  const handleDownload = () => {
    if (!exportData) {
      setMessage('エクスポートするデータがありません。');
      return;
    }

    const blob = new Blob([exportData], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'contacts.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex justify-center mt-8 bg-white dark:bg-gray-800">
      <Card className="w-[600px] bg-card">
        <CardHeader className="bg-card">
          <CardTitle className="text-center bg-card">CSV入出力</CardTitle>
          <CardDescription className="text-center bg-card">CSV形式でのデータインポート・エクスポートを行います。</CardDescription>
        </CardHeader>
        <CardContent className="bg-card">
          <div className="grid gap-4">
            <div>
              <Label htmlFor="import" className="bg-card">CSVファイルを選択:</Label>
              <Input type="file" id="import" accept=".csv" onChange={handleImportChange} className="bg-white dark:bg-gray-700" />
              <Button onClick={handleImport} className="mt-2">インポート</Button>
            </div>
            <Separator />
            <div>
              <Button onClick={handleExport}>エクスポート</Button>
              {exportData && (
                <Button onClick={handleDownload} className="ml-2">ダウンロード</Button>
              )}
            </div>
            {message && (
              <div className="mt-4 text-center">
                {message}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default csv_handler;
