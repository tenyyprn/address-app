import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  Input,
  Label,
  Button,
} from 'src/components/ui/shadcn';

const test_validator: React.FC = () => {
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [isValidEmail, setIsValidEmail] = useState(true);
  const [isValidPhoneNumber, setIsValidPhoneNumber] = useState(true);
  const [emailErrorMessage, setEmailErrorMessage] = useState('');
  const [phoneNumberErrorMessage, setPhoneNumberErrorMessage] = useState('');

  const validateEmail = () => {
    // ここにメールアドレスのバリデーションロジックを実装
    // 例: 簡単な形式チェック
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(email);
    setIsValidEmail(isValid);
    setEmailErrorMessage(isValid ? '' : '無効なメールアドレス形式です。');
  };

  const validatePhoneNumber = () => {
    // ここに電話番号のバリデーションロジックを実装
    // 例: 数字のみで指定の桁数
    const phoneRegex = /^\d{10,11}$/;
    const isValid = phoneRegex.test(phoneNumber);
    setIsValidPhoneNumber(isValid);
    setPhoneNumberErrorMessage(isValid ? '' : '無効な電話番号形式です。');
  };

  return (
    <div className="w-full bg-white dark:bg-gray-800 flex justify-center pt-4">
      <Card className="w-full max-w-md bg-card">
        <CardHeader className="bg-card">
          <CardTitle className="bg-card">データ検証テスト</CardTitle>
          <CardDescription className="bg-card">
            入力値の検証とエラーメッセージのテストを行います。
          </CardDescription>
        </CardHeader>
        <CardContent className="bg-card">
          <div className="grid gap-4">
            <div className="space-y-2">
              <Label htmlFor="email">メールアドレス</Label>
              <Input
                id="email"
                placeholder="example@example.com"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              {!isValidEmail && (
                <p className="text-red-500">{emailErrorMessage}</p>
              )}
              <Button variant="outline" onClick={validateEmail}>
                メールアドレスを検証
              </Button>
            </div>
            <div className="space-y-2">
              <Label htmlFor="phoneNumber">電話番号</Label>
              <Input
                id="phoneNumber"
                placeholder="09012345678"
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
              {!isValidPhoneNumber && (
                <p className="text-red-500">{phoneNumberErrorMessage}</p>
              )}
              <Button variant="outline" onClick={validatePhoneNumber}>
                電話番号を検証
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default test_validator;
