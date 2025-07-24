import React, { useState, useEffect } from 'react';

const search_dialog: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchField, setSearchField] = useState('name');
  const [matchType, setMatchType] = useState('partial');
  const [dateRangeStart, setDateRangeStart] = useState('');
  const [dateRangeEnd, setDateRangeEnd] = useState('');
  const [searchHistory, setSearchHistory] = useState<string[]>([]);
  const [sortField, setSortField] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [savedSearches, setSavedSearches] = useState<string[]>([]);

  useEffect(() => {
    // 検索履歴のロード
    const storedHistory = localStorage.getItem('searchHistory');
    if (storedHistory) {
      setSearchHistory(JSON.parse(storedHistory));
    }

    // 保存された検索条件のロード
    const storedSearches = localStorage.getItem('savedSearches');
    if (storedSearches) {
      setSavedSearches(JSON.parse(storedSearches));
    }
  }, []);

  useEffect(() => {
    // 検索履歴の保存
    localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
  }, [searchHistory]);

  useEffect(() => {
    // 保存された検索条件の保存
    localStorage.setItem('savedSearches', JSON.stringify(savedSearches));
  }, [savedSearches]);

  const handleSearch = () => {
    // 検索処理の実装 (search_engine.pyの利用を想定)
    console.log('検索:', searchTerm, searchField, matchType, dateRangeStart, dateRangeEnd);

    // 検索履歴の更新
    setSearchHistory([...searchHistory, searchTerm]);
  };

  const handleSaveSearch = () => {
    // 検索条件の保存
    setSavedSearches([...savedSearches, JSON.stringify({ searchTerm, searchField, matchType, dateRangeStart, dateRangeEnd })]);
  };

  const handleLoadSearch = (search: string) => {
    // 検索条件の読み込み
    const searchParams = JSON.parse(search);
    setSearchTerm(searchParams.searchTerm);
    setSearchField(searchParams.searchField);
    setMatchType(searchParams.matchType);
    setDateRangeStart(searchParams.dateRangeStart);
    setDateRangeEnd(searchParams.dateRangeEnd);
  };

  const handleSort = (field: string) => {
    // ソート処理の実装
    setSortField(field);
    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
  };

  return (
    <div className="flex justify-center items-center h-full bg-white dark:bg-gray-800">
      <Card className="w-full max-w-2xl bg-card">
        <CardHeader className="bg-card">
          <CardTitle className="text-lg font-bold bg-card">検索</CardTitle>
          <CardDescription className="bg-card">連絡先を検索するための高度なオプション</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 bg-card">
          <div className="grid gap-2">
            <Label htmlFor="searchTerm">検索語句</Label>
            <Input
              type="text"
              id="searchTerm"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="searchField">検索フィールド</Label>
            <select
              id="searchField"
              className="px-4 py-2 rounded-md bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
              value={searchField}
              onChange={(e) => setSearchField(e.target.value)}
            >
              <option value="name">名前</option>
              <option value="address">住所</option>
              <option value="phone">電話番号</option>
              <option value="email">メールアドレス</option>
            </select>
          </div>
          <div className="grid gap-2">
            <Label>一致タイプ</Label>
            <RadioGroup defaultValue={matchType} className="flex">
              <RadioGroupItem value="partial" id="partial" onClick={() => setMatchType('partial')} />
              <Label htmlFor="partial">部分一致</Label>
              <RadioGroupItem value="exact" id="exact" onClick={() => setMatchType('exact')} />
              <Label htmlFor="exact">完全一致</Label>
            </RadioGroup>
          </div>
          <div className="grid gap-2">
            <Label>日付範囲 (誕生日)</Label>
            <div className="flex space-x-2">
              <Input
                type="date"
                value={dateRangeStart}
                onChange={(e) => setDateRangeStart(e.target.value)}
              />
              <Input
                type="date"
                value={dateRangeEnd}
                onChange={(e) => setDateRangeEnd(e.target.value)}
              />
            </div>
          </div>
          <Button onClick={handleSearch}>検索</Button>
          <Separator />
          <div>
            <p className="font-bold">検索履歴</p>
            <ul>
              {searchHistory.map((term, index) => (
                <li key={index}>{term}</li>
              ))}
            </ul>
          </div>
          <Separator />
          <div>
            <p className="font-bold">保存された検索条件</p>
            <ul>
              {savedSearches.map((search, index) => (
                <li key={index}>
                  <Button variant="secondary" onClick={() => handleLoadSearch(search)}>
                    {search}
                  </Button>
                </li>
              ))}
            </ul>
            <Button onClick={handleSaveSearch}>検索条件を保存</Button>
          </div>
          <Separator />
          <div>
            <p className="font-bold">ソート</p>
            <div className="flex space-x-2">
              <Button variant="outline" onClick={() => handleSort('name')}>名前</Button>
              <Button variant="outline" onClick={() => handleSort('address')}>住所</Button>
            </div>
            <p>ソート順: {sortOrder === 'asc' ? '昇順' : '降順'}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default search_dialog;
