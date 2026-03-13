CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),

    avatar VARCHAR(255),

    role ENUM('CUSTOMER','ADMIN','STAFF') DEFAULT 'CUSTOMER',

    status ENUM('ACTIVE','INACTIVE','BANNED') DEFAULT 'ACTIVE',

    email_verified BOOLEAN DEFAULT FALSE,

    last_login DATETIME,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_addresses (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
	address_id BIGINT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (address_id) References address(id)
);




create table address (
	id BIGINT PRIMARY KEY auto_increment,
	
    recipient_name VARCHAR(100),
    phone VARCHAR(20),

    province VARCHAR(100),
    district VARCHAR(100),
    ward VARCHAR(100),
    street VARCHAR(255),

    is_default BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

)