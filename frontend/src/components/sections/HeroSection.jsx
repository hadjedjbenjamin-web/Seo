import React from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import { translations } from '../../mock';
import { ArrowRight } from 'lucide-react';

const HeroSection = () => {
  const { language } = useLanguage();
  const t = translations[language].hero;

  const scrollToContact = () => {
    const element = document.getElementById('contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden bg-white">
      {/* Technological Wave Background */}
      <div className="absolute inset-0 tech-wave-bg opacity-5"></div>
      
      {/* Gradient Orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-200/30 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-200/30 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 text-center">
        {/* Logo with Large Halo */}
        <div className="flex justify-center mb-12">
          <div className="relative">
            <div className="absolute inset-0 blur-3xl bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-500 opacity-30 scale-150"></div>
            <img 
              src="https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/jbuevisw_ChatGPT_Image_29_oct._2025__08_32_21-removebg-preview.png" 
              alt="BK Tech" 
              className="relative h-32 md:h-40 w-auto hero-logo"
            />
          </div>
        </div>

        {/* Title */}
        <h1 className="text-5xl md:text-7xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-gray-900 via-blue-900 to-gray-900 hero-title">
          {t.title}
        </h1>

        {/* Subtitle */}
        <p className="text-xl md:text-2xl text-gray-700 mb-12 max-w-3xl mx-auto leading-relaxed">
          {t.subtitle}
        </p>

        {/* CTA Button */}
        <button
          onClick={scrollToContact}
          className="group inline-flex items-center space-x-3 px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg text-lg font-semibold hover:shadow-xl hover:shadow-blue-500/50 transform hover:-translate-y-1 transition-all duration-300"
        >
          <span>{t.cta}</span>
          <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
        </button>
      </div>
    </section>
  );
};

export default HeroSection;
