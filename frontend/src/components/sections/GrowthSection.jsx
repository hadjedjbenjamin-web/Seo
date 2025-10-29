import React from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import { translations } from '../../mock';
import { TrendingUp, Users, Briefcase, DollarSign } from 'lucide-react';

const GrowthSection = () => {
  const { language } = useLanguage();
  const t = translations[language].growth;

  return (
    <section id="growth" className="py-24 bg-white relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute top-1/3 left-1/4 w-96 h-96 bg-blue-100/30 rounded-full blur-3xl"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-gray-900 to-blue-900">
            {t.title}
          </h2>
          <p className="text-xl text-gray-600">{t.subtitle}</p>
        </div>

        {/* Key Highlights */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-16">
          {t.highlights.map((highlight, index) => (
            <div
              key={index}
              className="bg-gradient-to-br from-blue-50 to-cyan-50 p-8 rounded-2xl text-center transform hover:-translate-y-2 transition-all duration-300 border border-blue-100"
            >
              <div className="text-4xl md:text-5xl font-bold text-blue-600 mb-2">
                {highlight.number}
              </div>
              <div className="text-gray-700 font-medium">{highlight.label}</div>
            </div>
          ))}
        </div>

        {/* Growth Chart */}
        <div className="bg-white p-4 md:p-8 rounded-2xl shadow-lg border border-gray-100 mb-12">
          <h3 className="text-xl md:text-2xl font-bold text-gray-900 mb-6 md:mb-8 text-center">
            {language === 'fr' ? 'Évolution du Chiffre d\'Affaires' : 'Revenue Growth'}
          </h3>
          
          {/* Simple Bar Chart - Responsive */}
          <div className="flex items-end justify-between h-64 md:h-96 gap-2 md:gap-4 px-2 md:px-4">
            {t.stats.map((stat, index) => {
              const maxRevenue = 21;
              // Extract numeric value (1.4M€ -> 1.4)
              const revenueValue = parseFloat(stat.revenue);
              const heightPercent = (revenueValue / maxRevenue) * 100;
              
              return (
                <div key={index} className="flex-1 flex flex-col items-center">
                  <div className="w-full flex flex-col items-center justify-end" style={{ height: '200px' }}>
                    <div className="relative w-full group">
                      {/* Value label - always visible */}
                      <div className="mb-1 md:mb-2 text-center font-bold text-blue-600 text-xs md:text-lg">
                        {stat.revenue}
                      </div>
                      {/* Bar */}
                      <div
                        className="w-full bg-gradient-to-t from-blue-600 to-cyan-400 rounded-t-lg transition-all duration-500 hover:opacity-80 md:hover:scale-105"
                        style={{ height: `${heightPercent}%`, minHeight: '20px' }}
                      >
                      </div>
                    </div>
                  </div>
                  {/* Year label */}
                  <div className="mt-2 md:mt-4 font-bold text-gray-700 text-sm md:text-lg">{stat.year}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Detailed Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Clients Evolution */}
          <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
            <div className="flex items-center mb-6">
              <div className="p-3 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg mr-4">
                <Users className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900">
                {language === 'fr' ? 'Clients' : 'Clients'}
              </h3>
            </div>
            <div className="space-y-3">
              {t.stats.map((stat, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-gray-600">{stat.year}</span>
                  <span className="font-bold text-blue-600">{stat.clients}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Projects Evolution */}
          <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
            <div className="flex items-center mb-6">
              <div className="p-3 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg mr-4">
                <Briefcase className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900">
                {language === 'fr' ? 'Projets' : 'Projects'}
              </h3>
            </div>
            <div className="space-y-3">
              {t.stats.map((stat, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-gray-600">{stat.year}</span>
                  <span className="font-bold text-blue-600">{stat.projects}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Revenue Evolution */}
          <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
            <div className="flex items-center mb-6">
              <div className="p-3 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg mr-4">
                <DollarSign className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900">
                {language === 'fr' ? 'CA' : 'Revenue'}
              </h3>
            </div>
            <div className="space-y-3">
              {t.stats.map((stat, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-gray-600">{stat.year}</span>
                  <span className="font-bold text-blue-600">{stat.revenue}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Growth Indicator */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-green-50 to-green-100 px-6 py-3 rounded-full">
            <TrendingUp className="w-5 h-5 text-green-600" />
            <span className="text-green-700 font-semibold">
              {language === 'fr' 
                ? '+1400% de croissance depuis notre création' 
                : '+1400% growth since our creation'}
            </span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default GrowthSection;
