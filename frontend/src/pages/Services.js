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
  Wrench,
  Code,
  Wifi,
  Mountain,
  ShoppingCart,
  Zap,
  Video,
  Palette,
  Mic,
  Globe,
  Building,
  Smartphone,
  Paintbrush,
  TrendingUp,
  MessageSquareText
} from "lucide-react";
import { mockData } from "../mock";

const Services = () => {
  // Comprehensive services data
  const allServices = [
    {
      id: 1,
      title: "Event Management",
      description: "Comprehensive event management services including hybrid meetings, virtual events, and live streaming solutions.",
      icon: Users,
      category: "Media & Events",
      features: [
        "Hybrid & Virtual Meetings with seamless communication",
        "Professional Event Live Streaming services",
        "High-quality Video Coverage for all event types",
        "Real-time engagement across physical and virtual platforms"
      ],
      image: "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400&h=300&fit=crop"
    },
    {
      id: 2,
      title: "Design & Branding",
      description: "Creative and innovative design solutions to help businesses establish and grow their brand identity.",
      icon: Palette,
      category: "Media & Events",
      features: [
        "Professional Logo Design and Corporate Identity",
        "Complete Brand Development and Guidelines",
        "Promotional Material Design and Marketing Collateral",
        "Creative Brand Strategy and Implementation"
      ],
      image: "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400&h=300&fit=crop"
    },
    {
      id: 3,
      title: "Audio-Visual Services",
      description: "Professional audio-visual production services for documentaries, commercials, and corporate communications.",
      icon: Video,
      category: "Media & Events",
      features: [
        "Documentary Video Production with compelling narratives",
        "Professional Photography for events and corporate branding",
        "TV and Radio Commercial Production",
        "Video Teleconferencing Solutions with high-quality audio/video"
      ],
      image: "https://images.unsplash.com/photo-1492619375914-88005aa9e8fb?w=400&h=300&fit=crop"
    },
    {
      id: 4,
      title: "Software Development",
      description: "Custom software development solutions ranging from mobile apps to enterprise software systems.",
      icon: Code,
      category: "Technology Services",
      features: [
        "Custom Mobile App Development (iOS & Android)",
        "Enterprise Software Solutions tailored to business needs",
        "Web Application Development and Maintenance",
        "Software Integration and API Development"
      ],
      image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&h=300&fit=crop"
    },
    {
      id: 5,
      title: "Internet Provider",
      description: "Fast and reliable internet services with robust infrastructure for seamless connectivity.",
      icon: Wifi,
      category: "Technology Services",
      features: [
        "High-speed Internet Connectivity for businesses",
        "Reliable Network Infrastructure and Support",
        "Dedicated Business Internet Plans",
        "24/7 Network Monitoring and Maintenance"
      ],
      image: "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop"
    },
    {
      id: 6,
      title: "General Supply",
      description: "High-quality products and materials delivery for government agencies, businesses, and institutions.",
      icon: ShoppingCart,
      category: "Production & Supply",
      features: [
        "Government Agency Supply Solutions",
        "Business Equipment and Material Procurement",
        "Quality Assurance and Timely Delivery",
        "Institutional Supply Chain Management"
      ],
      image: "https://images.unsplash.com/photo-1566492031773-4f4e44671d66?w=400&h=300&fit=crop"
    },
    {
      id: 7,
      title: "Interpretation Services",
      description: "Comprehensive interpretation services with professional interpreters and state-of-the-art equipment.",
      icon: Mic,
      category: "Media & Events",
      features: [
        "Simultaneous Interpretation for live events and conferences",
        "Consecutive Interpretation for business meetings",
        "Professional Interpretation Equipment Rental",
        "Multi-language Communication Solutions"
      ],
      image: "https://images.unsplash.com/photo-1573166364524-d9d73aff5d15?w=400&h=300&fit=crop"
    },
    {
      id: 8,
      title: "Marble Dust Production",
      description: "Premium marble dust manufactured exclusively in Rwanda for construction and industrial applications.",
      icon: Mountain,
      category: "Production & Supply",
      featured: true,
      features: [
        "Exclusively Produced in Rwanda with Premium Quality",
        "Construction Industry Grade Marble Dust",
        "Industrial Applications and Custom Processing",
        "Sustainable Production and Environmental Compliance"
      ],
      image: "https://images.unsplash.com/photo-1586864387967-d02ef85d93e8?w=400&h=300&fit=crop"
    },
    // New IT Services
    {
      id: 13,
      title: "Web Application",
      description: "Creating dynamic web solutions for your business",
      icon: Globe,
      category: "Technology Services",
      features: [
        "Custom Web Application Development",
        "Responsive Design and Mobile Optimization",
        "Database Integration and API Development",
        "E-commerce and Business Platform Solutions"
      ],
      image: "https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=400&h=300&fit=crop"
    },
    {
      id: 14,
      title: "Mobile Application",
      description: "Building innovative and user-friendly mobile apps",
      icon: Smartphone,
      category: "Technology Services",
      features: [
        "Native iOS and Android App Development",
        "Cross-platform Mobile Solutions",
        "App Store Optimization and Publishing",
        "Mobile App Maintenance and Updates"
      ],
      image: "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400&h=300&fit=crop"
    },
    {
      id: 15,
      title: "UI/UX Design",
      description: "Crafting intuitive designs for optimal user experiences",
      icon: Paintbrush,
      category: "Technology Services",
      features: [
        "User Experience Research and Analysis",
        "Modern Interface Design and Prototyping",
        "Usability Testing and Optimization",
        "Design System Creation and Implementation"
      ],
      image: "https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?w=400&h=300&fit=crop"
    },
    {
      id: 16,
      title: "Domain & Hosting",
      description: "Providing reliable domain registration and hosting services",
      icon: Server,
      category: "Technology Services",
      features: [
        "Domain Registration and Management",
        "Web Hosting Solutions with 99.9% Uptime",
        "SSL Certificates and Security Features",
        "Email Hosting and Professional Email Setup"
      ],
      image: "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop"
    },
    {
      id: 17,
      title: "Digital Marketing",
      description: "Driving online growth through strategic marketing solutions",
      icon: TrendingUp,
      category: "Technology Services",
      features: [
        "Search Engine Optimization (SEO)",
        "Social Media Marketing and Management",
        "Pay-per-Click (PPC) Advertising Campaigns",
        "Content Marketing and Email Marketing"
      ],
      image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop"
    },
    {
      id: 18,
      title: "Tech Consultancy",
      description: "Offering expert guidance for technical challenges",
      icon: MessageSquareText,
      category: "Technology Services",
      features: [
        "Technology Strategy and Planning",
        "Digital Transformation Consulting",
        "IT Infrastructure Assessment and Recommendations",
        "Software Architecture and Technical Advisory"
      ],
      image: "https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&h=300&fit=crop"
    },
    // Traditional IT Services
    {
      id: 19,
      title: "Network Setup & Maintenance",
      description: "Professional network infrastructure design and implementation with ongoing support.",
      icon: Network,
      category: "Technology Services",
      features: [
        "Network Design and Architecture Planning",
        "Router and Switch Configuration",
        "Wireless Network Implementation",
        "Ongoing Maintenance and Support"
      ],
      image: "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop"
    },
    {
      id: 20,
      title: "CCTV & Access Control",
      description: "Comprehensive security solutions with advanced monitoring and access control systems.",
      icon: Camera,
      category: "Technology Services",
      features: [
        "HD CCTV Camera Installation",
        "Access Control Systems",
        "Remote Monitoring Solutions",
        "Security System Integration"
      ],
      image: "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400&h=300&fit=crop"
    },
    {
      id: 21,
      title: "Server Installation",
      description: "Enterprise-grade server deployment and configuration with professional setup.",
      icon: Server,
      category: "Technology Services",
      features: [
        "Server Hardware Installation",
        "Operating System Configuration",
        "Database Setup and Optimization",
        "Backup and Recovery Solutions"
      ],
      image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400&h=300&fit=crop"
    },
    {
      id: 22,
      title: "Technical Support",
      description: "Round-the-clock technical assistance and IT support for all your technology needs.",
      icon: Headphones,
      category: "Technology Services",
      features: [
        "24/7 Technical Support Helpdesk",
        "Remote Troubleshooting and Resolution",
        "On-site Technical Assistance",
        "Preventive Maintenance Services"
      ],
      image: "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=400&h=300&fit=crop"
    }
  ];

  const serviceCategories = [
    { name: "Technology Services", color: "bg-[#0c4864]", icon: Network },
    { name: "Media & Events", color: "bg-[#3b8ea4]", icon: Camera },
    { name: "Production & Supply", color: "bg-[#66cadb]", icon: Mountain }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2">🚀 Comprehensive Services</Badge>
          <h1 className="text-4xl md:text-6xl font-bold mb-6">Our Services</h1>
          <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90">
            A dynamic and versatile company operating in Rwanda and Central African Republic, providing comprehensive services across multiple industries.
          </p>
        </div>
      </section>

      {/* Service Categories Overview */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Service Categories</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We operate across three main service categories, providing comprehensive solutions for all your business needs.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            {serviceCategories.map((category, index) => {
              const IconComponent = category.icon;
              return (
                <Card key={index} className="hover:shadow-lg transition-shadow text-center">
                  <CardHeader>
                    <div className={`inline-flex p-4 rounded-full ${category.color} mx-auto mb-4`}>
                      <IconComponent className="h-8 w-8 text-white" />
                    </div>
                    <CardTitle className="text-xl text-[#0c4864]">{category.name}</CardTitle>
                  </CardHeader>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* All Services */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Complete Service Portfolio</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              From technology infrastructure to creative services and specialized production, we cover all aspects of modern business needs.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {allServices.map((service) => {
              const IconComponent = service.icon;
              return (
                <Card key={service.id} className={`hover:shadow-xl transition-all duration-300 overflow-hidden ${
                  service.featured ? 'ring-2 ring-[#66cadb] ring-opacity-50' : ''
                }`}>
                  <div className="relative h-48 bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] flex items-center justify-center">
                    <img 
                      src={service.image} 
                      alt={service.title}
                      className="absolute inset-0 w-full h-full object-cover opacity-30"
                    />
                    <div className="relative bg-white/10 backdrop-blur-sm rounded-full p-4">
                      <IconComponent className="h-12 w-12 text-white" />
                    </div>
                    {service.featured && (
                      <Badge className="absolute top-4 right-4 bg-[#66cadb] text-white animate-pulse">
                        🇷🇼 Made in Rwanda
                      </Badge>
                    )}
                  </div>
                  
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-2xl text-[#0c4864] mb-2">{service.title}</CardTitle>
                      <Badge variant="outline" className="text-xs">
                        {service.category}
                      </Badge>
                    </div>
                    <CardDescription className="text-base">
                      {service.description}
                    </CardDescription>
                  </CardHeader>
                  
                  <CardContent>
                    <div className="space-y-3 mb-6">
                      {service.features.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-center space-x-3">
                          <CheckCircle className="h-5 w-5 text-[#3b8ea4] flex-shrink-0" />
                          <span className="text-gray-700 text-sm">{feature}</span>
                        </div>
                      ))}
                    </div>
                    
                    <Button className={`w-full transition-all duration-300 ${
                      service.featured 
                        ? 'bg-[#66cadb] hover:bg-[#0c4864] text-white' 
                        : 'bg-[#3b8ea4] hover:bg-[#0c4864] text-white'
                    }`}>
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