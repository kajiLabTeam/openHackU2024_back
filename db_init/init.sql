-- データベースの作成
CREATE DATABASE IF NOT EXISTS tomato_db;
USE tomato_db;

-- 一般ユーザーの作成
CREATE USER IF NOT EXISTS 'tomato'@'localhost' IDENTIFIED BY 'kaji2024';
GRANT ALL PRIVILEGES ON tomato_db.* TO 'tomato'@'localhost';
FLUSH PRIVILEGES;

-- テーブルの作成
CREATE TABLE IF NOT EXISTS group_tb (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP


);

CREATE TABLE IF NOT EXISTS user_tb (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    uuid VARCHAR(255) NOT NULL,
    song TEXT NOT NULL,
    group_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL
);