import React, { createContext, useState, useContext } from 'react';

interface LanguageContextType {
    language: string;
    setLanguage: (lang: string) => void;
}

const LanguageContext = createContext<LanguageContextType>({
    language: 'en-US',
    setLanguage: () => {}
});

export const LanguageProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
    const [language, setLanguage] = useState('en-US');

    return (
        <LanguageContext.Provider value={{ language, setLanguage }}>
            {children}
        </LanguageContext.Provider>
    );
};

export const useLanguage = () => useContext(LanguageContext);