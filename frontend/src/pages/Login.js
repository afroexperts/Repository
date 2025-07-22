import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Alert, AlertDescription } from "../components/ui/alert";
import { Badge } from "../components/ui/badge";
import { useToast } from "../hooks/use-toast";
import axios from "axios";
import { Eye, EyeOff, Lock, Mail, Loader2, Shield, Users, BarChart3 } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: ""
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const { toast } = useToast();

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (error) setError(""); // Clear error when user starts typing
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const response = await axios.post(`${API}/auth/login`, formData);
      
      if (response.data.success) {
        // Store user data and token
        localStorage.setItem("auth_token", response.data.token);
        localStorage.setItem("user_data", JSON.stringify(response.data.user));
        
        toast({
          title: "Login Successful!",
          description: `Welcome back, ${response.data.user.full_name}!`,
          duration: 3000,
        });

        // Redirect to dashboard
        navigate('/dashboard');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || "Login failed. Please try again.";
      setError(errorMessage);
      toast({
        title: "Login Failed",
        description: errorMessage,
        variant: "destructive",
        duration: 5000,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const demoAccounts = [
    {
      role: "Administrator",
      email: "admin@afroexperts.com",
      password: "AfroExperts2025!",
      permissions: "Full system access",
      icon: Shield,
      color: "bg-red-500"
    },
    {
      role: "Manager",
      email: "manager@afroexperts.com", 
      password: "Manager2025!",
      permissions: "Sales, inventory, reports",
      icon: Users,
      color: "bg-blue-500"
    },
    {
      role: "Cashier",
      email: "cashier@afroexperts.com",
      password: "Cashier2025!",
      permissions: "POS terminal, orders",
      icon: BarChart3,
      color: "bg-green-500"
    }
  ];

  const fillDemoCredentials = (account) => {
    setFormData({
      email: account.email,
      password: account.password
    });
    setError("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0c4864] to-[#3b8ea4] flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        {/* Left Side - Company Info */}
        <div className="text-white space-y-8">
          <div>
            <div className="flex items-center space-x-3 mb-6">
              <div className="bg-white text-[#0c4864] px-4 py-3 rounded-xl font-bold text-2xl">
                AE
              </div>
              <div>
                <h1 className="text-3xl font-bold">Afro Experts</h1>
                <p className="text-xl opacity-90">ERP & POS System</p>
              </div>
            </div>
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Welcome Back
            </h2>
            <p className="text-xl opacity-90">
              Access your comprehensive business management system
            </p>
          </div>

          {/* Features */}
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold mb-6">System Features</h3>
            {[
              "Multi-vertical business management",
              "Real-time inventory tracking",
              "Advanced point-of-sale system",
              "Client & order management",
              "Financial reporting & analytics",
              "Role-based access control"
            ].map((feature, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-[#66cadb] rounded-full"></div>
                <span className="opacity-90">{feature}</span>
              </div>
            ))}
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 pt-8">
            <div className="text-center">
              <div className="text-2xl font-bold">1,247</div>
              <div className="text-sm opacity-75">Products</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">234</div>
              <div className="text-sm opacity-75">Clients</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">4</div>
              <div className="text-sm opacity-75">Locations</div>
            </div>
          </div>
        </div>

        {/* Right Side - Login Form */}
        <div className="space-y-6">
          {/* Login Card */}
          <Card className="w-full max-w-md mx-auto">
            <CardHeader>
              <CardTitle className="text-2xl text-center text-[#0c4864]">Sign In</CardTitle>
              <CardDescription className="text-center">
                Enter your credentials to access the dashboard
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {error && (
                  <Alert variant="destructive">
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email Address
                    </label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                      <Input
                        type="email"
                        required
                        placeholder="your.email@afroexperts.com"
                        value={formData.email}
                        onChange={(e) => handleInputChange("email", e.target.value)}
                        className="pl-10 border-gray-300 focus:border-[#3b8ea4]"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Password
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                      <Input
                        type={showPassword ? "text" : "password"}
                        required
                        placeholder="Enter your password"
                        value={formData.password}
                        onChange={(e) => handleInputChange("password", e.target.value)}
                        className="pl-10 pr-10 border-gray-300 focus:border-[#3b8ea4]"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                      >
                        {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>
                </div>

                <Button 
                  type="submit" 
                  className="w-full bg-[#0c4864] hover:bg-[#3b8ea4] text-white"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Signing in...
                    </>
                  ) : (
                    "Sign In"
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Demo Accounts */}
          <Card className="w-full max-w-md mx-auto">
            <CardHeader>
              <CardTitle className="text-lg text-center text-[#0c4864]">Demo Accounts</CardTitle>
              <CardDescription className="text-center">
                Click on any account to auto-fill credentials
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {demoAccounts.map((account, index) => {
                const IconComponent = account.icon;
                return (
                  <button
                    key={index}
                    onClick={() => fillDemoCredentials(account)}
                    className="w-full p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left"
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`${account.color} p-2 rounded-lg text-white`}>
                        <IconComponent className="h-5 w-5" />
                      </div>
                      <div className="flex-grow">
                        <div className="flex items-center justify-between">
                          <span className="font-medium text-gray-900">{account.role}</span>
                          <Badge variant="outline" className="text-xs">
                            Demo
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600">{account.permissions}</p>
                        <p className="text-xs text-gray-500 mt-1">{account.email}</p>
                      </div>
                    </div>
                  </button>
                );
              })}
            </CardContent>
          </Card>

          {/* Security Note */}
          <div className="text-center text-white text-sm opacity-75">
            <p>🔒 Secure authentication with role-based access control</p>
            <p>Protected by industry-standard security protocols</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;