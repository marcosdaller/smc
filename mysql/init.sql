SET NAMES 'utf8mb4';

CREATE TABLE tenant (
    id   CHAR(36) PRIMARY KEY,     -- p.ej. "52f14cd4-c6f1-4fbd-8f87-4025e1d49242"
    name VARCHAR(200) NOT NULL     -- p.ej. "ChirpStack"
);

CREATE TABLE application (
    id         CHAR(36) PRIMARY KEY,   -- p.ej. "9c0f2a01-78e0-42f6-9db6-839137906b89"
    tenant_id  CHAR(36) NOT NULL,
    name       VARCHAR(200) NOT NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenant(id) ON DELETE CASCADE
);

CREATE TABLE device_profile (
    id         CHAR(36) PRIMARY KEY,   -- p.ej. "3701ff6e-5e6c-49ac-a996-08481fb1b938"
    tenant_id  CHAR(36) NOT NULL,
    name       VARCHAR(200) NOT NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenant(id) ON DELETE CASCADE
);

CREATE TABLE gateway (
    gateway_id   VARCHAR(32) PRIMARY KEY,  -- p.ej. "a84041ffff1fa2c0"
    tenant_id    CHAR(36),
    name         VARCHAR(200),
    FOREIGN KEY (tenant_id) REFERENCES tenant(id) ON DELETE CASCADE
);

CREATE TABLE device (
    dev_eui            VARCHAR(32) PRIMARY KEY,  -- p.ej. "1f8eef13eef89c5f"
    application_id     CHAR(36) NOT NULL,
    device_profile_id  CHAR(36) NOT NULL,
    name               VARCHAR(200) NOT NULL,  -- p.ej. "OTAA_node"
    device_class       VARCHAR(50),           -- p.ej. "CLASS_A"
    dev_addr           VARCHAR(32),
    FOREIGN KEY (application_id) REFERENCES application(id) ON DELETE CASCADE,
    FOREIGN KEY (device_profile_id) REFERENCES device_profile(id) ON DELETE CASCADE
);

CREATE TABLE device_variable (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    dev_eui   VARCHAR(32) NOT NULL,
    name      VARCHAR(100) NOT NULL,  -- nombre de la variable (ej: humidity, co2_ppm)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_dev_var (dev_eui, name),
    FOREIGN KEY (dev_eui) REFERENCES device(dev_eui) ON DELETE CASCADE
);

