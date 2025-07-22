import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const SettingsContext = createContext();

export const useSettings = () => {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error('useSettings must be used within a SettingsProvider');
  }
  return context;
};

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const SettingsProvider = ({ children }) => {
  const [settings, setSettings] = useState({});
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  // Default settings structure
  const defaultSettings = {
    hero: {
      title: "Empowering Africa's Digital Future",
      subtitle: "Comprehensive IT Services & Starlink Internet Solutions for Modern Africa",
      description: "From network infrastructure to satellite internet, we connect African businesses and communities to the global digital economy.",
      primaryButtonText: "Get Started Today",
      primaryButtonLink: "/contact",
      secondaryButtonText: "Learn More", 
      secondaryButtonLink: "/about",
      backgroundImage: null,
      featureImages: []
    },
    starlink: {
      title: "Revolutionary Starlink Technology",
      description: "Experience lightning-fast internet speeds of up to 150 Mbps even in the most remote locations across Africa.",
      showSection: true
    },
    services: {
      title: "Our Services",
      description: "Comprehensive technology solutions designed to empower African businesses with modern infrastructure and support.",
      showSection: true,
      serviceList: [
        "Network Setup & Maintenance",
        "CCTV & Access Control",
        "Server Installation", 
        "Technical Support",
        "Software Development",
        "Internet Provider"
      ]
    },
    clients: {
      title: "Our Clients",
      description: "Trusted by leading organizations across Africa for reliable technology solutions and connectivity.",
      footerText: "Join 1,000+ businesses already transformed by our solutions",
      showSection: true
    },
    general: {
      websiteTitle: "Afro Experts - IT Services & Starlink Solutions",
      companyName: "Afro Experts",
      contactEmail: "info@afroexperts.com",
      supportPhone: "+250 788 123 456",
      companyLogo: null,
      favicon: null
    },
    footer: {
      companyDescription: "Leading provider of IT services and Starlink internet solutions across Africa, connecting communities to the digital future.",
      address: "Kigali, Rwanda",
      phone: "+250 788 123 456",
      email: "info@afroexperts.com",
      copyrightText: "© 2025 Afro Experts. All rights reserved.",
      showDashboardLink: true,
      socialMedia: [
        { platform: "LinkedIn", url: "https://linkedin.com/company/afroexperts" },
        { platform: "Twitter", url: "https://twitter.com/afroexperts" },
        { platform: "Facebook", url: "https://facebook.com/afroexperts" },
        { platform: "Instagram", url: "https://instagram.com/afroexperts" }
      ]
    }
  };

  // Load settings from API
  const loadSettings = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('auth-token');
      const response = await axios.get(`${API}/settings`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      
      if (response.data && response.data.length > 0) {
        const settingsObj = {};
        response.data.forEach(setting => {
          settingsObj[setting.section] = setting.data;
        });
        setSettings({ ...defaultSettings, ...settingsObj });
      } else {
        setSettings(defaultSettings);
      }
    } catch (error) {
      console.error('Error loading settings:', error);
      setSettings(defaultSettings);
    } finally {
      setLoading(false);
    }
  };

  // Save settings to API
  const saveSettings = async (section, data) => {
    try {
      setSaving(true);
      const token = localStorage.getItem('auth-token');
      
      if (!token) {
        throw new Error('No authentication token found');
      }

      await axios.put(`${API}/settings`, {
        section,
        data
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      // Update local state
      setSettings(prev => ({
        ...prev,
        [section]: data
      }));

      return { success: true, message: `${section} settings saved successfully!` };
    } catch (error) {
      console.error('Error saving settings:', error);
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Failed to save settings' 
      };
    } finally {
      setSaving(false);
    }
  };

  // Update local settings without saving
  const updateSettings = (section, data) => {
    setSettings(prev => ({
      ...prev,
      [section]: { ...prev[section], ...data }
    }));
  };

  // Upload image
  const uploadImage = async (file, type = 'general') => {
    try {
      setSaving(true);
      
      // Convert file to base64
      const base64 = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.readAsDataURL(file);
      });

      return { success: true, url: base64 };
    } catch (error) {
      console.error('Error uploading image:', error);
      return { success: false, message: 'Failed to upload image' };
    } finally {
      setSaving(false);
    }
  };

  useEffect(() => {
    loadSettings();
  }, []);

  return (
    <SettingsContext.Provider value={{
      settings,
      loading,
      saving,
      loadSettings,
      saveSettings,
      updateSettings,
      uploadImage
    }}>
      {children}
    </SettingsContext.Provider>
  );
};