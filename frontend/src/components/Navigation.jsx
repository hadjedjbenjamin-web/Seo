import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { translations } from '../mock';
import { Globe, Menu, X } from 'lucide-react';

const Navigation = () => {
  const { language, toggleLanguage } = useLanguage();
  const t = translations[language].nav;
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      scrolled ? 'bg-white/95 backdrop-blur-md shadow-lg' : 'bg-white/80 backdrop-blur-sm'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div className="flex items-center cursor-pointer" onClick={() => scrollToSection('home')}>
            <img 
              src="https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/3ks6etk8_ChatGPT%20Image%2029%20oct.%202025%2C%2008_32_21.png" 
              alt="BK Tech Logo" 
              className="h-12 w-auto logo-glow"
            />
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <button onClick={() => scrollToSection('home')} className="nav-link">{t.home}</button>
            <button onClick={() => scrollToSection('mission')} className="nav-link">{t.mission}</button>
            <button onClick={() => scrollToSection('expertise')} className="nav-link">{t.expertise}</button>
            <button onClick={() => scrollToSection('projects')} className="nav-link">{t.projects}</button>
            <button onClick={() => scrollToSection('team')} className="nav-link">{t.team}</button>
            <button onClick={() => scrollToSection('contact')} className="nav-link">{t.contact}</button>
          </div>

          {/* Language Switch */}
          <button
            onClick={toggleLanguage}
            className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-gradient-to-r from-blue-50 to-blue-100 hover:from-blue-100 hover:to-blue-200 transition-all duration-300"
          >
            <Globe className="w-4 h-4 text-blue-600" />
            <span className="text-sm font-medium text-blue-600">{language.toUpperCase()}</span>
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
