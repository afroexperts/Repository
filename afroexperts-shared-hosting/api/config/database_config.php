<?php
// Update these with your CPanel database credentials
$db_config = [
    'host' => 'localhost',
    'username' => 'cpanel_username_dbname',  // Format: cpanelusername_dbname
    'password' => 'your_database_password',   // Your database password
    'database' => 'cpanel_username_afroexperts',  // Format: cpanelusername_afroexperts
    'charset' => 'utf8mb4'
];

// JWT Secret Key - CHANGE THIS!
$jwt_secret = 'your_super_secret_jwt_key_change_this_in_production';
?>
