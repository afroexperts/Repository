import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
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
  Menu
} from "lucide-react";

const Dashboard = () => {
  const [activeModule, setActiveModule] = useState("dashboard");
  const [notifications, setNotifications] = useState(3);

  // Mock data for dashboard
  const dashboardStats = {
    totalSales: 125000,
    monthlyGrowth: 12.5,
    activeOrders: 45,
    lowStockItems: 8,
    totalClients: 234,
    pendingQuotes: 12
  };

  const recentTransactions = [
    { id: 1, type: "Sale", client: "ABC Construction", amount: 15000, product: "Marble Dust - 5 tons", status: "Completed" },
    { id: 2, type: "Service", client: "Tech Solutions Ltd", amount: 2500, product: "Network Setup", status: "In Progress" },
    { id: 3, type: "Product", client: "Rural Connectivity", amount: 5000, product: "Starlink Residential Kit", status: "Shipped" },
    { id: 4, type: "Refurbished", client: "Local Merchant", amount: 800, product: "Refurbished Laptop", status: "Completed" }
  ];

  const lowStockAlerts = [
    { product: "Starlink Business Kit", current: 2, minimum: 5, category: "starlink" },
    { product: "Marble Dust Premium", current: 8, minimum: 20, category: "marble", unit: "tons" },
    { product: "Refurbished Tablets", current: 1, minimum: 3, category: "secondhand" },
    { product: "Network Cables", current: 15, minimum: 25, category: "services" }
  ];

  const modules = [
    {
      id: "dashboard",
      title: "Dashboard",
      icon: BarChart3,
      description: "Overview and Analytics"
    },
    {
      id: "products",
      title: "Product Management",
      icon: Package,
      description: "Manage Products & Services"
    },
    {
      id: "inventory",
      title: "Inventory",
      icon: Warehouse,
      description: "Stock Management"
    },
    {
      id: "pos",
      title: "Point of Sale",
      icon: ShoppingCart,
      description: "Sales Terminal"
    },
    {
      id: "orders",
      title: "Order Management",
      icon: FileText,
      description: "Track Orders & Deliveries"
    },
    {
      id: "clients",
      title: "Client Management",
      icon: Users,
      description: "Customer Relations"
    },
    {
      id: "services",
      title: "Service Booking",
      icon: Calendar,
      description: "IT & Logistics Services"
    },
    {
      id: "secondhand",
      title: "Second-Hand Sales",
      icon: Recycle,
      description: "Used Products Management"
    },
    {
      id: "marble",
      title: "Marble Dust",
      icon: Mountain,
      description: "Production & Sales"
    },
    {
      id: "starlink",
      title: "Starlink Resale",
      icon: Satellite,
      description: "Satellite Internet Products"
    },
    {
      id: "finance",
      title: "Finance",
      icon: CreditCard,
      description: "Financial Management"
    },
    {
      id: "reports",
      title: "Reports",
      icon: TrendingUp,
      description: "Business Analytics"
    }
  ];

  const renderDashboardContent = () => {
    switch (activeModule) {
      case "dashboard":
        return (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Sales (RWF)</CardTitle>
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardStats.totalSales.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">
                    <span className="text-green-600">+{dashboardStats.monthlyGrowth}%</span> from last month
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Orders</CardTitle>
                  <FileText className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardStats.activeOrders}</div>
                  <p className="text-xs text-muted-foreground">Processing & Delivery</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Clients</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardStats.totalClients}</div>
                  <p className="text-xs text-muted-foreground">Active customers</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Low Stock Alerts</CardTitle>
                  <TrendingDown className="h-4 w-4 text-red-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-red-600">{dashboardStats.lowStockItems}</div>
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
                  <div className="space-y-4">
                    {recentTransactions.map((transaction) => (
                      <div key={transaction.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div className="space-y-1">
                          <p className="text-sm font-medium">{transaction.client}</p>
                          <p className="text-xs text-gray-600">{transaction.product}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-semibold">RWF {transaction.amount.toLocaleString()}</p>
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
                </CardContent>
              </Card>

              {/* Low Stock Alerts */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-red-600">Low Stock Alerts</CardTitle>
                  <CardDescription>Items requiring immediate attention</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {lowStockAlerts.map((item, index) => (
                      <div key={index} className="flex items-center justify-between p-3 border border-red-200 rounded-lg bg-red-50">
                        <div className="space-y-1">
                          <p className="text-sm font-medium">{item.product}</p>
                          <p className="text-xs text-red-600">
                            Current: {item.current}{item.unit ? ` ${item.unit}` : ' units'} 
                            (Min: {item.minimum})
                          </p>
                        </div>
                        <Badge variant="destructive" className="text-xs">
                          Restock
                        </Badge>
                      </div>
                    ))}
                  </div>
                  <Button className="w-full mt-4 bg-red-600 hover:bg-red-700">
                    View All Inventory Alerts
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        );

      case "pos":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Point of Sale Terminal</h2>
                <p className="text-gray-600">Process sales across all business verticals</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Search className="h-4 w-4 mr-2" />
                  Search Products
                </Button>
                <Button className="bg-[#0c4864]">
                  <Plus className="h-4 w-4 mr-2" />
                  New Sale
                </Button>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Product Categories */}
              <Card>
                <CardHeader>
                  <CardTitle>Product Categories</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {[
                    { name: "Marble Dust", icon: Mountain, count: 15 },
                    { name: "IT Services", icon: Settings, count: 8 },
                    { name: "Starlink Products", icon: Satellite, count: 12 },
                    { name: "Second-Hand Items", icon: Recycle, count: 25 }
                  ].map((category, index) => {
                    const IconComponent = category.icon;
                    return (
                      <Button 
                        key={index}
                        variant="ghost" 
                        className="w-full justify-between h-12"
                      >
                        <div className="flex items-center">
                          <IconComponent className="h-4 w-4 mr-3" />
                          {category.name}
                        </div>
                        <Badge variant="secondary">{category.count}</Badge>
                      </Button>
                    );
                  })}
                </CardContent>
              </Card>

              {/* Sales Cart */}
              <Card>
                <CardHeader>
                  <CardTitle>Current Sale</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8 text-gray-500">
                    <ShoppingCart className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>No items in cart</p>
                    <p className="text-sm">Scan or search products to add</p>
                  </div>
                </CardContent>
              </Card>

              {/* Quick Actions */}
              <Card>
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <Button variant="outline" className="w-full justify-start">
                    <Eye className="h-4 w-4 mr-2" />
                    View Sales History
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Users className="h-4 w-4 mr-2" />
                    Select Customer
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <CreditCard className="h-4 w-4 mr-2" />
                    Payment Methods
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Download className="h-4 w-4 mr-2" />
                    Print Receipt
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        );

      case "inventory":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Inventory Management</h2>
                <p className="text-gray-600">Track stock levels across all locations and categories</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Filter className="h-4 w-4 mr-2" />
                  Filter
                </Button>
                <Button className="bg-[#0c4864]">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Stock
                </Button>
              </div>
            </div>

            <Tabs defaultValue="overview" className="w-full">
              <TabsList>
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="marble">Marble Dust</TabsTrigger>
                <TabsTrigger value="starlink">Starlink</TabsTrigger>
                <TabsTrigger value="secondhand">Second-Hand</TabsTrigger>
                <TabsTrigger value="services">Services</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="mt-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                  <Card>
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Total Products</p>
                          <p className="text-2xl font-bold">1,247</p>
                        </div>
                        <Package className="h-8 w-8 text-[#3b8ea4]" />
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Low Stock</p>
                          <p className="text-2xl font-bold text-red-600">8</p>
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
                          <p className="text-2xl font-bold">RWF 2.1M</p>
                        </div>
                        <DollarSign className="h-8 w-8 text-green-600" />
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Locations</p>
                          <p className="text-2xl font-bold">3</p>
                        </div>
                        <Warehouse className="h-8 w-8 text-[#66cadb]" />
                      </div>
                    </CardContent>
                  </Card>
                </div>

                <Card>
                  <CardHeader>
                    <CardTitle>Inventory Status by Category</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {[
                        { category: "Marble Dust", total: 45, unit: "tons", value: 850000, status: "Good" },
                        { category: "Starlink Products", total: 23, unit: "units", value: 580000, status: "Low" },
                        { category: "Second-Hand Items", total: 156, unit: "items", value: 234000, status: "Good" },
                        { category: "Service Equipment", total: 67, unit: "items", value: 445000, status: "Adequate" }
                      ].map((item, index) => (
                        <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                          <div>
                            <h4 className="font-medium">{item.category}</h4>
                            <p className="text-sm text-gray-600">
                              {item.total} {item.unit} • RWF {item.value.toLocaleString()}
                            </p>
                          </div>
                          <Badge 
                            variant={item.status === 'Low' ? 'destructive' : item.status === 'Good' ? 'default' : 'secondary'}
                          >
                            {item.status}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
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
            <Button variant="ghost" size="icon">
              <User className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon">
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