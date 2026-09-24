# AI Customer Support Ticket Analytics & Risk Monitoring

A portfolio project using **Python, MySQL, SQL, VADER sentiment analysis, and Power BI** to analyze support workload, customer satisfaction, response-to-resolution time, and tickets requiring priority review.

The dataset contains **8,469 unique tickets**. A transparent rule identifies **791 high-risk tickets** for human review. This project does not predict escalation or send notifications.

## Objectives

- Compare ticket volume by issue type, status, priority, channel, and product.
- Analyze customer satisfaction and valid response-to-resolution durations.
- Use ticket-text sentiment alongside priority and status to identify review candidates.
- Present the findings in an interactive three-page Power BI report.

## Technology

| Tool | Purpose |
|---|---|
| Python and pandas | Data inspection, cleaning, and transformation |
| VADER | Lexicon- and rule-based sentiment scoring |
| MySQL | Storage of processed tickets |
| SQLAlchemy and PyMySQL | Database connection and primary-key upserts |
| SQL | Business analysis and data-quality checks |
| Power BI | Interactive reporting |

VADER is a rule-based NLP baseline. No predictive model is trained, and no large language model is used.

## Dataset

Source: [Customer Support Ticket Dataset on Kaggle](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset).

The raw CSV contains **8,469 rows and 17 columns**, including ticket ID, subject, description, product, priority, status, channel, customer information, timestamps, and satisfaction ratings. The AI-ready output contains **25 columns** after adding duration, age-group, sentiment, risk, and review-flag fields.

## Repository Structure

```text
AI-Customer-Support-Ticket-Analytics/
├── dashboard/
│   ├── Customer Support Ticket Analytics & AI Risk Monitoring Dashboard.pbix
│   ├── Executive Overview.png
│   ├── Support Performance Analysis.png
│   └── AI Risk Monitoring Dashboard.png
├── data/
│   ├── raw/customer_support_tickets.csv
│   └── processed/
│       ├── support_tickets_clean.csv
│       └── support_tickets_ai_ready.csv
├── images/
│   ├── Project Workflow.jpg
│   └── Automation Workflow Design.jpg
├── python/
│   ├── 01_data_understanding.py
│   ├── 02_clean_data.py
│   ├── 03_sentiment_and_risk.py
│   └── 04_import_to_mysql.py
├── sql/
│   ├── 01_create_database.sql
│   └── 02_analysis.sql
├── .gitignore
├── requirement.txt
└── README.md
```

## Processing Workflow

1. Inspect the source data.
2. Standardize column names, trim whitespace, and remove identical duplicate rows.
3. Validate unique positive ticket IDs and recognized status/priority values.
4. Parse timestamps, clean ages and ratings, and handle missing ticket text.
5. Calculate duration and age groups.
6. Score the combined ticket subject and description with VADER.
7. Assign risk levels and review flags.
8. Import the AI-ready CSV into MySQL and run SQL analysis.
9. Refresh Power BI using its configured data source.

The scripts retain tickets with invalid durations, blanking only the duration and preserving an invalid-duration flag. Missing satisfaction ratings are not converted to zero. Age 18 belongs to the 18–25 group.

Power BI can read the processed CSV directly. A CSV-connected report does not automatically read the MySQL table; MySQL provides a separate storage and SQL analysis layer.

## Sentiment and Risk Rules

| VADER compound score | Sentiment |
|---|---|
| At least 0.05 | Positive |
| At most -0.05 | Negative |
| Between -0.05 and 0.05 | Neutral |

Unresolved means **Open** or **Pending Customer Response**.

| Conditions | Risk level |
|---|---|
| Unresolved AND High/Critical priority AND Negative sentiment | High Risk |
| Unresolved AND either High/Critical priority OR Negative sentiment, excluding High Risk above | Medium Risk |
| Remaining cases | Low Risk |

`needs_alert` is `Yes` for High Risk tickets and `No` otherwise. It indicates eligibility for review, not notification delivery. The automation diagram is a proposed workflow.

## Dashboard Pages

### Executive Overview

Shows total tickets, unresolved tickets, high-risk tickets, average satisfaction, and volume by issue type, status, channel, and priority.

### Support Performance Analysis

Shows average response-to-resolution hours, valid duration count, average satisfaction, and rated ticket count. Charts compare duration by priority, the five highest-rated products, satisfaction by issue type, and product-average duration versus satisfaction.

### AI Risk Monitoring Dashboard

Shows high-risk count/share, Critical and Open high-risk counts, priority breakdowns, overall sentiment, and a high-risk review queue with Critical cases first.

All three pages include status, priority, channel, and product slicers. Clear-slicer buttons reset slicer selections on their respective pages.

## Verified Results

These values describe the complete dataset before report filtering.

| Metric | Result |
|---|---:|
| Total / unique tickets | 8,469 / 8,469 |
| Unresolved tickets | 5,700 |
| Unresolved share | 67.3% |
| High-risk tickets | 791 |
| High-risk share of unresolved tickets | 13.9% |
| Critical high-risk tickets | 399 |
| Open high-risk tickets | 401 |
| Average satisfaction | 2.99 / 5 |
| Rated tickets | 2,769 |
| Valid duration tickets | 1,404 |
| Average response-to-resolution hours | 7.58 |
| Invalid-duration tickets retained | 1,365 |

## Insights and Recommendations

### Unresolved Workload

There are **2,819 Open** and **2,881 Pending Customer Response** tickets, together representing **67.3%** of all tickets.

**Recommendation:** separate cases requiring support action from those awaiting customers. Historical snapshots and ticket-created timestamps would be needed to assess backlog growth or overdue work.

### Priority Review

The **791 high-risk tickets** include **399 Critical** and **392 High** priority cases. By status, **401 are Open** and **390 await customer responses**.

**Recommendation:** review Critical cases first and inspect their text before acting. Risk flags are business rules, not probabilities of escalation.

### Workload Distribution

Refund Request has **1,752 tickets**, narrowly ahead of Technical Issue with **1,747**. Channel volumes are also similar: Email **2,143**, Phone **2,132**, Social Media **2,121**, and Chat **2,073**.

**Recommendation:** do not recommend major staffing changes based on volume alone. Consider handling effort, capacity, and customer outcomes.

### Customer Satisfaction

Average satisfaction is **2.99/5** across **2,769 rated tickets**. The five highest-rated product averages are close together at approximately **3.20–3.22**.

**Recommendation:** show sample sizes alongside averages and investigate lower-rated issue types. Small average differences do not by themselves establish meaningful performance differences.

### Timestamp Quality

Of **2,769 closed tickets**, **1,365 (49.3%)** have resolution timestamps earlier than first response. The duration average uses only **1,404 valid records**.

**Recommendation:** investigate timestamp inconsistencies before using duration averages for service targets or performance evaluation.

## Metric Definitions and Limitations

### Response-to-Resolution Time

Calculated as resolution timestamp minus first-response timestamp. It does not measure the entire interval from ticket creation to resolution. Negative durations are excluded from averages while their tickets remain in the dataset.

### Satisfaction

The average uses available ratings from 1 to 5. Missing ratings are excluded. Rated tickets account for approximately **32.7%** of the dataset, so the mean does not represent a response from every customer.

### Scatterplot

Each dot represents one product. Duration and satisfaction averages may use different tickets because valid durations and ratings are not always available together. The chart supports exploratory comparison, not causal conclusions.

### High-Risk Share

Calculated as high-risk tickets divided by unresolved tickets, multiplied by 100. The denominator is not all tickets.

### Other Limitations

- Sentiment labels have not been validated against a manually reviewed sample.
- Ticket-text sentiment is not equivalent to a satisfaction rating.
- Purchase date is not a ticket-created timestamp and should not represent ticket arrivals.
- Product ticket counts are not defect rates without sales or usage denominators.
- Live monitoring and notification delivery are not implemented.
- Results describe the supplied dataset, not a measured business improvement.

## Run Locally

### Prerequisites

Python 3.10 or later, MySQL Server, a SQL client such as MySQL Workbench, and Power BI Desktop. Run terminal commands from the project root.

### 1. Prepare Python

Create the environment if it does not already exist:

```powershell
py -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirement.txt
```

Activation is optional because these commands call the environment's Python directly. MySQL and Power BI must be installed separately.

### 2. Process the Data

Ensure `data/raw/customer_support_tickets.csv` exists. Run each command separately, continuing only after success:

```powershell
.\.venv\Scripts\python.exe python/01_data_understanding.py
.\.venv\Scripts\python.exe python/02_clean_data.py
.\.venv\Scripts\python.exe python/03_sentiment_and_risk.py
```

The cleaning and sentiment scripts overwrite their generated CSV outputs. Expect **8,469 rows** in each processed file for the supplied dataset.

### 3. Set Up MySQL

Execute `sql/01_create_database.sql` in Workbench. It defines the `customer_support_analytics` database and a 25-column InnoDB table named `support_tickets`, with `ticket_id` as its primary key.

`CREATE TABLE IF NOT EXISTS` does not upgrade an existing table. An older table requires compatible columns and a primary key before import. A working database does not need to be deleted or rebuilt for subsequent imports.

### 4. Import Tickets

```powershell
.\.venv\Scripts\python.exe python/04_import_to_mysql.py
```

Enter the MySQL password at the hidden prompt. The current script uses `localhost:3306`, user `root`, and database `customer_support_analytics`. Edit those non-secret settings if your setup differs.

The importer reads `support_tickets_ai_ready.csv`, inserts new IDs, and updates matching IDs with CSV values, including missing values as SQL NULL. It retains database rows absent from the CSV and does not replace the table. It prints row counts before and after importing.

### 5. Analyze and Refresh

Execute `sql/02_analysis.sql` in Workbench.

Open the PBIX in `dashboard/`. Update its source location or connection settings for your computer while preserving the existing query/table name. For a CSV source, select `data/processed/support_tickets_ai_ready.csv`.

Choose **Home → Refresh**, clear slicers, and compare the report with the verified results above.

## Validation

Script output and SQL results confirmed 8,469 unique ticket IDs, no missing IDs, no invalid ratings, no remaining negative durations, no unknown statuses/priorities, and no mismatches between risk level and the review flag. The invalid-duration count is 1,365 and the valid-duration count is 1,404.

These checks were performed through Python output and SQL queries. The repository does not currently include an automated test suite.

## Future Improvements

- Validate sentiment with manually reviewed examples.
- Investigate timestamp inconsistencies at the source.
- Obtain ticket-created timestamps for backlog age and full-resolution analysis.
- Compare duration and satisfaction using tickets with both measurements.
- Add automated cleaning and risk-rule tests.
- If alerts are implemented, add duplicate prevention and delivery logging.
