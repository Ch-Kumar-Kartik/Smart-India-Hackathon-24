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
    ->     no_of_tickets TINYINT UNSIGNED CHECK (no_of_tickets <= 10),
    ->     aadhar_id CHAR(12),
    ->     FOREIGN KEY (id) REFERENCES monuments(ID),
    ->     FOREIGN KEY (product_id) REFERENCES items(product_id)
    -> );
INSERT INTO monuments (NAME, CITY)
    -> VALUES
    ->     ('National Gallery of Modern Art', 'New Delhi'),
    ->     ('Salar Jung Museum', 'Hyderabad'),
    ->     ('Victoria Memorial Hall', 'Kolkata'),
    ->     ('Allahabad Museum', 'Prayagraj'),
    ->     ('National Museum', 'New Delhi'),
    ->     ('Indian Museum', 'Kolkata');
-- Insert data into the items table with different product_ids for adult and child

-- National Gallery of Modern Art (New Delhi)
INSERT INTO items (id, ticket_type, price)
VALUES 
    ((SELECT ID FROM monuments WHERE NAME = 'National Gallery of Modern Art'), 'adult', 20.00),
    ((SELECT ID FROM monuments WHERE NAME = 'National Gallery of Modern Art'), 'child', 20.00);

-- Salar Jung Museum (Hyderabad)
INSERT INTO items (id, ticket_type, price)
VALUES 
    ((SELECT ID FROM monuments WHERE NAME = 'Salar Jung Museum'), 'adult', 50.00),
    ((SELECT ID FROM monuments WHERE NAME = 'Salar Jung Museum'), 'child', 20.00);

-- Victoria Memorial Hall (Kolkata)
INSERT INTO items (id, ticket_type, price)
VALUES 
    ((SELECT ID FROM monuments WHERE NAME = 'Victoria Memorial Hall'), 'adult', 50.00),
    ((SELECT ID FROM monuments WHERE NAME = 'Victoria Memorial Hall'), 'child', 50.00);

-- Allahabad Museum (Prayagraj)
INSERT INTO items (id, ticket_type, price)
VALUES 
    ((SELECT ID FROM monuments WHERE NAME = 'Allahabad Museum'), 'adult', 50.00),
    ((SELECT ID FROM monuments WHERE NAME = 'Allahabad Museum'), 'child', 20.00);

-- National Museum (New Delhi)
INSERT INTO items (id, ticket_type, price)
VALUES 
    ((SELECT ID FROM monuments WHERE NAME = 'National Museum'), 'adult', 20.00),
    ((SELECT ID FROM monuments WHERE NAME = 'National Museum'), 'child', 20.00);

-- Indian Museum (Kolkata)
INSERT INTO items (id, ticket_type, price)
VALUES 
    ((SELECT ID FROM monuments WHERE NAME = 'Indian Museum'), 'adult', 75.00),
    ((SELECT ID FROM monuments WHERE NAME = 'Indian Museum'), 'child', 20.00);

 ALTER TABLE invoice
    -> ADD COLUMN phone_number VARCHAR(15) NOT NULL,
    -> ADD COLUMN email VARCHAR(255) NOT NULL;
ALTER TABLE invoice
    -> ADD CONSTRAINT chk_phone_number_length
    -> CHECK (CHAR_LENGTH(phone_number) = 10);
