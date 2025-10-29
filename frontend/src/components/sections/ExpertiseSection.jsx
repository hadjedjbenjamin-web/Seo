import React from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import { translations } from '../../mock';
import { Code2, Bitcoin, Workflow, Palette } from 'lucide-react';

const iconMap = {
  0: Code2,
  1: Bitcoin,
  2: Workflow,
  3: Palette
};

const ExpertiseSection = () => {
  const { language } = useLanguage();
  const t = translations[language].expertise;

  return (
    <section id="expertise" className="py-16 bg-gradient-to-b from-gray-50 to-white relative overflow-hidden">
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-cyan-100/30 rounded-full blur-3xl"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 text-transparent bg-clip-text bg-gradient-to-r from-gray-900 to-blue-900">
          {t.title}
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {t.items.map((item, index) => {
            const Icon = iconMap[index];
            return (
              <div
                key={index}
                className="group bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 border border-gray-100 hover:border-blue-200"
              >
                <div className="flex items-start space-x-6">
                  <div className="flex-shrink-0 p-4 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl group-hover:shadow-lg group-hover:shadow-blue-200/50 transition-all duration-300">
                    <Icon className="w-8 h-8 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 mb-3">{item.title}</h3>
                    <p className="text-gray-600 leading-relaxed">{item.description}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default ExpertiseSection;
