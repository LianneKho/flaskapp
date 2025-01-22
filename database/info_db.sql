-- Maak een nieuwe database
CREATE DATABASE onboarding_db;

-- Gebruik de database
USE onboarding_db;

-- Maak een tabel voor gebruikers
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Voeg voorbeelddata toe aan de tabel
INSERT INTO users (username, email, password_hash) 
VALUES ('john_doe', 'john@example.com', 'hashed_password_123');