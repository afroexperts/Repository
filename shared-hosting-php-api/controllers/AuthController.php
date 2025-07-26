<?php
require_once '../config/database.php';

class AuthController {
    private $db;
    private $secret_key;
    
    public function __construct() {
        $database = new Database();
        $this->db = $database->connect();
        $this->secret_key = 'your_jwt_secret_key_change_this_in_production'; // Change this!
    }
    
    public function login() {
        try {
            $input = json_decode(file_get_contents('php://input'), true);
            
            if (!$input || empty($input['email']) || empty($input['password'])) {
                http_response_code(400);
                echo json_encode(['error' => 'Email and password are required']);
                return;
            }
            
            $email = $input['email'];
            $password = $input['password'];
            
            // Get user from database
            $query = "SELECT id, full_name, email, password_hash, role, status 
                     FROM users 
                     WHERE email = :email AND status = 'active'";
            
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':email', $email);
            $stmt->execute();
            
            $user = $stmt->fetch();
            
            if (!$user || !verifyPassword($password, $user['password_hash'])) {
                http_response_code(401);
                echo json_encode(['error' => 'Invalid email or password']);
                return;
            }
            
            // Update last login
            $update_query = "UPDATE users SET last_login = NOW() WHERE id = :id";
            $update_stmt = $this->db->prepare($update_query);
            $update_stmt->bindParam(':id', $user['id']);
            $update_stmt->execute();
            
            // Generate simple token (for production, use proper JWT library)
            $token = $this->generateSimpleToken($user);
            
            // Remove password hash from response
            unset($user['password_hash']);
            
            echo json_encode([
                'message' => 'Login successful',
                'user' => $user,
                'token' => $token
            ]);
            
        } catch(Exception $e) {
            error_log("Login error: " . $e->getMessage());
            http_response_code(500);
            echo json_encode(['error' => 'Login failed']);
        }
    }
    
    public function getCurrentUser() {
        try {
            $headers = getallheaders();
            $token = null;
            
            // Get token from Authorization header
            if (isset($headers['Authorization'])) {
                $auth_header = $headers['Authorization'];
                if (preg_match('/Bearer\s+(.*)$/i', $auth_header, $matches)) {
                    $token = $matches[1];
                }
            }
            
            if (!$token) {
                http_response_code(401);
                echo json_encode(['error' => 'Authorization token required']);
                return;
            }
            
            $user_data = $this->validateSimpleToken($token);
            
            if (!$user_data) {
                http_response_code(401);
                echo json_encode(['error' => 'Invalid or expired token']);
                return;
            }
            
            // Get fresh user data from database
            $query = "SELECT id, full_name, email, role, status, last_login 
                     FROM users 
                     WHERE id = :id AND status = 'active'";
            
            $stmt = $this->db->prepare($query);
            $stmt->bindParam(':id', $user_data['user_id']);
            $stmt->execute();
            
            $user = $stmt->fetch();
            
            if (!$user) {
                http_response_code(401);
                echo json_encode(['error' => 'User not found']);
                return;
            }
            
            echo json_encode($user);
            
        } catch(Exception $e) {
            error_log("Get current user error: " . $e->getMessage());
            http_response_code(500);
            echo json_encode(['error' => 'Failed to get user information']);
        }
    }
    
    private function generateSimpleToken($user) {
        // Simple token format for shared hosting (use proper JWT library in production)
        $payload = [
            'user_id' => $user['id'],
            'email' => $user['email'],
            'role' => $user['role'],
            'exp' => time() + (24 * 60 * 60) // 24 hours
        ];
        
        $payload_encoded = base64_encode(json_encode($payload));
        $signature = hash_hmac('sha256', $payload_encoded, $this->secret_key);
        
        return $payload_encoded . '.' . $signature;
    }
    
    private function validateSimpleToken($token) {
        $parts = explode('.', $token);
        
        if (count($parts) !== 2) {
            return false;
        }
        
        $payload_encoded = $parts[0];
        $signature = $parts[1];
        
        // Verify signature
        $expected_signature = hash_hmac('sha256', $payload_encoded, $this->secret_key);
        
        if (!hash_equals($expected_signature, $signature)) {
            return false;
        }
        
        // Decode payload
        $payload = json_decode(base64_decode($payload_encoded), true);
        
        if (!$payload || !isset($payload['exp'])) {
            return false;
        }
        
        // Check expiration
        if (time() > $payload['exp']) {
            return false;
        }
        
        return $payload;
    }
    
    public function requireAuth() {
        $headers = getallheaders();
        $token = null;
        
        if (isset($headers['Authorization'])) {
            $auth_header = $headers['Authorization'];
            if (preg_match('/Bearer\s+(.*)$/i', $auth_header, $matches)) {
                $token = $matches[1];
            }
        }
        
        if (!$token) {
            http_response_code(401);
            echo json_encode(['error' => 'Authorization required']);
            exit();
        }
        
        $user_data = $this->validateSimpleToken($token);
        
        if (!$user_data) {
            http_response_code(401);
            echo json_encode(['error' => 'Invalid or expired token']);
            exit();
        }
        
        return $user_data;
    }
}
?>