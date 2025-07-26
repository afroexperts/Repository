<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

require_once 'config/database.php';

// Simple routing
$request_uri = $_SERVER['REQUEST_URI'];
$path = parse_url($request_uri, PHP_URL_PATH);
$path = str_replace('/api', '', $path);
$method = $_SERVER['REQUEST_METHOD'];

// Route handling
switch (true) {
    case $path === '/' && $method === 'GET':
        echo json_encode([
            'message' => 'Afro Experts API is running', 
            'timestamp' => date('c'),
            'version' => '1.0.0'
        ]);
        break;
        
    case preg_match('/^\/clients\/showcase$/', $path) && $method === 'GET':
        require_once 'controllers/ClientController.php';
        $controller = new ClientController();
        $controller->getShowcase();
        break;
        
    case preg_match('/^\/auth\/login$/', $path) && $method === 'POST':
        require_once 'controllers/AuthController.php';
        $controller = new AuthController();
        $controller->login();
        break;
        
    case preg_match('/^\/auth\/me$/', $path) && $method === 'GET':
        require_once 'controllers/AuthController.php';
        $controller = new AuthController();
        $controller->getCurrentUser();
        break;
        
    case preg_match('/^\/products$/', $path) && $method === 'GET':
        require_once 'controllers/ProductController.php';
        $controller = new ProductController();
        $controller->getProducts();
        break;
        
    case preg_match('/^\/products$/', $path) && $method === 'POST':
        require_once 'controllers/ProductController.php';
        $controller = new ProductController();
        $controller->createProduct();
        break;
        
    case preg_match('/^\/stats\/impact$/', $path) && $method === 'GET':
        echo json_encode([
            'communities_connected' => 50,
            'businesses_served' => 1000,
            'people_online' => 10000,
            'countries_active' => 2,
            'last_updated' => date('c')
        ]);
        break;
        
    case preg_match('/^\/dashboard\/stats$/', $path) && $method === 'GET':
        require_once 'controllers/DashboardController.php';
        $controller = new DashboardController();
        $controller->getStats();
        break;
        
    default:
        http_response_code(404);
        echo json_encode(['error' => 'Endpoint not found', 'path' => $path, 'method' => $method]);
        break;
}
?>