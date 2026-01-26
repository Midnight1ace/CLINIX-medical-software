import { useTranslation } from 'react-i18next';

function LanguageSelector() {
  const { t, i18n } = useTranslation();

  const languages = [
    { code: 'en', name: t('language.english') },
    { code: 'ar', name: t('language.arabic') },
    { code: 'ja', name: t('language.japanese') },
    { code: 'ko', name: t('language.korean') }
  ];

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className="language-selector">
      <select
        value={i18n.language}
        onChange={(e) => changeLanguage(e.target.value)}
        className="language-select"
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default LanguageSelector;