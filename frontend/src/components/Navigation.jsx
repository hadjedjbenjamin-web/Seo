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
      setMobileMenuOpen(false); // Close mobile menu after clicking
    }
  };

  return (
    <>
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-white/95 backdrop-blur-md shadow-lg' : 'bg-white/80 backdrop-blur-sm'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo */}
            <div className="flex items-center cursor-pointer" onClick={() => scrollToSection('home')}>
              <img 
                src="https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/jbuevisw_ChatGPT_Image_29_oct._2025__08_32_21-removebg-preview.png" 
                alt="BK Tech Logo" 
                className="h-12 w-auto logo-glow"
              />
            </div>

            {/* Desktop Navigation Links */}
            <div className="hidden md:flex items-center space-x-8">
              <button onClick={() => scrollToSection('home')} className="nav-link">{t.home}</button>
              <button onClick={() => scrollToSection('mission')} className="nav-link">{t.mission}</button>
              <button onClick={() => scrollToSection('expertise')} className="nav-link">{t.expertise}</button>
              <button onClick={() => scrollToSection('projects')} className="nav-link">{t.projects}</button>
              <button onClick={() => scrollToSection('growth')} className="nav-link">{t.growth}</button>
              <button onClick={() => scrollToSection('team')} className="nav-link">{t.team}</button>
              <button onClick={() => scrollToSection('contact')} className="nav-link">{t.contact}</button>
            </div>

            {/* Right Side - Language Switch & Mobile Menu */}
            <div className="flex items-center space-x-4">
              {/* Language Switch */}
              <button
                onClick={toggleLanguage}
                className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-gradient-to-r from-blue-50 to-blue-100 hover:from-blue-100 hover:to-blue-200 transition-all duration-300"
              >
                <Globe className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-600">{language.toUpperCase()}</span>
              </button>

              {/* Mobile Menu Button */}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors duration-300"
              >
                {mobileMenuOpen ? (
                  <X className="w-6 h-6 text-gray-700" />
                ) : (
                  <Menu className="w-6 h-6 text-gray-700" />
                )}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="fixed top-20 left-0 right-0 z-40 bg-white/95 backdrop-blur-md shadow-lg md:hidden animate-slideDown">
        <div className="px-4 py-6 space-y-4">
          <button 
            onClick={() => scrollToSection('home')} 
            className="block w-full text-left px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-all duration-300 font-medium"
          >
            {t.home}
          </button>
          <button 
            onClick={() => scrollToSection('mission')} 
            className="block w-full text-left px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-all duration-300 font-medium"
          >
            {t.mission}
          </button>
          <button 
            onClick={() => scrollToSection('expertise')} 
            className="block w-full text-left px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-all duration-300 font-medium"
          >
            {t.expertise}
          </button>
          <button 
            onClick={() => scrollToSection('projects')} 
            className="block w-full text-left px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-all duration-300 font-medium"
          >
            {t.projects}
          </button>
          <button 
            onClick={() => scrollToSection('growth')} 
            className="block w-full text-left px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-all duration-300 font-medium"
          >
            {t.growth}
          </button>
          <button 
            onClick={() => scrollToSection('team')} 
            className="block w-full text-left px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-all duration-300 font-medium"
          >
            {t.team}
          </button>
          <button 
            onClick={() => scrollToSection('contact')} 
            className="block w-full text-left px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-all duration-300 font-medium"
          >
            {t.contact}
          </button>
        </div>
      </div>
      )}
    </>
  );
};

export default Navigation;
