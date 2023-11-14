-- Apaga o banco de daods caso ele já exista.
DROP DATABASE IF EXISTS db_items;

-- Criar o banco de dados com atenção à tabela dde caracteres.
CREATE DATABASE db_items 
	CHARACTER SET utf8mb4 
    COLLATE utf8mb4_general_ci;
    
    -- Selecionar o banco de dados.
USE db_items;

-- Cria a tebela 'user' conforme o modelo
CREATE TABLE user (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_name VARCHAR(127) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_password VARCHAR(63) NOT NULL,
    user_birth DATE,
    user_status ENUM('on', 'off') DEFAULT 'on'
);

-- Inserir dados em 'user'.
INSERT INTO user (user_name, user_email, user_password, user_birth) VALUE
('Gab7', 'gabx7@gmail.com', '157', '2005/09/02'), 
('jorge alex', 'jorgealex@gmail.com', '155', '2000/05/09'),
('leticya moraes', 'lety@gmail.com', '159', '2005/05/09');

-- Lista a inserção em 'user'.
SELECT * FROM user WHERE user_status = 'on';

-- Apagar o 'Joca'.
UPDATE user SET user_status = 'off' WHERE user_id = '1';