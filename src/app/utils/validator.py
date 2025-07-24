import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, Input, Label, Button, Separator } from '.src/components/ui/shadcn';

const Validator: React.FC = () => {
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');
  const [date, setDate] = useState('');
  const [text, setText] = useState('');

  const [emailError, setEmailError] = useState('');
  const [phoneError, setPhoneError] = useState('');
  const [addressError, setAddressError] = useState('');
  const [dateError, setDateError] = useState('');
  const [textError, setTextError] = useState('');

  const validateEmail = () => {
    if (!email) {
      setEmailError('メールアドレスを入力してください。');
      return false;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setEmailError('メールアドレスの形式が正しくありません。');
      return false;
    }
    setEmailError('');
    return true;
  };

  const validatePhone = () => {
    if (!phone) {
      setPhoneError('電話番号を入力してください。');
      return false;
    }
    const phoneRegex = /^[0-9]{2,4}-[0-9]{2,4}-[0-9]{3,4}$/;
    if (!phoneRegex.test(phone)) {
      setPhoneError('電話番号の形式が正しくありません。');
      return false;
    }
    setPhoneError('');
    return true;
  };

  const validateAddress = () => {
    if (!address) {
      setAddressError('住所を入力してください。');
      return false;
    }
    if (address.length > 100) {
      setAddressError('住所は100文字以内で入力してください。');
      return false;
    }
    setAddressError('');
    return true;
  };

  const validateDate = () => {
    if (!date) {
      setDateError('日付を入力してください。');
      return false;
    }
    const dateRegex = /^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$/;
    if (!dateRegex.test(date)) {
      setDateError('日付の形式が正しくありません (YYYY-MM-DD)。');
      return false;
    }
    setDateError('');
    return true;
  };

  const validateText = () => {
    if (!text) {
      setTextError('テキストを入力してください。');
      return false;
    }
    if (text.length > 20) {
      setTextError('テキストは20文字以内で入力してください。');
      return false;
    }
    setTextError('');
    return true;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const isEmailValid = validateEmail();
    const isPhoneValid = validatePhone();
    const isAddressValid = validateAddress();
    const isDateValid = validateDate();
    const isTextValid = validateText();

    if (isEmailValid && isPhoneValid && isAddressValid && isDateValid && isTextValid) {
      alert('入力はすべて有効です！');
    } else {
      alert('入力にエラーがあります。');
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-white dark:bg-gray-800">
      <Card className="w-full max-w-md bg-card">
        <CardHeader className="bg-card">
          <CardTitle className="text-lg font-semibold bg-card">データ検証</CardTitle>
          <CardDescription className="text-sm text-gray-500 dark:text-gray-400 bg-card">
            入力されたデータの妥当性をチェックします。
          </CardDescription>
        </CardHeader>
        <CardContent className="bg-card">
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4">
              <div>
                <Label htmlFor="email">メールアドレス</Label>
                <Input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onBlur={validateEmail}
                />
                {emailError && <p className="text-red-500 text-sm">{emailError}</p>}
              </div>
              <div>
                <Label htmlFor="phone">電話番号 (例: 03-1234-5678)</Label>
                <Input
                  type="tel"
                  id="phone"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  onBlur={validatePhone}
                />
                {phoneError && <p className="text-red-500 text-sm">{phoneError}</p>}
              </div>
              <div>
                <Label htmlFor="address">住所 (100文字以内)</Label>
                <Input
                  type="text"
                  id="address"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  onBlur={validateAddress}
                />
                {addressError && <p className="text-red-500 text-sm">{addressError}</p>}
              </div>
              <div>
                <Label htmlFor="date">日付 (YYYY-MM-DD)</Label>
                <Input
                  type="text"
                  id="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  onBlur={validateDate}
                />
                {dateError && <p className="text-red-500 text-sm">{dateError}</p>}
              </div>
              <div>
                <Label htmlFor="text">テキスト (20文字以内)</Label>
                <Input
                  type="text"
                  id="text"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  onBlur={validateText}
                />
                {textError && <p className="text-red-500 text-sm">{textError}</p>}
              </div>
              <Button type="submit">検証</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Validator;
