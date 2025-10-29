import React from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import { translations } from '../../mock';
import { Quote } from 'lucide-react';

const TestimonialsSection = () => {
  const { language } = useLanguage();
  const t = translations[language].testimonials;

  return (
    <section className="py-16 bg-white relative overflow-hidden">
      <div className="absolute bottom-0 right-1/3 w-96 h-96 bg-blue-100/30 rounded-full blur-3xl"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 text-transparent bg-clip-text bg-gradient-to-r from-gray-900 to-blue-900">
          {t.title}
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {t.items.map((testimonial, index) => (
            <div
              key={index}
              className="group bg-gradient-to-br from-gray-50 to-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 border border-gray-100 hover:border-blue-200"
            >
              <div className="flex flex-col space-y-4">
                <Quote className="w-10 h-10 text-blue-400 opacity-50" />
                <p className="text-gray-700 leading-relaxed italic">"{testimonial.text}"</p>
                <div className="pt-4 border-t border-gray-200">
                  <p className="font-bold text-gray-900">{testimonial.name}</p>
                  <p className="text-sm text-blue-600">{testimonial.company}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;
