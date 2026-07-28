SHOW DATABASES;
USE tailorflow_db;

CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_no VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100),
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE measurement (
    measurement_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    garment_type VARCHAR(50) NOT NULL,
    measurement_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    chest DECIMAL(5,2),
    waist DECIMAL(5,2),
    shoulder DECIMAL(5,2),
    sleeve DECIMAL(5,2),
    length DECIMAL(5,2),

    notes TEXT,

    FOREIGN KEY (customer_id)
        REFERENCES customer(customer_id)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    delivery_date DATETIME NOT NULL,

    total_amount DECIMAL(10,2),

    current_status VARCHAR(30) NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES customer(customer_id)
);

CREATE TABLE order_item(
	item_id INT AUTO_INCREMENT PRIMARY KEY,
	order_id INT NOT NULL,
	measurement_id INT NOT NULL,

	product_name VARCHAR(30) NOT NULL,
	quantity INT NOT NULL,
	unit_price DECIMAL(10,2) NOT NULL,
	item_status VARCHAR(30) NOT NULL,
	special_instruction TEXT,

	FOREIGN KEY (order_id)
		REFERENCES orders (order_id),

	FOREIGN KEY (measurement_id)
		REFERENCES measurement (measurement_id)
);

CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT NOT NULL,

    amount DECIMAL(10,2) NOT NULL,

    payment_method VARCHAR(20) NOT NULL,

    payment_status VARCHAR(20) NOT NULL,

    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    transaction_id VARCHAR(100),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);

CREATE TABLE image (
    image_id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT NOT NULL,

    file_path VARCHAR(255) NOT NULL,

    image_type VARCHAR(30) NOT NULL,

    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);

SHOW TABLES;