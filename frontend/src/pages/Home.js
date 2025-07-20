import { useState, useEffect } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Progress } from "../components/ui/progress";
import { useToast } from "../hooks/use-toast";
import axios from "axios";
import { 
  Globe, 
  Zap, 
  Settings, 
  Building, 
  Network, 
  Camera, 
  Server, 
  Headphones,
  MapPin,
  Users,
  TrendingUp,
  CheckCircle,
  ArrowRight,
  Star,
  Loader2
} from "lucide-react";
import { mockData } from "../mock";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [selectedPlan, setSelectedPlan] = useState("business");
  const [impactStats, setImpactStats] = useState(mockData.impact.stats);
  const [testimonials, setTestimonials] = useState(mockData.testimonials);
  const [isQuoteLoading, setIsQuoteLoading] = useState(false);
  const [isStarlinkLoading, setIsStarlinkLoading] = useState(false);
  const { toast } = useToast();

  const iconComponents = {
    Globe,
    Zap,
    Settings,
    Building,
    Network,
    Camera,
    Server,
    Headphones
  };

  // Fetch dynamic data on component mount
  useEffect(() => {
    const fetchDynamicData = async () => {
      try {
        // Fetch impact stats
        const statsResponse = await axios.get(`${API}/stats/impact`);
        if (statsResponse.data) {
          const stats = statsResponse.data;
          setImpactStats([
            { number: `${stats.communities_connected}+`, label: "Communities Connected" },
            { number: `${stats.businesses_served}+`, label: "Businesses Served" },
            { number: `${stats.people_online}+`, label: "People Online" },
            { number: stats.countries_active.toString(), label: "Countries Active" }
          ]);
        }

        // Fetch testimonials
        const testimonialsResponse = await axios.get(`${API}/content/testimonials`);
        if (testimonialsResponse.data?.testimonials) {
          setTestimonials(testimonialsResponse.data.testimonials);
        }
      } catch (error) {
        console.log("Using mock data due to API error:", error.message);
        // Continue using mock data if API fails
      }
    };

    fetchDynamicData();
  }, []);

  const handleQuoteRequest = async () => {
    setIsQuoteLoading(true);
    try {
      // In a real app, you might collect user email first
      // For now, we'll show a success message and redirect to contact
      toast({
        title: "Quote Request",
        description: "Please fill out the contact form to receive your personalized quote.",
        duration: 4000,
      });
      
      // Redirect to contact page after a short delay
      setTimeout(() => {
        window.location.href = '/contact';
      }, 1500);
    } catch (error) {
      toast({
        title: "Error",
        description: "Please try again or contact us directly.",
        variant: "destructive",
      });
    } finally {
      setIsQuoteLoading(false);
    }
  };

  const handleStarlinkProducts = async () => {
    setIsStarlinkLoading(true);
    try {
      // Redirect to products page
      setTimeout(() => {
        window.location.href = '/products';
      }, 500);
    } finally {
      setIsStarlinkLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section 
        className="relative h-screen flex items-center justify-center bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `linear-gradient(rgba(12, 72, 100, 0.8), rgba(59, 142, 164, 0.7)), url(${mockData.hero.backgroundImage})`
        }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 animate-fade-in">
            {mockData.hero.title}
          </h1>
          <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto opacity-90">
            {mockData.hero.subtitle}
          </p>
          <p className="text-lg mb-10 max-w-2xl mx-auto opacity-80">
            {mockData.hero.description}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              className="bg-[#66cadb] hover:bg-[#3b8ea4] text-white px-8 py-3 text-lg font-semibold transition-all duration-300 transform hover:scale-105"
              onClick={handleStarlinkProducts}
              disabled={isStarlinkLoading}
            >
              {isStarlinkLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Loading...
                </>
              ) : (
                <>
                  Explore Starlink Products
                  <ArrowRight className="ml-2 h-5 w-5" />
                </>
              )}
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="border-white text-white hover:bg-white hover:text-[#0c4864] px-8 py-3 text-lg font-semibold transition-all duration-300"
              onClick={handleQuoteRequest}
              disabled={isQuoteLoading}
            >
              {isQuoteLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Processing...
                </>
              ) : (
                "Get a Quote"
              )}
            </Button>
          </div>
        </div>
      </section>

      {/* Starlink Promotion Section */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2 text-sm font-medium">
              🚀 Revolutionary Technology
            </Badge>
            <h2 className="text-3xl md:text-5xl font-bold text-[#0c4864] mb-6">
              {mockData.starlink.title}
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              {mockData.starlink.description}
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            {mockData.starlink.features.map((feature, index) => {
              const IconComponent = iconComponents[feature.icon];
              return (
                <Card key={index} className="hover:shadow-lg transition-all duration-300 border-l-4 border-[#3b8ea4]">
                  <CardHeader className="text-center">
                    <div className="bg-[#66cadb] bg-opacity-10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                      <IconComponent className="h-8 w-8 text-[#0c4864]" />
                    </div>
                    <CardTitle className="text-[#0c4864]">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-center">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Comparison Section */}
          <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12">
            <h3 className="text-2xl md:text-3xl font-bold text-center text-[#0c4864] mb-12">
              Why Choose Starlink Over Traditional ISPs?
            </h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Traditional ISPs */}
              <div className="bg-red-50 rounded-xl p-8 border border-red-200">
                <h4 className="text-xl font-semibold text-red-800 mb-6 text-center">
                  {mockData.starlink.comparison.traditional.title}
                </h4>
                <ul className="space-y-3">
                  {mockData.starlink.comparison.traditional.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-red-700">
                      <div className="w-2 h-2 bg-red-500 rounded-full mr-3"></div>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Starlink */}
              <div className="bg-green-50 rounded-xl p-8 border border-green-200">
                <h4 className="text-xl font-semibold text-green-800 mb-6 text-center">
                  {mockData.starlink.comparison.starlink.title}
                </h4>
                <ul className="space-y-3">
                  {mockData.starlink.comparison.starlink.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-green-700">
                      <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="text-center mt-10">
              <Button size="lg" className="bg-[#0c4864] hover:bg-[#3b8ea4] text-white px-8 py-3">
                Buy Now
              </Button>
              <span className="mx-4 text-gray-400">or</span>
              <Button size="lg" variant="outline" className="border-[#0c4864] text-[#0c4864] hover:bg-[#0c4864] hover:text-white px-8 py-3">
                Book Installation
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Services Overview */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold mb-6">Our IT Services</h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Comprehensive technology solutions designed to empower African businesses with modern infrastructure and support.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {mockData.services.map((service) => {
              const IconComponent = iconComponents[service.icon];
              return (
                <Card key={service.id} className="bg-white/10 border-white/20 hover:bg-white/15 transition-all duration-300 text-white backdrop-blur-sm">
                  <CardHeader className="text-center">
                    <div className="bg-[#66cadb] bg-opacity-20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                      <IconComponent className="h-8 w-8 text-[#66cadb]" />
                    </div>
                    <CardTitle className="text-white">{service.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-gray-200 text-center mb-4">
                      {service.description}
                    </CardDescription>
                    <ul className="space-y-2 text-sm">
                      {service.features.map((feature, index) => (
                        <li key={index} className="flex items-center text-gray-300">
                          <CheckCircle className="w-4 h-4 text-[#66cadb] mr-2 flex-shrink-0" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          <div className="text-center mt-12">
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-[#0c4864] px-8 py-3">
              View All Services
            </Button>
          </div>
        </div>
      </section>

      {/* Impact Map Section */}
      <section className="py-20 bg-gradient-to-br from-white to-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <Badge className="mb-4 bg-[#3b8ea4] text-white px-4 py-2">
              📍 Our Impact
            </Badge>
            <h2 className="text-3xl md:text-5xl font-bold text-[#0c4864] mb-6">
              {mockData.impact.title}
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              See how we're transforming communities across Rwanda and Central African Republic with cutting-edge technology solutions.
            </p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            {impactStats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="bg-[#66cadb] bg-opacity-10 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl font-bold text-[#0c4864]">{stat.number}</span>
                </div>
                <p className="text-lg font-medium text-gray-700">{stat.label}</p>
              </div>
            ))}
          </div>

          {/* Deployment Stories */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {mockData.impact.deployments.map((deployment, index) => (
              <Card key={index} className="hover:shadow-lg transition-all duration-300">
                <CardHeader>
                  <div className="flex items-center space-x-2 mb-2">
                    <MapPin className="h-5 w-5 text-[#3b8ea4]" />
                    <CardTitle className="text-[#0c4864]">{deployment.location}</CardTitle>
                  </div>
                  <CardDescription className="text-base">
                    {deployment.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="bg-[#66cadb] bg-opacity-10 rounded-lg p-4">
                    <p className="font-medium text-[#0c4864] flex items-center">
                      <TrendingUp className="h-4 w-4 mr-2" />
                      Impact: {deployment.impact}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold mb-6">What Our Clients Say</h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Real stories from African businesses and communities we've connected to the digital world.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {testimonials.map((testimonial) => (
              <Card key={testimonial.id} className="bg-white/10 border-white/20 text-white backdrop-blur-sm">
                <CardHeader>
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <CardTitle className="text-white">{testimonial.name}</CardTitle>
                      <CardDescription className="text-gray-300">
                        {testimonial.title} • {testimonial.location}
                      </CardDescription>
                    </div>
                    <div className="flex space-x-1">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                      ))}
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-200 italic">"{testimonial.message}"</p>
                  {testimonial.verified && (
                    <Badge className="mt-3 bg-green-500 text-white">
                      <CheckCircle className="w-3 h-3 mr-1" />
                      Verified
                    </Badge>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-[#3b8ea4] to-[#66cadb] text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-5xl font-bold mb-6">
            Ready to Transform Your Digital Future?
          </h2>
          <p className="text-xl mb-10 opacity-90">
            Join thousands of African businesses already connected to the global digital economy through our innovative solutions.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              className="bg-white text-[#0c4864] hover:bg-gray-100 px-8 py-3 text-lg font-semibold"
              onClick={handleQuoteRequest}
              disabled={isQuoteLoading}
            >
              {isQuoteLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Processing...
                </>
              ) : (
                "Get Started Today"
              )}
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-[#0c4864] px-8 py-3 text-lg font-semibold">
              Schedule Consultation
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;