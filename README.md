# AI Customer Support Ticket Analytics & Risk Monitoring

A portfolio project using **Python, MySQL, SQL, VADER sentiment analysis, and Power BI** to analyze customer support workload, satisfaction, response-to-resolution time, and tickets requiring priority review.

The project analyzes **8,469 unique tickets** and identifies **791 high-risk tickets** using transparent business rules.

## Project Objectives

- Understand ticket volume across issue types, channels, priorities, and statuses.
- Compare customer satisfaction across products and issue types.
- Analyze elapsed time from first response to resolution.
- Use ticket-text sentiment to support rule-based risk classification.
- Present findings in an interactive, three-page Power BI report.

## Technology Stack

| Tool | Purpose |
|---|---|
| Python | Data preparation and processing |
| pandas | Data cleaning, transformation, and CSV handling |
| VADER | Sentiment analysis of ticket text |
| MySQL | Storage of processed ticket data |
| SQLAlchemy and PyMySQL | Database connection and ticket upserts |
| SQL | Business analysis and data-quality checks |
| Power BI | Interactive reporting and visualization |

VADER is a lexicon- and rule-based sentiment tool. This project does not train a predictive model or use a large language model.

## Dataset

Source: [Customer Support Ticket Dataset on Kaggle](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)

The raw dataset contains **8,469 rows and 17 columns**, including:

- Ticket ID, subject, and description
- Product purchased
- Ticket type, status, priority, and channel
- First-response and resolution timestamps
- Customer satisfaction rating
- Customer demographic and purchase information

The final AI-ready dataset contains **25 columns**, including derived duration, sentiment, risk, and review-flag fields.

## Repository Structure

```text
AI-Customer-Support-Ticket-Analytics/
├── dashboard/
│   ├── Customer Support Ticket Analytics & AI Risk Monitoring Dashboard.pbix
│   ├── Executive Overview.png
│   ├── Support Performance Analysis.png
│   └── AI Risk Monitoring Dashboard.png
├── data/
│   ├── raw/
│   │   └── customer_support_tickets.csv
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
└── README.md
```

## Workflow

1. Inspect the raw dataset.
2. Clean and validate ticket data.
3. Calculate response-to-resolution durations and age groups.
4. Score ticket text using VADER.
5. Assign risk levels and review flags.
6. Import the AI-ready CSV into MySQL.
7. Run SQL analysis and validation queries.
8. Refresh and explore the Power BI report.

Power BI can read the processed CSV directly. MySQL provides a separate storage and SQL analysis layer; a CSV-connected report does not automatically read from MySQL.

## Data Cleaning

The cleaning script:

- Standardizes column names and categorical values.
- Removes leading and trailing whitespace.
- Removes identical duplicate rows.
- Rejects missing, invalid, or conflicting duplicate ticket IDs.
- Validates ticket status and priority values.
- Converts date and timestamp columns.
- Replaces missing or invalid ages with the median valid age.
- Preserves missing satisfaction ratings and excludes ratings outside 1–5.
- Handles missing ticket-text values.
- Creates age groups with corrected boundaries.
- Flags invalid durations without deleting the affected tickets.

### Handling Invalid Durations

Some records have resolution timestamps earlier than their first-response timestamps.

These tickets remain in the dataset. Their `resolution_hours` values are set to missing, and `invalid_resolution_time` is set to True.

This preserves ticket counts while excluding invalid durations from time-based averages.

## Sentiment and Risk Classification

### Sentiment Analysis

VADER analyzes the combined ticket subject and description.

| Compound Score | Sentiment |
|---|---|
| At least 0.05 | Positive |
| At most -0.05 | Negative |
| Between -0.05 and 0.05 | Neutral |

Sentiment represents the tone of ticket text. It is not the same measurement as a customer satisfaction rating.

### Risk Rules

Unresolved tickets are those with status **Open** or **Pending Customer Response**.

| Conditions | Risk Level |
|---|---|
| Unresolved AND High/Critical priority AND Negative sentiment | High Risk |
| Unresolved AND either High/Critical priority OR Negative sentiment, excluding High Risk cases | Medium Risk |
| Remaining cases | Low Risk |

`needs_alert` is set to `Yes` for High Risk tickets and `No` otherwise.

This flag identifies tickets for human review. It does not mean a notification was sent. The automation diagram represents a proposed workflow; notification delivery is not implemented.

## Power BI Dashboard

### Executive Overview

Answers questions about overall workload:

- How many tickets are unresolved?
- Which issue types generate the most tickets?
- Which ticket status is most common?
- Which channel receives the most tickets?
- Which priority level has the most tickets?

Key cards show total tickets, unresolved tickets, high-risk tickets, and average satisfaction.

### Support Performance Analysis

Examines customer ratings and usable duration records:

- Response-to-resolution time versus customer satisfaction
- Average response-to-resolution time by priority
- Top five products by average satisfaction
- Satisfaction and rating counts by issue type

Key cards show average duration, average satisfaction, valid duration tickets, and rated tickets.

### AI Risk Monitoring Dashboard

Supports review of tickets meeting the high-risk rule:

- High-risk tickets and their share of unresolved tickets
- Critical high-risk tickets
- Open high-risk tickets
- High-risk tickets by priority
- Overall ticket sentiment
- A review queue prioritizing Critical tickets

Each page includes status, priority, channel, and product slicers.

## Verified Results

These results describe the complete dataset before dashboard filtering.

| Metric | Result |
|---|---:|
| Total tickets | 8,469 |
| Unique ticket IDs | 8,469 |
| Unresolved tickets | 5,700 |
| Unresolved share | 67.3% |
| High-risk tickets | 791 |
| High-risk share of unresolved tickets | 13.9% |
| Critical high-risk tickets | 399 |
| Open high-risk tickets | 401 |
| Average satisfaction | 2.99 / 5 |
| Rated tickets | 2,769 |
| Valid duration tickets | 1,404 |
| Average response-to-resolution time | 7.58 hours |
| Invalid-duration tickets retained | 1,365 |

## Insights and Recommendations

### 1. Unresolved Tickets Form Most of the Dataset

There are **5,700 unresolved tickets**, comprising:

- **2,819 Open**
- **2,881 Pending Customer Response**

Together, they represent **67.3%** of all tickets.

**Recommendation:** distinguish tickets requiring support action from those awaiting a customer reply. Ticket age and historical snapshots would be needed to determine whether the backlog is overdue or growing.

### 2. The Risk Rule Identifies a Focused Review Queue

The **791 high-risk tickets** include:

- **399 Critical** and **392 High** priority tickets
- **401 Open** and **390 Pending Customer Response** tickets

**Recommendation:** review Critical cases first and inspect the underlying ticket text before taking action. The rule supports prioritization; it does not predict escalation.

### 3. Workload Is Fairly Evenly Distributed

Refund Request has **1,752 tickets**, narrowly ahead of Technical Issue with **1,747**.

Channel volumes are also similar:

| Channel | Tickets |
|---|---:|
| Email | 2,143 |
| Phone | 2,132 |
| Social Media | 2,121 |
| Chat | 2,073 |

**Recommendation:** avoid major staffing changes based on volume alone. Include handling effort, staffing capacity, and customer outcomes in further analysis.

### 4. Satisfaction Is Close to the Middle of the Scale

Average satisfaction is **2.99/5** across **2,769 rated tickets**.

The five highest-rated products have averages around **3.20–3.22**, so the differences between them are small.

**Recommendation:** show rating counts alongside averages. Investigate lower-rated issue types, but avoid treating small average differences as conclusive evidence of better product performance.

### 5. Timestamp Quality Limits Duration Analysis

Of **2,769 closed tickets**, **1,365 have invalid durations**, representing **49.3%**.

The **7.58-hour** average therefore describes only **1,404 valid records**.

**Recommendation:** investigate timestamp inconsistencies before using these averages to set service targets or evaluate support performance.

## Metric Definitions and Limitations

### Response-to-Resolution Time

Calculated as:

```text
Resolution timestamp − First-response timestamp
```

It does not measure the full time from ticket creation to resolution.

Invalid negative durations are excluded from averages, while their tickets are retained.

### Satisfaction

Average satisfaction uses available ratings between **1 and 5**. Missing ratings are excluded rather than treated as zero.

Rated tickets represent approximately **32.7%** of the dataset, so the average should not be interpreted as the opinion of every customer.

### Scatterplot Interpretation

Each dot represents one product.

Its average duration and average satisfaction may use different tickets because some records lack valid durations or ratings.

The chart supports exploratory comparison. It does not establish that faster resolution causes higher satisfaction.

### High-Risk Share

Calculated as:

```text
High-risk tickets ÷ Unresolved tickets × 100
```

The denominator is unresolved tickets, not all tickets.

### Additional Limitations

- Sentiment labels have not been validated against a manually reviewed sample.
- Purchase date is not a ticket-created date and should not be used for ticket-arrival trends.
- Product ticket counts are not defect rates without sales or usage data.
- Risk levels are business rules, not calibrated probabilities.
- The project does not implement live monitoring or notification delivery.
- Results describe this dataset; they do not demonstrate a measured business improvement.

## Run the Project Locally

### Prerequisites

- Python 3.10 or later
- MySQL Server and a SQL client such as MySQL Workbench
- Power BI Desktop

Run the following commands from the repository root.

### 1. Create a Virtual Environment

```powershell
py -m venv .venv
```

The commands below use the virtual environment directly, so activation is optional.

### 2. Install Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install pandas "SQLAlchemy>=2.0,<2.1" "PyMySQL[rsa]>=1.1,<2" vaderSentiment
```

### 3. Prepare the Source Data

Ensure the raw CSV is available at:

```text
data/raw/customer_support_tickets.csv
```

If absent, obtain it from the dataset source linked above.

### 4. Run the Python Processing Scripts

Run each command separately and continue only after it succeeds:

```powershell
.\.venv\Scripts\python.exe python/01_data_understanding.py
```

```powershell
.\.venv\Scripts\python.exe python/02_clean_data.py
```

```powershell
.\.venv\Scripts\python.exe python/03_sentiment_and_risk.py
```

For the supplied dataset, both processed files should contain **8,469 tickets**.

### 5. Create the MySQL Schema

Open MySQL Workbench and execute:

```text
sql/01_create_database.sql
```

This creates:

- Database: `customer_support_analytics`
- Table: `support_tickets`
- Primary key: `ticket_id`
- Storage engine: InnoDB

`CREATE TABLE IF NOT EXISTS` does not modify an older table's schema. An existing table must have compatible columns and `ticket_id` as its primary key before importing.

### 6. Import the AI-Ready CSV

```powershell
.\.venv\Scripts\python.exe python/04_import_to_mysql.py
```

Enter the MySQL password when prompted. Password characters are hidden while typing.

The current importer connects to `localhost:3306` as `root`. Edit these non-secret connection settings in the script if your setup differs.

The importer:

- Inserts new ticket IDs.
- Updates matching ticket IDs with the CSV values.
- Preserves records absent from the CSV.
- Does not replace the table.
- Prints database row counts before and after importing.

The password is requested at runtime rather than stored in the script.

### 7. Run SQL Analysis

Execute:

```text
sql/02_analysis.sql
```

The file includes executive overview queries, performance analysis, risk monitoring, and data-quality checks.

### 8. Refresh Power BI

Open:

```text
dashboard/Customer Support Ticket Analytics & AI Risk Monitoring Dashboard.pbix
```

Update the data-source location or connection details for your computer, preserving the existing query/table name.

For a CSV connection, use:

```text
data/processed/support_tickets_ai_ready.csv
```

Select **Home → Refresh**, clear slicers, and compare the report totals with the verified results above.

## Validation

The current dataset and supplied SQL results confirm:

- **8,469 unique ticket IDs**
- No missing ticket IDs
- No duplicate ticket IDs
- No satisfaction ratings outside 1–5
- No remaining negative duration values
- No unknown or missing ticket statuses or priorities
- No inconsistencies between risk level and the review flag
- **1,365 invalid-duration tickets retained**
- **1,404 valid durations**

These checks were performed through script output and SQL queries. The repository does not currently include an automated test suite.

## Future Improvements

- Validate sentiment against manually reviewed ticket text.
- Investigate and correct timestamp inconsistencies at the source.
- Add ticket-created timestamps for backlog-age and full-resolution analysis.
- Analyze tickets with both valid duration and satisfaction values.
- Add automated tests for cleaning and risk-rule boundaries.
- Implement notification delivery with duplicate prevention and delivery logging if operational alerts are required.
