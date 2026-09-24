CREATE DATABASE IF NOT EXISTS customer_support_analytics
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE customer_support_analytics;

CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id INT NOT NULL PRIMARY KEY,
    customer_name VARCHAR(255),
    customer_email VARCHAR(320),
    customer_age DOUBLE,
    customer_gender VARCHAR(50),
    product_purchased VARCHAR(255),
    date_of_purchase DATE,
    ticket_type VARCHAR(100),
    ticket_subject TEXT,
    ticket_description TEXT,
    ticket_status VARCHAR(100) NOT NULL,
    resolution TEXT,
    ticket_priority VARCHAR(50) NOT NULL,
    ticket_channel VARCHAR(100),
    first_response_time DATETIME,
    time_to_resolution DATETIME,
    customer_satisfaction_rating DOUBLE,
    resolution_hours DOUBLE,
    invalid_resolution_time BOOLEAN NOT NULL,
    age_group VARCHAR(20),
    ticket_text TEXT,
    sentiment_score DOUBLE,
    sentiment_label VARCHAR(20),
    risk_level VARCHAR(20),
    needs_alert VARCHAR(3)
) ENGINE=InnoDB;