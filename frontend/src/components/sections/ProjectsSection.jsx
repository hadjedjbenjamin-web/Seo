import React from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import { translations } from '../../mock';

const ProjectsSection = () => {
  const { language } = useLanguage();
  const t = translations[language].projects;

  return (
    <section id="projects" className="py-16 bg-white relative overflow-hidden">
      <div className="absolute top-1/2 right-0 w-96 h-96 bg-blue-100/30 rounded-full blur-3xl"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-gray-900 to-blue-900">
            {t.title}
          </h2>
          <p className="text-xl text-gray-600">{t.subtitle}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {t.items.map((project, index) => (
            <div
              key={index}
              className="group bg-gradient-to-br from-gray-50 to-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 border border-gray-200 hover:border-blue-300"
            >
              {/* Project Image */}
              {index === 0 ? (
                <div className="h-48 rounded-xl mb-6 overflow-hidden">
                  <img 
                    src="https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/hgvvagft_visuel%20trading%20BK%20tech.png" 
                    alt="Plateforme de Trading BK Tech" 
                    className="w-full h-full object-cover"
                  />
                </div>
              ) : (
                <div className="bg-gradient-to-br from-blue-100 to-cyan-100 h-48 rounded-xl mb-6 flex items-center justify-center">
                  <div className="text-6xl font-bold text-white/50">{index + 1}</div>
                </div>
              )}
              
              <h3 className="text-2xl font-bold text-gray-900 mb-3">{project.title}</h3>
              <p className="text-gray-600 leading-relaxed">{project.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ProjectsSection;
