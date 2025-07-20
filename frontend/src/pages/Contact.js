import { useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Badge } from "../components/ui/badge";
import { useToast } from "../hooks/use-toast";
import axios from "axios";
import { 
  MapPin,
  Phone,
  Mail,
  MessageSquare,
  Clock,
  Send,
  CheckCircle,
  Building,
  Loader2
} from "lucide-react";
import { mockData } from "../mock";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Contact = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    country: "",
    service: "",
    message: ""
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      const response = await axios.post(`${API}/contact/submit`, formData);
      
      if (response.data.success) {
        toast({
          title: "Message Sent Successfully!",
          description: response.data.message,
          duration: 5000,
        });
        
        // Reset form
        setFormData({
          name: "",
          email: "",
          phone: "",
          country: "",
          service: "",
          message: ""
        });
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || "Failed to send message. Please try again.";
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
        duration: 5000,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2">📞 Get In Touch</Badge>
          <h1 className="text-4xl md:text-6xl font-bold mb-6">Contact Us</h1>
          <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90">
            Ready to transform your business with our IT solutions? Let's discuss your project and explore how we can help you succeed.
          </p>
        </div>
      </section>

      {/* Contact Form & Info */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <Card className="hover:shadow-lg transition-all duration-300">
              <CardHeader>
                <CardTitle className="text-2xl text-[#0c4864] mb-2">Send us a Message</CardTitle>
                <CardDescription>
                  Fill out the form below and we'll get back to you within 24 hours.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Full Name *
                      </label>
                      <Input
                        required
                        placeholder="Your full name"
                        value={formData.name}
                        onChange={(e) => handleInputChange("name", e.target.value)}
                        className="border-gray-300 focus:border-[#3b8ea4]"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Email Address *
                      </label>
                      <Input
                        type="email"
                        required
                        placeholder="your.email@company.com"
                        value={formData.email}
                        onChange={(e) => handleInputChange("email", e.target.value)}
                        className="border-gray-300 focus:border-[#3b8ea4]"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Phone Number
                      </label>
                      <Input
                        placeholder="+250 xxx xxx xxx"
                        value={formData.phone}
                        onChange={(e) => handleInputChange("phone", e.target.value)}
                        className="border-gray-300 focus:border-[#3b8ea4]"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Country/Location *
                      </label>
                      <Select onValueChange={(value) => handleInputChange("country", value)}>
                        <SelectTrigger className="border-gray-300 focus:border-[#3b8ea4]">
                          <SelectValue placeholder="Select your country" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="rwanda">Rwanda</SelectItem>
                          <SelectItem value="car">Central African Republic</SelectItem>
                          <SelectItem value="other">Other African Country</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Service Interest *
                    </label>
                    <Select onValueChange={(value) => handleInputChange("service", value)}>
                      <SelectTrigger className="border-gray-300 focus:border-[#3b8ea4]">
                        <SelectValue placeholder="What service are you interested in?" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="starlink">Starlink Installation</SelectItem>
                        <SelectItem value="network">Network Setup</SelectItem>
                        <SelectItem value="cctv">CCTV & Security</SelectItem>
                        <SelectItem value="software">Custom Software</SelectItem>
                        <SelectItem value="cloud">Cloud Solutions</SelectItem>
                        <SelectItem value="erp">ERP/CRM Systems</SelectItem>
                        <SelectItem value="support">Technical Support</SelectItem>
                        <SelectItem value="other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Project Details *
                    </label>
                    <Textarea
                      required
                      placeholder="Tell us about your project, requirements, timeline, and any specific needs you have..."
                      rows={5}
                      value={formData.message}
                      onChange={(e) => handleInputChange("message", e.target.value)}
                      className="border-gray-300 focus:border-[#3b8ea4]"
                    />
                  </div>

                  <Button 
                    type="submit" 
                    size="lg" 
                    className="w-full bg-[#3b8ea4] hover:bg-[#0c4864] text-white"
                  >
                    <Send className="mr-2 h-4 w-4" />
                    Send Message
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Contact Information */}
            <div className="space-y-8">
              {/* Quick Contact */}
              <Card className="bg-[#0c4864] text-white">
                <CardHeader>
                  <CardTitle className="text-white mb-4">Get Quick Support</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <Phone className="h-5 w-5 text-[#66cadb]" />
                      <span>Call us now for immediate assistance</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <MessageSquare className="h-5 w-5 text-[#66cadb]" />
                      <span>WhatsApp support available 24/7</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <Clock className="h-5 w-5 text-[#66cadb]" />
                      <span>Response time: Within 2 hours</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Office Locations */}
              <div className="space-y-6">
                <h3 className="text-2xl font-bold text-[#0c4864]">Our Offices</h3>
                {mockData.offices.map((office) => (
                  <Card key={office.id} className="hover:shadow-lg transition-all duration-300">
                    <CardHeader>
                      <CardTitle className="text-[#0c4864] flex items-center">
                        <Building className="h-5 w-5 text-[#3b8ea4] mr-2" />
                        {office.country} Office
                      </CardTitle>
                      <CardDescription>{office.city} Operations Center</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="flex items-start space-x-3">
                        <MapPin className="h-5 w-5 text-[#3b8ea4] mt-0.5" />
                        <span className="text-gray-700">{office.address}</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Phone className="h-5 w-5 text-[#3b8ea4]" />
                        <span className="text-gray-700">{office.phone}</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Mail className="h-5 w-5 text-[#3b8ea4]" />
                        <span className="text-gray-700">{office.email}</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <MessageSquare className="h-5 w-5 text-[#3b8ea4]" />
                        <span className="text-gray-700">{office.whatsapp}</span>
                      </div>
                      <div className="pt-3 flex space-x-2">
                        <Button size="sm" className="bg-[#3b8ea4] hover:bg-[#0c4864] text-white">
                          <Phone className="mr-2 h-4 w-4" />
                          Call Now
                        </Button>
                        <Button size="sm" variant="outline" className="border-[#3b8ea4] text-[#3b8ea4] hover:bg-[#3b8ea4] hover:text-white">
                          <MessageSquare className="mr-2 h-4 w-4" />
                          WhatsApp
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Map Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Find Us on the Map</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Visit our offices across Africa for in-person consultations and support.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Rwanda Map */}
            <Card className="overflow-hidden">
              <CardHeader className="bg-[#0c4864] text-white">
                <CardTitle>Rwanda - Kigali Office</CardTitle>
                <CardDescription className="text-gray-300">
                  Main headquarters and technical center
                </CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                <div className="h-64 bg-gray-200 flex items-center justify-center">
                  <div className="text-center text-gray-500">
                    <MapPin className="h-12 w-12 mx-auto mb-4 text-[#3b8ea4]" />
                    <p className="font-medium">Interactive Map</p>
                    <p className="text-sm">Kigali, Rwanda</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* CAR Map */}
            <Card className="overflow-hidden">
              <CardHeader className="bg-[#3b8ea4] text-white">
                <CardTitle>Central African Republic - Bangui Office</CardTitle>
                <CardDescription className="text-gray-300">
                  Regional operations and support center
                </CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                <div className="h-64 bg-gray-200 flex items-center justify-center">
                  <div className="text-center text-gray-500">
                    <MapPin className="h-12 w-12 mx-auto mb-4 text-[#66cadb]" />
                    <p className="font-medium">Interactive Map</p>
                    <p className="text-sm">Bangui, CAR</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Frequently Asked Questions</h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Quick answers to common questions about our services and support.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {[
              {
                question: "How quickly can you install Starlink?",
                answer: "Most Starlink installations can be completed within 24-48 hours of equipment arrival. Remote locations may require additional planning time."
              },
              {
                question: "Do you provide ongoing technical support?",
                answer: "Yes, we offer 24/7 technical support for all our services including phone, WhatsApp, and on-site assistance when needed."
              },
              {
                question: "What areas do you currently serve?",
                answer: "We currently operate in Rwanda and Central African Republic, with plans to expand to additional African countries in 2025."
              },
              {
                question: "Can you help migrate existing systems?",
                answer: "Absolutely! We provide complete migration services for networks, servers, and software systems with minimal downtime."
              }
            ].map((faq, index) => (
              <Card key={index} className="bg-white/10 border-white/20 backdrop-blur-sm text-white">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-start">
                    <CheckCircle className="h-5 w-5 text-[#66cadb] mr-2 mt-1 flex-shrink-0" />
                    {faq.question}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-200 ml-7">
                    {faq.answer}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Emergency Contact */}
      <section className="py-20 bg-gradient-to-r from-[#3b8ea4] to-[#66cadb] text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Need Immediate Assistance?
          </h2>
          <p className="text-xl mb-10 opacity-90">
            For urgent technical issues or emergency support, contact us directly.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-[#0c4864] hover:bg-gray-100 px-8 py-3 text-lg font-semibold">
              <Phone className="mr-2 h-5 w-5" />
              Call Emergency Line
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-[#0c4864] px-8 py-3 text-lg font-semibold">
              <MessageSquare className="mr-2 h-5 w-5" />
              WhatsApp Support
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Contact;