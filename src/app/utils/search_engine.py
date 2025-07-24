import React, { useState, useCallback } from 'react';

const search_engine: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searchHistory, setSearchHistory] = useState([]);

  const handleSearch = useCallback(() => {
    // ここに検索ロジックを実装します。
    // 例: データベースからデータを取得し、検索条件に一致する結果をsearchResultsに設定します。
    // あいまい検索、正規表現検索、複数条件での検索などを実装します。
    // 検索結果のランキングも考慮します。

    // ダミーデータ
    const dummyData = [
      { id: 1, name: '山田太郎', address: '東京都', phone: '090-1234-5678', email: 'taro@example.com' },
      { id: 2, name: '田中花子', address: '神奈川県', phone: '080-1111-2222', email: 'hanako@example.com' },
      { id: 3, name: '鈴木一郎', address: '埼玉県', phone: '070-3333-4444', email: 'ichiro@example.com' },
    ];

    // 簡単な検索例（名前による部分一致検索）
    const results = dummyData.filter(item =>
      item.name.includes(searchTerm)
    );

    setSearchResults(results);

    // 検索履歴の更新
    setSearchHistory(prevHistory => [searchTerm, ...prevHistory.slice(0, 4)]); // 最新5件を保持
  }, [searchTerm]);

  return (
    <div className="flex flex-col items-center justify-start min-h-screen bg-white dark:bg-gray-800 pt-10">
      <div className="container w-full max-w-2xl p-4 bg-white dark:bg-gray-800 rounded-lg shadow-md">
        <Card className="w-full bg-card">
          <CardHeader className="bg-card">
            <CardTitle className="text-lg font-semibold bg-card">高度な検索機能</CardTitle>
            <CardDescription className="text-sm text-gray-500 dark:text-gray-400 bg-card">
              名前、住所、電話番号、メールアドレスで検索できます。
            </CardDescription>
          </CardHeader>
          <CardContent className="bg-card">
            <div className="mb-4">
              <Label htmlFor="search" className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2">
                検索キーワード:
              </Label>
              <Input
                type="text"
                id="search"
                placeholder="キーワードを入力"
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
              />
            </div>
            <Button onClick={handleSearch} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
              検索
            </Button>
          </CardContent>
        </Card>

        {/* 検索結果表示 */}
        {searchResults.length > 0 && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">検索結果</h2>
            <ul>
              {searchResults.map(result => (
                <li key={result.id} className="mb-2 p-4 bg-gray-100 dark:bg-gray-700 rounded-md">
                  <p className="text-gray-800 dark:text-gray-200">名前: {result.name}</p>
                  <p className="text-gray-800 dark:text-gray-200">住所: {result.address}</p>
                  <p className="text-gray-800 dark:text-gray-200">電話番号: {result.phone}</p>
                  <p className="text-gray-800 dark:text-gray-200">メールアドレス: {result.email}</p>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* 検索履歴表示 */}
        {searchHistory.length > 0 && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">検索履歴</h2>
            <ul>
              {searchHistory.map((term, index) => (
                <li key={index} className="mb-1 text-gray-800 dark:text-gray-200">{term}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default search_engine;
