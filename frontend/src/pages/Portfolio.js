import { useState, useEffect } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { 
  ExternalLink,
  Calendar,
  MapPin,
  Users,
  CheckCircle,
  ArrowRight,
  Lightbulb,
  Star,
  Filter,
  Search,
  Eye,
  Code,
  Smartphone,
  Globe,
  Network,
  Building,
  Camera,
  Satellite,
  Mountain,
  MessageSquare,
  CreditCard
} from "lucide-react";
import { Input } from "../components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";

const Portfolio = () => {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  // Portfolio data
  const portfolioItems = [
    {
      id: 1,
      title: "Afro Bulk SMS Platform",
      category: "Digital Platforms",
      description: "Professional bulk SMS messaging platform serving businesses across Africa with API integration and delivery analytics.",
      image: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=600&h=400&fit=crop",
      technologies: ["React", "Node.js", "MongoDB", "SMS API"],
      client: "Afro Experts",
      date: "2024",
      status: "Live",
      link: "https://afrobulksms.com/",
      results: [
        "50,000+ SMS delivered monthly",
        "99.9% delivery success rate",
        "200+ active business clients"
      ]
    },
    {
      id: 2,
      title: "Afro Pay Payment System",
      category: "Digital Platforms",
      description: "Secure payment processing platform with mobile money integration for MTN, Airtel, and multi-currency support.",
      image: "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600&h=400&fit=crop",
      technologies: ["React", "FastAPI", "Payment APIs", "Security"],
      client: "Afro Experts",
      date: "2024",
      status: "Live",
      link: "https://afropayi.com/",
      results: [
        "$500K+ transactions processed",
        "Secure payment infrastructure",
        "Multi-currency support"
      ]
    },
    {
      id: 3,
      title: "Afro Event Management Platform",
      category: "Digital Platforms",
      description: "Complete event management solution with ticketing, registration, and analytics for African events.",
      image: "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=600&h=400&fit=crop",
      technologies: ["React", "Node.js", "Payment Integration", "Analytics"],
      client: "Afro Experts",
      date: "2024",
      status: "Live",
      link: "http://afroeventz.com/",
      results: [
        "100+ events managed",
        "10,000+ tickets sold",
        "Real-time analytics dashboard"
      ]
    },
    {
      id: 4,
      title: "Enterprise ERP & POS System",
      category: "Business Solutions",
      description: "Comprehensive business management system for multi-vertical operations including marble dust, Starlink, and IT services.",
      image: "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&h=400&fit=crop",
      technologies: ["React", "FastAPI", "MongoDB", "Authentication"],
      client: "Afro Experts",
      date: "2025",
      status: "Active",
      results: [
        "12 integrated modules",
        "Multi-user role management",
        "Real-time business analytics"
      ]
    },
    {
      id: 5,
      title: "Rural School Network Infrastructure",
      category: "Network Solutions",
      description: "Complete network infrastructure setup for rural school in Nyagatare with fiber optic connectivity and Wi-Fi coverage.",
      image: "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=600&h=400&fit=crop",
      technologies: ["Fiber Optic", "Wi-Fi", "Network Security", "Infrastructure"],
      client: "Nyagatare District",
      date: "2024",
      status: "Completed",
      results: [
        "500+ students connected",
        "99% network uptime",
        "High-speed internet access"
      ]
    },
    {
      id: 6,
      title: "Corporate CCTV Security System",
      category: "Security Solutions",
      description: "Advanced CCTV surveillance system with 24/7 monitoring, access control, and remote management for corporate offices.",
      image: "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=600&h=400&fit=crop",
      technologies: ["IP Cameras", "Access Control", "Remote Monitoring", "Cloud Storage"],
      client: "ABC Construction Ltd",
      date: "2024",
      status: "Completed",
      results: [
        "24/7 security monitoring",
        "50+ cameras deployed",
        "Zero security incidents"
      ]
    },
    {
      id: 7,
      title: "Starlink Business Installation",
      category: "Connectivity Solutions",
      description: "High-speed satellite internet installation for remote business operations with full technical support and maintenance.",
      image: "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=600&h=400&fit=crop",
      technologies: ["Starlink", "Satellite Internet", "Network Configuration", "Support"],
      client: "Remote Mining Operation",
      date: "2024",
      status: "Completed",
      results: [
        "150 Mbps internet speed",
        "99% satellite connectivity",
        "Remote location coverage"
      ]
    },
    {
      id: 8,
      title: "Documentary Video Production",
      category: "Media & Events",
      description: "Professional documentary production showcasing Rwanda's technology transformation and digital innovation journey.",
      image: "https://images.unsplash.com/photo-1492619375914-88005aa9e8fb?w=600&h=400&fit=crop",
      technologies: ["4K Video", "Professional Audio", "Post-Production", "Storytelling"],
      client: "Rwanda Tech Initiative",
      date: "2024",
      status: "Completed",
      results: [
        "45-minute documentary",
        "1M+ online views",
        "Award-winning production"
      ]
    },
    {
      id: 9,
      title: "Marble Dust Production Facility",
      category: "Manufacturing",
      description: "Premium marble dust production facility in Rwanda with automated processing and quality control systems.",
      image: "https://images.unsplash.com/photo-1586864387967-d02ef85d93e8?w=600&h=400&fit=crop",
      technologies: ["Industrial Equipment", "Quality Control", "Processing Systems", "Safety"],
      client: "Afro Experts",
      date: "2024",
      status: "Operating",
      results: [
        "50 tons monthly production",
        "Premium quality grade",
        "Rwanda exclusive manufacturing"
      ]
    }
  ];

  const categories = [
    { value: "all", label: "All Projects" },
    { value: "Digital Platforms", label: "Digital Platforms" },
    { value: "Business Solutions", label: "Business Solutions" },
    { value: "Network Solutions", label: "Network Solutions" },
    { value: "Security Solutions", label: "Security Solutions" },
    { value: "Connectivity Solutions", label: "Connectivity Solutions" },
    { value: "Media & Events", label: "Media & Events" },
    { value: "Manufacturing", label: "Manufacturing" }
  ];

  const filteredItems = portfolioItems.filter(item => {
    const matchesCategory = selectedCategory === "all" || item.category === selectedCategory;
    const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const getCategoryIcon = (category) => {
    switch(category) {
      case "Digital Platforms": return MessageSquare;
      case "Business Solutions": return Building;
      case "Network Solutions": return Network;
      case "Security Solutions": return Camera;
      case "Connectivity Solutions": return Satellite;
      case "Media & Events": return Users;
      case "Manufacturing": return Mountain;
      default: return Code;
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case "Live": return "bg-green-500";
      case "Active": return "bg-blue-500";
      case "Completed": return "bg-gray-500";
      case "Operating": return "bg-purple-500";
      default: return "bg-gray-500";
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2">🎯 Our Work</Badge>
          <h1 className="text-4xl md:text-6xl font-bold mb-6">Portfolio</h1>
          <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90">
            Showcasing our successful projects across technology, business solutions, and digital innovation serving clients in Rwanda and Central African Republic.
          </p>
        </div>
      </section>

      {/* Portfolio Stats */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { number: "50+", label: "Projects Completed" },
              { number: "25+", label: "Happy Clients" },
              { number: "3", label: "Live Platforms" },
              { number: "2", label: "Countries Served" }
            ].map((stat, index) => (
              <div key={index} className="text-center">
                <div className="bg-[#66cadb] bg-opacity-10 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-[#0c4864]">{stat.number}</span>
                </div>
                <p className="text-gray-700 font-medium">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Portfolio Filter Section */}
      <section className="py-8 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="flex items-center space-x-4">
              <Filter className="h-5 w-5 text-gray-600" />
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger className="w-[200px]">
                  <SelectValue placeholder="Filter by category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((category) => (
                    <SelectItem key={category.value} value={category.value}>
                      {category.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="flex items-center space-x-2">
              <Search className="h-5 w-5 text-gray-600" />
              <Input
                placeholder="Search projects..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-64"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Portfolio Grid */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-4">Featured Projects</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Explore our diverse portfolio of successful projects spanning digital platforms, business solutions, and infrastructure implementations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredItems.map((item) => {
              const IconComponent = getCategoryIcon(item.category);
              return (
                <Card key={item.id} className="hover:shadow-xl transition-all duration-300 overflow-hidden group">
                  <div className="relative h-48 overflow-hidden">
                    <img 
                      src={item.image} 
                      alt={item.title}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    />
                    <div className="absolute top-4 left-4">
                      <Badge className={`${getStatusColor(item.status)} text-white animate-pulse`}>
                        {item.status}
                      </Badge>
                    </div>
                    <div className="absolute top-4 right-4">
                      <div className="bg-white/20 backdrop-blur-sm rounded-full p-2">
                        <IconComponent className="h-5 w-5 text-white" />
                      </div>
                    </div>
                  </div>
                  
                  <CardHeader>
                    <div className="flex items-center justify-between mb-2">
                      <Badge variant="outline" className="text-xs">
                        {item.category}
                      </Badge>
                      <div className="flex items-center text-sm text-gray-500">
                        <Calendar className="h-4 w-4 mr-1" />
                        {item.date}
                      </div>
                    </div>
                    <CardTitle className="text-xl text-[#0c4864] group-hover:text-[#3b8ea4] transition-colors">
                      {item.title}
                    </CardTitle>
                    <CardDescription className="text-base">
                      {item.description}
                    </CardDescription>
                  </CardHeader>
                  
                  <CardContent>
                    <div className="space-y-4">
                      {/* Client Info */}
                      <div className="flex items-center text-sm text-gray-600">
                        <Building className="h-4 w-4 mr-2" />
                        <span className="font-medium">Client:</span>
                        <span className="ml-1">{item.client}</span>
                      </div>

                      {/* Technologies */}
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-2">Technologies:</p>
                        <div className="flex flex-wrap gap-2">
                          {item.technologies.map((tech, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {tech}
                            </Badge>
                          ))}
                        </div>
                      </div>

                      {/* Results */}
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-2">Key Results:</p>
                        <div className="space-y-1">
                          {item.results.map((result, index) => (
                            <div key={index} className="flex items-center text-sm text-gray-600">
                              <CheckCircle className="h-4 w-4 text-[#3b8ea4] mr-2 flex-shrink-0" />
                              {result}
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex space-x-2 pt-4">
                        <Button className="flex-1 bg-[#3b8ea4] hover:bg-[#0c4864] text-white">
                          <Eye className="h-4 w-4 mr-2" />
                          View Details
                        </Button>
                        {item.link && (
                          <Button 
                            variant="outline"
                            className="border-[#3b8ea4] text-[#3b8ea4] hover:bg-[#3b8ea4] hover:text-white"
                            onClick={() => window.open(item.link, '_blank')}
                          >
                            <ExternalLink className="h-4 w-4" />
                          </Button>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {filteredItems.length === 0 && (
            <div className="text-center py-12">
              <div className="bg-gray-100 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-4">
                <Search className="h-12 w-12 text-gray-400" />
              </div>
              <h3 className="text-xl font-medium text-gray-700 mb-2">No projects found</h3>
              <p className="text-gray-500">Try adjusting your search or filter criteria.</p>
            </div>
          )}
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2">🚀 Ready to Start?</Badge>
          <h2 className="text-3xl md:text-4xl font-bold mb-6">Let's Build Something Amazing Together</h2>
          <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
            Have a project in mind? Let's discuss how we can help bring your vision to life with our expertise and proven track record.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-[#0c4864]">
              Get a Quote
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" className="bg-[#66cadb] hover:bg-[#3b8ea4] text-white">
              Contact Us
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Portfolio;