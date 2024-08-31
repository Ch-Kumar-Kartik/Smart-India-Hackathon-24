CREATE DATABASE SIH;
USE SIH;
CREATE TABLE monuments (
    ->     ID INT AUTO_INCREMENT PRIMARY KEY,
    ->     NAME VARCHAR(255) NOT NULL,
    ->     CITY VARCHAR(255) NOT NULL
    -> );
CREATE TABLE items (
    ->     id INT,
    ->     product_id INT UNIQUE,
    ->     ticket_type ENUM('child', 'adult') NOT NULL,
    ->     price DECIMAL(4, 2) NOT NULL,
    ->     FOREIGN KEY (id) REFERENCES monuments(ID)
    -> );
CREATE TABLE invoice (
    ->     ticket_id INT PRIMARY KEY UNIQUE,
    ->     id INT,
    ->     product_id INT,
    ->     booking_date DATE NOT NULL,
    ->     visit_date DATE NOT NULL,
    ->     visit_time TIME NOT NULL,
    ->     no_of_tickets TINYINT UNSIGNED CHECK (no_of_tickets <= 10),
    ->     FOREIGN KEY (id) REFERENCES monuments(ID),
    ->     FOREIGN KEY (product_id) REFERENCES items(product_id)
    -> );
 ALTER TABLE invoice
    -> ADD COLUMN phone_number VARCHAR(15) NOT NULL,
    -> ADD COLUMN email VARCHAR(255) NOT NULL;
