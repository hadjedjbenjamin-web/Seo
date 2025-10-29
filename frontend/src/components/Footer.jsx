import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { translations } from '../mock';

const Footer = () => {
  const { language } = useLanguage();
  const t = translations[language].footer;

  return (
    <footer className="bg-gradient-to-b from-gray-50 to-white border-t border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          {/* Logo Small */}
          <div className="flex items-center">
            <img 
              src="https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/3ks6etk8_ChatGPT%20Image%2029%20oct.%202025%2C%2008_32_21.png" 
              alt="BK Tech" 
              className="h-8 w-auto opacity-80"
            />
          </div>

          {/* Copyright */}
          <div className="text-center">
            <p className="text-sm text-gray-600">{t.copyright}</p>
          </div>

          {/* Legal */}
          <div>
            <button className="text-sm text-gray-600 hover:text-blue-600 transition-colors duration-300">
              {t.legal}
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
