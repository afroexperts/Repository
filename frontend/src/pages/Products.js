import { useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { 
  Wifi,
  Building,
  ShoppingCart,
  BarChart3,
  CheckCircle,
  Download,
  ExternalLink,
  Star,
  Zap,
  Shield,
  Headphones
} from "lucide-react";
import { mockData } from "../mock";

const Products = () => {
  const [selectedCategory, setSelectedCategory] = useState("all");

  const filteredProducts = selectedCategory === "all" 
    ? mockData.products 
    : mockData.products.filter(product => product.category === selectedCategory);

  const categoryIcons = {
    starlink: Wifi,
    pos: ShoppingCart,
    erp: BarChart3
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2">🛍️ Products & Partners</Badge>
          <h1 className="text-4xl md:text-6xl font-bold mb-6">Products & Partners</h1>
          <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90">
            Discover our premium technology products and strategic partnerships that power Africa's digital transformation.
          </p>
        </div>
      </section>

      {/* Products Section */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Our Products</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
              Premium technology products designed for African businesses and communities.
            </p>
          </div>

          <Tabs defaultValue="all" className="w-full">
            <TabsList className="grid w-full grid-cols-2 lg:grid-cols-4 mb-12">
              <TabsTrigger value="all" onClick={() => setSelectedCategory("all")}>All Products</TabsTrigger>
              <TabsTrigger value="starlink" onClick={() => setSelectedCategory("starlink")}>Starlink</TabsTrigger>
              <TabsTrigger value="pos" onClick={() => setSelectedCategory("pos")}>POS Systems</TabsTrigger>
              <TabsTrigger value="erp" onClick={() => setSelectedCategory("erp")}>ERP Solutions</TabsTrigger>
            </TabsList>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {filteredProducts.map((product) => {
                const IconComponent = categoryIcons[product.category] || Building;
                return (
                  <Card key={product.id} className="hover:shadow-xl transition-all duration-300 overflow-hidden card-hover">
                    <div className="bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] text-white p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <Badge className="mb-2 bg-[#66cadb] text-white capitalize">
                            {product.category === 'starlink' ? 'Starlink' : product.category.toUpperCase()}
                          </Badge>
                          <CardTitle className="text-2xl text-white mb-2">{product.title}</CardTitle>
                          <CardDescription className="text-gray-200">
                            {product.description}
                          </CardDescription>
                        </div>
                        <div className="bg-white/20 backdrop-blur-sm rounded-full p-3">
                          <IconComponent className="h-8 w-8 text-white" />
                        </div>
                      </div>
                      <div className="mt-4">
                        <div className="text-3xl font-bold text-white">{product.price}</div>
                      </div>
                    </div>
                    
                    <CardContent className="p-6">
                      <h4 className="font-semibold text-[#0c4864] mb-4">What's Included:</h4>
                      <div className="space-y-3 mb-6">
                        {product.features.map((feature, index) => (
                          <div key={index} className="flex items-center space-x-3">
                            <CheckCircle className="h-5 w-5 text-[#3b8ea4] flex-shrink-0" />
                            <span className="text-gray-700">{feature}</span>
                          </div>
                        ))}
                      </div>
                      
                      <div className="flex space-x-3">
                        <Button 
                          className="flex-1 bg-[#3b8ea4] hover:bg-[#0c4864] text-white"
                          onClick={() => {
                            if (product.category === 'erp') {
                              window.location.href = '/erp-pos-system';
                            } else {
                              // Handle other product orders
                              console.log('Order product:', product.title);
                            }
                          }}
                        >
                          <ShoppingCart className="mr-2 h-4 w-4" />
                          {product.category === 'erp' ? 'View Details' : 'Order Now'}
                        </Button>
                        <Button variant="outline" className="border-[#3b8ea4] text-[#3b8ea4] hover:bg-[#3b8ea4] hover:text-white">
                          <Download className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </Tabs>
        </div>
      </section>

      {/* Starlink Highlight Section */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <Badge className="mb-4 bg-[#66cadb] text-white px-4 py-2">🚀 Featured Partner</Badge>
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Starlink by SpaceX</h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Official Starlink partner bringing high-speed satellite internet to every corner of Africa.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <Card className="bg-white/10 border-white/20 text-white backdrop-blur-sm text-center">
              <CardHeader>
                <div className="bg-[#66cadb] bg-opacity-20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Zap className="h-8 w-8 text-[#66cadb]" />
                </div>
                <CardTitle className="text-white">High Speed</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-200">
                  Download speeds up to 150 Mbps with ultra-low latency for seamless connectivity across Africa.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="bg-white/10 border-white/20 text-white backdrop-blur-sm text-center">
              <CardHeader>
                <div className="bg-[#66cadb] bg-opacity-20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Shield className="h-8 w-8 text-[#66cadb]" />
                </div>
                <CardTitle className="text-white">Reliability</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-200">
                  99.9% uptime with weather-resistant equipment designed for challenging African conditions.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="bg-white/10 border-white/20 text-white backdrop-blur-sm text-center">
              <CardHeader>
                <div className="bg-[#66cadb] bg-opacity-20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Headphones className="h-8 w-8 text-[#66cadb]" />
                </div>
                <CardTitle className="text-white">Local Support</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-200">
                  Professional installation and 24/7 technical support from our certified African team.
                </CardDescription>
              </CardContent>
            </Card>
          </div>

          <div className="text-center mt-12">
            <Button size="lg" className="bg-[#66cadb] hover:bg-[#3b8ea4] text-white px-8 py-3 mr-4">
              View Starlink Plans
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-[#0c4864] px-8 py-3">
              <Download className="mr-2 h-4 w-4" />
              Download Brochure
            </Button>
          </div>
        </div>
      </section>

      {/* Partners Section */}
      <section className="py-20 bg-gradient-to-br from-white to-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Our Technology Partners</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Strategic partnerships with global technology leaders to deliver world-class solutions.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {mockData.partners.map((partner) => (
              <Card key={partner.id} className="hover:shadow-lg transition-all duration-300 text-center">
                <CardHeader>
                  <div className="bg-[#66cadb] bg-opacity-10 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <div className="text-2xl font-bold text-[#0c4864]">
                      {partner.name.charAt(0)}
                    </div>
                  </div>
                  <CardTitle className="text-[#0c4864]">{partner.name}</CardTitle>
                  <Badge variant="secondary" className="w-fit mx-auto capitalize">
                    {partner.category}
                  </Badge>
                </CardHeader>
                <CardContent>
                  <CardDescription className="mb-4">
                    {partner.description}
                  </CardDescription>
                  <Button variant="outline" size="sm" className="border-[#3b8ea4] text-[#3b8ea4] hover:bg-[#3b8ea4] hover:text-white">
                    <ExternalLink className="mr-2 h-4 w-4" />
                    Learn More
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Downloads Section */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Product Resources</h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Download detailed product specifications, installation guides, and comparison charts.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: "Starlink Product Guide",
                description: "Complete specifications and pricing for residential and business plans",
                fileType: "PDF • 2.4 MB"
              },
              {
                title: "Installation Manual",
                description: "Step-by-step installation guide for all Starlink equipment",
                fileType: "PDF • 1.8 MB"
              },
              {
                title: "POS System Catalog",
                description: "Features and pricing for our complete POS solution suite",
                fileType: "PDF • 3.1 MB"
              }
            ].map((resource, index) => (
              <Card key={index} className="bg-white/10 border-white/20 text-white backdrop-blur-sm">
                <CardHeader>
                  <div className="bg-[#66cadb] bg-opacity-20 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                    <Download className="h-6 w-6 text-[#66cadb]" />
                  </div>
                  <CardTitle className="text-white">{resource.title}</CardTitle>
                  <CardDescription className="text-gray-300">
                    {resource.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">{resource.fileType}</span>
                    <Button variant="outline" size="sm" className="border-[#66cadb] text-[#66cadb] hover:bg-[#66cadb] hover:text-white">
                      Download
                    </Button>
                  </div>
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
            Ready to Upgrade Your Technology?
          </h2>
          <p className="text-xl mb-10 opacity-90">
            Explore our complete product catalog or speak with our experts to find the perfect solution for your needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-[#0c4864] hover:bg-gray-100 px-8 py-3 text-lg font-semibold">
              Shop Products
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-[#0c4864] px-8 py-3 text-lg font-semibold">
              Consult Expert
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Products;