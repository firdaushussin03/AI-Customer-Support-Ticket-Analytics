USE customer_support_analytics;


/* ============================================================
   1. EXECUTIVE OVERVIEW
   ============================================================ */

-- Overall ticket volume and unresolved workload.
SELECT
    COUNT(*) AS total_tickets,
    COUNT(DISTINCT ticket_id) AS unique_ticket_ids,
    SUM(
        CASE
            WHEN ticket_status IN ('Open', 'Pending Customer Response')
            THEN 1 ELSE 0
        END
    ) AS unresolved_tickets,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN ticket_status IN ('Open', 'Pending Customer Response')
                THEN 1 ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        1
    ) AS unresolved_percentage
FROM support_tickets;


-- Which ticket status is most common?
SELECT
    ticket_status,
    COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY ticket_status
ORDER BY total_tickets DESC;


-- Which issue types generate the most tickets?
SELECT
    ticket_type,
    COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY ticket_type
ORDER BY total_tickets DESC;


-- Which channel receives the most tickets?
SELECT
    ticket_channel,
    COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY ticket_channel
ORDER BY total_tickets DESC;


-- Which priority level has the most tickets?
SELECT
    ticket_priority,
    COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY ticket_priority
ORDER BY total_tickets DESC;


-- Which products generate the most tickets?
-- Ticket counts do not represent defect rates without sales/usage data.
SELECT
    product_purchased,
    COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY product_purchased
ORDER BY total_tickets DESC, product_purchased ASC;


/* ============================================================
   2. SUPPORT PERFORMANCE ANALYSIS
   ============================================================ */

-- Overall satisfaction and valid response-to-resolution time.
-- Missing or invalid ratings/durations are excluded, not scored as zero.
SELECT
    COUNT(
        CASE
            WHEN customer_satisfaction_rating BETWEEN 1 AND 5
            THEN 1
        END
    ) AS rated_tickets,
    ROUND(
        AVG(
            CASE
                WHEN customer_satisfaction_rating BETWEEN 1 AND 5
                THEN customer_satisfaction_rating
            END
        ),
        2
    ) AS average_satisfaction_out_of_5,
    COUNT(
        CASE
            WHEN resolution_hours >= 0
            THEN 1
        END
    ) AS valid_duration_tickets,
    ROUND(
        AVG(
            CASE
                WHEN resolution_hours >= 0
                THEN resolution_hours
            END
        ),
        2
    ) AS avg_response_to_resolution_hours
FROM support_tickets;


-- How does customer satisfaction vary by issue type?
SELECT
    ticket_type,
    COUNT(*) AS total_tickets,
    COUNT(
        CASE
            WHEN customer_satisfaction_rating BETWEEN 1 AND 5
            THEN 1
        END
    ) AS rated_tickets,
    ROUND(
        AVG(
            CASE
                WHEN customer_satisfaction_rating BETWEEN 1 AND 5
                THEN customer_satisfaction_rating
            END
        ),
        2
    ) AS average_satisfaction_out_of_5
FROM support_tickets
GROUP BY ticket_type
ORDER BY average_satisfaction_out_of_5 DESC, ticket_type ASC;


-- Which priority takes longest from first response to resolution?
SELECT
    ticket_priority,
    COUNT(*) AS valid_duration_tickets,
    ROUND(
        AVG(resolution_hours),
        2
    ) AS avg_response_to_resolution_hours
FROM support_tickets
WHERE resolution_hours >= 0
GROUP BY ticket_priority
ORDER BY
    avg_response_to_resolution_hours DESC,
    ticket_priority ASC;


-- Which five products have the highest average satisfaction?
-- Sort by the unrounded average to avoid rounding changing the ranking.
SELECT
    product_purchased,
    COUNT(*) AS rated_tickets,
    ROUND(
        AVG(customer_satisfaction_rating),
        2
    ) AS average_satisfaction_out_of_5
FROM support_tickets
WHERE customer_satisfaction_rating BETWEEN 1 AND 5
GROUP BY product_purchased
ORDER BY
    AVG(customer_satisfaction_rating) DESC,
    product_purchased ASC
LIMIT 5;


-- Product-level scatterplot:
-- response-to-resolution time vs customer satisfaction.
-- Each average uses its available valid records, so sample sizes may differ.
SELECT
    product_purchased,
    COUNT(*) AS total_tickets,
    COUNT(
        CASE
            WHEN resolution_hours >= 0
            THEN 1
        END
    ) AS valid_duration_tickets,
    ROUND(
        AVG(
            CASE
                WHEN resolution_hours >= 0
                THEN resolution_hours
            END
        ),
        4
    ) AS avg_response_to_resolution_hours,
    COUNT(
        CASE
            WHEN customer_satisfaction_rating BETWEEN 1 AND 5
            THEN 1
        END
    ) AS rated_tickets,
    ROUND(
        AVG(
            CASE
                WHEN customer_satisfaction_rating BETWEEN 1 AND 5
                THEN customer_satisfaction_rating
            END
        ),
        4
    ) AS average_satisfaction_out_of_5
FROM support_tickets
GROUP BY product_purchased
HAVING valid_duration_tickets > 0
   AND rated_tickets > 0
ORDER BY product_purchased ASC;


/* ============================================================
   3. AI RISK MONITORING
   ============================================================ */

-- High-risk KPI cards.
-- High-risk share uses unresolved tickets as the denominator.
SELECT
    SUM(
        CASE WHEN risk_level = 'High Risk'
            THEN 1 ELSE 0
        END
    ) AS high_risk_tickets,
    ROUND(
        100.0 * SUM(
            CASE WHEN risk_level = 'High Risk'
                THEN 1 ELSE 0
            END
        ) / NULLIF(
            SUM(
                CASE
                    WHEN ticket_status IN (
                        'Open',
                        'Pending Customer Response'
                    )
                    THEN 1 ELSE 0
                END
            ),
            0
        ),
        1
    ) AS high_risk_percentage_of_unresolved,
    SUM(
        CASE
            WHEN risk_level = 'High Risk'
             AND ticket_priority = 'Critical'
            THEN 1 ELSE 0
        END
    ) AS critical_high_risk_tickets,
    SUM(
        CASE
            WHEN risk_level = 'High Risk'
             AND ticket_status = 'Open'
            THEN 1 ELSE 0
        END
    ) AS open_high_risk_tickets
FROM support_tickets;


-- Which priorities have the most high-risk tickets?
SELECT
    ticket_priority,
    COUNT(*) AS high_risk_tickets
FROM support_tickets
WHERE risk_level = 'High Risk'
GROUP BY ticket_priority
ORDER BY high_risk_tickets DESC, ticket_priority ASC;


-- What is the overall customer sentiment?
SELECT
    sentiment_label,
    COUNT(*) AS total_tickets,
    ROUND(
        100.0 * COUNT(*) / NULLIF(
            (SELECT COUNT(*) FROM support_tickets),
            0
        ),
        2
    ) AS percentage_of_all_tickets
FROM support_tickets
GROUP BY sentiment_label
ORDER BY total_tickets DESC;


-- How are tickets distributed across risk levels?
SELECT
    risk_level,
    COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY risk_level
ORDER BY
    CASE risk_level
        WHEN 'High Risk' THEN 1
        WHEN 'Medium Risk' THEN 2
        WHEN 'Low Risk' THEN 3
        ELSE 4
    END;


-- High-risk review queue.
-- Prioritize Critical cases, then High cases, with ticket ID as a tie-breaker.
-- needs_alert indicates review eligibility, not notification delivery.
SELECT
    ticket_id,
    product_purchased,
    ticket_type,
    ticket_priority,
    ticket_status,
    ticket_channel,
    sentiment_label,
    ROUND(sentiment_score, 4) AS sentiment_score,
    risk_level,
    needs_alert
FROM support_tickets
WHERE needs_alert = 'Yes'
ORDER BY
    CASE ticket_priority
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
        ELSE 5
    END,
    ticket_id ASC;


-- Which products have the most negative-sentiment tickets?
-- Include the within-product percentage to provide volume context.
SELECT
    product_purchased,
    COUNT(*) AS total_tickets,
    SUM(
        CASE WHEN sentiment_label = 'Negative'
            THEN 1 ELSE 0
        END
    ) AS negative_tickets,
    ROUND(
        100.0 * SUM(
            CASE WHEN sentiment_label = 'Negative'
                THEN 1 ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS negative_percentage
FROM support_tickets
GROUP BY product_purchased
ORDER BY negative_tickets DESC, product_purchased ASC;


/* ============================================================
   4. DATA QUALITY CHECKS
   ============================================================ */

-- Duplicate ticket IDs: expected no rows.
SELECT
    ticket_id,
    COUNT(*) AS occurrences
FROM support_tickets
GROUP BY ticket_id
HAVING COUNT(*) > 1;


-- Missing IDs, invalid ratings, and remaining negative durations.
-- Expected: zero for all three checks.
SELECT
    SUM(
        CASE WHEN ticket_id IS NULL
            THEN 1 ELSE 0
        END
    ) AS missing_ticket_ids,
    SUM(
        CASE
            WHEN customer_satisfaction_rating IS NOT NULL
             AND customer_satisfaction_rating NOT BETWEEN 1 AND 5
            THEN 1 ELSE 0
        END
    ) AS invalid_ratings,
    SUM(
        CASE WHEN resolution_hours < 0
            THEN 1 ELSE 0
        END
    ) AS negative_durations_remaining
FROM support_tickets;


-- How many closed-ticket durations are flagged as invalid?
-- The original negative values were blanked during cleaning;
-- the flag preserves evidence of those invalid source durations.
SELECT
    COUNT(*) AS closed_tickets,
    SUM(
        CASE WHEN invalid_resolution_time = 1
            THEN 1 ELSE 0
        END
    ) AS invalid_duration_tickets,
    ROUND(
        100.0 * SUM(
            CASE WHEN invalid_resolution_time = 1
                THEN 1 ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        1
    ) AS invalid_duration_percentage_of_closed
FROM support_tickets
WHERE ticket_status = 'Closed';


-- Unknown or missing statuses/priorities: expected no rows.
SELECT
    ticket_id,
    ticket_status,
    ticket_priority
FROM support_tickets
WHERE ticket_status IS NULL
   OR ticket_status NOT IN (
       'Open',
       'Pending Customer Response',
       'Closed'
   )
   OR ticket_priority IS NULL
   OR ticket_priority NOT IN (
       'Critical',
       'High',
       'Medium',
       'Low'
   );


-- Alert flag inconsistencies: expected no rows.
-- MySQL's <=> operator compares values safely when NULL is present.
SELECT
    ticket_id,
    risk_level,
    needs_alert
FROM support_tickets
WHERE NOT (
    needs_alert <=> CASE
        WHEN risk_level = 'High Risk' THEN 'Yes'
        ELSE 'No'
    END
);