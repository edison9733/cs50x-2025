-- Create Users table for authentication
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Categories table for transaction classification
CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Create Transactions table linked to Users and Categories
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type VARCHAR(10) NOT NULL CHECK (type IN ('input', 'output')),
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    balance_after DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- Create Investments/Growth table linked to Users
CREATE TABLE Investments (
    investment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('investment', 'growth')),
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
