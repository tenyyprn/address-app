import React, { useState, useEffect, useCallback } from 'react';
import { readSettings, writeSettings } from './settings';

const translations: React.FC = () => {
  const [language, setLanguage] = useState<string>('ja');
  const [translations, setTranslations] = useState<{ [key: string]: string }>({});

  const loadTranslations = useCallback(async (lang: string) => {
    try {
      const translationFile = await import(`./${lang}.json`);
      setTranslations(translationFile.default);
    } catch (error) {
      console.error(`Failed to load translations for ${lang}:`, error);
      setTranslations({});
    }
  }, []);

  useEffect(() => {
    const loadInitialLanguage = async () => {
      const settings = await readSettings();
      const initialLanguage = settings.language || 'ja';
      setLanguage(initialLanguage);
      loadTranslations(initialLanguage);
    };

    loadInitialLanguage();
  }, [loadTranslations]);

  const changeLanguage = async (newLanguage: string) => {
    setLanguage(newLanguage);
    loadTranslations(newLanguage);
    await writeSettings({ language: newLanguage });
  };

  const translate = (key: string): string => {
    return translations[key] || key;
  };

  return (
    <div className="w-full bg-white dark:bg-gray-800 p-4">
      <div className="max-w-md mx-auto">
        <Card className="bg-card">
          <CardHeader className="bg-card">
            <CardTitle className="bg-card">{translate('Language Settings')}</CardTitle>
            <CardDescription className="bg-card">{translate('Select your preferred language')}</CardDescription>
          </CardHeader>
          <CardContent className="bg-card">
            <RadioGroup defaultValue={language} onValueChange={changeLanguage} className="flex flex-col space-y-1">
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="ja" id="ja" />
                <Label htmlFor="ja">{translate('Japanese')}</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="en" id="en" />
                <Label htmlFor="en">{translate('English')}</Label>
              </div>
            </RadioGroup>
            <Separator className="my-4" />
            <div>
              <p>{translate('Current Language')}: {language}</p>
              <p>{translate('Translated Text')}: {translate('Hello, world!')}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default translations;
