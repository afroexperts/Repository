<?php
require_once '../config/database.php';

class ClientController {
    private $db;
    
    public function __construct() {
        $database = new Database();
        $this->db = $database->connect();
    }
    
    public function getShowcase() {
        try {
            $query = "SELECT 
                        id, 
                        name, 
                        company_name, 
                        logo, 
                        website_url, 
                        display_order 
                      FROM clients 
                      WHERE showcase_on_website = 1 
                        AND logo IS NOT NULL 
                        AND logo != '' 
                      ORDER BY display_order ASC, name ASC";
            
            $stmt = $this->db->prepare($query);
            $stmt->execute();
            
            $clients = $stmt->fetchAll(PDO::FETCH_ASSOC);
            
            // Convert display_order to integer
            foreach ($clients as &$client) {
                $client['display_order'] = (int)$client['display_order'];
            }
            
            echo json_encode($clients);
        } catch(Exception $e) {
            error_log("Client showcase error: " . $e->getMessage());
            http_response_code(500);
            echo json_encode(['error' => 'Failed to fetch client showcase']);
        }
    }
    
    public function getClients() {
        try {
            // Check for authentication (implement JWT validation here if needed)
            
            $query = "SELECT 
                        id,
                        name,
                        email,
                        phone,
                        company_name,
                        client_type,
                        credit_limit,
                        current_balance,
                        showcase_on_website,
                        display_order,
                        created_at
                      FROM clients 
                      ORDER BY name ASC";
            
            $stmt = $this->db->prepare($query);
            $stmt->execute();
            
            $clients = $stmt->fetchAll(PDO::FETCH_ASSOC);
            
            echo json_encode($clients);
        } catch(Exception $e) {
            error_log("Get clients error: " . $e->getMessage());
            http_response_code(500);
            echo json_encode(['error' => 'Failed to fetch clients']);
        }
    }
    
    public function createClient() {
        try {
            $input = json_decode(file_get_contents('php://input'), true);
            
            if (!$input) {
                http_response_code(400);
                echo json_encode(['error' => 'Invalid input data']);
                return;
            }
            
            // Validate required fields
            if (empty($input['name'])) {
                http_response_code(400);
                echo json_encode(['error' => 'Client name is required']);
                return;
            }
            
            $id = generateUUID();
            
            $query = "INSERT INTO clients (
                        id, name, email, phone, company_name, client_type,
                        credit_limit, current_balance, logo, website_url,
                        showcase_on_website, display_order, created_at
                      ) VALUES (
                        :id, :name, :email, :phone, :company_name, :client_type,
                        :credit_limit, :current_balance, :logo, :website_url,
                        :showcase_on_website, :display_order, NOW()
                      )";
            
            $stmt = $this->db->prepare($query);
            
            $stmt->bindParam(':id', $id);
            $stmt->bindParam(':name', $input['name']);
            $stmt->bindParam(':email', $input['email'] ?? null);
            $stmt->bindParam(':phone', $input['phone'] ?? null);
            $stmt->bindParam(':company_name', $input['company_name'] ?? null);
            $stmt->bindParam(':client_type', $input['client_type'] ?? 'individual');
            
            $credit_limit = $input['credit_limit'] ?? 0.0;
            $stmt->bindParam(':credit_limit', $credit_limit);
            
            $current_balance = 0.0;
            $stmt->bindParam(':current_balance', $current_balance);
            
            $stmt->bindParam(':logo', $input['logo'] ?? null);
            $stmt->bindParam(':website_url', $input['website_url'] ?? null);
            
            $showcase = $input['showcase_on_website'] ?? false;
            $stmt->bindParam(':showcase_on_website', $showcase, PDO::PARAM_BOOL);
            
            $display_order = $input['display_order'] ?? 0;
            $stmt->bindParam(':display_order', $display_order);
            
            $stmt->execute();
            
            echo json_encode([
                'success' => true,
                'message' => 'Client created successfully',
                'id' => $id
            ]);
            
        } catch(Exception $e) {
            error_log("Create client error: " . $e->getMessage());
            http_response_code(500);
            echo json_encode(['error' => 'Failed to create client']);
        }
    }
    
    public function toggleShowcase($client_id) {
        try {
            // Get current showcase status
            $query = "SELECT showcase_on_website FROM clients WHERE id = :id";
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':id', $client_id);
            $stmt->execute();
            
            $client = $stmt->fetch();
            if (!$client) {
                http_response_code(404);
                echo json_encode(['error' => 'Client not found']);
                return;
            }
            
            $new_status = !$client['showcase_on_website'];
            
            // Update showcase status
            $update_query = "UPDATE clients 
                           SET showcase_on_website = :status, 
                               updated_at = NOW() 
                           WHERE id = :id";
            
            $update_stmt = $this->db->prepare($update_query);
            $update_stmt->bindParam(':status', $new_status, PDO::PARAM_BOOL);
            $update_stmt->bindParam(':id', $client_id);
            $update_stmt->execute();
            
            echo json_encode([
                'success' => true,
                'message' => 'Client showcase ' . ($new_status ? 'enabled' : 'disabled'),
                'showcase_enabled' => $new_status
            ]);
            
        } catch(Exception $e) {
            error_log("Toggle showcase error: " . $e->getMessage());
            http_response_code(500);
            echo json_encode(['error' => 'Failed to toggle client showcase']);
        }
    }
}
?>