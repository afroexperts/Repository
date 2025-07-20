import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { 
  Network, 
  Camera, 
  Server, 
  Headphones,
  CheckCircle,
  ArrowRight,
  Clock,
  Shield,
  Users,
  Wrench
} from "lucide-react";
import { mockData } from "../mock";

const Services = () => {
  const iconComponents = {
    Network,
    Camera,
    Server,
    Headphones
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2">🔧 Professional Services</Badge>
          <h1 className="text-4xl md:text-6xl font-bold mb-6">IT Services</h1>
          <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90">
            Comprehensive technology infrastructure services designed to empower African businesses with reliable, scalable solutions.
          </p>
        </div>
      </section>

      {/* Services Overview */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Our IT Services</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              From network infrastructure to security systems, we provide end-to-end IT solutions that keep your business connected and protected.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {mockData.services.map((service, index) => {
              const IconComponent = iconComponents[service.icon];
              return (
                <Card key={service.id} className="hover:shadow-xl transition-all duration-300 overflow-hidden">
                  <div className="relative h-48 bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] flex items-center justify-center">
                    <img 
                      src={service.image} 
                      alt={service.title}
                      className="absolute inset-0 w-full h-full object-cover opacity-30"
                    />
                    <div className="relative bg-white/10 backdrop-blur-sm rounded-full p-4">
                      <IconComponent className="h-12 w-12 text-white" />
                    </div>
                  </div>
                  
                  <CardHeader>
                    <CardTitle className="text-2xl text-[#0c4864] mb-2">{service.title}</CardTitle>
                    <CardDescription className="text-base">
                      {service.description}
                    </CardDescription>
                  </CardHeader>
                  
                  <CardContent>
                    <div className="space-y-3 mb-6">
                      {service.features.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-center space-x-3">
                          <CheckCircle className="h-5 w-5 text-[#3b8ea4] flex-shrink-0" />
                          <span className="text-gray-700">{feature}</span>
                        </div>
                      ))}
                    </div>
                    
                    <Button className="w-full bg-[#3b8ea4] hover:bg-[#0c4864] text-white">
                      Learn More
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Service Features */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Why Choose Our Services?</h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              We deliver enterprise-grade solutions with local expertise and global standards.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: Clock,
                title: "24/7 Support",
                description: "Round-the-clock technical assistance and monitoring for all our services"
              },
              {
                icon: Shield,
                title: "Secure Solutions",
                description: "Enterprise-grade security protocols to protect your business infrastructure"
              },
              {
                icon: Users,
                title: "Expert Team",
                description: "Certified professionals with deep expertise in African market needs"
              },
              {
                icon: Wrench,
                title: "Maintenance",
                description: "Proactive maintenance and optimization to ensure peak performance"
              }
            ].map((feature, index) => {
              const IconComponent = feature.icon;
              return (
                <Card key={index} className="bg-white/10 border-white/20 text-white backdrop-blur-sm text-center">
                  <CardHeader>
                    <div className="bg-[#66cadb] bg-opacity-20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                      <IconComponent className="h-8 w-8 text-[#66cadb]" />
                    </div>
                    <CardTitle className="text-white">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-gray-200">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Service Process */}
      <section className="py-20 bg-gradient-to-br from-white to-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Our Service Process</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              A streamlined approach to delivering exceptional IT services
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              {
                step: "01",
                title: "Assessment",
                description: "We analyze your current infrastructure and identify areas for improvement"
              },
              {
                step: "02",
                title: "Planning",
                description: "Custom solution design tailored to your specific business requirements"
              },
              {
                step: "03",
                title: "Implementation",
                description: "Professional installation and configuration by our certified technicians"
              },
              {
                step: "04",
                title: "Support",
                description: "Ongoing maintenance, monitoring, and support to ensure optimal performance"
              }
            ].map((process, index) => (
              <div key={index} className="text-center relative">
                <div className="bg-[#66cadb] text-white w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6 text-xl font-bold">
                  {process.step}
                </div>
                <h3 className="text-xl font-semibold text-[#0c4864] mb-4">{process.title}</h3>
                <p className="text-gray-600">{process.description}</p>
                
                {index < 3 && (
                  <div className="hidden md:block absolute top-8 left-full w-full">
                    <ArrowRight className="h-8 w-8 text-[#3b8ea4] mx-auto" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-[#3b8ea4] to-[#66cadb] text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Upgrade Your IT Infrastructure?
          </h2>
          <p className="text-xl mb-10 opacity-90">
            Let our experts assess your current setup and recommend the best solutions for your business growth.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-[#0c4864] hover:bg-gray-100 px-8 py-3 text-lg font-semibold">
              Schedule Assessment
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-[#0c4864] px-8 py-3 text-lg font-semibold">
              Get Quote
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Services;