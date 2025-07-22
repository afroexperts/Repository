import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../hooks/use-toast";
import axios from "axios";
import { 
  BarChart3,
  Package,
  Warehouse,
  ShoppingCart,
  FileText,
  Users,
  Calendar,
  Recycle,
  Mountain,
  Satellite,
  CreditCard,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Eye,
  Plus,
  Search,
  Filter,
  Download,
  Settings,
  Bell,
  User,
  LogOut,
  Home,
  Menu,
  Loader2,
  AlertTriangle,
  CheckCircle
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const { user, logout, hasPermission } = useAuth();
  const { toast } = useToast();
  const [activeModule, setActiveModule] = useState("dashboard");
  const [notifications, setNotifications] = useState(0);
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState({
    stats: {},
    recentTransactions: [],
    lowStockProducts: [],
    products: [],
    orders: [],
    clients: []
  });

  // Fetch dashboard data on component mount
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // Fetch dashboard stats
        const statsResponse = await axios.get(`${API}/dashboard/stats`);
        const recentTransactionsResponse = await axios.get(`${API}/dashboard/recent-transactions?limit=5`);
        const lowStockResponse = await axios.get(`${API}/products/low-stock`);
        
        // Set notifications count based on low stock items
        setNotifications(lowStockResponse.data.length);
        
        setDashboardData(prev => ({
          ...prev,
          stats: statsResponse.data,
          recentTransactions: recentTransactionsResponse.data.transactions,
          lowStockProducts: lowStockResponse.data
        }));
        
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        toast({
          title: "Error",
          description: "Failed to load dashboard data. Please refresh the page.",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [toast]);

  // Fetch module-specific data when switching modules
  useEffect(() => {
    const fetchModuleData = async () => {
      try {
        switch (activeModule) {
          case "products":
          case "inventory":
            if (dashboardData.products.length === 0) {
              const productsResponse = await axios.get(`${API}/products`);
              setDashboardData(prev => ({ ...prev, products: productsResponse.data }));
            }
            break;
          case "orders":
            if (dashboardData.orders.length === 0) {
              const ordersResponse = await axios.get(`${API}/orders`);
              setDashboardData(prev => ({ ...prev, orders: ordersResponse.data }));
            }
            break;
          case "clients":
            if (dashboardData.clients.length === 0) {
              const clientsResponse = await axios.get(`${API}/clients`);
              setDashboardData(prev => ({ ...prev, clients: clientsResponse.data }));
            }
            break;
        }
      } catch (error) {
        console.error(`Error fetching ${activeModule} data:`, error);
      }
    };

    if (!loading) {
      fetchModuleData();
    }
  }, [activeModule, loading, dashboardData.products.length, dashboardData.orders.length, dashboardData.clients.length]);

  const modules = [
    {
      id: "dashboard",
      title: "Dashboard",
      icon: BarChart3,
      description: "Overview and Analytics",
      permission: "view_dashboard"
    },
    {
      id: "products",
      title: "Product Management",
      icon: Package,
      description: "Manage Products & Services",
      permission: "manage_products"
    },
    {
      id: "inventory",
      title: "Inventory",
      icon: Warehouse,
      description: "Stock Management", 
      permission: "manage_products"
    },
    {
      id: "pos",
      title: "Point of Sale",
      icon: ShoppingCart,
      description: "Sales Terminal",
      permission: "create_orders"
    },
    {
      id: "orders",
      title: "Order Management",
      icon: FileText,
      description: "Track Orders & Deliveries",
      permission: "manage_orders"
    },
    {
      id: "clients",
      title: "Client Management",
      icon: Users,
      description: "Customer Relations",
      permission: "manage_clients"
    },
    {
      id: "services",
      title: "Service Booking",
      icon: Calendar,
      description: "IT & Logistics Services",
      permission: "view_services"
    },
    {
      id: "secondhand",
      title: "Second-Hand Sales",
      icon: Recycle,
      description: "Used Products Management",
      permission: "manage_products"
    },
    {
      id: "marble",
      title: "Marble Dust",
      icon: Mountain,
      description: "Production & Sales",
      permission: "manage_products"
    },
    {
      id: "starlink",
      title: "Starlink Resale",
      icon: Satellite,
      description: "Satellite Internet Products",
      permission: "manage_products"
    },
    {
      id: "finance",
      title: "Finance",
      icon: CreditCard,
      description: "Financial Management",
      permission: "view_reports"
    },
    {
      id: "reports",
      title: "Reports",
      icon: TrendingUp,
      description: "Business Analytics",
      permission: "view_reports"
    },
    {
      id: "settings",
      title: "Settings",
      icon: Settings,
      description: "System Configuration",
      permission: "admin"
    }
  ].filter(module => hasPermission(module.permission));

  const renderDashboardContent = () => {
    if (loading) {
      return (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin text-[#0c4864] mx-auto mb-4" />
            <p className="text-gray-600">Loading dashboard data...</p>
          </div>
        </div>
      );
    }

    switch (activeModule) {
      case "dashboard":
        return (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="hover:shadow-lg transition-all duration-300">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Sales (RWF)</CardTitle>
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardData.stats.total_sales?.toLocaleString() || 0}</div>
                  <p className="text-xs text-muted-foreground">
                    <span className="text-green-600">+{dashboardData.stats.monthly_growth || 0}%</span> from last month
                  </p>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-all duration-300">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Orders</CardTitle>
                  <FileText className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardData.stats.active_orders || 0}</div>
                  <p className="text-xs text-muted-foreground">Processing & Delivery</p>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-all duration-300">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Clients</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardData.stats.total_clients || 0}</div>
                  <p className="text-xs text-muted-foreground">Active customers</p>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-all duration-300 border-l-4 border-red-500">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Low Stock Alerts</CardTitle>
                  <AlertTriangle className="h-4 w-4 text-red-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-red-600">{dashboardData.stats.low_stock_items || 0}</div>
                  <p className="text-xs text-muted-foreground">Items need restocking</p>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activity and Alerts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Recent Transactions */}
              <Card>
                <CardHeader>
                  <CardTitle>Recent Transactions</CardTitle>
                  <CardDescription>Latest business activity across all verticals</CardDescription>
                </CardHeader>
                <CardContent>
                  {dashboardData.recentTransactions.length > 0 ? (
                    <div className="space-y-4">
                      {dashboardData.recentTransactions.map((transaction) => (
                        <div key={transaction.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="space-y-1">
                            <p className="text-sm font-medium">{transaction.client}</p>
                            <p className="text-xs text-gray-600">{transaction.product}</p>
                            <p className="text-xs text-gray-500">
                              {new Date(transaction.created_at).toLocaleDateString()}
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm font-semibold">RWF {transaction.amount?.toLocaleString()}</p>
                            <Badge 
                              variant={transaction.status === 'Completed' ? 'default' : 'secondary'}
                              className="text-xs"
                            >
                              {transaction.status}
                            </Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                      <p>No recent transactions</p>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Low Stock Alerts */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-red-600 flex items-center">
                    <AlertTriangle className="h-5 w-5 mr-2" />
                    Low Stock Alerts
                  </CardTitle>
                  <CardDescription>Items requiring immediate attention</CardDescription>
                </CardHeader>
                <CardContent>
                  {dashboardData.lowStockProducts.length > 0 ? (
                    <div className="space-y-4">
                      {dashboardData.lowStockProducts.slice(0, 5).map((item) => (
                        <div key={item.id} className="flex items-center justify-between p-3 border border-red-200 rounded-lg bg-red-50">
                          <div className="space-y-1">
                            <p className="text-sm font-medium">{item.name}</p>
                            <p className="text-xs text-red-600">
                              Current: {item.current_stock} {item.unit} 
                              (Min: {item.minimum_stock})
                            </p>
                          </div>
                          <Badge variant="destructive" className="text-xs">
                            Restock
                          </Badge>
                        </div>
                      ))}
                      {dashboardData.lowStockProducts.length > 5 && (
                        <Button 
                          className="w-full mt-4 bg-red-600 hover:bg-red-700"
                          onClick={() => setActiveModule('inventory')}
                        >
                          View All {dashboardData.lowStockProducts.length} Alerts
                        </Button>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-500" />
                      <p>All products are well stocked!</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div>
        );

      case "products":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Product Management</h2>
                <p className="text-gray-600">Manage your inventory across all business verticals</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Filter className="h-4 w-4 mr-2" />
                  Filter
                </Button>
                {hasPermission('manage_products') && (
                  <Button className="bg-[#0c4864]">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Product
                  </Button>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Products</p>
                      <p className="text-2xl font-bold">{dashboardData.products.length}</p>
                    </div>
                    <Package className="h-8 w-8 text-[#3b8ea4]" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Categories</p>
                      <p className="text-2xl font-bold">
                        {new Set(dashboardData.products.map(p => p.category)).size}
                      </p>
                    </div>
                    <Warehouse className="h-8 w-8 text-[#66cadb]" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Low Stock</p>
                      <p className="text-2xl font-bold text-red-600">{dashboardData.lowStockProducts.length}</p>
                    </div>
                    <TrendingDown className="h-8 w-8 text-red-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Value</p>
                      <p className="text-2xl font-bold">
                        RWF {dashboardData.products.reduce((sum, p) => sum + (p.price * p.current_stock), 0).toLocaleString()}
                      </p>
                    </div>
                    <DollarSign className="h-8 w-8 text-green-600" />
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Product List</CardTitle>
                <CardDescription>All products across business verticals</CardDescription>
              </CardHeader>
              <CardContent>
                {dashboardData.products.length > 0 ? (
                  <div className="space-y-4">
                    {dashboardData.products.slice(0, 10).map((product) => (
                      <div key={product.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors">
                        <div className="space-y-1">
                          <h4 className="font-medium">{product.name}</h4>
                          <p className="text-sm text-gray-600 capitalize">{product.category.replace('_', ' ')}</p>
                          <p className="text-xs text-gray-500">SKU: {product.sku}</p>
                        </div>
                        <div className="text-right space-y-1">
                          <p className="font-semibold">RWF {product.price.toLocaleString()}</p>
                          <p className="text-sm text-gray-600">
                            Stock: {product.current_stock} {product.unit}
                          </p>
                          <Badge 
                            variant={product.current_stock <= product.minimum_stock ? 'destructive' : 'default'}
                            className="text-xs"
                          >
                            {product.current_stock <= product.minimum_stock ? 'Low Stock' : 'In Stock'}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <Package className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>No products found</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        );

      default:
        return (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="text-6xl mb-4">🚧</div>
              <h3 className="text-xl font-semibold mb-2">Module Under Development</h3>
              <p className="text-gray-600">This module is being built. Check back soon!</p>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="bg-[#0c4864] text-white px-3 py-2 rounded-lg font-bold text-lg">
              AE
            </div>
            <div>
              <h1 className="text-xl font-bold text-[#0c4864]">Afro Experts ERP & POS</h1>
              <p className="text-sm text-gray-600">Business Management System</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon" className="relative">
              <Bell className="h-5 w-5" />
              {notifications > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {notifications}
                </span>
              )}
            </Button>
            <div className="flex items-center space-x-2">
              <div className="bg-[#3b8ea4] text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold">
                {user?.full_name.split(' ').map(n => n[0]).join('').toUpperCase()}
              </div>
              <div className="text-sm">
                <p className="font-medium">{user?.full_name}</p>
                <p className="text-gray-500 capitalize">{user?.role}</p>
              </div>
            </div>
            <Button variant="ghost" size="icon" onClick={logout}>
              <LogOut className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r border-gray-200 min-h-screen">
          <nav className="p-4 space-y-2">
            {modules.map((module) => {
              const IconComponent = module.icon;
              return (
                <button
                  key={module.id}
                  onClick={() => setActiveModule(module.id)}
                  className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                    activeModule === module.id
                      ? "bg-[#0c4864] text-white"
                      : "text-gray-700 hover:bg-gray-100"
                  }`}
                >
                  <IconComponent className="h-5 w-5" />
                  <div>
                    <div className="font-medium">{module.title}</div>
                    <div className="text-xs opacity-75">{module.description}</div>
                  </div>
                </button>
              );
            })}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {renderDashboardContent()}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;