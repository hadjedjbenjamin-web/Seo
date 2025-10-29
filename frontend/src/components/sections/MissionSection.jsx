import React from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import { translations } from '../../mock';

const MissionSection = () => {
  const { language } = useLanguage();
  const t = translations[language].mission;

  return (
    <section id="mission" className="py-24 bg-white relative overflow-hidden">
      {/* Blue Wave Effect */}
      <div className="absolute inset-0 opacity-5">
        <svg className="w-full h-full" viewBox="0 0 1440 320">
          <path
            fill="#0066FF"
            fillOpacity="1"
            d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,149.3C960,160,1056,160,1152,138.7C1248,117,1344,75,1392,53.3L1440,32L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
          ></path>
        </svg>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-6 md:mb-8 text-transparent bg-clip-text bg-gradient-to-r from-gray-900 via-blue-900 to-gray-900">
          {t.title}
        </h2>
        <p className="text-lg md:text-xl text-gray-700 leading-relaxed">
          {t.description}
        </p>
      </div>
    </section>
  );
};

export default MissionSection;
