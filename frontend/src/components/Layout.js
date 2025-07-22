import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Button } from "./ui/button";
import { Sheet, SheetContent, SheetTrigger } from "./ui/sheet";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { useTheme } from "../contexts/ThemeContext";
import { useSettings } from "../contexts/SettingsContext";
import { 
  Menu, 
  Phone, 
  Mail, 
  MapPin, 
  ChevronDown,
  Network,
  Camera,
  Server,
  Headphones,
  Code,
  Cloud,
  Users,
  Smartphone,
  Wifi,
  ShoppingCart,
  BarChart3,
  Building,
  ArrowRight,
  Zap,
  Globe,
  Mountain,
  Wrench,
  Recycle,
  Satellite,
  CreditCard,
  Calendar,
  Sun,
  Moon
} from "lucide-react";
import { mockData } from "../mock";

const Layout = ({ children }) => {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const { settings } = useSettings();
  const [activeMenu, setActiveMenu] = useState(null);
  const [isOpen, setIsOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  // Mega menu data structure
  const megaMenuData = {
    services: {
      title: "Our Services",
      subtitle: "Comprehensive services across multiple industries",
      sections: [
        {
          title: "Technology Services",
          items: [
            {
              title: "Network Setup & Maintenance",
              description: "Professional network infrastructure design and implementation",
              icon: Network,
              link: "/services#network"
            },
            {
              title: "CCTV & Access Control",
              description: "Comprehensive security solutions with advanced monitoring",
              icon: Camera,
              link: "/services#cctv"
            },
            {
              title: "Server Installation",
              description: "Enterprise-grade server deployment and configuration",
              icon: Server,
              link: "/services#server"
            },
            {
              title: "Technical Support",
              description: "Round-the-clock technical assistance and IT support",
              icon: Headphones,
              link: "/services#support"
            },
            {
              title: "Software Development",
              description: "Custom software, mobile apps, and enterprise solutions",
              icon: Code,
              link: "/services#software"
            },
            {
              title: "Internet Provider",
              description: "Fast and reliable internet services with robust infrastructure",
              icon: Wifi,
              link: "/services#internet"
            }
          ]
        },
        {
          title: "Media & Events",
          items: [
            {
              title: "Event Management",
              description: "Hybrid & virtual meetings, live streaming, video coverage",
              icon: Users,
              link: "/services#events"
            },
            {
              title: "Audio-Visual Services",
              description: "Documentary videos, photography, TV & radio commercials",
              icon: Camera,
              link: "/services#audiovisual"
            },
            {
              title: "Design & Branding",
              description: "Logo design, corporate branding, promotional materials",
              icon: Zap,
              link: "/services#design"
            },
            {
              title: "Interpretation Services",
              description: "Simultaneous & consecutive interpretation with equipment",
              icon: Headphones,
              link: "/services#interpretation"
            }
          ]
        },
        {
          title: "Production & Supply",
          items: [
            {
              title: "Marble Dust Production",
              description: "Premium marble dust manufactured exclusively in Rwanda",
              icon: Mountain,
              link: "/services#marble",
              featured: true
            },
            {
              title: "General Supply",
              description: "Quality products and materials for government & businesses",
              icon: ShoppingCart,
              link: "/services#supply"
            }
          ]
        },
        {
          title: "Featured",
          items: [
            {
              title: "Starlink Installation",
              description: "High-speed satellite internet for rural Africa",
              icon: Satellite,
              link: "/products#starlink",
              featured: true
            }
          ]
        }
      ]
    },
    solutions: {
      title: "IT Solutions",
      subtitle: "Custom software development and business solutions",
      sections: [
        {
          title: "Our Solutions",
          items: [
            {
              title: "Afro Bulk SMS",
              description: "Professional bulk SMS messaging platform for businesses",
              icon: Smartphone,
              link: "https://afrobulksms.com/",
              featured: true
            },
            {
              title: "Afro Pay",
              description: "Secure payment processing and financial solutions",
              icon: CreditCard,
              link: "https://afropayi.com/",
              featured: true
            },
            {
              title: "Afro Event",
              description: "Complete event management and ticketing platform",
              icon: Calendar,
              link: "http://afroeventz.com/",
              featured: true
            }
          ]
        },
        {
          title: "Development Services",
          items: [
            {
              title: "Custom Software Development",
              description: "Tailored applications for your business needs",
              icon: Code,
              link: "/solutions#software"
            },
            {
              title: "Cloud Hosting Solutions",
              description: "Reliable and scalable cloud infrastructure",
              icon: Cloud,
              link: "/solutions#cloud"
            }
          ]
        },
        {
          title: "Business Solutions",
          items: [
            {
              title: "ERP/CRM Solutions", 
              description: "Comprehensive business management systems",
              icon: Users,
              link: "/solutions#erp"
            },
            {
              title: "IoT & Smart Office",
              description: "Intelligent automation and connected devices",
              icon: Smartphone,
              link: "/solutions#iot"
            }
          ]
        },
        {
          title: "Featured Solution",
          items: [
            {
              title: "Business Management System",
              description: "Complete ERP & POS solution for African enterprises",
              icon: BarChart3,
              link: "/dashboard",
              featured: true
            }
          ]
        }
      ]
    },
    products: {
      title: "Products & Partners",
      subtitle: "Premium technology products and strategic partnerships",
      sections: [
        {
          title: "Starlink Products",
          items: [
            {
              title: "Residential Kit",
              description: "Complete home internet solution",
              icon: Wifi,
              link: "/products#residential",
              price: "$599"
            },
            {
              title: "Business Kit",
              description: "Enterprise-grade internet solution",
              icon: Building,
              link: "/products#business", 
              price: "$2,500"
            }
          ]
        },
        {
          title: "Business Systems",
          items: [
            {
              title: "POS Terminal",
              description: "Advanced point-of-sale system",
              icon: ShoppingCart,
              link: "/products#pos",
              price: "$399"
            },
            {
              title: "ERP System",
              description: "Enterprise resource planning suite",
              icon: BarChart3,
              link: "/dashboard",
              price: "Custom"
            }
          ]
        }
      ]
    }
  };

  const handleMenuEnter = (menuKey) => {
    setActiveMenu(menuKey);
  };

  const handleMenuLeave = () => {
    setActiveMenu(null);
  };

  const renderMegaMenu = (menuKey) => {
    const menuData = megaMenuData[menuKey];
    if (!menuData) return null;

    return (
      <div 
        className="absolute top-full left-1/2 transform -translate-x-1/2 w-screen max-w-6xl bg-white shadow-2xl border-t border-gray-200 z-50 rounded-b-lg"
        onMouseEnter={() => setActiveMenu(menuKey)}
        onMouseLeave={handleMenuLeave}
      >
        <div className="p-8">
          {/* Menu Header */}
          <div className="mb-8 text-center">
            <h3 className="text-2xl font-bold text-[#0c4864] mb-2">{menuData.title}</h3>
            <p className="text-gray-600">{menuData.subtitle}</p>
          </div>

          {/* Menu Sections */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {menuData.sections.map((section, sectionIndex) => (
              <div key={sectionIndex}>
                <h4 className="font-semibold text-[#0c4864] mb-4 text-lg border-b border-[#3b8ea4] pb-2">{section.title}</h4>
                <div className="space-y-3">
                  {section.items.map((item, itemIndex) => {
                    const IconComponent = item.icon;
                    return (
                      <Link
                        key={itemIndex}
                        to={item.link}
                        className={`block group p-4 rounded-lg hover:bg-gradient-to-r hover:from-[#66cadb] hover:from-5% hover:to-transparent transition-all duration-300 border hover:border-[#3b8ea4] ${
                          item.featured ? 'bg-gradient-to-r from-[#66cadb] from-5% to-transparent border border-[#66cadb] border-opacity-30' : 'border-transparent'
                        }`}
                        onClick={() => setActiveMenu(null)}
                      >
                        <div className="flex items-start space-x-3">
                          <div className={`flex-shrink-0 p-2 rounded-lg transition-colors ${
                            item.featured 
                              ? 'bg-[#0c4864] text-white' 
                              : 'bg-[#3b8ea4] bg-opacity-10 group-hover:bg-[#0c4864] group-hover:text-white'
                          }`}>
                            <IconComponent className={`h-5 w-5 ${
                              item.featured ? 'text-white' : 'text-[#3b8ea4] group-hover:text-white'
                            }`} />
                          </div>
                          <div className="flex-grow">
                            <div className="flex items-center justify-between">
                              <h5 className="font-medium text-gray-900 group-hover:text-[#0c4864] transition-colors">
                                {item.title}
                              </h5>
                              {item.price && (
                                <Badge className="bg-[#66cadb] text-white text-xs">
                                  {item.price}
                                </Badge>
                              )}
                              {item.featured && (
                                <Badge className="bg-[#0c4864] text-white text-xs animate-pulse">
                                  Featured
                                </Badge>
                              )}
                            </div>
                            <p className="text-sm text-gray-600 mt-1 group-hover:text-gray-700 transition-colors">
                              {item.description}
                            </p>
                          </div>
                        </div>
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* Call-to-Action */}
          <div className="mt-8 pt-8 border-t border-gray-200 bg-gradient-to-r from-[#66cadb] from-5% to-transparent rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-semibold text-[#0c4864] mb-1">Ready to get started?</h4>
                <p className="text-gray-600 text-sm">Contact our experts for a personalized consultation.</p>
              </div>
              <div className="flex space-x-3">
                <Button 
                  size="sm" 
                  className="bg-[#3b8ea4] hover:bg-[#0c4864] text-white transition-all duration-300 transform hover:scale-105"
                  onClick={() => {
                    setActiveMenu(null);
                    window.location.href = '/contact';
                  }}
                >
                  Get Quote
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-40 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <div className="bg-[#0c4864] text-white px-3 py-2 rounded-lg font-bold text-lg">
                AE
              </div>
              <span className="font-bold text-xl text-[#0c4864]">Afro Experts</span>
            </Link>

            {/* Desktop Navigation with Mega Menu */}
            <nav className="hidden lg:flex items-center space-x-8 relative">
              <Link
                to="/"
                className={`font-medium transition-colors duration-200 ${
                  isActive("/")
                    ? "text-[#0c4864] border-b-2 border-[#3b8ea4]"
                    : "text-gray-700 hover:text-[#3b8ea4]"
                }`}
              >
                Home
              </Link>
              
              <Link
                to="/about"
                className={`font-medium transition-colors duration-200 ${
                  isActive("/about")
                    ? "text-[#0c4864] border-b-2 border-[#3b8ea4]"
                    : "text-gray-700 hover:text-[#3b8ea4]"
                }`}
              >
                About Us
              </Link>

              {/* Our Services with Mega Menu */}
              <div 
                className="relative"
                onMouseEnter={() => handleMenuEnter('services')}
                onMouseLeave={handleMenuLeave}
              >
                <Link
                  to="/services"
                  className={`font-medium transition-colors duration-200 flex items-center ${
                    isActive("/services")
                      ? "text-[#0c4864] border-b-2 border-[#3b8ea4]"
                      : "text-gray-700 hover:text-[#3b8ea4]"
                  }`}
                >
                  Our Services
                  <ChevronDown className="ml-1 h-4 w-4" />
                </Link>
                {activeMenu === 'services' && renderMegaMenu('services')}
              </div>

              {/* IT Solutions with Mega Menu */}
              <div 
                className="relative"
                onMouseEnter={() => handleMenuEnter('solutions')}
                onMouseLeave={handleMenuLeave}
              >
                <Link
                  to="/solutions"
                  className={`font-medium transition-colors duration-200 flex items-center ${
                    isActive("/solutions")
                      ? "text-[#0c4864] border-b-2 border-[#3b8ea4]"
                      : "text-gray-700 hover:text-[#3b8ea4]"
                  }`}
                >
                  IT Solutions
                  <ChevronDown className="ml-1 h-4 w-4" />
                </Link>
                {activeMenu === 'solutions' && renderMegaMenu('solutions')}
              </div>

              {/* Products with Mega Menu */}
              <div 
                className="relative"
                onMouseEnter={() => handleMenuEnter('products')}
                onMouseLeave={handleMenuLeave}
              >
                <Link
                  to="/products"
                  className={`font-medium transition-colors duration-200 flex items-center ${
                    isActive("/products")
                      ? "text-[#0c4864] border-b-2 border-[#3b8ea4]"
                      : "text-gray-700 hover:text-[#3b8ea4]"
                  }`}
                >
                  Products & Partners
                  <ChevronDown className="ml-1 h-4 w-4" />
                </Link>
                {activeMenu === 'products' && renderMegaMenu('products')}
              </div>

              <Link
                to="/portfolio"
                className={`font-medium transition-colors duration-200 ${
                  isActive("/portfolio")
                    ? "text-[#0c4864] border-b-2 border-[#3b8ea4]"
                    : "text-gray-700 hover:text-[#3b8ea4]"
                }`}
              >
                Portfolio
              </Link>

              <Link
                to="/contact"
                className={`font-medium transition-colors duration-200 ${
                  isActive("/contact")
                    ? "text-[#0c4864] border-b-2 border-[#3b8ea4]"
                    : "text-gray-700 hover:text-[#3b8ea4]"
                }`}
              >
                Contact Us
              </Link>

              <Button className="bg-[#3b8ea4] hover:bg-[#0c4864] text-white transition-all duration-300">
                Get Quote
              </Button>
              
              {/* Theme Toggle */}
              <Button
                variant="ghost"
                size="icon"
                onClick={toggleTheme}
                className="theme-toggle ml-2"
                title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
              >
                {theme === 'light' ? (
                  <Moon className="h-5 w-5" />
                ) : (
                  <Sun className="h-5 w-5" />
                )}
              </Button>
            </nav>

            {/* Mobile Menu and Theme Toggle */}
            <div className="flex items-center space-x-2 lg:hidden">
              {/* Theme Toggle for Mobile */}
              <Button
                variant="ghost"
                size="icon"
                onClick={toggleTheme}
                className="theme-toggle"
                title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
              >
                {theme === 'light' ? (
                  <Moon className="h-5 w-5" />
                ) : (
                  <Sun className="h-5 w-5" />
                )}
              </Button>
              
              {/* Mobile Menu Button */}
              <Sheet open={isOpen} onOpenChange={setIsOpen}>
                <SheetTrigger asChild>
                  <Button variant="ghost" size="icon">
                    <Menu className="h-6 w-6" />
                  </Button>
                </SheetTrigger>
              <SheetContent side="right" className="w-[300px]">
                <div className="flex flex-col space-y-4 mt-8">
                  {mockData.navigation.map((item) => (
                    <Link
                      key={item.path}
                      to={item.path}
                      onClick={() => setIsOpen(false)}
                      className={`font-medium text-lg transition-colors ${
                        isActive(item.path)
                          ? "text-[#0c4864]"
                          : "text-gray-700 hover:text-[#3b8ea4]"
                      }`}
                    >
                      {item.name}
                    </Link>
                  ))}
                  <Button className="bg-[#3b8ea4] hover:bg-[#0c4864] text-white w-full mt-4">
                    Get Quote
                  </Button>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Company Info */}
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="bg-white text-[#0c4864] px-3 py-2 rounded-lg font-bold text-lg">
                  AE
                </div>
                <span className="font-bold text-xl">Afro Experts</span>
              </div>
              <p className="text-gray-300 mb-4">
                {mockData.company.description}
              </p>
              <Link 
                to="/dashboard"
                className="inline-flex items-center bg-[#66cadb] hover:bg-[#3b8ea4] text-white px-4 py-2 rounded-lg font-medium transition-all duration-300 transform hover:scale-105"
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                Access ERP Dashboard
              </Link>
            </div>

            {/* Quick Links */}
            <div>
              <h3 className="font-semibold text-lg mb-4">Quick Links</h3>
              <ul className="space-y-2">
                {mockData.navigation.map((item) => (
                  <li key={item.path}>
                    <Link
                      to={item.path}
                      className="text-gray-300 hover:text-[#66cadb] transition-colors"
                    >
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Services */}
            <div>
              <h3 className="font-semibold text-lg mb-4">Services</h3>
              <ul className="space-y-2 text-gray-300">
                <li>Starlink Installation</li>
                <li>Network Setup</li>
                <li>CCTV Systems</li>
                <li>Cloud Solutions</li>
                <li>Technical Support</li>
                <li>
                  <Link 
                    to="/dashboard" 
                    className="text-[#66cadb] hover:text-white transition-colors font-medium"
                  >
                    🚀 ERP Dashboard
                  </Link>
                </li>
              </ul>
            </div>

            {/* Contact Info */}
            <div>
              <h3 className="font-semibold text-lg mb-4">Contact</h3>
              <div className="space-y-3">
                {mockData.offices.map((office) => (
                  <div key={office.id} className="text-gray-300">
                    <div className="flex items-center space-x-2 mb-1">
                      <MapPin className="h-4 w-4 text-[#66cadb]" />
                      <span className="font-medium">{office.country}</span>
                    </div>
                    <div className="flex items-center space-x-2 mb-1">
                      <Phone className="h-4 w-4 text-[#66cadb]" />
                      <span>{office.phone}</span>
                    </div>
                    <div className="flex items-center space-x-2 mb-3">
                      <Mail className="h-4 w-4 text-[#66cadb]" />
                      <span>{office.email}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-300">
            <p>&copy; 2025 Afro Experts. All rights reserved. Built for Africa's Digital Future.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;