import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { useAuth } from "../contexts/AuthContext";
import { useSettings } from "../contexts/SettingsContext";
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
  CheckCircle,
  Network,
  Headphones,
  Building,
  Camera,
  MessageSquare,
  X
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const { user, logout, hasPermission } = useAuth();
  const { settings, loading: settingsLoading, saving, saveSettings, updateSettings, uploadImage } = useSettings();
  const { toast } = useToast();
  const [activeModule, setActiveModule] = useState("dashboard");
  const [notifications, setNotifications] = useState(0);
  const [loading, setLoading] = useState(true);
  
  // CRUD Modal States
  const [showAddProductModal, setShowAddProductModal] = useState(false);
  const [showAddClientModal, setShowAddClientModal] = useState(false);
  const [showAddOrderModal, setShowAddOrderModal] = useState(false);
  const [showPosModal, setShowPosModal] = useState(false);
  const [showInventoryModal, setShowInventoryModal] = useState(false);
  const [showServiceBookingModal, setShowServiceBookingModal] = useState(false);
  const [showFinanceModal, setShowFinanceModal] = useState(false);
  const [showSecondHandModal, setShowSecondHandModal] = useState(false);
  const [showMarbleDustModal, setShowMarbleDustModal] = useState(false);
  const [showStarlinkModal, setShowStarlinkModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [formLoading, setFormLoading] = useState(false);
  
  // POS State
  const [posCart, setPosCart] = useState([]);
  const [posSelectedProduct, setPosSelectedProduct] = useState('');
  const [posQuantity, setPosQuantity] = useState(1);
  
  // Form Data States
  const [productForm, setProductForm] = useState({
    name: '',
    category: '',
    description: '',
    price: '',
    cost_price: '',
    sku: '',
    unit: 'pieces',
    minimum_stock: '',
    current_stock: '',
    location: ''
  });
  
  const [clientForm, setClientForm] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    client_type: 'individual',
    company_name: '',
    tax_number: ''
  });
  
  const [orderForm, setOrderForm] = useState({
    client_id: '',
    items: [],
    payment_method: 'cash',
    notes: ''
  });
  
  const [inventoryForm, setInventoryForm] = useState({
    product_id: '',
    movement_type: 'stock_in',
    quantity: '',
    unit_cost: '',
    notes: '',
    reference_number: ''
  });
  
  const [serviceBookingForm, setServiceBookingForm] = useState({
    client_name: '',
    client_email: '',
    client_phone: '',
    service_type: 'it_support',
    description: '',
    location: '',
    preferred_date: ''
  });
  
  const [financeForm, setFinanceForm] = useState({
    transaction_type: 'income',
    category: '',
    description: '',
    amount: '',
    reference_id: ''
  });
  
  const [secondHandForm, setSecondHandForm] = useState({
    product_name: '',
    condition: 'good',
    original_price: '',
    selling_price: '',
    description: '',
    category: ''
  });
  
  const [marbleDustForm, setMarbleDustForm] = useState({
    batch_number: '',
    production_date: '',
    quantity_kg: '',
    quality_grade: 'premium',
    notes: ''
  });
  
  const [starlinkForm, setStarlinkForm] = useState({
    customer_name: '',
    customer_phone: '',
    installation_address: '',
    kit_type: 'residential',
    installation_date: '',
    technician_id: ''
  });
  
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

  // CRUD Functions
  const handleAddProduct = async (e) => {
    e.preventDefault();
    setFormLoading(true);
    
    try {
      const response = await axios.post(`${API}/products`, productForm);
      
      if (response.status === 200) {
        // Refresh products data
        const productsResponse = await axios.get(`${API}/products`);
        setDashboardData(prev => ({ ...prev, products: productsResponse.data }));
        
        // Reset form and close modal
        setProductForm({
          name: '', category: '', description: '', price: '', cost_price: '',
          sku: '', unit: 'pieces', minimum_stock: '', current_stock: '', location: ''
        });
        setShowAddProductModal(false);
        
        toast({
          title: "Success",
          description: "Product added successfully!",
        });
      }
    } catch (error) {
      console.error('Error adding product:', error);
      toast({
        title: "Error",
        description: "Failed to add product. Please try again.",
        variant: "destructive",
      });
    } finally {
      setFormLoading(false);
    }
  };

  const handleAddClient = async (e) => {
    e.preventDefault();
    setFormLoading(true);
    
    try {
      const response = await axios.post(`${API}/clients`, clientForm);
      
      if (response.status === 200) {
        // Refresh clients data
        const clientsResponse = await axios.get(`${API}/clients`);
        setDashboardData(prev => ({ ...prev, clients: clientsResponse.data }));
        
        // Reset form and close modal
        setClientForm({
          name: '', email: '', phone: '', address: '',
          client_type: 'individual', company_name: '', tax_number: ''
        });
        setShowAddClientModal(false);
        
        toast({
          title: "Success",
          description: "Client added successfully!",
        });
      }
    } catch (error) {
      console.error('Error adding client:', error);
      toast({
        title: "Error",
        description: "Failed to add client. Please try again.",
        variant: "destructive",
      });
    } finally {
      setFormLoading(false);
    }
  };

  const handleAddOrder = async (e) => {
    e.preventDefault();
    setFormLoading(true);
    
    try {
      const response = await axios.post(`${API}/orders`, orderForm);
      
      if (response.status === 200) {
        // Refresh orders data
        const ordersResponse = await axios.get(`${API}/orders`);
        setDashboardData(prev => ({ ...prev, orders: ordersResponse.data }));
        
        // Reset form and close modal
        setOrderForm({
          client_id: '', items: [], payment_method: 'cash', notes: ''
        });
        setShowAddOrderModal(false);
        
        toast({
          title: "Success",
          description: "Order created successfully!",
        });
      }
    } catch (error) {
      console.error('Error adding order:', error);
      toast({
        title: "Error",
        description: "Failed to create order. Please try again.",
        variant: "destructive",
      });
    } finally {
      setFormLoading(false);
    }
  };

  const handleInventoryMovement = async (e) => {
    e.preventDefault();
    setFormLoading(true);
    
    try {
      const response = await axios.post(`${API}/inventory/movements`, inventoryForm);
      
      if (response.status === 200) {
        // Refresh inventory data
        const inventoryResponse = await axios.get(`${API}/inventory/movements`);
        setDashboardData(prev => ({ ...prev, inventoryMovements: inventoryResponse.data }));
        
        // Reset form and close modal
        setInventoryForm({
          product_id: '', movement_type: 'stock_in', quantity: '',
          unit_cost: '', notes: '', reference_number: ''
        });
        setShowInventoryModal(false);
        
        toast({
          title: "Success",
          description: "Inventory movement recorded successfully!",
        });
      }
    } catch (error) {
      console.error('Error recording inventory movement:', error);
      toast({
        title: "Error",
        description: "Failed to record inventory movement. Please try again.",
        variant: "destructive",
      });
    } finally {
      setFormLoading(false);
    }
  };

  const handleAddServiceBooking = async (e) => {
    e.preventDefault();
    setFormLoading(true);
    
    try {
      const response = await axios.post(`${API}/services/bookings`, serviceBookingForm);
      
      if (response.status === 200) {
        // Refresh service bookings data
        const bookingsResponse = await axios.get(`${API}/services/bookings`);
        setDashboardData(prev => ({ ...prev, serviceBookings: bookingsResponse.data }));
        
        // Reset form and close modal
        setServiceBookingForm({
          client_name: '', client_email: '', client_phone: '',
          service_type: 'it_support', description: '', location: '', preferred_date: ''
        });
        setShowServiceBookingModal(false);
        
        toast({
          title: "Success",
          description: "Service booking created successfully!",
        });
      }
    } catch (error) {
      console.error('Error adding service booking:', error);
      toast({
        title: "Error",
        description: "Failed to create service booking. Please try again.",
        variant: "destructive",
      });
    } finally {
      setFormLoading(false);
    }
  };

  const handleAddFinanceTransaction = async (e) => {
    e.preventDefault();
    setFormLoading(true);
    
    try {
      const response = await axios.post(`${API}/finance/transactions`, financeForm);
      
      if (response.status === 200) {
        // Refresh finance data
        const financeResponse = await axios.get(`${API}/finance/transactions`);
        setDashboardData(prev => ({ ...prev, financialTransactions: financeResponse.data }));
        
        // Reset form and close modal
        setFinanceForm({
          transaction_type: 'income', category: '', description: '',
          amount: '', reference_id: ''
        });
        setShowFinanceModal(false);
        
        toast({
          title: "Success",
          description: "Financial transaction recorded successfully!",
        });
      }
    } catch (error) {
      console.error('Error adding financial transaction:', error);
      toast({
        title: "Error",
        description: "Failed to record transaction. Please try again.",
        variant: "destructive",
      });
    } finally {
      setFormLoading(false);
    }
  };

  // POS Functions
  const addToCart = () => {
    if (!posSelectedProduct || posQuantity <= 0) return;
    
    const product = dashboardData.products.find(p => p.id === posSelectedProduct);
    if (!product) return;
    
    const existingItem = posCart.find(item => item.id === product.id);
    
    if (existingItem) {
      setPosCart(posCart.map(item => 
        item.id === product.id 
          ? { ...item, quantity: item.quantity + posQuantity, total: (item.quantity + posQuantity) * item.price }
          : item
      ));
    } else {
      setPosCart([...posCart, {
        id: product.id,
        name: product.name,
        price: product.price,
        quantity: posQuantity,
        total: product.price * posQuantity
      }]);
    }
    
    setPosSelectedProduct('');
    setPosQuantity(1);
  };

  const removeFromCart = (productId) => {
    setPosCart(posCart.filter(item => item.id !== productId));
  };

  const completePOSSale = async () => {
    if (posCart.length === 0) return;
    
    setFormLoading(true);
    try {
      const subtotal = posCart.reduce((sum, item) => sum + item.total, 0);
      const taxAmount = subtotal * 0.18;
      const total = subtotal + taxAmount;
      
      const posTransaction = {
        items: posCart,
        subtotal,
        tax_percentage: 18,
        tax_amount: taxAmount,
        total_amount: total,
        payment_method: 'cash',
        payment_received: total,
        change_given: 0
      };
      
      const response = await axios.post(`${API}/pos/transactions`, posTransaction);
      
      if (response.status === 200) {
        setPosCart([]);
        toast({
          title: "Success",
          description: "Sale completed successfully!",
        });
      }
    } catch (error) {
      console.error('Error completing sale:', error);
      toast({
        title: "Error",
        description: "Failed to complete sale. Please try again.",
        variant: "destructive",
      });
    } finally {
      setFormLoading(false);
    }
  };

  const handleDeleteProduct = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return;
    }
    
    try {
      await axios.delete(`${API}/products/${productId}`);
      
      // Remove product from local state
      setDashboardData(prev => ({
        ...prev,
        products: prev.products.filter(p => p.id !== productId)
      }));
      
      toast({
        title: "Success",
        description: "Product deleted successfully!",
      });
    } catch (error) {
      console.error('Error deleting product:', error);
      toast({
        title: "Error",
        description: "Failed to delete product. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleDeleteClient = async (clientId) => {
    if (!window.confirm('Are you sure you want to delete this client?')) {
      return;
    }
    
    try {
      await axios.delete(`${API}/clients/${clientId}`);
      
      // Remove client from local state
      setDashboardData(prev => ({
        ...prev,
        clients: prev.clients.filter(c => c.id !== clientId)
      }));
      
      toast({
        title: "Success",
        description: "Client deleted successfully!",
      });
    } catch (error) {
      console.error('Error deleting client:', error);
      toast({
        title: "Error",
        description: "Failed to delete client. Please try again.",
        variant: "destructive",
      });
    }
  };

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
      id: "portfolio",
      title: "Portfolio",
      icon: Building,
      description: "Project Showcase",
      permission: "admin"
    },
    {
      id: "settings",
      title: "Settings",
      icon: Settings,
      description: "System Configuration",
      permission: "admin"
    }
  ].filter(module => hasPermission(module.permission));

  // Settings form handlers
  const handleSaveSettings = async (section) => {
    try {
      const result = await saveSettings(section, settings[section]);
      toast({
        title: result.success ? "Success" : "Error",
        description: result.message,
        variant: result.success ? "default" : "destructive",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save settings",
        variant: "destructive",
      });
    }
  };

  const handleInputChange = (section, field, value) => {
    updateSettings(section, { [field]: value });
  };

  const handleImageUpload = async (file, section, field) => {
    try {
      const result = await uploadImage(file);
      if (result.success) {
        updateSettings(section, { [field]: result.url });
        toast({
          title: "Success",
          description: "Image uploaded successfully!",
        });
      } else {
        toast({
          title: "Error",
          description: result.message,
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to upload image",
        variant: "destructive",
      });
    }
  };

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
                  <Button 
                    className="bg-[#0c4864]"
                    onClick={() => setShowAddProductModal(true)}
                  >
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

      case "inventory":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Inventory Management</h2>
                <p className="text-gray-600">Track stock movements and manage inventory across all products</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
                {hasPermission('manage_products') && (
                  <Button 
                    className="bg-[#0c4864]"
                    onClick={() => setShowInventoryModal(true)}
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Stock Movement
                  </Button>
                )}
              </div>
            </div>

            {/* Inventory Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Stock Value</p>
                      <p className="text-2xl font-bold">RWF {dashboardData.products.reduce((sum, p) => sum + (p.price * p.current_stock), 0).toLocaleString()}</p>
                    </div>
                    <DollarSign className="h-8 w-8 text-green-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Low Stock Items</p>
                      <p className="text-2xl font-bold text-red-600">{dashboardData.lowStockProducts.length}</p>
                    </div>
                    <AlertTriangle className="h-8 w-8 text-red-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Items</p>
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
                      <p className="text-2xl font-bold">{new Set(dashboardData.products.map(p => p.category)).size}</p>
                    </div>
                    <Warehouse className="h-8 w-8 text-[#66cadb]" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Stock Alerts */}
            <Card>
              <CardHeader>
                <CardTitle className="text-red-600">Stock Alerts</CardTitle>
                <CardDescription>Items requiring immediate attention</CardDescription>
              </CardHeader>
              <CardContent>
                {dashboardData.lowStockProducts.length > 0 ? (
                  <div className="space-y-4">
                    {dashboardData.lowStockProducts.map((item) => (
                      <div key={item.id} className="flex items-center justify-between p-3 border border-red-200 rounded-lg bg-red-50">
                        <div>
                          <h4 className="font-medium">{item.name}</h4>
                          <p className="text-sm text-red-600">Current: {item.current_stock} {item.unit} (Min: {item.minimum_stock})</p>
                        </div>
                        <div className="flex space-x-2">
                          <Button size="sm" className="bg-red-600 hover:bg-red-700 text-white">
                            Restock
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-500" />
                    <p className="text-gray-500">All items are well stocked!</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        );

      case "pos":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Point of Sale</h2>
                <p className="text-gray-600">Process sales transactions and manage cash register</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <FileText className="h-4 w-4 mr-2" />
                  Sales Report
                </Button>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Product Selection */}
              <div className="lg:col-span-2">
                <Card>
                  <CardHeader>
                    <CardTitle>Select Products</CardTitle>
                    <div className="flex space-x-2">
                      <select
                        className="flex-1 p-2 border rounded-lg"
                        value={posSelectedProduct}
                        onChange={(e) => setPosSelectedProduct(e.target.value)}
                      >
                        <option value="">Select a product...</option>
                        {dashboardData.products.map((product) => (
                          <option key={product.id} value={product.id}>
                            {product.name} - RWF {product.price.toLocaleString()} (Stock: {product.current_stock})
                          </option>
                        ))}
                      </select>
                      <Input
                        type="number"
                        min="1"
                        value={posQuantity}
                        onChange={(e) => setPosQuantity(parseInt(e.target.value) || 1)}
                        className="w-20"
                        placeholder="Qty"
                      />
                      <Button 
                        onClick={addToCart}
                        className="bg-[#0c4864]"
                        disabled={!posSelectedProduct}
                      >
                        <Plus className="h-4 w-4" />
                        Add
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-96 overflow-y-auto">
                      {dashboardData.products.slice(0, 6).map((product) => (
                        <div key={product.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                          <div>
                            <h4 className="font-medium">{product.name}</h4>
                            <p className="text-sm text-gray-600">RWF {product.price.toLocaleString()}</p>
                            <p className="text-xs text-gray-500">Stock: {product.current_stock}</p>
                          </div>
                          <Button 
                            size="sm" 
                            className="bg-[#0c4864]"
                            onClick={() => {
                              setPosSelectedProduct(product.id);
                              addToCart();
                            }}
                          >
                            <Plus className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Cart & Payment */}
              <div>
                <Card>
                  <CardHeader>
                    <CardTitle>Current Sale</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {posCart.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                          <ShoppingCart className="h-12 w-12 mx-auto mb-4 opacity-50" />
                          <p>No items added</p>
                        </div>
                      ) : (
                        <div className="space-y-2 max-h-64 overflow-y-auto">
                          {posCart.map((item) => (
                            <div key={item.id} className="flex justify-between items-center p-2 border rounded">
                              <div className="flex-1">
                                <p className="font-medium text-sm">{item.name}</p>
                                <p className="text-xs text-gray-500">{item.quantity} × RWF {item.price.toLocaleString()}</p>
                              </div>
                              <div className="flex items-center space-x-2">
                                <span className="font-medium">RWF {item.total.toLocaleString()}</span>
                                <Button
                                  size="sm"
                                  variant="destructive"
                                  onClick={() => removeFromCart(item.id)}
                                >
                                  <X className="h-3 w-3" />
                                </Button>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                      
                      <div className="border-t pt-4">
                        <div className="flex justify-between text-sm">
                          <span>Subtotal:</span>
                          <span>RWF {posCart.reduce((sum, item) => sum + item.total, 0).toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span>Tax (18%):</span>
                          <span>RWF {Math.round(posCart.reduce((sum, item) => sum + item.total, 0) * 0.18).toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between font-bold">
                          <span>Total:</span>
                          <span>RWF {Math.round(posCart.reduce((sum, item) => sum + item.total, 0) * 1.18).toLocaleString()}</span>
                        </div>
                      </div>
                      
                      <Button 
                        className="w-full bg-green-600 hover:bg-green-700" 
                        disabled={posCart.length === 0 || formLoading}
                        onClick={completePOSSale}
                      >
                        {formLoading ? (
                          <>
                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                            Processing...
                          </>
                        ) : (
                          'Complete Sale'
                        )}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        );

      case "orders":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Order Management</h2>
                <p className="text-gray-600">Track and manage customer orders</p>
              </div>
              <div className="flex space-x-2">
                <Select>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Filter by status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Orders</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="processing">Processing</SelectItem>
                    <SelectItem value="shipped">Shipped</SelectItem>
                    <SelectItem value="delivered">Delivered</SelectItem>
                  </SelectContent>
                </Select>
                <Button 
                  className="bg-[#0c4864]"
                  onClick={() => setShowAddOrderModal(true)}
                >
                  <Plus className="h-4 w-4 mr-2" />
                  New Order
                </Button>
              </div>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Recent Orders</CardTitle>
                <CardDescription>Latest customer orders and their status</CardDescription>
              </CardHeader>
              <CardContent>
                {dashboardData.orders.length > 0 ? (
                  <div className="space-y-4">
                    {dashboardData.orders.map((order) => (
                      <div key={order.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                        <div className="space-y-1">
                          <h4 className="font-medium">{order.order_number}</h4>
                          <p className="text-sm text-gray-600">{order.client_name}</p>
                          <p className="text-xs text-gray-500">{new Date(order.created_at).toLocaleDateString()}</p>
                        </div>
                        <div className="text-right space-y-1">
                          <p className="font-semibold">RWF {order.total_amount.toLocaleString()}</p>
                          <Badge variant={order.status === 'completed' ? 'default' : 'secondary'}>
                            {order.status}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>No orders found</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        );

      case "clients":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Client Management</h2>
                <p className="text-gray-600">Manage customer relationships and information</p>
              </div>
              <div className="flex space-x-2">
                <Input placeholder="Search clients..." className="w-64" />
                <Button 
                  className="bg-[#0c4864]"
                  onClick={() => setShowAddClientModal(true)}
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Client
                </Button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Clients</p>
                      <p className="text-2xl font-bold">{dashboardData.clients.length}</p>
                    </div>
                    <Users className="h-8 w-8 text-[#3b8ea4]" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Business Clients</p>
                      <p className="text-2xl font-bold">{dashboardData.clients.filter(c => c.client_type === 'business').length}</p>
                    </div>
                    <Building className="h-8 w-8 text-[#66cadb]" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Individual Clients</p>
                      <p className="text-2xl font-bold">{dashboardData.clients.filter(c => c.client_type === 'individual').length}</p>
                    </div>
                    <User className="h-8 w-8 text-green-600" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Credit</p>
                      <p className="text-2xl font-bold">RWF {dashboardData.clients.reduce((sum, c) => sum + c.credit_limit, 0).toLocaleString()}</p>
                    </div>
                    <CreditCard className="h-8 w-8 text-purple-600" />
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Client List</CardTitle>
                <CardDescription>All registered clients and their information</CardDescription>
              </CardHeader>
              <CardContent>
                {dashboardData.clients.length > 0 ? (
                  <div className="space-y-4">
                    {dashboardData.clients.map((client) => (
                      <div key={client.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                        <div className="space-y-1">
                          <h4 className="font-medium">{client.name}</h4>
                          <p className="text-sm text-gray-600">{client.email}</p>
                          <div className="flex items-center space-x-2">
                            <Badge variant="outline" className="text-xs">
                              {client.client_type === 'business' ? 'Business' : 'Individual'}
                            </Badge>
                            <span className="text-xs text-gray-500">{client.phone}</span>
                          </div>
                        </div>
                        <div className="text-right space-y-1">
                          <p className="text-sm font-medium">Credit Limit: RWF {client.credit_limit.toLocaleString()}</p>
                          <p className="text-xs text-gray-500">Orders: {client.total_orders || 0}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <Users className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>No clients found</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        );

      case "services":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Service Booking</h2>
                <p className="text-gray-600">Manage IT services and logistics bookings</p>
              </div>
              <div className="flex space-x-2">
                <Select>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Filter by status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Services</SelectItem>
                    <SelectItem value="requested">Requested</SelectItem>
                    <SelectItem value="confirmed">Confirmed</SelectItem>
                    <SelectItem value="in_progress">In Progress</SelectItem>
                    <SelectItem value="completed">Completed</SelectItem>
                  </SelectContent>
                </Select>
                <Button className="bg-[#0c4864]">
                  <Plus className="h-4 w-4 mr-2" />
                  New Booking
                </Button>
              </div>
            </div>

            {/* Service Categories */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <Network className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Network Installation</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Professional network infrastructure setup</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">5 Active</Badge>
                    <Button size="sm">View Details</Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <Satellite className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Starlink Installation</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Satellite internet setup and configuration</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">8 Active</Badge>
                    <Button size="sm">View Details</Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <Headphones className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Technical Support</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">24/7 technical assistance and maintenance</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">12 Active</Badge>
                    <Button size="sm">View Details</Button>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Recent Bookings */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Service Bookings</CardTitle>
                <CardDescription>Latest service requests and their status</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { id: 1, client: "ABC Construction Ltd", service: "Network Installation", date: "2025-01-22", status: "In Progress" },
                    { id: 2, client: "Tech Solutions Rwanda", service: "Starlink Installation", date: "2025-01-21", status: "Confirmed" },
                    { id: 3, client: "Jean Baptiste", service: "Technical Support", date: "2025-01-20", status: "Completed" }
                  ].map((booking) => (
                    <div key={booking.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                      <div className="space-y-1">
                        <h4 className="font-medium">{booking.client}</h4>
                        <p className="text-sm text-gray-600">{booking.service}</p>
                        <p className="text-xs text-gray-500">{booking.date}</p>
                      </div>
                      <div className="text-right">
                        <Badge variant={booking.status === 'Completed' ? 'default' : 'secondary'}>
                          {booking.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        );

      case "finance":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Financial Management</h2>
                <p className="text-gray-600">Track income, expenses, and financial performance</p>
              </div>
              <div className="flex space-x-2">
                <Select>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="This Month" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="this-month">This Month</SelectItem>
                    <SelectItem value="last-month">Last Month</SelectItem>
                    <SelectItem value="this-year">This Year</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline">
                  <Download className="h-4 w-4 mr-2" />
                  Export Report
                </Button>
                <Button 
                  className="bg-[#0c4864]"
                  onClick={() => setShowFinanceModal(true)}
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Transaction
                </Button>
              </div>
            </div>

            {/* Financial Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Income</p>
                      <p className="text-2xl font-bold text-green-600">RWF 2,450,000</p>
                    </div>
                    <TrendingUp className="h-8 w-8 text-green-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Expenses</p>
                      <p className="text-2xl font-bold text-red-600">RWF 890,000</p>
                    </div>
                    <TrendingDown className="h-8 w-8 text-red-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Net Profit</p>
                      <p className="text-2xl font-bold text-blue-600">RWF 1,560,000</p>
                    </div>
                    <DollarSign className="h-8 w-8 text-blue-600" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Cash on Hand</p>
                      <p className="text-2xl font-bold text-purple-600">RWF 750,000</p>
                    </div>
                    <CreditCard className="h-8 w-8 text-purple-600" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Recent Transactions */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-green-600">Recent Income</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { description: "Starlink Installation - ABC Ltd", amount: 2500000, date: "2025-01-22" },
                      { description: "Network Setup - Tech Solutions", amount: 850000, date: "2025-01-21" },
                      { description: "POS System Sale", amount: 399000, date: "2025-01-20" }
                    ].map((transaction, index) => (
                      <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <p className="font-medium text-sm">{transaction.description}</p>
                          <p className="text-xs text-gray-500">{transaction.date}</p>
                        </div>
                        <p className="font-semibold text-green-600">+RWF {transaction.amount.toLocaleString()}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-red-600">Recent Expenses</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { description: "Office Supplies", amount: 150000, date: "2025-01-22" },
                      { description: "Equipment Maintenance", amount: 200000, date: "2025-01-21" },
                      { description: "Transportation", amount: 75000, date: "2025-01-20" }
                    ].map((transaction, index) => (
                      <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <p className="font-medium text-sm">{transaction.description}</p>
                          <p className="text-xs text-gray-500">{transaction.date}</p>
                        </div>
                        <p className="font-semibold text-red-600">-RWF {transaction.amount.toLocaleString()}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        );

      case "reports":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Reports & Analytics</h2>
                <p className="text-gray-600">Business intelligence and performance metrics</p>
              </div>
              <div className="flex space-x-2">
                <Select>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Select Period" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="today">Today</SelectItem>
                    <SelectItem value="week">This Week</SelectItem>
                    <SelectItem value="month">This Month</SelectItem>
                    <SelectItem value="quarter">This Quarter</SelectItem>
                    <SelectItem value="year">This Year</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline">
                  <Download className="h-4 w-4 mr-2" />
                  Export All
                </Button>
              </div>
            </div>

            {/* Report Categories */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <BarChart3 className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Sales Report</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Comprehensive sales analysis and trends</p>
                  <Button size="sm" className="w-full">Generate Report</Button>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <Package className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Inventory Report</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Stock levels and movement analysis</p>
                  <Button size="sm" className="w-full">Generate Report</Button>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <Users className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Client Report</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Customer behavior and analytics</p>
                  <Button size="sm" className="w-full">Generate Report</Button>
                </CardContent>
              </Card>
            </div>

            {/* Performance Metrics */}
            <Card>
              <CardHeader>
                <CardTitle>Key Performance Indicators</CardTitle>
                <CardDescription>Real-time business performance metrics</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="text-center p-4 border rounded-lg">
                    <p className="text-2xl font-bold text-[#0c4864]">85%</p>
                    <p className="text-sm text-gray-600">Customer Satisfaction</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <p className="text-2xl font-bold text-green-600">+12%</p>
                    <p className="text-sm text-gray-600">Monthly Growth</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <p className="text-2xl font-bold text-blue-600">95%</p>
                    <p className="text-sm text-gray-600">Order Fulfillment</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <p className="text-2xl font-bold text-purple-600">24h</p>
                    <p className="text-sm text-gray-600">Avg Response Time</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        );

      case "secondhand":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Second-Hand Sales</h2>
                <p className="text-gray-600">Manage refurbished and used product sales</p>
              </div>
              <div className="flex space-x-2">
                <Select>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Filter by grade" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Grades</SelectItem>
                    <SelectItem value="grade-a">Grade A</SelectItem>
                    <SelectItem value="grade-b">Grade B</SelectItem>
                    <SelectItem value="grade-c">Grade C</SelectItem>
                  </SelectContent>
                </Select>
                <Button className="bg-[#0c4864]">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Product
                </Button>
              </div>
            </div>

            {/* Second-hand Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Available Items</p>
                      <p className="text-2xl font-bold">{dashboardData.products.filter(p => p.category === 'secondhand').length}</p>
                    </div>
                    <Recycle className="h-8 w-8 text-green-600" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Grade A Items</p>
                      <p className="text-2xl font-bold">12</p>
                    </div>
                    <CheckCircle className="h-8 w-8 text-blue-600" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Value</p>
                      <p className="text-2xl font-bold">RWF {dashboardData.products.filter(p => p.category === 'secondhand').reduce((sum, p) => sum + (p.price * p.current_stock), 0).toLocaleString()}</p>
                    </div>
                    <DollarSign className="h-8 w-8 text-purple-600" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Sold This Month</p>
                      <p className="text-2xl font-bold">28</p>
                    </div>
                    <TrendingUp className="h-8 w-8 text-[#3b8ea4]" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Product Categories */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <CardTitle className="text-lg">Laptops & Computers</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Refurbished laptops, desktops, and accessories</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">15 Available</Badge>
                    <Button size="sm">View All</Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <CardTitle className="text-lg">Mobile Devices</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Smartphones, tablets, and mobile accessories</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">8 Available</Badge>
                    <Button size="sm">View All</Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <CardTitle className="text-lg">Networking Equipment</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Used routers, switches, and network gear</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">6 Available</Badge>
                    <Button size="sm">View All</Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        );

      case "marble":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Marble Dust Production</h2>
                <p className="text-gray-600">Track marble dust production and sales operations</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <FileText className="h-4 w-4 mr-2" />
                  Production Report
                </Button>
                <Button className="bg-[#0c4864]">
                  <Plus className="h-4 w-4 mr-2" />
                  New Batch
                </Button>
              </div>
            </div>

            {/* Production Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Current Stock</p>
                      <p className="text-2xl font-bold">{dashboardData.products.find(p => p.category === 'marble_dust')?.current_stock || 0} tons</p>
                    </div>
                    <Mountain className="h-8 w-8 text-gray-600" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Monthly Production</p>
                      <p className="text-2xl font-bold">45 tons</p>
                    </div>
                    <TrendingUp className="h-8 w-8 text-green-600" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Sales Revenue</p>
                      <p className="text-2xl font-bold">RWF 1,125,000</p>
                    </div>
                    <DollarSign className="h-8 w-8 text-blue-600" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Active Orders</p>
                      <p className="text-2xl font-bold">12</p>
                    </div>
                    <FileText className="h-8 w-8 text-[#3b8ea4]" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Production Batches */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Production Batches</CardTitle>
                <CardDescription>Latest marble dust production and quality records</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { batch: "MD-2025-001", quantity: "15 tons", quality: "Premium", date: "2025-01-22", status: "Completed" },
                    { batch: "MD-2025-002", quantity: "12 tons", quality: "Standard", date: "2025-01-20", status: "Processing" },
                    { batch: "MD-2025-003", quantity: "18 tons", quality: "Premium", date: "2025-01-18", status: "Completed" }
                  ].map((batch, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                      <div className="space-y-1">
                        <h4 className="font-medium">{batch.batch}</h4>
                        <p className="text-sm text-gray-600">{batch.quantity} - {batch.quality} Grade</p>
                        <p className="text-xs text-gray-500">{batch.date}</p>
                      </div>
                      <Badge variant={batch.status === 'Completed' ? 'default' : 'secondary'}>
                        {batch.status}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        );

      case "starlink":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Starlink Resale</h2>
                <p className="text-gray-600">Manage Starlink products and installation services</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Download className="h-4 w-4 mr-2" />
                  Installation Report
                </Button>
                <Button className="bg-[#0c4864]">
                  <Plus className="h-4 w-4 mr-2" />
                  New Installation
                </Button>
              </div>
            </div>

            {/* Starlink Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Kits in Stock</p>
                      <p className="text-2xl font-bold">{dashboardData.products.filter(p => p.category === 'starlink').reduce((sum, p) => sum + p.current_stock, 0)}</p>
                    </div>
                    <Satellite className="h-8 w-8 text-[#0c4864]" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Installations This Month</p>
                      <p className="text-2xl font-bold">24</p>
                    </div>
                    <TrendingUp className="h-8 w-8 text-green-600" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Revenue This Month</p>
                      <p className="text-2xl font-bold">RWF 14,376,000</p>
                    </div>
                    <DollarSign className="h-8 w-8 text-blue-600" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Pending Installations</p>
                      <p className="text-2xl font-bold">8</p>
                    </div>
                    <Calendar className="h-8 w-8 text-orange-600" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Product Types */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Residential Kits</CardTitle>
                  <CardDescription>Home internet solutions</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm">In Stock:</span>
                      <span className="font-medium">{dashboardData.products.find(p => p.name.includes('Residential'))?.current_stock || 0} kits</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm">Price:</span>
                      <span className="font-medium">RWF 599,000</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm">Installed This Month:</span>
                      <span className="font-medium">18 units</span>
                    </div>
                    <Button className="w-full" size="sm">Manage Inventory</Button>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Business Kits</CardTitle>
                  <CardDescription>Enterprise-grade solutions</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm">In Stock:</span>
                      <span className="font-medium">{dashboardData.products.find(p => p.name.includes('Business'))?.current_stock || 0} kits</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm">Price:</span>
                      <span className="font-medium">RWF 2,500,000</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm">Installed This Month:</span>
                      <span className="font-medium">6 units</span>
                    </div>
                    <Button className="w-full" size="sm">Manage Inventory</Button>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Installation Schedule */}
            <Card>
              <CardHeader>
                <CardTitle>Upcoming Installations</CardTitle>
                <CardDescription>Scheduled Starlink installations and services</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { client: "ABC Construction Ltd", kit: "Business Kit", date: "2025-01-24", technician: "John Rwigema", status: "Confirmed" },
                    { client: "Marie Uwimana", kit: "Residential Kit", date: "2025-01-25", technician: "Paul Nkusi", status: "Confirmed" },
                    { client: "Rural School Nyagatare", kit: "Business Kit", date: "2025-01-26", technician: "Jean Baptiste", status: "Pending" }
                  ].map((installation, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                      <div className="space-y-1">
                        <h4 className="font-medium">{installation.client}</h4>
                        <p className="text-sm text-gray-600">{installation.kit}</p>
                        <p className="text-xs text-gray-500">Technician: {installation.technician}</p>
                      </div>
                      <div className="text-right space-y-1">
                        <p className="text-sm font-medium">{installation.date}</p>
                        <Badge variant={installation.status === 'Confirmed' ? 'default' : 'secondary'}>
                          {installation.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        );

      case "portfolio":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Portfolio Management</h2>
                <p className="text-gray-600">Manage project showcase and company portfolio</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Download className="h-4 w-4 mr-2" />
                  Export Portfolio
                </Button>
                <Button className="bg-[#0c4864]">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Project
                </Button>
              </div>
            </div>

            {/* Portfolio Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Projects</p>
                      <p className="text-2xl font-bold">9</p>
                    </div>
                    <Building className="h-8 w-8 text-[#3b8ea4]" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Live Platforms</p>
                      <p className="text-2xl font-bold text-green-600">3</p>
                    </div>
                    <CheckCircle className="h-8 w-8 text-green-500" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Categories</p>
                      <p className="text-2xl font-bold">7</p>
                    </div>
                    <Package className="h-8 w-8 text-blue-600" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Happy Clients</p>
                      <p className="text-2xl font-bold">25+</p>
                    </div>
                    <Users className="h-8 w-8 text-purple-600" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Portfolio Categories */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <MessageSquare className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Digital Platforms</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Live operational platforms and web applications</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">3 Projects</Badge>
                    <Button size="sm">Manage</Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <Network className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Network Solutions</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Infrastructure and connectivity projects</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">2 Projects</Badge>
                    <Button size="sm">Manage</Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <Users className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Media & Events</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Creative and event management projects</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">1 Project</Badge>
                    <Button size="sm">Manage</Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <Building className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Business Solutions</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Enterprise software and ERP systems</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">1 Project</Badge>
                    <Button size="sm">Manage</Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <Mountain className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Manufacturing</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">Production and manufacturing operations</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">1 Project</Badge>
                    <Button size="sm">Manage</Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    <Camera className="h-6 w-6 text-[#0c4864]" />
                    <CardTitle className="text-lg">Security Solutions</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">CCTV and security system installations</p>
                  <div className="flex justify-between items-center">
                    <Badge variant="outline">1 Project</Badge>
                    <Button size="sm">Manage</Button>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Recent Projects */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Portfolio Projects</CardTitle>
                <CardDescription>Latest additions to the project portfolio</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { 
                      title: "Afro Bulk SMS Platform", 
                      category: "Digital Platforms", 
                      status: "Live", 
                      date: "2024",
                      client: "Afro Experts"
                    },
                    { 
                      title: "Enterprise ERP & POS System", 
                      category: "Business Solutions", 
                      status: "Active", 
                      date: "2025",
                      client: "Afro Experts"
                    },
                    { 
                      title: "Rural School Network Infrastructure", 
                      category: "Network Solutions", 
                      status: "Completed", 
                      date: "2024",
                      client: "Nyagatare District"
                    }
                  ].map((project, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                      <div className="space-y-1">
                        <h4 className="font-medium">{project.title}</h4>
                        <div className="flex items-center space-x-2">
                          <Badge variant="outline" className="text-xs">{project.category}</Badge>
                          <span className="text-xs text-gray-500">Client: {project.client}</span>
                        </div>
                        <p className="text-xs text-gray-500">{project.date}</p>
                      </div>
                      <div className="text-right space-y-1">
                        <Badge variant={project.status === 'Live' ? 'default' : project.status === 'Active' ? 'secondary' : 'outline'}>
                          {project.status}
                        </Badge>
                        <div className="flex space-x-2">
                          <Button variant="outline" size="sm">
                            Edit
                          </Button>
                          <Button variant="outline" size="sm">
                            <Eye className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        );

      case "settings":
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Website Settings</h2>
                <p className="text-gray-600">Manage homepage content and website configurations</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Eye className="h-4 w-4 mr-2" />
                  Preview Changes
                </Button>
                <Button 
                  className="bg-[#0c4864]"
                  onClick={() => handleSaveSettings('hero')}
                  disabled={saving}
                >
                  {saving ? (
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  ) : null}
                  Save Changes
                </Button>
              </div>
            </div>

            {/* Settings Categories */}
            <Tabs defaultValue="homepage" className="w-full">
              <TabsList className="grid w-full grid-cols-7">
                <TabsTrigger value="homepage">Homepage</TabsTrigger>
                <TabsTrigger value="media">Media</TabsTrigger>
                <TabsTrigger value="about">About</TabsTrigger>
                <TabsTrigger value="services">Services</TabsTrigger>
                <TabsTrigger value="footer">Footer</TabsTrigger>
                <TabsTrigger value="general">General</TabsTrigger>
                <TabsTrigger value="users">Users</TabsTrigger>
              </TabsList>

              <TabsContent value="homepage" className="space-y-6">
                {/* Hero Section Settings */}
                <Card>
                  <CardHeader>
                    <CardTitle>Hero Section</CardTitle>
                    <CardDescription>Manage the main hero banner content and background images</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Text Content */}
                    <div className="space-y-4">
                      <h4 className="font-medium text-lg">Content</h4>
                      <div>
                        <label className="text-sm font-medium">Main Title</label>
                        <Input 
                          value={settings.hero?.title || ""} 
                          onChange={(e) => handleInputChange('hero', 'title', e.target.value)}
                          className="mt-1" 
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium">Subtitle</label>
                        <Input 
                          value={settings.hero?.subtitle || ""}
                          onChange={(e) => handleInputChange('hero', 'subtitle', e.target.value)}
                          className="mt-1" 
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium">Description</label>
                        <textarea 
                          className="w-full mt-1 p-3 border rounded-lg min-h-[100px]"
                          value={settings.hero?.description || ""}
                          onChange={(e) => handleInputChange('hero', 'description', e.target.value)}
                        />
                      </div>
                    </div>

                    {/* Image Management */}
                    <div className="space-y-4 border-t pt-6">
                      <h4 className="font-medium text-lg">Background Images</h4>
                      
                      {/* Current Background Image */}
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Hero Background Image</label>
                        <div className="border rounded-lg p-4 bg-gray-50">
                          <div className="flex items-center justify-between mb-3">
                            <p className="text-sm text-gray-600">Current: Hero Background</p>
                            <div className="flex space-x-2">
                              <Button size="sm" variant="outline">
                                <Eye className="h-4 w-4 mr-1" />
                                Preview
                              </Button>
                              <Button size="sm" variant="destructive">
                                Remove
                              </Button>
                            </div>
                          </div>
                          <div className="w-full h-32 bg-gradient-to-r from-[#0c4864] to-[#3b8ea4] rounded-lg flex items-center justify-center">
                            <p className="text-white text-sm">Current Hero Background</p>
                          </div>
                        </div>
                        <div className="flex space-x-2">
                          <Button size="sm" className="bg-[#0c4864]">
                            <Plus className="h-4 w-4 mr-1" />
                            Upload New Background
                          </Button>
                          <Button size="sm" variant="outline">
                            Choose from Gallery
                          </Button>
                        </div>
                      </div>

                      {/* Secondary Images */}
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Feature Images</label>
                        <div className="grid grid-cols-2 gap-4">
                          <div className="border rounded-lg p-3 bg-gray-50">
                            <div className="w-full h-24 bg-gray-200 rounded mb-2 flex items-center justify-center">
                              <p className="text-xs text-gray-500">Network Infrastructure</p>
                            </div>
                            <div className="flex justify-between items-center">
                              <p className="text-xs font-medium">Network Image</p>
                              <Button size="xs" variant="outline">Edit</Button>
                            </div>
                          </div>
                          <div className="border rounded-lg p-3 bg-gray-50">
                            <div className="w-full h-24 bg-gray-200 rounded mb-2 flex items-center justify-center">
                              <p className="text-xs text-gray-500">Starlink Satellite</p>
                            </div>
                            <div className="flex justify-between items-center">
                              <p className="text-xs font-medium">Starlink Image</p>
                              <Button size="xs" variant="outline">Edit</Button>
                            </div>
                          </div>
                        </div>
                        <Button size="sm" variant="outline" className="w-full">
                          <Plus className="h-4 w-4 mr-1" />
                          Add Feature Image
                        </Button>
                      </div>
                    </div>

                    {/* Call-to-Action Settings */}
                    <div className="space-y-4 border-t pt-6">
                      <h4 className="font-medium text-lg">Call-to-Action Buttons</h4>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-medium">Primary Button Text</label>
                          <Input 
                            value={settings.hero?.primaryButtonText || ""}
                            onChange={(e) => handleInputChange('hero', 'primaryButtonText', e.target.value)}
                            className="mt-1" 
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Primary Button Link</label>
                          <Input 
                            value={settings.hero?.primaryButtonLink || ""}
                            onChange={(e) => handleInputChange('hero', 'primaryButtonLink', e.target.value)}
                            className="mt-1" 
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Secondary Button Text</label>
                          <Input 
                            value={settings.hero?.secondaryButtonText || ""}
                            onChange={(e) => handleInputChange('hero', 'secondaryButtonText', e.target.value)}
                            className="mt-1" 
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Secondary Button Link</label>
                          <Input 
                            value={settings.hero?.secondaryButtonLink || ""}
                            onChange={(e) => handleInputChange('hero', 'secondaryButtonLink', e.target.value)}
                            className="mt-1" 
                          />
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Starlink Section Settings */}
                <Card>
                  <CardHeader>
                    <CardTitle>Starlink Promotion Section</CardTitle>
                    <CardDescription>Configure Starlink promotional content</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <label className="text-sm font-medium">Section Title</label>
                      <Input 
                        value={settings.starlink?.title || ""} 
                        onChange={(e) => handleInputChange('starlink', 'title', e.target.value)}
                        className="mt-1" 
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Description</label>
                      <textarea 
                        className="w-full mt-1 p-3 border rounded-lg min-h-[80px]"
                        value={settings.starlink?.description || ""}
                        onChange={(e) => handleInputChange('starlink', 'description', e.target.value)}
                      />
                    </div>
                    <div className="flex items-center space-x-2">
                      <input 
                        type="checkbox" 
                        id="show-starlink" 
                        checked={settings.starlink?.showSection || false}
                        onChange={(e) => handleInputChange('starlink', 'showSection', e.target.checked)}
                      />
                      <label htmlFor="show-starlink" className="text-sm">Show Starlink section</label>
                    </div>
                    <div className="flex justify-end pt-4 border-t">
                      <Button 
                        className="bg-[#0c4864]"
                        onClick={() => handleSaveSettings('starlink')}
                        disabled={saving}
                      >
                        {saving ? (
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        ) : null}
                        Save Starlink Settings
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                {/* Services Section Settings */}
                <Card>
                  <CardHeader>
                    <CardTitle>IT Services Section</CardTitle>
                    <CardDescription>Manage IT services showcase</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <label className="text-sm font-medium">Section Title</label>
                      <Input 
                        value={settings.services?.title || ""} 
                        onChange={(e) => handleInputChange('services', 'title', e.target.value)}
                        className="mt-1" 
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Description</label>
                      <textarea 
                        className="w-full mt-1 p-3 border rounded-lg min-h-[80px]"
                        value={settings.services?.description || ""}
                        onChange={(e) => handleInputChange('services', 'description', e.target.value)}
                      />
                    </div>
                    <div className="flex items-center space-x-2">
                      <input 
                        type="checkbox" 
                        id="show-services" 
                        checked={settings.services?.showSection || false}
                        onChange={(e) => handleInputChange('services', 'showSection', e.target.checked)}
                      />
                      <label htmlFor="show-services" className="text-sm">Show services section</label>
                    </div>
                    <div className="flex justify-end pt-4 border-t">
                      <Button 
                        className="bg-[#0c4864]"
                        onClick={() => handleSaveSettings('services')}
                        disabled={saving}
                      >
                        {saving ? (
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        ) : null}
                        Save Services Settings
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                {/* Our Clients Section Settings */}
                <Card>
                  <CardHeader>
                    <CardTitle>Our Clients Section</CardTitle>
                    <CardDescription>Configure client showcase and logos</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <label className="text-sm font-medium">Section Title</label>
                      <Input 
                        value={settings.clients?.title || ""} 
                        onChange={(e) => handleInputChange('clients', 'title', e.target.value)}
                        className="mt-1" 
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Description</label>
                      <textarea 
                        className="w-full mt-1 p-3 border rounded-lg min-h-[80px]"
                        value={settings.clients?.description || ""}
                        onChange={(e) => handleInputChange('clients', 'description', e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Footer Text</label>
                      <Input 
                        value={settings.clients?.footerText || ""} 
                        onChange={(e) => handleInputChange('clients', 'footerText', e.target.value)}
                        className="mt-1" 
                      />
                    </div>
                    <div className="flex items-center space-x-2">
                      <input 
                        type="checkbox" 
                        id="show-clients" 
                        checked={settings.clients?.showSection || false}
                        onChange={(e) => handleInputChange('clients', 'showSection', e.target.checked)}
                      />
                      <label htmlFor="show-clients" className="text-sm">Show clients section</label>
                    </div>
                    <div className="flex justify-end pt-4 border-t">
                      <Button 
                        className="bg-[#0c4864]"
                        onClick={() => handleSaveSettings('clients')}
                        disabled={saving}
                      >
                        {saving ? (
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        ) : null}
                        Save Clients Settings
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                {/* Impact Section Settings */}
                <Card>
                  <CardHeader>
                    <CardTitle>Impact Map Section</CardTitle>
                    <CardDescription>Update impact statistics and stories</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-sm font-medium">Communities Connected</label>
                        <Input type="number" defaultValue="50" className="mt-1" />
                      </div>
                      <div>
                        <label className="text-sm font-medium">Businesses Served</label>
                        <Input type="number" defaultValue="1000" className="mt-1" />
                      </div>
                      <div>
                        <label className="text-sm font-medium">People Online</label>
                        <Input type="number" defaultValue="10000" className="mt-1" />
                      </div>
                      <div>
                        <label className="text-sm font-medium">Countries Active</label>
                        <Input type="number" defaultValue="2" className="mt-1" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="about" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>About Page Content</CardTitle>
                    <CardDescription>Manage about page information</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <label className="text-sm font-medium">Company Mission</label>
                      <textarea 
                        className="w-full mt-1 p-3 border rounded-lg min-h-[120px]"
                        defaultValue="To bridge the digital divide across Africa by providing cutting-edge technology solutions and reliable internet connectivity that empowers communities and businesses to thrive in the digital economy."
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Company Vision</label>
                      <textarea 
                        className="w-full mt-1 p-3 border rounded-lg min-h-[120px]"
                        defaultValue="To be Africa's leading technology solutions provider, connecting every community and business to the global digital future through innovative infrastructure and unparalleled service excellence."
                      />
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="services" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Services Configuration</CardTitle>
                    <CardDescription>Manage all service offerings across different categories</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Technology Services */}
                    <div className="space-y-4">
                      <h4 className="font-medium text-lg text-[#0c4864] border-b border-[#3b8ea4] pb-2">Technology Services</h4>
                      {[
                        "Network Setup & Maintenance",
                        "CCTV & Access Control", 
                        "Server Installation",
                        "Technical Support",
                        "Software Development",
                        "Internet Provider"
                      ].map((service, index) => (
                        <div key={index} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50">
                          <div className="flex-1">
                            <Input defaultValue={service} />
                          </div>
                          <div className="flex space-x-2 ml-4">
                            <Button variant="outline" size="sm">
                              Edit
                            </Button>
                            <Button variant="destructive" size="sm">
                              Delete
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Media & Events Services */}
                    <div className="space-y-4">
                      <h4 className="font-medium text-lg text-[#0c4864] border-b border-[#3b8ea4] pb-2">Media & Events Services</h4>
                      {[
                        "Event Management",
                        "Audio-Visual Services",
                        "Design & Branding",
                        "Interpretation Services"
                      ].map((service, index) => (
                        <div key={index} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50">
                          <div className="flex-1">
                            <Input defaultValue={service} />
                          </div>
                          <div className="flex space-x-2 ml-4">
                            <Button variant="outline" size="sm">
                              Edit
                            </Button>
                            <Button variant="destructive" size="sm">
                              Delete
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Production & Supply Services */}
                    <div className="space-y-4">
                      <h4 className="font-medium text-lg text-[#0c4864] border-b border-[#3b8ea4] pb-2">Production & Supply Services</h4>
                      {[
                        "Marble Dust Production (Rwanda Exclusive)",
                        "General Supply"
                      ].map((service, index) => (
                        <div key={index} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50">
                          <div className="flex-1 flex items-center space-x-2">
                            <Input defaultValue={service.replace(' (Rwanda Exclusive)', '')} />
                            {service.includes('Rwanda Exclusive') && (
                              <Badge className="bg-[#66cadb] text-white text-xs">🇷🇼 Rwanda Only</Badge>
                            )}
                          </div>
                          <div className="flex space-x-2 ml-4">
                            <Button variant="outline" size="sm">
                              Edit
                            </Button>
                            <Button variant="destructive" size="sm">
                              Delete
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>

                    <Button className="w-full">
                      <Plus className="h-4 w-4 mr-2" />
                      Add New Service
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="general" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>General Website Settings</CardTitle>
                    <CardDescription>Configure global website settings and branding</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Basic Information */}
                    <div className="space-y-4">
                      <div>
                        <label className="text-sm font-medium">Website Title</label>
                        <Input 
                          value={settings.general?.websiteTitle || ""} 
                          onChange={(e) => handleInputChange('general', 'websiteTitle', e.target.value)}
                          className="mt-1" 
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium">Company Name</label>
                        <Input 
                          value={settings.general?.companyName || ""}
                          onChange={(e) => handleInputChange('general', 'companyName', e.target.value)}
                          className="mt-1" 
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium">Contact Email</label>
                        <Input 
                          value={settings.general?.contactEmail || ""}
                          onChange={(e) => handleInputChange('general', 'contactEmail', e.target.value)}
                          className="mt-1" 
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium">Support Phone</label>
                        <Input 
                          value={settings.general?.supportPhone || ""}
                          onChange={(e) => handleInputChange('general', 'supportPhone', e.target.value)}
                          className="mt-1" 
                        />
                      </div>
                    </div>

                    {/* Logo Management Section */}
                    <div className="space-y-4 border-t pt-6">
                      <h4 className="font-medium text-lg">Branding & Logo</h4>
                      
                      {/* Company Logo */}
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Company Logo</label>
                        <div className="border rounded-lg p-4 bg-gray-50">
                          <div className="flex items-center justify-between mb-3">
                            <p className="text-sm text-gray-600">
                              {settings.general?.companyLogo ? 'Current Logo' : 'No Logo Uploaded'}
                            </p>
                            {settings.general?.companyLogo && (
                              <div className="flex space-x-2">
                                <Button size="sm" variant="outline">
                                  <Eye className="h-4 w-4 mr-1" />
                                  Preview
                                </Button>
                                <Button 
                                  size="sm" 
                                  variant="destructive"
                                  onClick={() => handleInputChange('general', 'companyLogo', null)}
                                >
                                  Remove
                                </Button>
                              </div>
                            )}
                          </div>
                          <div className="w-full h-32 bg-white border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
                            {settings.general?.companyLogo ? (
                              <img 
                                src={settings.general.companyLogo} 
                                alt="Company Logo" 
                                className="max-h-28 max-w-full object-contain"
                              />
                            ) : (
                              <div className="text-center">
                                <div className="bg-[#0c4864] text-white px-3 py-2 rounded-lg font-bold text-lg mb-2">
                                  AE
                                </div>
                                <p className="text-sm text-gray-500">Default Logo</p>
                              </div>
                            )}
                          </div>
                        </div>
                        <div className="flex space-x-2">
                          <label className="cursor-pointer">
                            <input
                              type="file"
                              accept="image/*"
                              className="hidden"
                              onChange={(e) => {
                                const file = e.target.files[0];
                                if (file) {
                                  handleImageUpload(file, 'general', 'companyLogo');
                                }
                              }}
                            />
                            <Button size="sm" className="bg-[#0c4864]" asChild>
                              <span>
                                <Plus className="h-4 w-4 mr-1" />
                                Upload New Logo
                              </span>
                            </Button>
                          </label>
                        </div>
                      </div>

                      {/* Favicon */}
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Favicon</label>
                        <div className="border rounded-lg p-4 bg-gray-50">
                          <div className="flex items-center justify-between mb-3">
                            <p className="text-sm text-gray-600">
                              {settings.general?.favicon ? 'Current Favicon' : 'Using Default'}
                            </p>
                            {settings.general?.favicon && (
                              <Button 
                                size="sm" 
                                variant="destructive"
                                onClick={() => handleInputChange('general', 'favicon', null)}
                              >
                                Remove
                              </Button>
                            )}
                          </div>
                          <div className="w-16 h-16 bg-white border rounded-lg flex items-center justify-center">
                            {settings.general?.favicon ? (
                              <img 
                                src={settings.general.favicon} 
                                alt="Favicon" 
                                className="w-8 h-8 object-contain"
                              />
                            ) : (
                              <div className="bg-[#0c4864] text-white px-1 py-1 rounded text-xs font-bold">
                                AE
                              </div>
                            )}
                          </div>
                        </div>
                        <div className="flex space-x-2">
                          <label className="cursor-pointer">
                            <input
                              type="file"
                              accept="image/*"
                              className="hidden"
                              onChange={(e) => {
                                const file = e.target.files[0];
                                if (file) {
                                  handleImageUpload(file, 'general', 'favicon');
                                }
                              }}
                            />
                            <Button size="sm" variant="outline" asChild>
                              <span>
                                <Plus className="h-4 w-4 mr-1" />
                                Upload Favicon
                              </span>
                            </Button>
                          </label>
                        </div>
                      </div>
                    </div>

                    {/* Save Button */}
                    <div className="flex justify-end pt-4 border-t">
                      <Button 
                        className="bg-[#0c4864]"
                        onClick={() => handleSaveSettings('general')}
                        disabled={saving}
                      >
                        {saving ? (
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        ) : null}
                        Save General Settings
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="users" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>User Management</CardTitle>
                    <CardDescription>Manage system users and permissions</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <Input placeholder="Search users..." className="flex-1 mr-4" />
                      <Button className="bg-[#0c4864]">
                        <Plus className="h-4 w-4 mr-2" />
                        Add User
                      </Button>
                    </div>
                    <div className="space-y-2">
                      {[
                        { name: "System Administrator", email: "admin@afroexperts.com", role: "Admin", status: "Active" },
                        { name: "Business Manager", email: "manager@afroexperts.com", role: "Manager", status: "Active" },
                        { name: "Sales Cashier", email: "cashier@afroexperts.com", role: "Cashier", status: "Active" }
                      ].map((user, index) => (
                        <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                          <div>
                            <p className="font-medium">{user.name}</p>
                            <p className="text-sm text-gray-600">{user.email}</p>
                          </div>
                          <div className="flex items-center space-x-4">
                            <Badge variant="outline">{user.role}</Badge>
                            <Badge variant={user.status === 'Active' ? 'default' : 'secondary'}>
                              {user.status}
                            </Badge>
                            <Button variant="outline" size="sm">
                              Edit
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="media" className="space-y-6">
                {/* Media Library */}
                <Card>
                  <CardHeader>
                    <CardTitle>Media Library</CardTitle>
                    <CardDescription>Manage all website images and media files</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Upload Section */}
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <h4 className="font-medium text-lg">Upload New Media</h4>
                        <div className="flex space-x-2">
                          <Button size="sm" className="bg-[#0c4864]">
                            <Plus className="h-4 w-4 mr-1" />
                            Upload Files
                          </Button>
                          <Button size="sm" variant="outline">
                            <Download className="h-4 w-4 mr-1" />
                            Bulk Download
                          </Button>
                        </div>
                      </div>
                      
                      {/* Upload Zone */}
                      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer">
                        <div className="space-y-2">
                          <div className="flex justify-center">
                            <Plus className="h-12 w-12 text-gray-400" />
                          </div>
                          <p className="text-lg font-medium text-gray-600">Drop files here to upload</p>
                          <p className="text-sm text-gray-500">or click to browse your computer</p>
                          <p className="text-xs text-gray-400">Supported formats: JPG, PNG, GIF, SVG, MP4 (Max 10MB)</p>
                        </div>
                      </div>
                    </div>

                    {/* Media Gallery */}
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <h4 className="font-medium text-lg">Media Gallery</h4>
                        <div className="flex space-x-2">
                          <Select>
                            <SelectTrigger className="w-[150px]">
                              <SelectValue placeholder="Filter by type" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="all">All Files</SelectItem>
                              <SelectItem value="images">Images</SelectItem>
                              <SelectItem value="videos">Videos</SelectItem>
                              <SelectItem value="docs">Documents</SelectItem>
                            </SelectContent>
                          </Select>
                          <Input placeholder="Search media..." className="w-48" />
                        </div>
                      </div>

                      {/* Media Grid */}
                      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                        {[
                          { name: "hero-background.jpg", type: "image", size: "2.1 MB", date: "Jan 20, 2025" },
                          { name: "starlink-dish.jpg", type: "image", size: "1.8 MB", date: "Jan 19, 2025" },
                          { name: "network-setup.jpg", type: "image", size: "1.5 MB", date: "Jan 18, 2025" },
                          { name: "team-photo.jpg", type: "image", size: "3.2 MB", date: "Jan 17, 2025" },
                          { name: "office-building.jpg", type: "image", size: "2.7 MB", date: "Jan 16, 2025" },
                          { name: "client-logos.png", type: "image", size: "0.8 MB", date: "Jan 15, 2025" }
                        ].map((file, index) => (
                          <div key={index} className="border rounded-lg p-3 bg-white hover:shadow-md transition-shadow">
                            <div className="w-full h-24 bg-gray-200 rounded mb-2 flex items-center justify-center">
                              <p className="text-xs text-gray-500">{file.name.split('.')[0]}</p>
                            </div>
                            <div className="space-y-1">
                              <p className="text-xs font-medium truncate">{file.name}</p>
                              <p className="text-xs text-gray-500">{file.size} • {file.date}</p>
                            </div>
                            <div className="flex justify-between items-center mt-2">
                              <Button size="xs" variant="outline">
                                <Eye className="h-3 w-3 mr-1" />
                                View
                              </Button>
                              <div className="flex space-x-1">
                                <Button size="xs" variant="outline">Edit</Button>
                                <Button size="xs" variant="destructive">Delete</Button>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Image Optimization */}
                    <div className="space-y-4 border-t pt-6">
                      <h4 className="font-medium text-lg">Image Optimization</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Card>
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                              <p className="font-medium">Auto-optimization</p>
                              <input type="checkbox" defaultChecked />
                            </div>
                            <p className="text-sm text-gray-600">Automatically optimize images for web performance</p>
                          </CardContent>
                        </Card>
                        <Card>
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                              <p className="font-medium">WebP Conversion</p>
                              <input type="checkbox" defaultChecked />
                            </div>
                            <p className="text-sm text-gray-600">Convert images to WebP format for better compression</p>
                          </CardContent>
                        </Card>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="footer" className="space-y-6">
                {/* Footer Settings */}
                <Card>
                  <CardHeader>
                    <CardTitle>Footer Configuration</CardTitle>
                    <CardDescription>Manage footer content, links, and contact information</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Company Information */}
                    <div className="space-y-4">
                      <h4 className="font-medium text-lg">Company Information</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-medium">Company Description</label>
                          <textarea 
                            className="w-full mt-1 p-3 border rounded-lg min-h-[100px]"
                            defaultValue="Leading provider of IT services and Starlink internet solutions across Africa, connecting communities to the digital future."
                          />
                        </div>
                        <div className="space-y-4">
                          <div>
                            <label className="text-sm font-medium">Address</label>
                            <Input defaultValue="Kigali, Rwanda" className="mt-1" />
                          </div>
                          <div>
                            <label className="text-sm font-medium">Phone</label>
                            <Input defaultValue="+250 788 123 456" className="mt-1" />
                          </div>
                          <div>
                            <label className="text-sm font-medium">Email</label>
                            <Input defaultValue="info@afroexperts.com" className="mt-1" />
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Footer Links */}
                    <div className="space-y-4 border-t pt-6">
                      <h4 className="font-medium text-lg">Footer Navigation</h4>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Services Column */}
                        <div>
                          <label className="text-sm font-medium mb-3 block">Services</label>
                          <div className="space-y-2">
                            {[
                              "Starlink Installation",
                              "Network Setup", 
                              "CCTV Systems",
                              "Cloud Solutions",
                              "Technical Support"
                            ].map((service, index) => (
                              <div key={index} className="flex items-center justify-between">
                                <Input defaultValue={service} className="flex-1 mr-2" />
                                <Button size="sm" variant="destructive">×</Button>
                              </div>
                            ))}
                            <Button size="sm" variant="outline" className="w-full">
                              <Plus className="h-4 w-4 mr-1" />
                              Add Service
                            </Button>
                          </div>
                        </div>

                        {/* Quick Links Column */}
                        <div>
                          <label className="text-sm font-medium mb-3 block">Quick Links</label>
                          <div className="space-y-2">
                            {[
                              { text: "About Us", link: "/about" },
                              { text: "Contact", link: "/contact" },
                              { text: "Privacy Policy", link: "/privacy" },
                              { text: "Terms of Service", link: "/terms" }
                            ].map((item, index) => (
                              <div key={index} className="flex space-x-2">
                                <Input defaultValue={item.text} className="flex-1" />
                                <Input defaultValue={item.link} className="flex-1" placeholder="URL" />
                                <Button size="sm" variant="destructive">×</Button>
                              </div>
                            ))}
                            <Button size="sm" variant="outline" className="w-full">
                              <Plus className="h-4 w-4 mr-1" />
                              Add Link
                            </Button>
                          </div>
                        </div>

                        {/* Social Media Column */}
                        <div>
                          <label className="text-sm font-medium mb-3 block">Social Media</label>
                          <div className="space-y-2">
                            {[
                              { platform: "LinkedIn", url: "https://linkedin.com/company/afroexperts" },
                              { platform: "Twitter", url: "https://twitter.com/afroexperts" },
                              { platform: "Facebook", url: "https://facebook.com/afroexperts" },
                              { platform: "Instagram", url: "https://instagram.com/afroexperts" }
                            ].map((social, index) => (
                              <div key={index} className="flex space-x-2">
                                <Input defaultValue={social.platform} className="flex-1" />
                                <Input defaultValue={social.url} className="flex-1" placeholder="URL" />
                                <Button size="sm" variant="destructive">×</Button>
                              </div>
                            ))}
                            <Button size="sm" variant="outline" className="w-full">
                              <Plus className="h-4 w-4 mr-1" />
                              Add Social
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Copyright & Legal */}
                    <div className="space-y-4 border-t pt-6">
                      <h4 className="font-medium text-lg">Copyright & Legal</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm font-medium">Copyright Text</label>
                          <Input defaultValue="© 2025 Afro Experts. All rights reserved." className="mt-1" />
                        </div>
                        <div className="flex items-center space-x-2">
                          <input type="checkbox" id="show-dashboard-link" defaultChecked />
                          <label htmlFor="show-dashboard-link" className="text-sm">Show ERP Dashboard link</label>
                        </div>
                      </div>
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
      {/* Add Product Modal */}
      {showAddProductModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Add New Product</h3>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowAddProductModal(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <form onSubmit={handleAddProduct} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Product Name *</label>
                <Input
                  required
                  value={productForm.name}
                  onChange={(e) => setProductForm(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Enter product name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Category *</label>
                <Input
                  required
                  value={productForm.category}
                  onChange={(e) => setProductForm(prev => ({ ...prev, category: e.target.value }))}
                  placeholder="e.g., satellite_internet, network_hardware"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea
                  className="w-full p-2 border rounded-lg"
                  value={productForm.description}
                  onChange={(e) => setProductForm(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Product description"
                  rows="3"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Price (RWF) *</label>
                  <Input
                    required
                    type="number"
                    value={productForm.price}
                    onChange={(e) => setProductForm(prev => ({ ...prev, price: e.target.value }))}
                    placeholder="0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Cost Price (RWF)</label>
                  <Input
                    type="number"
                    value={productForm.cost_price}
                    onChange={(e) => setProductForm(prev => ({ ...prev, cost_price: e.target.value }))}
                    placeholder="0"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">SKU</label>
                  <Input
                    value={productForm.sku}
                    onChange={(e) => setProductForm(prev => ({ ...prev, sku: e.target.value }))}
                    placeholder="Product SKU"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Unit</label>
                  <select
                    className="w-full p-2 border rounded-lg"
                    value={productForm.unit}
                    onChange={(e) => setProductForm(prev => ({ ...prev, unit: e.target.value }))}
                  >
                    <option value="pieces">Pieces</option>
                    <option value="kg">Kilograms</option>
                    <option value="meters">Meters</option>
                    <option value="hours">Hours</option>
                    <option value="kit">Kit</option>
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Current Stock</label>
                  <Input
                    type="number"
                    value={productForm.current_stock}
                    onChange={(e) => setProductForm(prev => ({ ...prev, current_stock: e.target.value }))}
                    placeholder="0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Minimum Stock</label>
                  <Input
                    type="number"
                    value={productForm.minimum_stock}
                    onChange={(e) => setProductForm(prev => ({ ...prev, minimum_stock: e.target.value }))}
                    placeholder="0"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Location</label>
                <Input
                  value={productForm.location}
                  onChange={(e) => setProductForm(prev => ({ ...prev, location: e.target.value }))}
                  placeholder="e.g., Warehouse A"
                />
              </div>
              <div className="flex justify-end space-x-2 pt-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowAddProductModal(false)}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  className="bg-[#0c4864]"
                  disabled={formLoading}
                >
                  {formLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Adding...
                    </>
                  ) : (
                    <>
                      <Plus className="h-4 w-4 mr-2" />
                      Add Product
                    </>
                  )}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Client Modal */}
      {showAddClientModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Add New Client</h3>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowAddClientModal(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <form onSubmit={handleAddClient} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Client Name *</label>
                <Input
                  required
                  value={clientForm.name}
                  onChange={(e) => setClientForm(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Enter client name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <Input
                  type="email"
                  value={clientForm.email}
                  onChange={(e) => setClientForm(prev => ({ ...prev, email: e.target.value }))}
                  placeholder="client@example.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Phone</label>
                <Input
                  value={clientForm.phone}
                  onChange={(e) => setClientForm(prev => ({ ...prev, phone: e.target.value }))}
                  placeholder="+250 788 123 456"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Address</label>
                <textarea
                  className="w-full p-2 border rounded-lg"
                  value={clientForm.address}
                  onChange={(e) => setClientForm(prev => ({ ...prev, address: e.target.value }))}
                  placeholder="Client address"
                  rows="2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Client Type</label>
                <select
                  className="w-full p-2 border rounded-lg"
                  value={clientForm.client_type}
                  onChange={(e) => setClientForm(prev => ({ ...prev, client_type: e.target.value }))}
                >
                  <option value="individual">Individual</option>
                  <option value="business">Business</option>
                </select>
              </div>
              {clientForm.client_type === 'business' && (
                <>
                  <div>
                    <label className="block text-sm font-medium mb-1">Company Name</label>
                    <Input
                      value={clientForm.company_name}
                      onChange={(e) => setClientForm(prev => ({ ...prev, company_name: e.target.value }))}
                      placeholder="Company name"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Tax Number</label>
                    <Input
                      value={clientForm.tax_number}
                      onChange={(e) => setClientForm(prev => ({ ...prev, tax_number: e.target.value }))}
                      placeholder="Tax registration number"
                    />
                  </div>
                </>
              )}
              <div className="flex justify-end space-x-2 pt-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowAddClientModal(false)}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  className="bg-[#0c4864]"
                  disabled={formLoading}
                >
                  {formLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Adding...
                    </>
                  ) : (
                    <>
                      <Plus className="h-4 w-4 mr-2" />
                      Add Client
                    </>
                  )}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Order Modal */}
      {showAddOrderModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Create New Order</h3>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowAddOrderModal(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <form onSubmit={handleAddOrder} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Client *</label>
                <select
                  className="w-full p-2 border rounded-lg"
                  required
                  value={orderForm.client_id}
                  onChange={(e) => setOrderForm(prev => ({ ...prev, client_id: e.target.value }))}
                >
                  <option value="">Select a client...</option>
                  {dashboardData.clients.map((client) => (
                    <option key={client.id} value={client.id}>
                      {client.name} {client.company_name && `(${client.company_name})`}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Order Items</label>
                <div className="space-y-2 max-h-40 overflow-y-auto">
                  {orderForm.items.length === 0 ? (
                    <p className="text-gray-500 text-sm">No items added</p>
                  ) : (
                    orderForm.items.map((item, index) => (
                      <div key={index} className="flex justify-between items-center p-2 border rounded">
                        <span className="text-sm">{item.product_name} × {item.quantity}</span>
                        <Button
                          type="button"
                          size="sm"
                          variant="destructive"
                          onClick={() => {
                            const newItems = orderForm.items.filter((_, i) => i !== index);
                            setOrderForm(prev => ({ ...prev, items: newItems }));
                          }}
                        >
                          Remove
                        </Button>
                      </div>
                    ))
                  )}
                </div>
                
                <div className="flex space-x-2 mt-2">
                  <select
                    className="flex-1 p-2 border rounded"
                    onChange={(e) => {
                      const product = dashboardData.products.find(p => p.id === e.target.value);
                      if (product) {
                        const newItem = {
                          product_id: product.id,
                          product_name: product.name,
                          quantity: 1,
                          unit_price: product.price
                        };
                        setOrderForm(prev => ({ ...prev, items: [...prev.items, newItem] }));
                        e.target.value = '';
                      }
                    }}
                  >
                    <option value="">Add product...</option>
                    {dashboardData.products.map((product) => (
                      <option key={product.id} value={product.id}>
                        {product.name} - RWF {product.price.toLocaleString()}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Payment Method</label>
                <select
                  className="w-full p-2 border rounded-lg"
                  value={orderForm.payment_method}
                  onChange={(e) => setOrderForm(prev => ({ ...prev, payment_method: e.target.value }))}
                >
                  <option value="cash">Cash</option>
                  <option value="card">Card</option>
                  <option value="mobile_money">Mobile Money</option>
                  <option value="bank_transfer">Bank Transfer</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Notes</label>
                <textarea
                  className="w-full p-2 border rounded-lg"
                  value={orderForm.notes}
                  onChange={(e) => setOrderForm(prev => ({ ...prev, notes: e.target.value }))}
                  placeholder="Order notes..."
                  rows="2"
                />
              </div>
              
              <div className="flex justify-end space-x-2 pt-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowAddOrderModal(false)}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  className="bg-[#0c4864]"
                  disabled={formLoading || orderForm.items.length === 0}
                >
                  {formLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Creating...
                    </>
                  ) : (
                    <>
                      <Plus className="h-4 w-4 mr-2" />
                      Create Order
                    </>
                  )}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Inventory Movement Modal */}
      {showInventoryModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Record Inventory Movement</h3>
              <Button variant="ghost" size="icon" onClick={() => setShowInventoryModal(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            <form onSubmit={handleInventoryMovement} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Product *</label>
                <select
                  className="w-full p-2 border rounded-lg"
                  required
                  value={inventoryForm.product_id}
                  onChange={(e) => setInventoryForm(prev => ({ ...prev, product_id: e.target.value }))}
                >
                  <option value="">Select product...</option>
                  {dashboardData.products.map((product) => (
                    <option key={product.id} value={product.id}>
                      {product.name} (Stock: {product.current_stock})
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Movement Type *</label>
                <select
                  className="w-full p-2 border rounded-lg"
                  required
                  value={inventoryForm.movement_type}
                  onChange={(e) => setInventoryForm(prev => ({ ...prev, movement_type: e.target.value }))}
                >
                  <option value="stock_in">Stock In</option>
                  <option value="stock_out">Stock Out</option>
                  <option value="adjustment">Adjustment</option>
                  <option value="damaged">Damaged</option>
                  <option value="returned">Returned</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Quantity *</label>
                  <Input
                    type="number"
                    required
                    min="1"
                    value={inventoryForm.quantity}
                    onChange={(e) => setInventoryForm(prev => ({ ...prev, quantity: e.target.value }))}
                    placeholder="0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Unit Cost</label>
                  <Input
                    type="number"
                    value={inventoryForm.unit_cost}
                    onChange={(e) => setInventoryForm(prev => ({ ...prev, unit_cost: e.target.value }))}
                    placeholder="0"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Reference Number</label>
                <Input
                  value={inventoryForm.reference_number}
                  onChange={(e) => setInventoryForm(prev => ({ ...prev, reference_number: e.target.value }))}
                  placeholder="e.g., PO-123, INV-456"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Notes</label>
                <textarea
                  className="w-full p-2 border rounded-lg"
                  value={inventoryForm.notes}
                  onChange={(e) => setInventoryForm(prev => ({ ...prev, notes: e.target.value }))}
                  placeholder="Additional notes..."
                  rows="2"
                />
              </div>
              <div className="flex justify-end space-x-2 pt-4">
                <Button type="button" variant="outline" onClick={() => setShowInventoryModal(false)}>
                  Cancel
                </Button>
                <Button type="submit" className="bg-[#0c4864]" disabled={formLoading}>
                  {formLoading ? (
                    <><Loader2 className="h-4 w-4 mr-2 animate-spin" />Recording...</>
                  ) : (
                    <><Plus className="h-4 w-4 mr-2" />Record Movement</>
                  )}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Finance Transaction Modal */}
      {showFinanceModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Add Financial Transaction</h3>
              <Button variant="ghost" size="icon" onClick={() => setShowFinanceModal(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            <form onSubmit={handleAddFinanceTransaction} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Transaction Type *</label>
                <select
                  className="w-full p-2 border rounded-lg"
                  required
                  value={financeForm.transaction_type}
                  onChange={(e) => setFinanceForm(prev => ({ ...prev, transaction_type: e.target.value }))}
                >
                  <option value="income">Income</option>
                  <option value="expense">Expense</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Category *</label>
                <select
                  className="w-full p-2 border rounded-lg"
                  required
                  value={financeForm.category}
                  onChange={(e) => setFinanceForm(prev => ({ ...prev, category: e.target.value }))}
                >
                  <option value="">Select category...</option>
                  <option value="sales">Sales Revenue</option>
                  <option value="services">Service Revenue</option>
                  <option value="office_supplies">Office Supplies</option>
                  <option value="marketing">Marketing</option>
                  <option value="utilities">Utilities</option>
                  <option value="rent">Rent</option>
                  <option value="salaries">Salaries</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Amount (RWF) *</label>
                <Input
                  type="number"
                  required
                  min="0"
                  step="0.01"
                  value={financeForm.amount}
                  onChange={(e) => setFinanceForm(prev => ({ ...prev, amount: e.target.value }))}
                  placeholder="0.00"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Description *</label>
                <textarea
                  className="w-full p-2 border rounded-lg"
                  required
                  value={financeForm.description}
                  onChange={(e) => setFinanceForm(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Transaction description..."
                  rows="3"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Reference ID</label>
                <Input
                  value={financeForm.reference_id}
                  onChange={(e) => setFinanceForm(prev => ({ ...prev, reference_id: e.target.value }))}
                  placeholder="e.g., Invoice #123, Receipt #456"
                />
              </div>
              <div className="flex justify-end space-x-2 pt-4">
                <Button type="button" variant="outline" onClick={() => setShowFinanceModal(false)}>
                  Cancel
                </Button>
                <Button type="submit" className="bg-[#0c4864]" disabled={formLoading}>
                  {formLoading ? (
                    <><Loader2 className="h-4 w-4 mr-2 animate-spin" />Adding...</>
                  ) : (
                    <><Plus className="h-4 w-4 mr-2" />Add Transaction</>
                  )}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Service Booking Modal */}
      {showServiceBookingModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Book Service</h3>
              <Button variant="ghost" size="icon" onClick={() => setShowServiceBookingModal(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            <form onSubmit={handleAddServiceBooking} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Client Name *</label>
                <Input
                  required
                  value={serviceBookingForm.client_name}
                  onChange={(e) => setServiceBookingForm(prev => ({ ...prev, client_name: e.target.value }))}
                  placeholder="Enter client name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Client Phone *</label>
                <Input
                  required
                  value={serviceBookingForm.client_phone}
                  onChange={(e) => setServiceBookingForm(prev => ({ ...prev, client_phone: e.target.value }))}
                  placeholder="+250 788 123 456"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Client Email</label>
                <Input
                  type="email"
                  value={serviceBookingForm.client_email}
                  onChange={(e) => setServiceBookingForm(prev => ({ ...prev, client_email: e.target.value }))}
                  placeholder="client@example.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Service Type *</label>
                <select
                  className="w-full p-2 border rounded-lg"
                  required
                  value={serviceBookingForm.service_type}
                  onChange={(e) => setServiceBookingForm(prev => ({ ...prev, service_type: e.target.value }))}
                >
                  <option value="it_support">IT Support</option>
                  <option value="network_installation">Network Installation</option>
                  <option value="starlink_installation">Starlink Installation</option>
                  <option value="software_development">Software Development</option>
                  <option value="consultation">Consultation</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Location *</label>
                <Input
                  required
                  value={serviceBookingForm.location}
                  onChange={(e) => setServiceBookingForm(prev => ({ ...prev, location: e.target.value }))}
                  placeholder="Service location"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Preferred Date</label>
                <Input
                  type="datetime-local"
                  value={serviceBookingForm.preferred_date}
                  onChange={(e) => setServiceBookingForm(prev => ({ ...prev, preferred_date: e.target.value }))}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Description *</label>
                <textarea
                  className="w-full p-2 border rounded-lg"
                  required
                  value={serviceBookingForm.description}
                  onChange={(e) => setServiceBookingForm(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Describe the service needed..."
                  rows="3"
                />
              </div>
              <div className="flex justify-end space-x-2 pt-4">
                <Button type="button" variant="outline" onClick={() => setShowServiceBookingModal(false)}>
                  Cancel
                </Button>
                <Button type="submit" className="bg-[#0c4864]" disabled={formLoading}>
                  {formLoading ? (
                    <><Loader2 className="h-4 w-4 mr-2 animate-spin" />Booking...</>
                  ) : (
                    <><Plus className="h-4 w-4 mr-2" />Book Service</>
                  )}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

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