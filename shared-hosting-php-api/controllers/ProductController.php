<?php
require_once '../config/database.php';

class ProductController {
    private $db;
    
    public function __construct() {
        $database = new Database();
        $this->db = $database->connect();
    }
    
    public function getProducts() {
        try {
            // Basic authentication check (implement proper auth validation)
            $this->requireBasicAuth();
            
            $limit = isset($_GET['limit']) ? (int)$_GET['limit'] : 100;
            $offset = isset($_GET['offset']) ? (int)$_GET['offset'] : 0;
            $category = isset($_GET['category']) ? $_GET['category'] : null;
            
            $query = "SELECT 
                        id,
                        name,
                        category,
                        description,
                        price,
                        cost_price,
                        sku,
                        unit,
                        minimum_stock,
                        current_stock,
                        location,
                        created_at
                      FROM products";
            
            $params = [];
            
            if ($category) {
                $query .= " WHERE category = :category";
                $params[':category'] = $category;
            }
            
            $query .= " ORDER BY name ASC LIMIT :limit OFFSET :offset";
            
            $stmt = $this->db->prepare($query);
            
            foreach ($params as $key => $value) {
                $stmt->bindValue($key, $value);
            }
            
            $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
            $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
            
            $stmt->execute();
            
            $products = $stmt->fetchAll(PDO::FETCH_ASSOC);
            
            // Convert numeric fields
            foreach ($products as &$product) {
                $product['price'] = (float)$product['price'];
                $product['cost_price'] = (float)$product['cost_price'];
                $product['minimum_stock'] = (int)$product['minimum_stock'];
                $product['current_stock'] = (int)$product['current_stock'];
            }
            
            echo json_encode($products);
            
        } catch(Exception $e) {
            error_log("Get products error: " . $e->getMessage());
            http_response_code(500);
            echo json_encode(['error' => 'Failed to fetch products']);
        }
    }
    
    public function getLowStockProducts() {
        try {
            $this->requireBasicAuth();
            
            $query = "SELECT 
                        id,
                        name,
                        category,
                        current_stock,
                        minimum_stock,
                        unit
                      FROM products 
                      WHERE current_stock <= minimum_stock 
                      ORDER BY (current_stock - minimum_stock) ASC";
            
            $stmt = $this->db->prepare($query);
            $stmt->execute();
            
            $products = $stmt->fetchAll(PDO::FETCH_ASSOC);
            
            foreach ($products as &$product) {
                $product['current_stock'] = (int)$product['current_stock'];
                $product['minimum_stock'] = (int)$product['minimum_stock'];
                $product['stock_deficit'] = $product['minimum_stock'] - $product['current_stock'];
            }
            
            echo json_encode($products);
            
        } catch(Exception $e) {
            error_log("Get low stock products error: " . $e->getMessage());
            http_response_code(500);
            echo json_encode(['error' => 'Failed to fetch low stock products']);
        }
    }
    
    public function createProduct() {
        try {
            $this->requireBasicAuth();
            
            $input = json_decode(file_get_contents('php://input'), true);
            
            if (!$input || empty($input['name']) || empty($input['price'])) {
                http_response_code(400);
                echo json_encode(['error' => 'Product name and price are required']);
                return;
            }
            
            $id = generateUUID();
            
            // Generate SKU if not provided
            $sku = $input['sku'] ?? 'AE' . rand(10000, 99999);
            
            $query = "INSERT INTO products (
                        id, name, category, description, price, cost_price,
                        sku, unit, minimum_stock, current_stock, location, created_at
                      ) VALUES (
                        :id, :name, :category, :description, :price, :cost_price,
                        :sku, :unit, :minimum_stock, :current_stock, :location, NOW()
                      )";
            
            $stmt = $this->db->prepare($query);
            
            $stmt->bindParam(':id', $id);
            $stmt->bindParam(':name', $input['name']);
            $stmt->bindParam(':category', $input['category'] ?? 'general');
            $stmt->bindParam(':description', $input['description'] ?? null);
            
            $price = (float)$input['price'];
            $stmt->bindParam(':price', $price);
            
            $cost_price = isset($input['cost_price']) ? (float)$input['cost_price'] : 0.0;
            $stmt->bindParam(':cost_price', $cost_price);
            
            $stmt->bindParam(':sku', $sku);
            $stmt->bindParam(':unit', $input['unit'] ?? 'pieces');
            
            $minimum_stock = isset($input['minimum_stock']) ? (int)$input['minimum_stock'] : 0;
            $stmt->bindParam(':minimum_stock', $minimum_stock);
            
            $current_stock = isset($input['current_stock']) ? (int)$input['current_stock'] : 0;
            $stmt->bindParam(':current_stock', $current_stock);
            
            $stmt->bindParam(':location', $input['location'] ?? null);
            
            $stmt->execute();
            
            echo json_encode([
                'success' => true,
                'message' => 'Product created successfully',
                'id' => $id,
                'sku' => $sku
            ]);
            
        } catch(Exception $e) {
            error_log("Create product error: " . $e->getMessage());
            http_response_code(500);
            echo json_encode(['error' => 'Failed to create product']);
        }
    }
    
    public function updateStock($product_id, $new_stock) {
        try {
            $this->requireBasicAuth();
            
            $query = "UPDATE products 
                     SET current_stock = :stock, updated_at = NOW() 
                     WHERE id = :id";
            
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':stock', $new_stock, PDO::PARAM_INT);
            $stmt->bindParam(':id', $product_id);
            
            $success = $stmt->execute();
            
            if ($stmt->rowCount() === 0) {
                http_response_code(404);
                echo json_encode(['error' => 'Product not found']);
                return;
            }
            
            echo json_encode([
                'success' => true,
                'message' => 'Stock updated successfully'
            ]);
            
        } catch(Exception $e) {
            error_log("Update stock error: " . $e->getMessage());
            http_response_code(500);
            echo json_encode(['error' => 'Failed to update stock']);
        }
    }
    
    private function requireBasicAuth() {
        // Simple authentication check - implement proper JWT validation here
        $headers = getallheaders();
        if (!isset($headers['Authorization'])) {
            http_response_code(401);
            echo json_encode(['error' => 'Authorization required']);
            exit();
        }
        // Add proper token validation here
    }
}
?>