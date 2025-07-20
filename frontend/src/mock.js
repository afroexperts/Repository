// Mock data for Afro Experts Website
export const mockData = {
  company: {
    name: "Afro Experts",
    tagline: "Empowering Africa's Digital Future",
    description: "Leading IT services and digital solutions provider across Africa, specializing in network infrastructure, smart office solutions, and bringing high-speed internet connectivity to rural communities.",
    mission: "To bridge the digital divide across Africa by providing cutting-edge IT solutions and reliable internet connectivity that empowers businesses and communities to thrive in the digital age.",
    vision: "To be Africa's most trusted technology partner, connecting every corner of the continent to global opportunities through innovative IT services and infrastructure."
  },
  
  hero: {
    title: "Empowering Africa's Digital Future",
    subtitle: "Comprehensive IT Services & Starlink Internet Solutions for Modern Africa",
    description: "From network infrastructure to satellite internet, we connect African businesses and communities to the global digital economy.",
    backgroundImage: "https://images.unsplash.com/photo-1660742533971-eb413acbfb47?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwyfHxBZnJpY2FuJTIwdGVjaG5vbG9neXxlbnwwfHx8fDE3NTMwMDA1Nzh8MA&ixlib=rb-4.1.0&q=85"
  },

  starlink: {
    title: "High-Speed Internet for Rural Africa",
    subtitle: "Bridging the Digital Divide with Satellite Technology",
    description: "Experience lightning-fast internet speeds of up to 150 Mbps even in the most remote locations across Africa. Our Starlink solutions provide reliable, low-latency connectivity that traditional ISPs simply cannot match.",
    features: [
      {
        title: "Global Coverage",
        description: "Reliable internet access in remote and rural areas where traditional providers fail",
        icon: "Globe"
      },
      {
        title: "High Speed",
        description: "Download speeds up to 150 Mbps with ultra-low latency for seamless connectivity",
        icon: "Zap"
      },
      {
        title: "Easy Installation",
        description: "Quick setup with minimal infrastructure requirements - get online in hours, not months",
        icon: "Settings"
      },
      {
        title: "Business Ready",
        description: "Scalable solutions for enterprises, schools, healthcare facilities, and government offices",
        icon: "Building"
      }
    ],
    comparison: {
      traditional: {
        title: "Traditional ISPs",
        features: ["Limited rural coverage", "Infrastructure dependent", "Slower deployment", "Weather affected"]
      },
      starlink: {
        title: "Starlink by Afro Experts",
        features: ["99% coverage across Africa", "Satellite-based reliability", "Rapid deployment", "Weather resistant"]
      }
    }
  },

  services: [
    {
      id: 1,
      title: "Network Setup & Maintenance",
      description: "Professional network infrastructure design, implementation, and ongoing maintenance for businesses of all sizes.",
      image: "https://images.unsplash.com/photo-1683322499436-f4383dd59f5a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwzfHxzZXJ2ZXIlMjByb29tfGVufDB8fHx8MTc1MzAwMDYyM3ww&ixlib=rb-4.1.0&q=85",
      features: ["LAN/WAN Configuration", "WiFi Network Design", "Network Security", "24/7 Monitoring"],
      icon: "Network"
    },
    {
      id: 2,
      title: "CCTV & Access Control",
      description: "Comprehensive security solutions with advanced CCTV systems and intelligent access control for enhanced safety.",
      image: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxJVCUyMHNlcnZpY2VzfGVufDB8fHx8MTc1MzAwMDYxNnww&ixlib=rb-4.1.0&q=85",
      features: ["HD Camera Installation", "Remote Monitoring", "Access Card Systems", "Mobile App Control"],
      icon: "Camera"
    },
    {
      id: 3,
      title: "Server Installation",
      description: "Enterprise-grade server deployment and configuration for optimal performance and reliability.",
      image: "https://images.unsplash.com/photo-1580106815433-a5b1d1d53d85?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwxfHxzZXJ2ZXIlMjByb29tfGVufDB8fHx8MTc1MzAwMDYyM3ww&ixlib=rb-4.1.0&q=85",
      features: ["Data Center Setup", "Cloud Migration", "Backup Solutions", "Performance Optimization"],
      icon: "Server"
    },
    {
      id: 4,
      title: "Technical Support",
      description: "Round-the-clock technical assistance and IT support to keep your business operations running smoothly.",
      image: "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxJVCUyMHNlcnZpY2VzfGVufDB8fHx8MTc1MzAwMDYxNnww&ixlib=rb-4.1.0&q=85",
      features: ["24/7 Help Desk", "Remote Assistance", "On-site Repairs", "Preventive Maintenance"],
      icon: "Headphones"
    }
  ],

  solutions: [
    {
      id: 1,
      title: "Custom Software Development",
      description: "Tailored software solutions designed to meet your specific business requirements and workflow needs.",
      features: ["Web Applications", "Mobile Apps", "Desktop Software", "API Development"]
    },
    {
      id: 2,
      title: "Cloud Hosting Solutions",
      description: "Reliable and scalable cloud infrastructure to power your applications and data storage needs.",
      features: ["AWS Implementation", "Microsoft Azure", "Google Cloud", "Hybrid Solutions"]
    },
    {
      id: 3,
      title: "ERP/CRM Solutions",
      description: "Comprehensive business management systems to streamline operations and enhance customer relationships.",
      features: ["Process Automation", "Data Analytics", "Customer Management", "Inventory Control"]
    },
    {
      id: 4,
      title: "IoT & Smart Office Integration",
      description: "Transform your workplace with intelligent automation and connected device ecosystems.",
      features: ["Smart Lighting", "Climate Control", "Security Integration", "Energy Management"]
    }
  ],

  products: [
    {
      id: 1,
      title: "Starlink Residential Kit",
      description: "Complete home internet solution with everything needed for high-speed connectivity.",
      price: "$599",
      features: ["Starlink Dish", "WiFi Router", "Cables & Mounting", "Mobile App Control"],
      category: "starlink"
    },
    {
      id: 2,
      title: "Starlink Business Kit",
      description: "Enterprise-grade internet solution with priority support and enhanced performance.",
      price: "$2,500",
      features: ["High-Performance Dish", "Enterprise Router", "Priority Support", "Static IP Options"],
      category: "starlink"
    },
    {
      id: 3,
      title: "Afro Experts POS System",
      description: "Integrated point-of-sale solution designed for African retail businesses.",
      price: "$299",
      features: ["Touch Screen Terminal", "Receipt Printer", "Cash Drawer", "Inventory Management"],
      category: "pos"
    },
    {
      id: 4,
      title: "Afro Experts ERP Suite",
      description: "Complete business management solution for growing African enterprises.",
      price: "$999",
      features: ["Financial Management", "HR Module", "Supply Chain", "Reporting Dashboard"],
      category: "erp"
    }
  ],

  partners: [
    {
      id: 1,
      name: "Starlink",
      description: "Official partner providing satellite internet solutions across Africa",
      logo: "/images/starlink-logo.png",
      category: "connectivity"
    },
    {
      id: 2,
      name: "Microsoft",
      description: "Certified partner for cloud solutions and enterprise software",
      logo: "/images/microsoft-logo.png",
      category: "software"
    },
    {
      id: 3,
      name: "Cisco",
      description: "Network infrastructure and security solutions partner",
      logo: "/images/cisco-logo.png",
      category: "networking"
    },
    {
      id: 4,
      name: "AWS",
      description: "Cloud computing and hosting solutions partnership",
      logo: "/images/aws-logo.png",
      category: "cloud"
    }
  ],

  team: {
    ceo: {
      name: "Dr. Kwame Asante",
      title: "CEO & Founder",
      message: "At Afro Experts, we believe technology should empower every African community, regardless of location. Our mission is to break down digital barriers and create opportunities for growth, education, and innovation across our beautiful continent. Through partnerships with global leaders like Starlink and our deep understanding of local needs, we're building the infrastructure that will power Africa's digital renaissance.",
      image: "/images/ceo.jpg"
    }
  },

  offices: [
    {
      id: 1,
      country: "Rwanda",
      city: "Kigali",
      address: "KG 15 Ave, Nyarugenge District, Kigali",
      phone: "+250 788 123 456",
      email: "rwanda@afroexperts.com",
      whatsapp: "+250 788 123 456",
      coordinates: { lat: -1.9441, lng: 30.0619 }
    },
    {
      id: 2,
      country: "Central African Republic",
      city: "Bangui",
      address: "Avenue de l'Indépendance, Bangui",
      phone: "+236 70 12 34 56",
      email: "car@afroexperts.com",
      whatsapp: "+236 70 12 34 56",
      coordinates: { lat: 4.3947, lng: 18.5582 }
    }
  ],

  impact: {
    title: "Our Impact Across Africa",
    stats: [
      { number: "50+", label: "Communities Connected" },
      { number: "1,000+", label: "Businesses Served" },
      { number: "10,000+", label: "People Online" },
      { number: "2", label: "Countries Active" }
    ],
    deployments: [
      {
        location: "Rural Rwanda",
        description: "Connected 15 schools and health centers with high-speed internet",
        impact: "Improved education and healthcare access for 5,000+ residents"
      },
      {
        location: "Central African Republic",
        description: "Established internet infrastructure in 8 remote communities",
        impact: "Enabled digital commerce and communication for local businesses"
      }
    ]
  },

  testimonials: [
    {
      id: 1,
      name: "Marie Uwimana",
      title: "School Principal",
      location: "Kigali, Rwanda",
      message: "Afro Experts transformed our school with reliable internet. Now our students can access online resources and prepare for the digital future.",
      rating: 5
    },
    {
      id: 2,
      name: "Jean Baptiste",
      title: "Business Owner",
      location: "Bangui, CAR",
      message: "The Starlink installation was seamless. Our business now operates efficiently with cloud-based systems and international communication.",
      rating: 5
    }
  ],

  navigation: [
    { name: "Home", path: "/" },
    { name: "About Us", path: "/about" },
    { name: "IT Services", path: "/services" },
    { name: "IT Solutions", path: "/solutions" },
    { name: "Products & Partners", path: "/products" },
    { name: "Contact Us", path: "/contact" }
  ]
};