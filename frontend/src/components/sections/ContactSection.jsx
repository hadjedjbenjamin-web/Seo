import React, { useState, useEffect } from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import { translations } from '../../mock';
import { Mail, Phone, Send, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const ContactSection = () => {
  const { language } = useLanguage();
  const t = translations[language].contact;
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });
  
  const [countryCode, setCountryCode] = useState('+33');
  const [status, setStatus] = useState({ type: '', message: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Get country code based on IP
  useEffect(() => {
    const fetchCountryCode = async () => {
      try {
        const response = await axios.get('https://ipapi.co/json/');
        const code = response.data.country_calling_code || '+33';
        setCountryCode(code);
        setFormData(prev => ({ ...prev, phone: code }));
      } catch (error) {
        console.error('Error fetching country code:', error);
        setFormData(prev => ({ ...prev, phone: '+33' }));
      }
    };
    fetchCountryCode();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Pour le téléphone, garder l'indicatif au début
    if (name === 'phone') {
      if (!value.startsWith(countryCode)) {
        setFormData({ ...formData, [name]: countryCode });
        return;
      }
    }
    
    setFormData({ ...formData, [name]: value });
  };

  const validateForm = () => {
    if (!formData.name || !formData.email || !formData.phone || !formData.message) {
      return false;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      return false;
    }
    if (formData.message.length < 10) {
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      setStatus({ 
        type: 'error', 
        message: language === 'fr' 
          ? 'Veuillez remplir tous les champs correctement' 
          : 'Please fill all fields correctly'
      });
      return;
    }

    setIsSubmitting(true);
    setStatus({ type: '', message: '' });

    try {
      const response = await axios.post(`${BACKEND_URL}/api/contact`, formData);
      
      if (response.data.success) {
        setStatus({ 
          type: 'success', 
          message: response.data.message || (language === 'fr' 
            ? 'Votre message a été envoyé avec succès !' 
            : 'Your message has been sent successfully!')
        });
        
        // Reset form
        setFormData({ 
          name: '', 
          email: '', 
          phone: countryCode, 
          message: '' 
        });
      } else {
        setStatus({ 
          type: 'error', 
          message: response.data.message || (language === 'fr'
            ? 'Erreur lors de l\'envoi du message' 
            : 'Error sending message')
        });
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      setStatus({ 
        type: 'error', 
        message: language === 'fr'
          ? 'Erreur lors de l\'envoi du message. Veuillez réessayer.'
          : 'Error sending message. Please try again.'
      });
    } finally {
      setIsSubmitting(false);
      // Clear success message after 5 seconds
      setTimeout(() => {
        if (status.type === 'success') {
          setStatus({ type: '', message: '' });
        }
      }, 5000);
    }
  };

  return (
    <section id="contact" className="py-16 bg-gradient-to-b from-gray-50 to-white relative overflow-hidden">
      <div className="absolute top-1/2 left-1/4 w-96 h-96 bg-blue-100/30 rounded-full blur-3xl"></div>
      
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-gray-900 to-blue-900">
            {t.title}
          </h2>
          <p className="text-xl text-gray-600">{t.subtitle}</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Form */}
          <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-semibold text-gray-700 mb-2">
                  {t.form.name} <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all duration-300"
                  required
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
                  {t.form.email} <span className="text-red-500">*</span>
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all duration-300"
                  required
                />
              </div>

              <div>
                <label htmlFor="phone" className="block text-sm font-semibold text-gray-700 mb-2">
                  {t.form.phone} <span className="text-red-500">*</span>
                </label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  placeholder={`${countryCode} 6 12 34 56 78`}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all duration-300"
                  required
                />
              </div>

              <div>
                <label htmlFor="message" className="block text-sm font-semibold text-gray-700 mb-2">
                  {t.form.message} <span className="text-red-500">*</span>
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  rows="5"
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all duration-300 resize-none"
                  required
                  minLength="10"
                ></textarea>
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className={`w-full flex items-center justify-center space-x-2 px-6 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-semibold hover:shadow-xl hover:shadow-blue-500/50 transform hover:-translate-y-1 transition-all duration-300 ${
                  isSubmitting ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                <span>{isSubmitting ? (language === 'fr' ? 'Envoi...' : 'Sending...') : t.form.submit}</span>
                {!isSubmitting && <Send className="w-5 h-5" />}
              </button>

              {/* Status Message */}
              {status.message && (
                <div className={`flex items-center space-x-2 p-4 rounded-lg ${
                  status.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
                }`}>
                  {status.type === 'success' ? (
                    <CheckCircle className="w-5 h-5" />
                  ) : (
                    <AlertCircle className="w-5 h-5" />
                  )}
                  <span>{status.message}</span>
                </div>
              )}
            </form>
          </div>

          {/* Contact Info */}
          <div className="space-y-8">
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg">
                  <Mail className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Email</h3>
                  <a href="mailto:contact@bktech.dev" className="text-blue-600 hover:text-blue-700 transition-colors duration-300">
                    {t.info.email}
                  </a>
                </div>
              </div>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg">
                  <Phone className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Téléphone / Phone</h3>
                  <a href="tel:+33780913457" className="text-blue-600 hover:text-blue-700 transition-colors duration-300">
                    {t.info.phone}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;
