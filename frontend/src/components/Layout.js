import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Button } from "./ui/button";
import { Sheet, SheetContent, SheetTrigger } from "./ui/sheet";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
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
  Satellite
} from "lucide-react";
import { mockData } from "../mock";

const Layout = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeMenu, setActiveMenu] = useState(null);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  // Mega menu data structure
  const megaMenuData = {
    services: {
      title: "IT Services",
      subtitle: "Professional technology infrastructure services",
      sections: [
        {
          title: "Core Services",
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
              title: "Afro Experts ERP & POS",
              description: "Complete business management for multiple verticals",
              icon: BarChart3,
              link: "/erp-pos-system",
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
              link: "/erp-pos-system",
              price: "Custom"
            }
          ]
        }
      ]
    },
    "erp-pos-system": {
      title: "ERP & POS System",
      subtitle: "Comprehensive business management for African enterprises",
      sections: [
        {
          title: "Business Verticals",
          items: [
            {
              title: "Marble Dust Production",
              description: "Production tracking and wholesale management",
              icon: Mountain,
              link: "/erp-pos-system#marble"
            },
            {
              title: "IT & Logistics Services",
              description: "Service scheduling and project management",
              icon: Wrench,
              link: "/erp-pos-system#services"
            },
            {
              title: "Second-Hand Products",
              description: "Purchase logging and resale management",
              icon: Recycle,
              link: "/erp-pos-system#secondhand"
            },
            {
              title: "Starlink Resale",
              description: "Inventory and warranty management",
              icon: Satellite,
              link: "/erp-pos-system#starlink"
            }
          ]
        },
        {
          title: "Core Features",
          items: [
            {
              title: "15+ Modules",
              description: "Complete business management suite",
              icon: BarChart3,
              link: "/erp-pos-system#modules"
            },
            {
              title: "Multi-Language",
              description: "English, French, Kinyarwanda support",
              icon: Globe,
              link: "/erp-pos-system#features"
            }
          ]
        }
      ]
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <div className="bg-[#0c4864] text-white px-3 py-2 rounded-lg font-bold text-lg">
                AE
              </div>
              <span className="font-bold text-xl text-[#0c4864]">Afro Experts</span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex items-center space-x-8">
              {mockData.navigation.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`font-medium transition-colors duration-200 ${
                    isActive(item.path)
                      ? "text-[#0c4864] border-b-2 border-[#3b8ea4]"
                      : "text-gray-700 hover:text-[#3b8ea4]"
                  }`}
                >
                  {item.name}
                </Link>
              ))}
              <Button className="bg-[#3b8ea4] hover:bg-[#0c4864] text-white transition-all duration-300">
                Get Quote
              </Button>
            </nav>

            {/* Mobile Menu Button */}
            <Sheet open={isOpen} onOpenChange={setIsOpen}>
              <SheetTrigger asChild className="lg:hidden">
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