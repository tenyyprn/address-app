import React from 'react';

const conftest: React.FC = () => {
  return (
    <Card className="w-full bg-card">
      <CardHeader className="bg-card">
        <CardTitle className="bg-card">pytest設定とフィクスチャ定義</CardTitle>
        <CardDescription className="bg-card">テスト用データベースのセットアップやテストデータの作成を行います。</CardDescription>
      </CardHeader>
      <CardContent className="bg-card">
        <ul>
          <li>テスト用データベースのセットアップ</li>
          <li>テストデータの作成</li>
          <li>テスト環境の初期化</li>
          <li>モックデータの生成</li>
          <li>テスト後のクリーンアップ</li>
          <li>共通フィクスチャの定義</li>
        </ul>
      </CardContent>
    </Card>
  );
};

export default conftest;