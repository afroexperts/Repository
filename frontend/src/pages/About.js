import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { MapPin, Mail, Phone, MessageSquare } from "lucide-react";
import { mockData } from "../mock";

const About = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">About Afro Experts</h1>
          <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90">
            Pioneering Africa's digital transformation through innovative technology solutions and reliable connectivity.
          </p>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Mission */}
            <Card className="hover:shadow-lg transition-all duration-300 border-l-4 border-[#3b8ea4]">
              <CardHeader>
                <Badge className="w-fit bg-[#66cadb] text-white mb-4">Our Mission</Badge>
                <CardTitle className="text-2xl text-[#0c4864]">Bridging the Digital Divide</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  {mockData.company.mission}
                </CardDescription>
              </CardContent>
            </Card>

            {/* Vision */}
            <Card className="hover:shadow-lg transition-all duration-300 border-l-4 border-[#66cadb]">
              <CardHeader>
                <Badge className="w-fit bg-[#3b8ea4] text-white mb-4">Our Vision</Badge>
                <CardTitle className="text-2xl text-[#0c4864]">Africa's Technology Partner</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  {mockData.company.vision}
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CEO Message */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <Badge className="mb-4 bg-[#66cadb] text-white">Leadership Message</Badge>
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Message from our CEO</h2>
          </div>

          <Card className="bg-white/10 border-white/20 backdrop-blur-sm">
            <CardContent className="p-8 md:p-12">
              <div className="flex flex-col lg:flex-row items-center lg:items-start gap-8">
                <div className="flex-shrink-0">
                  <div className="w-32 h-32 bg-[#66cadb] bg-opacity-20 rounded-full flex items-center justify-center">
                    <div className="w-24 h-24 bg-[#3b8ea4] rounded-full flex items-center justify-center text-2xl font-bold text-white">
                      {mockData.team.ceo.name.split(' ').map(n => n[0]).join('')}
                    </div>
                  </div>
                </div>
                <div className="flex-grow text-center lg:text-left">
                  <h3 className="text-2xl font-bold text-white mb-2">{mockData.team.ceo.name}</h3>
                  <p className="text-[#66cadb] mb-6 text-lg">{mockData.team.ceo.title}</p>
                  <blockquote className="text-gray-200 text-lg leading-relaxed italic">
                    "{mockData.team.ceo.message}"
                  </blockquote>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Company Story */}
      <section className="py-20 bg-gradient-to-br from-white to-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Our Story</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              From humble beginnings to transforming Africa's digital landscape
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Timeline Items */}
            <Card className="text-center hover:shadow-lg transition-all duration-300">
              <CardHeader>
                <div className="bg-[#66cadb] bg-opacity-10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-[#0c4864]">2020</span>
                </div>
                <CardTitle className="text-[#0c4864]">Foundation</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Founded with a vision to bring reliable IT services to African businesses and communities.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-all duration-300">
              <CardHeader>
                <div className="bg-[#3b8ea4] bg-opacity-10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-[#0c4864]">2022</span>
                </div>
                <CardTitle className="text-[#0c4864]">Expansion</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Expanded operations to Central African Republic, becoming the first Starlink partner in the region.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-all duration-300">
              <CardHeader>
                <div className="bg-[#0c4864] bg-opacity-10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-[#0c4864]">2025</span>
                </div>
                <CardTitle className="text-[#0c4864]">Innovation</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Leading Africa's digital transformation with cutting-edge solutions and expanding to new markets.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Offices */}
      <section className="py-20 bg-[#0c4864] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Our Offices</h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Strategically located across Africa to serve our clients with local expertise and global standards.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {mockData.offices.map((office) => (
              <Card key={office.id} className="bg-white/10 border-white/20 backdrop-blur-sm text-white">
                <CardHeader>
                  <CardTitle className="text-2xl text-white flex items-center">
                    <MapPin className="h-6 w-6 text-[#66cadb] mr-2" />
                    {office.country}
                  </CardTitle>
                  <CardDescription className="text-gray-300">
                    {office.city} Operations Center
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center space-x-3 text-gray-200">
                    <MapPin className="h-5 w-5 text-[#66cadb]" />
                    <span>{office.address}</span>
                  </div>
                  <div className="flex items-center space-x-3 text-gray-200">
                    <Phone className="h-5 w-5 text-[#66cadb]" />
                    <span>{office.phone}</span>
                  </div>
                  <div className="flex items-center space-x-3 text-gray-200">
                    <Mail className="h-5 w-5 text-[#66cadb]" />
                    <span>{office.email}</span>
                  </div>
                  <div className="flex items-center space-x-3 text-gray-200">
                    <MessageSquare className="h-5 w-5 text-[#66cadb]" />
                    <span>WhatsApp: {office.whatsapp}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-[#0c4864] mb-6">Our Values</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              The principles that guide everything we do
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: "Innovation",
                description: "Embracing cutting-edge technology to solve Africa's unique challenges",
                color: "bg-[#66cadb]"
              },
              {
                title: "Reliability",
                description: "Delivering consistent, dependable solutions that our clients can trust",
                color: "bg-[#3b8ea4]"
              },
              {
                title: "Community",
                description: "Building stronger communities through digital empowerment and connectivity",
                color: "bg-[#0c4864]"
              },
              {
                title: "Excellence",
                description: "Striving for the highest standards in everything we deliver",
                color: "bg-gradient-to-br from-[#3b8ea4] to-[#66cadb]"
              }
            ].map((value, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-all duration-300 card-hover">
                <CardHeader>
                  <div className={`${value.color} bg-opacity-10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4`}>
                    <div className={`${value.color} w-8 h-8 rounded-full`}></div>
                  </div>
                  <CardTitle className="text-[#0c4864]">{value.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>
                    {value.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;