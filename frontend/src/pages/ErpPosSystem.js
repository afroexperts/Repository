import { useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../components/ui/accordion";
import { 
  BarChart3,
  Package,
  Warehouse,
  ShoppingCart,
  FileText,
  Users,
  Wrench,
  Recycle,
  Mountain,
  Satellite,
  CreditCard,
  UserCheck,
  Settings,
  Download,
  Globe,
  DollarSign,
  Shield,
  CheckCircle,
  ArrowRight,
  Smartphone,
  Monitor
} from "lucide-react";

const ErpPosSystem = () => {
  const [selectedModule, setSelectedModule] = useState("dashboard");

  const businessVerticals = [
    {
      title: "Marble Dust Production & Wholesale",
      description: "Complete production tracking, inventory management, and wholesale distribution",
      icon: Mountain,
      color: "bg-[#0c4864]"
    },
    {
      title: "IT & Logistics Services",
      description: "Service scheduling, technician assignment, and project management",
      icon: Wrench,
      color: "bg-[#3b8ea4]"
    },
    {
      title: "Second-Hand Products Sales",
      description: "Purchase logging, condition grading, and resale management",
      icon: Recycle,
      color: "bg-[#66cadb]"
    },
    {
      title: "Starlink Product Resale",
      description: "Inventory management, warranty tracking, and regional distribution",
      icon: Satellite,
      color: "bg-gradient-to-br from-[#3b8ea4] to-[#66cadb]"
    }
  ];

  const coreModules = [
    {
      id: "dashboard",
      title: "Dashboard",
      icon: BarChart3,
      description: "Real-time business overview with performance analytics",
      features: [
        "Real-time sales, purchases, inventory, profit/loss summary",
        "Visual charts: daily/weekly/monthly performance",
        "Top-selling products/services analytics",
        "Key performance indicators (KPIs)",
        "Quick action shortcuts"
      ]
    },
    {
      id: "products",
      title: "Product Management",
      icon: Package,
      description: "Comprehensive product and service catalog management",
      features: [
        "Add/Edit/Delete products/services across all categories",
        "Categories: Marble Dust, Services, Second-Hand Products, Starlink Products",
        "Flexible pricing: retail, wholesale, per ton (for marble dust)",
        "Multiple units: per item, per kg, per ton",
        "SKU and barcode support with batch generation"
      ]
    },
    {
      id: "inventory",
      title: "Inventory Management",
      icon: Warehouse,
      description: "Multi-location inventory tracking and optimization",
      features: [
        "Track stock levels by warehouse/location",
        "Automated stock alerts (low stock, out of stock)",
        "Comprehensive stock-in and stock-out logs",
        "Bulk upload for new stock with CSV/Excel support",
        "Wastage and damaged goods logging with cost tracking"
      ]
    },
    {
      id: "pos",
      title: "POS (Point of Sale)",
      icon: ShoppingCart,
      description: "Advanced point-of-sale system with multi-payment support",
      features: [
        "Sell by barcode scanning, product name, or category browse",
        "Client selection (walk-in customers or registered clients)",
        "Apply discounts, VAT, and promotional offers",
        "Multiple payment methods (cash, card, Afro Payi, mobile money)",
        "Print/email/SMS receipt options with customizable templates"
      ]
    },
    {
      id: "orders",
      title: "Order Management",
      icon: FileText,
      description: "End-to-end order processing and fulfillment",
      features: [
        "Create client orders manually or directly from POS",
        "Generate professional pro forma and delivery notes",
        "Assign delivery and logistics team with route optimization",
        "Track order status (Pending, Processing, Shipped, Delivered)",
        "Automated customer notifications at each stage"
      ]
    },
    {
      id: "clients",
      title: "Client Management",
      icon: Users,
      description: "Complete customer relationship management",
      features: [
        "Register new clients (B2C individual or B2B corporate)",
        "Record contact, billing & delivery address information",
        "View comprehensive client order and payment history",
        "Credit limit and balance tracking with automated alerts",
        "Client segmentation and loyalty program support"
      ]
    }
  ];

  const specializedModules = [
    {
      title: "Service Booking Module",
      description: "Schedule and manage IT/logistics services with calendar integration",
      features: [
        "Service scheduling with technician assignment",
        "Invoice generation with deposit tracking",
        "Integrated service calendar",
        "Service completion tracking and quality assurance"
      ]
    },
    {
      title: "Second-Hand Product Sales",
      description: "Specialized module for used and refurbished items",
      features: [
        "Purchase logging (source, cost, acquisition date)",
        "Condition grading system (New, Used, Refurbished)",
        "Automated resale price assignment based on condition",
        "Individual item sales tracking with serial numbers"
      ]
    },
    {
      title: "Marble Dust Module",
      description: "Production-focused module for marble dust operations",
      features: [
        "Daily production input tracking (by ton)",
        "Production cost calculation per ton",
        "Real-time inventory level monitoring",
        "Bulk order management with client-specific pricing",
        "Multi-currency invoice export (RWF and USD)"
      ]
    },
    {
      title: "Starlink Product Resale Module",
      description: "Comprehensive Starlink product management system",
      features: [
        "Inventory management for routers, kits, and accessories",
        "Starlink pricing and bundle configuration",
        "Regional order tracking per country",
        "Warranty management with expiration tracking",
        "Installation scheduling and technician assignment"
      ]
    }
  ];

  const integrationFeatures = [
    {
      title: "Afro Payi Integration",
      description: "Seamless payment processing integration",
      icon: CreditCard
    },
    {
      title: "Afro Bulk SMS",
      description: "Automated order and status notifications",
      icon: Smartphone
    },
    {
      title: "Afro Events Module",
      description: "Event-related service order management",
      icon: FileText
    }
  ];

  const accessLevels = [
    {
      role: "Admin",
      access: "All modules access with full system control",
      permissions: ["Full system access", "User management", "System configuration", "All reports"]
    },
    {
      role: "Manager", 
      access: "All modules except HR settings",
      permissions: ["Sales & inventory management", "Financial reports", "Client management", "Order processing"]
    },
    {
      role: "Cashier",
      access: "POS and Orders modules",
      permissions: ["Point of sale operations", "Order creation", "Payment processing", "Receipt generation"]
    },
    {
      role: "Inventory Officer",
      access: "Stock-related modules only",
      permissions: ["Inventory management", "Stock updates", "Warehouse operations", "Stock reports"]
    },
    {
      role: "Technician",
      access: "Assigned services only",
      permissions: ["Service assignments", "Task completion", "Time tracking", "Service reports"]
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2">🚀 Enterprise Solution</Badge>
          <h1 className="text-4xl md:text-6xl font-bold mb-6">Afro Experts ERP & POS System</h1>
          <p className="text-xl md:text-2xl max-w-4xl mx-auto opacity-90">
            Comprehensive business management system designed for African enterprises. Manage sales, inventory, finance, and logistics across multiple business verticals.
          </p>
        </div>
      </section>

      {/* Business Verticals */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Business Verticals Supported</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our ERP system is specifically designed to handle the diverse operations of modern African businesses.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {businessVerticals.map((vertical, index) => {
              const IconComponent = vertical.icon;
              return (
                <Card key={index} className="hover:shadow-xl transition-all duration-300 text-center">
                  <CardHeader>
                    <div className={`${vertical.color} bg-opacity-10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4`}>
                      <IconComponent className="h-8 w-8 text-[#0c4864]" />
                    </div>
                    <CardTitle className="text-[#0c4864] text-lg">{vertical.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription>
                      {vertical.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Core Modules */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Core Modules</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive modules designed to handle every aspect of your business operations.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {coreModules.map((module) => {
              const IconComponent = module.icon;
              return (
                <Card key={module.id} className="hover:shadow-lg transition-all duration-300">
                  <CardHeader>
                    <div className="flex items-center space-x-4">
                      <div className="bg-[#66cadb] bg-opacity-10 p-3 rounded-lg">
                        <IconComponent className="h-6 w-6 text-[#0c4864]" />
                      </div>
                      <div>
                        <CardTitle className="text-[#0c4864]">{module.title}</CardTitle>
                        <CardDescription>{module.description}</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {module.features.map((feature, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <CheckCircle className="h-4 w-4 text-[#3b8ea4] mt-1 flex-shrink-0" />
                          <span className="text-gray-700 text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Specialized Modules */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Specialized Modules</h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Industry-specific modules tailored for your unique business requirements.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {specializedModules.map((module, index) => (
              <Card key={index} className="bg-white/10 border-white/20 backdrop-blur-sm text-white">
                <CardHeader>
                  <CardTitle className="text-white">{module.title}</CardTitle>
                  <CardDescription className="text-gray-300">
                    {module.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {module.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start space-x-2">
                        <CheckCircle className="h-4 w-4 text-[#66cadb] mt-1 flex-shrink-0" />
                        <span className="text-gray-200 text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Integration & Features */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
            {/* Integration Features */}
            <div>
              <h3 className="text-2xl font-bold text-[#0c4864] mb-8">Optional Integrations</h3>
              <div className="space-y-6">
                {integrationFeatures.map((feature, index) => {
                  const IconComponent = feature.icon;
                  return (
                    <Card key={index} className="hover:shadow-lg transition-all duration-300">
                      <CardContent className="p-6">
                        <div className="flex items-center space-x-4">
                          <div className="bg-[#3b8ea4] bg-opacity-10 p-3 rounded-lg">
                            <IconComponent className="h-6 w-6 text-[#0c4864]" />
                          </div>
                          <div>
                            <h4 className="font-semibold text-[#0c4864]">{feature.title}</h4>
                            <p className="text-gray-600 text-sm">{feature.description}</p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </div>

            {/* System Features */}
            <div>
              <h3 className="text-2xl font-bold text-[#0c4864] mb-8">System Features</h3>
              <Card className="h-fit">
                <CardContent className="p-6">
                  <div className="space-y-4">
                    {[
                      {
                        icon: Globe,
                        title: "Multi-Language Support",
                        description: "English, French, Kinyarwanda"
                      },
                      {
                        icon: DollarSign,
                        title: "Multi-Currency",
                        description: "Support for RWF and USD"
                      },
                      {
                        icon: Monitor,
                        title: "Cross-Platform",
                        description: "Web and mobile POS devices"
                      },
                      {
                        icon: Shield,
                        title: "Role-Based Access",
                        description: "Secure user permissions"
                      }
                    ].map((feature, index) => {
                      const IconComponent = feature.icon;
                      return (
                        <div key={index} className="flex items-start space-x-3">
                          <div className="bg-[#66cadb] bg-opacity-10 p-2 rounded-lg">
                            <IconComponent className="h-5 w-5 text-[#0c4864]" />
                          </div>
                          <div>
                            <h4 className="font-medium text-[#0c4864]">{feature.title}</h4>
                            <p className="text-gray-600 text-sm">{feature.description}</p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Access Levels */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Access Levels & Permissions</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Role-based access control ensures secure and efficient workflow management.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {accessLevels.map((level, index) => (
              <Card key={index} className="hover:shadow-lg transition-all duration-300">
                <CardHeader>
                  <div className="flex items-center space-x-3">
                    <div className="bg-[#66cadb] bg-opacity-10 p-2 rounded-lg">
                      <UserCheck className="h-5 w-5 text-[#0c4864]" />
                    </div>
                    <div>
                      <CardTitle className="text-[#0c4864]">{level.role}</CardTitle>
                      <CardDescription className="text-sm">{level.access}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {level.permissions.map((permission, idx) => (
                      <li key={idx} className="flex items-center space-x-2">
                        <CheckCircle className="h-4 w-4 text-[#3b8ea4]" />
                        <span className="text-gray-700 text-sm">{permission}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-[#3b8ea4] to-[#66cadb] text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Revolutionize Your Business Operations?
          </h2>
          <p className="text-xl mb-10 opacity-90">
            Get a personalized demo of our ERP & POS system and see how it can transform your business processes.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-[#0c4864] hover:bg-gray-100 px-8 py-3 text-lg font-semibold">
              Request Demo
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-[#0c4864] px-8 py-3 text-lg font-semibold">
              <Download className="mr-2 h-5 w-5" />
              Download Specs
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ErpPosSystem;