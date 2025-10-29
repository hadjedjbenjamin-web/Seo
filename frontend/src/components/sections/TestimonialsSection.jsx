import React, { useEffect, useCallback } from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import { translations } from '../../mock';
import { Quote, ChevronLeft, ChevronRight } from 'lucide-react';
import useEmblaCarousel from 'embla-carousel-react';
import Autoplay from 'embla-carousel-autoplay';

const TestimonialsSection = () => {
  const { language } = useLanguage();
  const t = translations[language].testimonials;
  
  const [emblaRef, emblaApi] = useEmblaCarousel(
    { loop: true, align: 'start' },
    [Autoplay({ delay: 4000, stopOnInteraction: false })]
  );

  const scrollPrev = useCallback(() => {
    if (emblaApi) emblaApi.scrollPrev();
  }, [emblaApi]);

  const scrollNext = useCallback(() => {
    if (emblaApi) emblaApi.scrollNext();
  }, [emblaApi]);

  return (
    <section className="py-12 bg-white relative overflow-hidden">
      <div className="absolute bottom-0 right-1/3 w-96 h-96 bg-blue-100/30 rounded-full blur-3xl"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-12 text-transparent bg-clip-text bg-gradient-to-r from-gray-900 to-blue-900 pt-4 pb-4 leading-tight">
          {t.title}
        </h2>

        {/* Carousel Container */}
        <div className="relative">
          <div className="overflow-hidden" ref={emblaRef}>
            <div className="flex">
              {t.items.map((testimonial, index) => (
                <div
                  key={index}
                  className="flex-[0_0_100%] min-w-0 md:flex-[0_0_50%] lg:flex-[0_0_33.333%] px-4"
                >
                  <div className="group bg-gradient-to-br from-gray-50 to-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 border border-gray-100 hover:border-blue-200 h-full">
                    <div className="flex flex-col space-y-4 h-full">
                      <Quote className="w-10 h-10 text-blue-400 opacity-50" />
                      <p className="text-gray-700 leading-relaxed italic flex-grow">
                        "{testimonial.text}"
                      </p>
                      <div className="pt-4 border-t border-gray-200">
                        <p className="font-bold text-gray-900">{testimonial.name}</p>
                        <p className="text-sm text-blue-600">{testimonial.company}</p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Navigation Buttons */}
          <button
            onClick={scrollPrev}
            className="hidden md:flex absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 w-12 h-12 bg-white rounded-full shadow-lg items-center justify-center hover:bg-blue-50 transition-colors duration-300 border-2 border-blue-900"
          >
            <ChevronLeft className="w-6 h-6 text-blue-900" />
          </button>
          
          <button
            onClick={scrollNext}
            className="hidden md:flex absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 w-12 h-12 bg-white rounded-full shadow-lg items-center justify-center hover:bg-blue-50 transition-colors duration-300 border-2 border-blue-900"
          >
            <ChevronRight className="w-6 h-6 text-blue-900" />
          </button>
        </div>

        {/* Indicator text */}
        <div className="text-center mt-8 text-sm text-gray-500">
          {language === 'fr' ? 'Défilement automatique' : 'Auto-scrolling'}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;
