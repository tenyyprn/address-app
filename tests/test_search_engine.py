import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '.src/components/ui/card';

const test_search_engine: React.FC = () => {
  return (
    <div className="flex justify-center bg-white dark:bg-gray-800 p-4">
      <div className="w-full max-w-2xl">
        <Card className="w-full bg-card">
          <CardHeader className="bg-card">
            <CardTitle className="text-lg font-semibold bg-card">検索エンジンのテストケース</CardTitle>
            <CardDescription className="text-sm text-muted-foreground bg-card">
              検索機能、フィルタリング機能、あいまい検索、パフォーマンステスト、大量データでのテスト、異常系テスト
            </CardDescription>
          </CardHeader>
          <CardContent className="bg-card">
            <div className="grid gap-4">
              <div>
                <h3 className="text-md font-semibold bg-card">検索機能のテスト</h3>
                <p className="text-sm text-muted-foreground bg-card">
                  連絡先データの検索が正しく機能することを確認します。
                </p>
              </div>
              <div>
                <h3 className="text-md font-semibold bg-card">フィルタリング機能のテスト</h3>
                <p className="text-sm text-muted-foreground bg-card">
                  特定の条件で連絡先データをフィルタリングできることを確認します。
                </p>
              </div>
              <div>
                <h3 className="text-md font-semibold bg-card">あいまい検索のテスト</h3>
                <p className="text-sm text-muted-foreground bg-card">
                  あいまいな検索条件でも適切な結果が返されることを確認します。
                </p>
              </div>
              <div>
                <h3 className="text-md font-semibold bg-card">パフォーマンステスト</h3>
                <p className="text-sm text-muted-foreground bg-card">
                  検索エンジンが大量のデータに対して効率的に動作することを確認します。
                </p>
              </div>
              <div>
                <h3 className="text-md font-semibold bg-card">大量データでのテスト</h3>
                <p className="text-sm text-muted-foreground bg-card">
                  大量の連絡先データが存在する場合でも、検索が正しく機能することを確認します。
                </p>
              </div>
              <div>
                <h3 className="text-md font-semibold bg-card">異常系テスト</h3>
                <p className="text-sm text-muted-foreground bg-card">
                  無効な入力や予期しない状況に対する検索エンジンの耐性をテストします。
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default test_search_engine;