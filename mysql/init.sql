SET NAMES 'utf8mb4';

CREATE TABLE tenant (
    id   CHAR(36) PRIMARY KEY,    
    name VARCHAR(200) NOT NULL    
);

CREATE TABLE application (
    id         CHAR(36) PRIMARY KEY,   
    tenant_id  CHAR(36) NOT NULL,
    name       VARCHAR(200) NOT NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenant(id) ON DELETE CASCADE
);

CREATE TABLE device_profile (
    id         CHAR(36) PRIMARY KEY,   
    tenant_id  CHAR(36) NOT NULL,
    name       VARCHAR(200) NOT NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenant(id) ON DELETE CASCADE
);

CREATE TABLE gateway (
    gateway_id   VARCHAR(32) PRIMARY KEY,  
    tenant_id    CHAR(36),
    name         VARCHAR(200),
    FOREIGN KEY (tenant_id) REFERENCES tenant(id) ON DELETE CASCADE
);

CREATE TABLE device (
    dev_eui            VARCHAR(32) PRIMARY KEY,  
    application_id     CHAR(36) NOT NULL,
    device_profile_id  CHAR(36) NOT NULL,
    name               VARCHAR(200) NOT NULL,  
    device_class       VARCHAR(50),           
    dev_addr           VARCHAR(32),
    FOREIGN KEY (application_id) REFERENCES application(id) ON DELETE CASCADE,
    FOREIGN KEY (device_profile_id) REFERENCES device_profile(id) ON DELETE CASCADE
);

CREATE TABLE device_variable (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    dev_eui   VARCHAR(32) NOT NULL,
    name      VARCHAR(100) NOT NULL,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_dev_var (dev_eui, name),
    FOREIGN KEY (dev_eui) REFERENCES device(dev_eui) ON DELETE CASCADE
);

