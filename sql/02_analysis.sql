SELECT *
FROM support_tickets;

SELECT COUNT(*) AS total_tickets
FROM support_tickets;

SELECT ticket_status, COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY ticket_status
ORDER BY total_tickets;

SELECT ticket_priority, COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY ticket_priority
ORDER BY total_tickets;

SELECT ticket_channel, COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY ticket_channel
ORDER BY total_tickets;

SELECT ticket_type, COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY ticket_type
ORDER BY total_tickets DESC;

SELECT 
    ticket_type,
    ROUND(AVG(customer_satisfaction_rating), 2) AS avg_satisfaction
FROM support_tickets
WHERE customer_satisfaction_rating > 0
GROUP BY ticket_type
ORDER BY avg_satisfaction ASC;

SELECT 
    ticket_priority,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM support_tickets
WHERE resolution_hours IS NOT NULL
GROUP BY ticket_priority
ORDER BY avg_resolution_hours DESC;

SELECT 
    ticket_id,
    product_purchased,
    ticket_type,
    ticket_priority,
    ticket_status,
    sentiment_label,
    risk_level,
    needs_alert
FROM support_tickets
WHERE risk_level = 'High Risk';

SELECT product_purchased, COUNT(*) AS total_tickets 
FROM support_tickets
GROUP BY product_purchased
ORDER BY total_tickets DESC;

SELECT product_purchased, COUNT(*) AS negative_tickets
FROM support_tickets
WHERE sentiment_label = 'Negative'
GROUP BY product_purchased
ORDER BY negative_tickets DESC;