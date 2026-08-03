CREATE DATABASE customer_support_analytics;

USE customer_support_analytics;

CREATE TABLE support_tickets (
    ticket_id INT,
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    customer_age INT,
    customer_gender VARCHAR(50),
    product_purchased VARCHAR(255),
    date_of_purchase DATE,
    ticket_type VARCHAR(100),
    ticket_subject TEXT,
    ticket_description TEXT,
    ticket_status VARCHAR(100),
    resolution TEXT,
    ticket_priority VARCHAR(50),
    ticket_channel VARCHAR(100),
    first_response_time DATETIME,
    time_to_resolution DATETIME,
    customer_satisfaction_rating DECIMAL(3,1),
    resolution_hours DECIMAL(10,2),
    age_group VARCHAR(50),
    ticket_text TEXT,
    sentiment_score DECIMAL(10,4),
    sentiment_label VARCHAR(50),
    risk_level VARCHAR(50),
    needs_alert VARCHAR(10)
);