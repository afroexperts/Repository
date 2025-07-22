import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { 
  Code,
  Cloud,
  Users,
  Smartphone,
  CheckCircle,
  ArrowRight,
  Lightbulb,
  BarChart3,
  Zap,
  Globe,
  CreditCard,
  Calendar,
  MessageSquare,
  ExternalLink
} from "lucide-react";
import { mockData } from "../mock";

const Solutions = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2">💡 Innovative Solutions</Badge>
          <h1 className="text-4xl md:text-6xl font-bold mb-6">IT Solutions</h1>
          <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90">
            Custom software development and intelligent business solutions that drive growth and efficiency for African enterprises.
          </p>
        </div>
      </section>

      {/* Featured ERP/POS System */}
      <section className="py-20 bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2">🏆 Featured Solution</Badge>
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Afro Experts ERP & POS System</h2>
            <p className="text-xl opacity-90 max-w-4xl mx-auto">
              Comprehensive business management system designed specifically for African enterprises operating across multiple verticals including marble dust production, IT services, second-hand products, and Starlink resale.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
            {[
              {
                title: "15+ Core Modules",
                description: "Dashboard, POS, Inventory, CRM, Finance, HR and more",
                icon: "🔧"
              },
              {
                title: "Multi-Business Support",
                description: "Marble dust, IT services, second-hand products, Starlink",
                icon: "🏭"
              },
              {
                title: "Multi-Language",
                description: "English, French, Kinyarwanda support",
                icon: "🌍"
              },
              {
                title: "Multi-Currency",
                description: "RWF and USD with real-time conversion",
                icon: "💰"
              }
            ].map((feature, index) => (
              <Card key={index} className="bg-white/10 border-white/20 backdrop-blur-sm text-white text-center">
                <CardContent className="p-6">
                  <div className="text-3xl mb-4">{feature.icon}</div>
                  <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
                  <p className="text-gray-300 text-sm">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="text-center">
            <Button 
              size="lg" 
              className="bg-[#66cadb] hover:bg-white hover:text-[#0c4864] text-white px-8 py-3 text-lg font-semibold mr-4"
              onClick={() => window.location.href = '/dashboard'}
            >
              Access Dashboard
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-[#0c4864] px-8 py-3 text-lg font-semibold">
              Request Demo
            </Button>
          </div>
        </div>
      </section>

      {/* Solutions Overview */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Our IT Solutions</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Transforming businesses with cutting-edge technology solutions designed for the African market.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {mockData.solutions.map((solution, index) => {
              const icons = [Code, Cloud, Users, Smartphone];
              const IconComponent = icons[index % icons.length];
              const colors = ['bg-[#66cadb]', 'bg-[#3b8ea4]', 'bg-[#0c4864]', 'bg-gradient-to-br from-[#3b8ea4] to-[#66cadb]'];
              
              return (
                <Card key={solution.id} className="hover:shadow-xl transition-all duration-300 overflow-hidden card-hover">
                  <CardHeader className={`${colors[index]} text-white relative`}>
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle className="text-2xl text-white mb-2">{solution.title}</CardTitle>
                        <CardDescription className="text-gray-200">
                          {solution.description}
                        </CardDescription>
                      </div>
                      <div className="bg-white/20 backdrop-blur-sm rounded-full p-3">
                        <IconComponent className="h-8 w-8 text-white" />
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent className="p-6">
                    <h4 className="font-semibold text-[#0c4864] mb-4">Key Features:</h4>
                    <div className="space-y-3 mb-6">
                      {solution.features.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-center space-x-3">
                          <CheckCircle className="h-5 w-5 text-[#3b8ea4] flex-shrink-0" />
                          <span className="text-gray-700">{feature}</span>
                        </div>
                      ))}
                    </div>
                    
                    <Button className="w-full bg-[#3b8ea4] hover:bg-[#0c4864] text-white">
                      Explore Solution
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Solution Categories */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Solution Categories</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Explore our comprehensive range of technology solutions
            </p>
          </div>

          <Tabs defaultValue="development" className="w-full">
            <TabsList className="grid w-full grid-cols-2 lg:grid-cols-4 mb-12">
              <TabsTrigger value="development" className="text-sm">Development</TabsTrigger>
              <TabsTrigger value="cloud" className="text-sm">Cloud</TabsTrigger>
              <TabsTrigger value="business" className="text-sm">Business</TabsTrigger>
              <TabsTrigger value="iot" className="text-sm">IoT</TabsTrigger>
            </TabsList>

            <TabsContent value="development" className="mt-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {[
                  {
                    title: "Web Applications",
                    description: "Modern, responsive web applications built with cutting-edge technologies",
                    features: ["React/Vue.js Frontend", "Node.js/Python Backend", "API Integration", "Mobile Responsive"]
                  },
                  {
                    title: "Mobile Apps",
                    description: "Native and cross-platform mobile applications for iOS and Android",
                    features: ["Cross-platform Development", "Native Performance", "Offline Capabilities", "Push Notifications"]
                  },
                  {
                    title: "Desktop Software",
                    description: "Powerful desktop applications for complex business processes",
                    features: ["Cross-platform Compatibility", "High Performance", "Secure Data Handling", "Custom Workflows"]
                  }
                ].map((item, index) => (
                  <Card key={index} className="hover:shadow-lg transition-all duration-300">
                    <CardHeader>
                      <CardTitle className="text-[#0c4864]">{item.title}</CardTitle>
                      <CardDescription>{item.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-2">
                        {item.features.map((feature, idx) => (
                          <li key={idx} className="flex items-center space-x-2">
                            <CheckCircle className="h-4 w-4 text-[#3b8ea4]" />
                            <span className="text-sm text-gray-600">{feature}</span>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="cloud" className="mt-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {[
                  {
                    title: "AWS Solutions",
                    description: "Comprehensive Amazon Web Services implementation and management",
                    features: ["EC2 & ECS Setup", "S3 Storage Solutions", "Lambda Functions", "RDS Management"]
                  },
                  {
                    title: "Microsoft Azure",
                    description: "Enterprise Azure cloud solutions and Office 365 integration",
                    features: ["Virtual Machines", "Azure AD Integration", "Office 365 Setup", "Backup Solutions"]
                  },
                  {
                    title: "Google Cloud",
                    description: "Google Cloud Platform services and AI/ML integration",
                    features: ["Compute Engine", "Cloud Storage", "BigQuery Analytics", "AI/ML Services"]
                  }
                ].map((item, index) => (
                  <Card key={index} className="hover:shadow-lg transition-all duration-300">
                    <CardHeader>
                      <CardTitle className="text-[#0c4864]">{item.title}</CardTitle>
                      <CardDescription>{item.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-2">
                        {item.features.map((feature, idx) => (
                          <li key={idx} className="flex items-center space-x-2">
                            <CheckCircle className="h-4 w-4 text-[#3b8ea4]" />
                            <span className="text-sm text-gray-600">{feature}</span>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="business" className="mt-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {[
                  {
                    title: "ERP Systems",
                    description: "Complete enterprise resource planning solutions",
                    features: ["Financial Management", "Inventory Control", "HR Management", "Reporting Dashboard"]
                  },
                  {
                    title: "CRM Solutions",
                    description: "Customer relationship management and sales automation",
                    features: ["Lead Management", "Sales Pipeline", "Customer Support", "Analytics & Reports"]
                  },
                  {
                    title: "Business Intelligence",
                    description: "Data analytics and business intelligence platforms",
                    features: ["Data Visualization", "Custom Dashboards", "Real-time Analytics", "Predictive Insights"]
                  }
                ].map((item, index) => (
                  <Card key={index} className="hover:shadow-lg transition-all duration-300">
                    <CardHeader>
                      <CardTitle className="text-[#0c4864]">{item.title}</CardTitle>
                      <CardDescription>{item.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-2">
                        {item.features.map((feature, idx) => (
                          <li key={idx} className="flex items-center space-x-2">
                            <CheckCircle className="h-4 w-4 text-[#3b8ea4]" />
                            <span className="text-sm text-gray-600">{feature}</span>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="iot" className="mt-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {[
                  {
                    title: "Smart Office",
                    description: "Intelligent office automation and control systems",
                    features: ["Smart Lighting", "Climate Control", "Security Integration", "Energy Management"]
                  },
                  {
                    title: "Industrial IoT",
                    description: "Industrial automation and monitoring solutions",
                    features: ["Equipment Monitoring", "Predictive Maintenance", "Process Automation", "Real-time Alerts"]
                  },
                  {
                    title: "Smart Buildings",
                    description: "Comprehensive building management systems",
                    features: ["Access Control", "Environmental Monitoring", "Energy Optimization", "Tenant Management"]
                  }
                ].map((item, index) => (
                  <Card key={index} className="hover:shadow-lg transition-all duration-300">
                    <CardHeader>
                      <CardTitle className="text-[#0c4864]">{item.title}</CardTitle>
                      <CardDescription>{item.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-2">
                        {item.features.map((feature, idx) => (
                          <li key={idx} className="flex items-center space-x-2">
                            <CheckCircle className="h-4 w-4 text-[#3b8ea4]" />
                            <span className="text-sm text-gray-600">{feature}</span>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Benefits of Our Solutions</h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Transform your business operations with our innovative technology solutions
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: Lightbulb,
                title: "Innovation",
                description: "Cutting-edge technology solutions that give you a competitive advantage"
              },
              {
                icon: BarChart3,
                title: "Efficiency",
                description: "Streamlined processes that reduce costs and increase productivity"
              },
              {
                icon: Zap,
                title: "Speed",
                description: "Rapid deployment and quick time-to-market for your digital initiatives"
              },
              {
                icon: Globe,
                title: "Scalability",
                description: "Solutions that grow with your business and adapt to changing needs"
              }
            ].map((benefit, index) => {
              const IconComponent = benefit.icon;
              return (
                <Card key={index} className="bg-white/10 border-white/20 text-white backdrop-blur-sm text-center">
                  <CardHeader>
                    <div className="bg-[#66cadb] bg-opacity-20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                      <IconComponent className="h-8 w-8 text-[#66cadb]" />
                    </div>
                    <CardTitle className="text-white">{benefit.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-gray-200">
                      {benefit.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-[#3b8ea4] to-[#66cadb] text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Transform Your Business?
          </h2>
          <p className="text-xl mb-10 opacity-90">
            Let's discuss how our custom solutions can drive your business forward in the digital age.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-[#0c4864] hover:bg-gray-100 px-8 py-3 text-lg font-semibold">
              Schedule Consultation
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-[#0c4864] px-8 py-3 text-lg font-semibold">
              View Portfolio
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Solutions;