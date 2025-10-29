import React, { useState } from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import { translations } from '../../mock';
import { X } from 'lucide-react';

const ProjectsSection = () => {
  const { language } = useLanguage();
  const t = translations[language].projects;
  const [isImageOpen, setIsImageOpen] = useState(false);
  const [selectedImage, setSelectedImage] = useState('');

  const openImage = (imageSrc) => {
    setSelectedImage(imageSrc);
    setIsImageOpen(true);
  };

  const closeImage = () => {
    setIsImageOpen(false);
    setSelectedImage('');
  };

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
                <div 
                  className="rounded-xl mb-6 overflow-hidden bg-gradient-to-br from-gray-900 to-gray-800 p-4 cursor-pointer hover:opacity-90 transition-opacity duration-300"
                  onClick={() => openImage('https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/hgvvagft_visuel%20trading%20BK%20tech.png')}
                >
                  <img 
                    src="https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/hgvvagft_visuel%20trading%20BK%20tech.png" 
                    alt="Plateforme de Trading BK Tech" 
                    className="w-full h-auto object-contain"
                  />
                </div>
              ) : index === 1 ? (
                <div 
                  className="rounded-xl mb-6 overflow-hidden bg-white p-4 cursor-pointer hover:opacity-90 transition-opacity duration-300 border-2 border-blue-500 shadow-lg shadow-blue-200/50"
                  onClick={() => openImage('https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/piq1wh9l_crypto%20sans%20fond%20d%27ecran.png')}
                >
                  <img 
                    src="https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/piq1wh9l_crypto%20sans%20fond%20d%27ecran.png" 
                    alt="Solution Crypto BK Tech" 
                    className="w-full h-auto object-contain"
                  />
                </div>
              ) : index === 2 ? (
                <div 
                  className="rounded-xl mb-6 overflow-hidden bg-white p-4 cursor-pointer hover:opacity-90 transition-opacity duration-300 border-2 border-blue-500 shadow-lg shadow-blue-200/50"
                  onClick={() => openImage('https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/dx2eebs2_dashboard%20analytic%20sans%20fond%20d%20ecran.png')}
                >
                  <img 
                    src="https://customer-assets.emergentagent.com/job_smart-tech-1/artifacts/dx2eebs2_dashboard%20analytic%20sans%20fond%20d%20ecran.png" 
                    alt="Dashboard Analytics BK Tech" 
                    className="w-full h-auto object-contain"
                  />
                </div>
              ) : (
                <div className="rounded-xl mb-6 overflow-hidden bg-white border-2 border-gray-200 p-8 h-48 md:h-56 lg:h-64 flex items-center justify-center">
                  <p className="text-gray-400 text-center font-medium">
                    {language === 'fr' ? 'Projet sur mesure' : 'Custom Project'}
                  </p>
                </div>
              )}
              
              <h3 className="text-2xl font-bold text-gray-900 mb-3">{project.title}</h3>
              <p className="text-gray-600 leading-relaxed">{project.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Image Modal/Lightbox */}
      {isImageOpen && (
        <div 
          className="fixed inset-0 z-[100] bg-black/95 flex items-center justify-center p-4 animate-fadeIn"
          onClick={closeImage}
        >
          <button
            onClick={closeImage}
            className="absolute top-4 right-4 p-2 bg-white/10 hover:bg-white/20 rounded-full transition-colors duration-300"
          >
            <X className="w-8 h-8 text-white" />
          </button>
          
          <div className="max-w-7xl max-h-[90vh] overflow-auto">
            <img 
              src={selectedImage} 
              alt="Vue complète" 
              className="w-full h-auto object-contain"
              onClick={(e) => e.stopPropagation()}
            />
          </div>
        </div>
      )}
    </section>
  );
};

export default ProjectsSection;
